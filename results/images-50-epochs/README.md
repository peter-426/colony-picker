## Results 

#### Example training log

<img src=https://github.com/peter-426/colony-picker/blob/main/results/images-50-epochs/5-epochs.png  width=800 > 

#### EfficientDet D1 Lite model predictions after being trained for 50 epochs.<br>
This data was was split into training, validation, and test sets. Although the total number of predicted bounding boxes was very high in this case, many were filtered out.
Boxes predicted with a confidence below the threshold were discarded. Where two bounding boxes overlapped, the box predicted with a lower confidence was discarded.
Consequently, predictions can be tuned by confidence and the extent to which two bounding boxes overlap, i.e. a small overlap due to close colonies might be acceptable for some applications. 

<a href=https://www.youtube.com/channel/UCkWYMoMaR-2BUtU9O6clCAA > YouTube </a> <br>
<table>
<td><img src=https://github.com/peter-426/colony-picker/blob/main/results/images-50-epochs/test-image-0-50-epochs.png  width=500 > </td>
<td><img src=https://github.com/peter-426/colony-picker/blob/main/results/images-50-epochs/test-image-1-50-epochs.png  width=500 > </td>
<tr>
<td><img src=https://github.com/peter-426/colony-picker/blob/main/results/images-50-epochs/test-image-2-50-epochs.png  width=500 > </td>	
<td><img src=https://github.com/peter-426/colony-picker/blob/main/results/images-50-epochs/test-image-3-50-epochs.png  width=500 > </td>	
</table>


