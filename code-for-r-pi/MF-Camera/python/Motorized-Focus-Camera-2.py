
import picamera
import os
import time
import sys
from datetime import datetime, timedelta
from threading import Thread
from ctypes import *
keyboard = CDLL('./lib/libarducam_keyboard.so')
arducam_vcm =CDLL('./lib/libarducam_vcm.so')

import Autofocus as af
import classify_picamera as cp


class Cam:
    # location cases 
    location_5_holder = ord('f'); # colony plate on flat holder at desk loc 5
    
    up   =  1;     down  =  2
    left = 68;     right = 67   
    larger = ord('+'); smaller = ord('-')
    
    focus_in = ord('i'); focus_out = ord('o')
    
    SAVE = ord('s')
    
    focus_val = 512; step = 10
    vflip = ord('v');    hflip = ord('h')
    
    x=10; y=20; width=512; height=512;
    
    # zx was 0.5,  made smaller to shift initial window position left
    zx=0.30; zy=0.520; zw=0.440; zh=0.440;
    
    expand=ord('e');  contract=ord('c')
    
    inc_brightness=ord('1'); dec_brightness=ord('2');
    inc_contrast  =ord('3'); dec_contrast  =ord('4');
    inc_saturation=ord('5'); dec_saturation=ord('6');
    inc_sharpness =ord('6'); dec_sharpness =ord('7');
    
    # default resolution: is bigger than 1600x1600 
    res_width=1600;  res_height=1600;  res_step=10;
    more_res=ord('m');  less_res=ord('l')
    
    camera = picamera.PiCamera()
    
    def menu(self):
        print("Press up, down, left, right keys to move window\n")
        
        print('f set window for location 5, plate on holder\n')
        
        print('+ inc window size,  - dec window size')
        print('i focus in,         o focus out')
        print('v vertical flip,    h horizontal flip')
        print('e expand,           c contract\n')
        
        print('1 increase brightness,  2 decrease brightness')
        print('3 increase contrast,    4 decrease contrast')
        print('5 increase saturation,  6 decrease saturation')        
        print('7 increase sharpness,   8 decrease sharpness\n')
        
        print('m more resolution, l less resolution\n')
        
        print('a autofocus')
        print('r recognize object')
        print('s save pic as img_ + time-stamp')
        print('q quit\n')            
    def __init__(self):
        self._running = True
        self.camera.resolution = (self.res_width, self.res_height)  # res set here!!!
        
    def terminate(self):  
        self._running = False  

    def run(self):
        #os.system("raspistill -t 0")     
        self.camera.start_preview(fullscreen=False, window=(self.x, self.y, self.width, self.height))
        self.camera.zoom=(self.zx, self.zy, self.zw, self.zh)
        #self.camera.zoom=(self.zx, self.zy, self.zw, self.zh)
        arducam_vcm.vcm_write(self.focus_val)
        
    def close(self):
        self.camera.close()

    def recognize_object(self):
        model  = "./models/mobile_net/mobilenet_v1_1.0_224_quant.tflite"
        labels = "./models/mobile_net/labels_mobilenet_quant_v1_224.txt"
        
        interpreter = cp.Interpreter(model)
        interpreter.allocate_tensors()
        _, height, width, _ = interpreter.get_input_details()[0]['shape']
        labels = cp.load_labels(labels)
        
        try:
          stream = cp.io.BytesIO()
          for _ in self.camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            stream.seek(0)
            image = cp.Image.open(stream).convert('RGB').resize((width, height),
                                                             cp.Image.ANTIALIAS)
            start_time = time.time()
            results = cp.classify_image(interpreter, image)
            elapsed_ms = (time.time() - start_time) * 1000
            label_id, prob = results[0]
            stream.seek(0)
            stream.truncate()
            self.camera.annotate_text = '%s %.2f\n%.1fms' % (labels[label_id], prob,
                                                        elapsed_ms)
            break
        finally:
          pass#image.save("temp.jpg", "JPEG")
       
    def save_pic(self, filename):
        try:
          self.camera.capture(filename)
        finally:
          pass


    def update(self, arducam_vcm, keyVal):
        # pan
        delta=0.01
        
        if keyVal == self.location_5_holder:
            self.zx=0.30; self.zy=0.520; self.zw=0.440; self.zh=0.440;
            self.camera.zoom=(self.zx, self.zy, self.zw, self.zh)
            print("f: loc 5, window position (x,y,w,h): %0.3f,%0.3f %0.3f,%0.3f" %(self.zx, self.zy, self.zw, self.zh))
                
        elif keyVal == self.up:
            self.zy -= delta
            if self.zy < 0:
                self.zy = 0
            self.camera.zoom=(self.zx, self.zy, self.zw, self.zh)
            print("up:   window position (x,y,w,h): %0.3f,%0.3f %0.3f,%0.3f" %(self.zx, self.zy, self.zw, self.zh))
            
        elif keyVal == self.down:         
            if self.zy + delta + self.zh <= 1:
                self.zy += delta
            self.camera.zoom=(self.zx, self.zy, self.zw, self.zh)
            print("down: window position (x,y,w,h): %0.3f,%0.3f %0.3f,%0.3f" %(self.zx, self.zy, self.zw, self.zh))
            
        elif keyVal == self.left:
            self.zx -= delta
            if self.zx < 0:
                self.zx = 0
            self.camera.zoom=(self.zx, self.zy, self.zw, self.zh)
            print("<--: window position (x,y,w,h): %0.3f,%0.3f %0.3f,%0.3f" %(self.zx, self.zy, self.zw, self.zh))
            
        elif keyVal == self.right:        
            if self.zx + delta + self.zw <= 1:
                self.zx += delta; 
            #print(self.zx, self.zw)
            self.camera.zoom=(self.zx, self.zy, self.zw, self.zh)
            print("-->: window position (x,y,w,h): %0.3f,%0.3f %0.3f,%0.3f" %(self.zx, self.zy, self.zw, self.zh))
            
        elif keyVal == self.expand:
            self.zx=0; self.zy=0; self.zw=1; self.zh=1;           
            self.camera.zoom=(0,0,1,1)           
            print("e: window position,zoom out (x,y,w,h): %0.3f,%0.3f %0.3f,%0.3f" %(self.zx, self.zy, self.zw, self.zh))
           
        elif keyVal == self.contract:      
            if self.zw - delta*2 >= 0.10 and self.zh - delta*2 >= 0.10:
                self.zw -= delta*2
                self.zh -= delta*2
                self.zx += delta;
                self.zy += delta
                self.camera.zoom=(self.zx, self.zy, self.zw, self.zh)
            print("c: window position,zoom in  (x,y,w,h): %0.3f,%0.3f %0.3f,%0.3f" %(self.zx, self.zy, self.zw, self.zh))
            
        elif keyVal == self.larger:
            self.width  += 50
            self.height += 50
            self.camera.preview_window=(self.x, self.y, self.width, self.height)
            print("+: window size: %dx%d" %(self.width,self.height))
            
        elif keyVal == self.smaller:
            self.width  -= 50
            self.height -= 50
            self.camera.preview_window=(self.x, self.y, self.width, self.height)
            print("-: window size: %dx%d" %(self.width,self.height))
            
        elif keyVal == self.focus_in:
            self.focus_val = self.focus_val+self.step
            if  self.focus_val > 1023:
                self.focus_val = 1023
            arducam_vcm.vcm_write(self.focus_val)
            
        elif keyVal == self.focus_out:
            self.focus_val = self.focus_val - self.step
            if self.focus_val < 0:
                self.focus_val = 0
            arducam_vcm.vcm_write(self.focus_val)
            
        elif keyVal == self.vflip:
            if self.camera.vflip == False:
                self.camera.vflip=True
            else:
                self.camera.vflip=False 
        elif keyVal == self.hflip:
            if self.camera.hflip == False:
                self.camera.hflip=True
            else:
                self.camera.hflip=False     
        elif keyVal == self.more_res:
            self.res_width  += self.res_step
            self.res_height += self.res_step
            self.camera.resolution = (self.res_width, self.res_height)
            print("m: resolution: %sx%s" %(self.res_width,self.res_height))
            
        elif keyVal == self.inc_brightness:
            self.camera.brightness += 1
            print('1: camera.brightness: ', self.camera.brightness)
            
        elif keyVal == self.dec_brightness:
            self.camera.brightness -= 1
            print('2: camera.brightness: ', self.camera.brightness)
            
        elif keyVal == self.inc_contrast:
            self.camera.contrast += 1
            print('3: camera.contrast: ', self.camera.contrast)
            
        elif keyVal == self.dec_contrast:
            self.camera.brightness -= 1
            print('4: camera.contrast: ', self.camera.contrast)

        elif keyVal == self.inc_saturation:
            self.camera.saturation += 1
            print('5: camera.saturation: ', self.camera.saturation)
            
        elif keyVal == self.dec_saturation:
            self.camera.saturation -= 1
            print('6: camera.saturation: ', self.camera.saturation)
 
        elif keyVal == self.inc_sharpness:
            self.camera.sharpness += 1
            print('5: camera.sharpness: ', self.camera.sharpness)
            
        elif keyVal == self.dec_sharpness:
            self.camera.sharpness -= 1
            print('6: camera.sharpness: ', self.camera.sharpness)
 
        elif keyVal == self.less_res:
            self.res_width  -= self.res_step
            self.res_height -= self.res_step
            self.camera.resolution = (self.res_width, self.res_height)
            print("l: resolution: %dx%d" %(self.res_width,self.res_height))
            
        return self.focus_val
    
    def auto_focus(self):
        self.camera.shutter_speed=30000
        print("Start focusing")
        
        max_index = 10
        max_value = 0.0
        last_value = 0.0
        dec_count = 0
        focal_distance = 10

        while True:
            #Adjust focus, then calculate image clarity
            af.focusing(focal_distance)
            val = af.calculation(self.camera)
            #Find the maximum image clarity
            if val > max_value:
                max_index = focal_distance
                max_value = val
                
            #If the image clarity starts to decrease
            if val < last_value:
                dec_count += 1
            else:
                dec_count = 0
            #Image clarity is reduced by six consecutive frames
            if dec_count > 6:
                break
            last_value = val
            
            #Increase the focal distance
            focal_distance += 10
            if focal_distance > 1000:
                break

        #Adjust focus to the best
        af.focusing(max_index)
        print("Done focusing")
        return max_index


