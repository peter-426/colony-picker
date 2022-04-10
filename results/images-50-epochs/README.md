## Results 

#### Example training log

<img src=5-epochs.png  width=800 > 

### EfficientDet D1 Lite model predictions after being trained for 50 epochs.<br>
This data was was split into training, validation, and test sets. Although the total number of predicted bounding boxes was very high in this case, many were filtered out.
Boxes predicted with a confidence below the threshold were discarded. Where two bounding boxes overlapped, the box predicted with a lower confidence was discarded.
Consequently, predictions can be tuned by confidence and the extent to which two bounding boxes overlap, i.e. a small overlap due to close colonies might be acceptable for some applications. In an application where the user sets a limit on the number of colonies to be picked (n), up to n target colonies would be picked in order from high to low confidence.

<a href=https://www.youtube.com/channel/UCkWYMoMaR-2BUtU9O6clCAA > YouTube </a> <br>
<table>
<td><img src=test-image-0-50-epochs.png  width=500 > </td>
<td><img src=test-image-1-50-epochs.png  width=500 > </td>
<tr>
<td><img src=test-image-2-50-epochs.png  width=500 > </td>	
<td><img src=test-image-3-50-epochs.png  width=500 > </td>	
</table>


