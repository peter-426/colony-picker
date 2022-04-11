## Intro

TensorFlow and the EfficientDet model were chosen for their ease of use and 
because this model family can be converted to TensorFlow Lite format and used 
on a Raspberry Pi. 

## Getting started.

Try testing a trained model on some test images first.

Make a new dataset for training and testing.
 
Try various training parameters and test. 

## Data preprocessing:

Images were taken with a Raspberry Pi camera, 1600x1600 pixels, must take 
square pics. TensorFlow Lite reduces images to small a small size, e.g. 320x320, 
before doing detection and classification.

labelImg was used to label the original images, saved to xml files.
[https://github.com/tzutalin/labelImg]

Almost all of those images and their xml files were deleted, a few were left 
as examples.

The folder data-set-maker/ contains 4 python scripts.

<list>
<li> 01_rotate_images.py </li>
<li> 02_label_to_csv.py </li>
<li> 03_rotate_boxes.py </li>
<li> 04_norm_coords_and_format.pl </li>
</list>

Final result is train_labels-normed.csv.

## Training a model:

train-model_maker_object_detection_tflite_yeast.ipynb

This notebook loads the training data from folder images-25-26-orange-white/,
trains the model for some number of epochs, saves the model in standard format 
and tflite format.

However, although this TensorFlow API is convenient, it does not provide much 
control. It may be worth considering PyTorch and other models for some 
applications, e.g. if deployed onto on a laptop.

## Testing a model:

test-model_maker_object_detection_tflite_yeast.ipynb 

This notebook uses a trained model to detect and classify objects of interest, 
e.g orange carotene yeast colonies and white yeast colonies.




