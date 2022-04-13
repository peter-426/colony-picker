#!/usr/bin/env python
# coding: utf-8


import numpy as np

from tflite_runtime.interpreter import Interpreter

# The EfficientDet-Lite0 model. EfficientDet-Lite[0-4] are a 
# family of mobile/IoT-friendly object detection models derived from the 
# [EfficientDet](https://arxiv.org/abs/1911.09070) architecture.
# 
# Here is the performance of each EfficientDet-Lite models compared to each others.
# 
# | Model architecture | Size(MB)* | Latency(ms)** | Average Precision*** |
# |--------------------|-----------|---------------|----------------------|
# | EfficientDet-Lite0 | 4.4       | 37            | 25.69%               |
# | EfficientDet-Lite1 | 5.8       | 49            | 30.55%               |
# | EfficientDet-Lite2 | 7.2       | 69            | 33.97%               |
# | EfficientDet-Lite3 | 11.4      | 116           | 37.70%               |
# | EfficientDet-Lite4 | 19.9      | 260           | 41.96%               |
# 


# Load the trained TFLite model and define some visualization functions

import cv2

from PIL import Image
from numpy import asarray

model_path = 'model.tflite'

# Load the labels into a list
classes = ['???'] * 1 # model.model_spec.config.num_classes
label_map = { 0: 'col'} #model.model_spec.config.label_map
#for label_id, label_name in label_map.as_dict().items():
#  classes[label_id-1] = label_name
classes = { 0: 'col'}

# Define a list of colors for visualization
COLORS = np.random.randint(0, 255, size=(len(classes), 3), dtype=np.uint8)


