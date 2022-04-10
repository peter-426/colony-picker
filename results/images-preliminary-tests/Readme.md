## Results from a preliminary test run

#### EfficientDet D1 Lite model was tested on various images, some not from the main data set.<br>
The main thing to notice from this preliminary test run is that after some training the deep learning model ignored the background and detected colonies even when the image is not very simlilar to the images in the main data set (the data set that was split into train/validation/test sets). The underlying assumption is that training and unseen test set images are from the same distibution. Expected prediction accuracy will decrease to the extent that test set images are from a dissimilar distribution. Predictions were filtered by Threshold T. 
<table border=5  >
<tr>
<td><img src=car-test.jpg  width=500 >  <br> four orange colonies </td>

<td><img src=car-test-thresh=0.30.png  width=500 > T=0.30 <br>
         note two adjacent orange colonies, pick best one. </td>	
<tr>
<br>&nbsp<br>
<td><img src=3.jpg  width=500 > </td>	
<td><img src=3-thresh=0.10.png  width=500 > T=0.10 </td>	
<tr>
<td><img src=1.jpg  width=500 > </td>
<td><img src=1-thresh=0.10.png  width=500 > T=0.10</td>
<tr>
<td><img src=2.jpg  width=500 > </td>	
<td><img src=2-thresh=0.10.png  width=500 > T=0.10 </td>	
<tr>
<td><img src=434.jpg  width=500 > </td>	
<td><img src=434-thresh=0.10.png  width=500 > T=0.10 </td>	
<tr>
<td><img src=carotene-01-600-600.jpg  width=500 > </td>	
<td><img src=carotene-01-600-600-thresh=0.25.png  width=500 > T=0.25</td>	
</table>
