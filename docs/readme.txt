

Try testing a trained model on some test images first.

Make a new dataset for training and testing.
 
Try various training parameters and test. 

## Data preprocessing:

Image were taken by a Raspeberrry Pi camera, 1600x1600 pixels, take square pics.
TensorFlow Lite reduces images to small a small size, e.g. 320x320, before 
doing detection and classification.

labelImg was used to labels the original images, svaed to xml files.

Almost all of those images and their xml files were deleted, a few were left as examples.

The folder data-set-maker/ contains 4 python scripts.

01_rotate_images.py: 
02_label_to_csv.py
03_rotate_boxes.py:
04_norm_coords_and_format.pl:

Final result is train_labels-normed.csv.

## Training a model:

train-model_maker_object_detection_tflite_yeast.ipynb

This notebook loads the training data from folder images-25-26-orange-white/,
train the model for some number of epochs, save the model in standrd format 
and tflite format.

## Testing a model:

train-model_maker_object_detection_tflite_yeast.ipynb uses a trained model
to detect and classify objects of interest, e.g orange carotene yeast colonies
and white colonies