def resize_pad(im, desired_size):
    ## opencv has copyMakeBorder() method for borders
    
    old_size = im.shape[:2] # old_size is in (height, width) format
    print(old_size)
    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])
    
    # new_size should be in (width, height) format
    im = cv2.resize(im, (new_size[1], new_size[0])) 
    
    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)
    
    color = [0, 0, 0]
    new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,
        value=color)
    
    img = cv2.cvtColor(new_im, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    return img

def preprocess_image(image_path, input_size):
  """Preprocess the input image to feed to the TFLite model"""
#   img = tf.io.read_file(image_path)
#   img = tf.io.decode_image(img, channels=3)
#   img = tf.image.convert_image_dtype(img, tf.uint8)
#   original_image = img
#   resized_img = tf.image.resize(img, input_size)
#   resized_img = resized_img[tf.newaxis, :]
  
  print("resize to 'input size'", input_size)
  im = Image.open(image_path)
  original_image = asarray(im)
  im=im.resize(input_size)
  #im = resize_pad(original_image, max(input_size) )
  return im, original_image


def set_input_tensor(interpreter, image):
  """Set the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Return the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


# A high confidence threshold will prevent most overlaps, but not all.
# boxes_overlap was designed to prevent the same colony from being detected more 
# once.
def boxes_overlap(ymin1, xmin1, ymax1, xmax1, ymin2, xmin2, ymax2, xmax2):
    
   # if (xmin1 == xmin2 or ymin1 == ymin2 or xmax1 == xmax2 or ymax1 == ymax2):
   #    # the line cannot have positive overlap
   #     return False
         
    # If one rectangle is on left side of other
    if(xmin1 >= xmax2 or xmax1 <= xmin2):
        return False
 
    # If one rectangle is above other
    if(ymax1 <= ymin2 or ymax2 <= ymin1):
        return False
    
    XA1=xmin1;  XA2=xmax1;   YA1=ymin1;   YA2=ymax2;
    XB1=xmin2;  XB2=xmax2;   YB1=ymin2;   YB2=ymax2
    
    SA = (XA2 - XA1) * (YA2 - YA1)
    SB = (XB2 - XB1) * (YB2 - YB1)
    
    SI = max(0, min(XA2, XB2) - max(XA1, XB1)) * max(0, min(YA2, YB2) - max(YA1, YB1))
    if SA > SB:
        pct_overlap = SI/SA
    else:
        pct_overlap = SI/SB
        
    if pct_overlap <= 0.10:
        return False
        
    #print(f"The two bounding boxes overlap is {pct_overlap}")
 
    return True



# Puts list of results in ascending order by score
# Returns true if two rectangles overlap
def filter_results(results):

    results_filtered = []  #{'bounding_box':[], 'score':0, 'class_id': 0 }
    
    mylist =[]
    for ii in range(len(results)):
        mylist.append(results[ii]['score'])

    mylist=np.array(mylist)
    idx = np.argsort(mylist*-1)  # want desceding order, == reverse

    results_sorted = []
    for ii in idx:
        results_sorted.append(results[ii])
        
    results = results_sorted   
    
    #verify order    
#     for ii in range(len(results)):
#         print(results[ii]['score'])
    
    for ii in range( len(results) ):
        ymin1, xmin1, ymax1, xmax1 = results[ii]['bounding_box']
        overlap=False
        
        for jj in range(len(results) ):
            if ii==jj:
                continue
        
            ymin2, xmin2, ymax2, xmax2 = results[jj]['bounding_box']
            
            if boxes_overlap(ymin1, xmin1, ymax1, xmax1, ymin2, xmin2, ymax2, xmax2) \
                and results[ii]['score'] <= results[jj]['score']:
                    overlap=True
                    break
            
        if overlap == False:    
            results_filtered.append(results[ii])  # for cases of overlap, this box had highest score
                  
    return results_filtered



def detect_objects(interpreter, image, threshold):
  """Returns a list of detection results, each a dictionary of object info."""
  # Feed the input image to the model
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all outputs from the model
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
        'bounding_box': boxes[i],
        'class_id': classes[i],
        'score': scores[i]
      }
      results.append(result)
        
  #print('first box: ', boxes[0])
  print('result count: ', len(results))
    
  return results



def run_odt_and_draw_results(image_path, interpreter, filter_boolean, threshold=0.5, max_boxes=10):
  """Run object detection on the input image and draw the detection results"""
  # Load the input shape required by the model
  _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

  # Load the input image and preprocess it
  preprocessed_image, original_image = preprocess_image(
      image_path,
      (input_height, input_width)
    )

  # Run object detection on the input image
  results = detect_objects(interpreter, preprocessed_image, threshold=threshold)

  if filter_boolean:
      results = filter_results(results)
      print("number of filtered results: ", len(results))

  # Plot the detection results on the input image
  original_image_np = original_image # .numpy().astype(np.uint8)
  #print(type(original_image_np))
  print(len(original_image_np))
  
  counter = 0
  centers =[]
  for obj in results:
    # Convert the object bounding box from relative coordinates to absolute
    # coordinates based on the original image resolution
    ymin, xmin, ymax, xmax = obj['bounding_box']
    xmin = int(xmin * original_image_np.shape[1])
    xmax = int(xmax * original_image_np.shape[1])
    ymin = int(ymin * original_image_np.shape[0])
    ymax = int(ymax * original_image_np.shape[0])

    # Find the class index of the current object
    class_id = int(obj['class_id'])
    score = "{}: {:.1f}%".format('col', obj['score'] * 100)
    
    print(( int((xmin+xmax)/2),  int((ymin+ymax)/2), classes[class_id]), score )
    
    centers.append( ( int((xmin+xmax)/2),  int((ymin+ymax)/2), classes[class_id], score ) )

    # Draw the bounding box and label on the image
    color = 1 # [int(c) for c in COLORS[class_id]]
    cv2.rectangle(original_image_np, (xmin, ymin), (xmax, ymax), color, 1)
    
    cv2.circle(original_image_np, centers[counter][0:2], 8, color, -1)
    
    # Make adjustments to make the label visible for all objects
    y = ymin - 7 if ymin - 7 > 7 else ymin + 7
    label = "{}: {:.0f}%".format(classes[class_id], obj['score'] * 100)

    label = "{}: {:.0f}%".format('col', obj['score'] * 100)
    
    cv2.putText(original_image_np, label, (xmin, y), 
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    counter +=1
    if counter >= max_boxes:
        break

  # Return the final image
  original_uint8 = original_image_np.astype(np.uint8)
  return original_uint8, centers


def run_od(TEMP_FILE, DETECTION_THRESHOLD, max_boxes, keyboard):
    DETECTION_THRESHOLD = 0.10 #@param {type:"number"}  # <<<<<<<<<<<==================
    filter_boolean=True

    #TEMP_FILE = 'images-marburg/test_images/image3.jpg'
    #TEMP_FILE = 'carotene-01-800-600.jpg'
    #TEMP_FILE = 'carotene-01-600-600.jpg'
    #TEMP_FILE ='images-test/434.jpg'


    im = Image.open(TEMP_FILE)

    # Load the TFLite model
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Run inference and draw detection result on the local copy of the original file
    detection_result_image, centers = run_odt_and_draw_results(
        TEMP_FILE,
        interpreter,
        filter_boolean,
        threshold=DETECTION_THRESHOLD,
        max_boxes=max_boxes
    )

    # Show the detection result
    im_boxed=Image.fromarray(detection_result_image)

    new_ext = ("-thresh=%0.2f.png" % DETECTION_THRESHOLD)

    fname=TEMP_FILE.replace(".jpg", new_ext)
    im_boxed.save(fname, 'PNG')
    
    print("Hit any key to close detected colonies window.")
    im_boxed = cv2.imread(fname)
    winname = "Detected Colonies"
    cv2.namedWindow(winname)        # Create a named window
    im=cv2.resize(im_boxed, (412,412))
    cv2.moveWindow(winname, 432,20)  # Move it to (40,30)
    cv2.imshow(winname, im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

    #keyboard.processKeyEvent() # consume that key event
    
    print("Run colony picker? y=yes, Enter key=no:")
    keyVal = keyboard.processKeyEvent()
    
    if keyVal == ord('y'):
        print("Running colony picker (wait for robot to finish).")
        fname_csv=fname.replace(".png", ".csv")
        header = "cX,cY,class\n"
        
        with open(fname_csv, 'w') as f:
            f.write(header)
            for c in centers:
                line = str(c[0]) + "," + str(c[1]) + "," + c[2]
                f.write(line)
                f.write("\n")
                
        # now save a temporary copy to be sent to the Opentrons robot
        with open("colony_centers.csv", 'w') as f:   # current set of centers
            f.write(header)
            for c in centers:
                line = str(c[0]) + "," + str(c[1]) + "," + c[2]
                f.write(line)
                f.write("\n")
                print(line)
    else:
        print("\nNot running colony picker.\n")
        