myCam = Cam()
myCamThread = Thread(target=myCam.run) 
myCamThread.start()

#Thread.start(run_camera) #, ("run_camera",))
#vcm init
arducam_vcm.vcm_init()
# arducam_vcm.vcm_write(myCam.focus_val)
# camera = picamera.PiCamera()
# camera.resolution = (640, 640)
# camera.start_preview(fullscreen=False, window=(100,100,640,640))
folder_name = 'images/'
try:
    print("Press ? for camera menu.")
    Quit=ord('q')
    focus=0
    while True:
        keyVal = keyboard.processKeyEvent()     
        #print(">> ", keyVal, " = ", chr(keyVal))
        
        if keyVal == Quit:
            break
        #time.sleep(0.01)
        if keyVal == ord('?'):
            myCam.menu()
        elif keyVal == ord('a'):
            focus_val = myCam.auto_focus()
            myCam.focus_val = focus_val
        elif keyVal == ord('r'):
            myCam.recognize_object()
        elif keyVal == ord('s'):
            print("Current folder: ", folder_name)
            
            image_set_number = input("Enter image set number, or hit Enter for no change: ")
            if image_set_number.isnumeric():
                folder_name = "images-" + image_set_number + "/"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                
            filename= folder_name + "img_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
            print("saved to : ", filename)
            myCam.save_pic(filename)
        else:
            #print(keyVal)
            focus_val = myCam.update(arducam_vcm, keyVal)

finally:
    myCam.close()
