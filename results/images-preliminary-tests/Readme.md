## Results from a preliminary test run

#### EfficientDet D1 Lite model was tested on various images, some not from the training data set.<br>
The main thing to notice from this preliminary test run is that after some training the deep learning model ignored the background and detected colonies even when the image is not very simlilar to images in the training data set (split into train/validation/test sets). The underlying assumption is that training images (like the first image) and the unseen test set images are from the same distribution. Expected prediction accuracy will decrease to the extent that test set images are from a dissimilar distribution. Predictions were filtered by thresholds: confidence >= 0.10 AND overlapping bounding box IOU < 0.10 (if IOU >= 0.10, lower confidence box was discarded).
<table border=5 >
<td><img src=0-pred.jpg  width=500 > </td>	
<td><img src=1-pred.jpg  width=500 > </td>	
<tr>
<td><img src=2-pred.jpg  width=500 > </td>
<td><img src=3-pred.jpg  width=500 > </td>
<tr>
<td><img src=4-pred.jpg  width=500 > </td>	
<td> &nbsp; </td>		
</table>
