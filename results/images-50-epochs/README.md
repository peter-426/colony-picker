## Results 

<!-- #### Example training log -->

<!-- <img src=5-epochs.png  width=800 > -->

### EfficientDet D1 Lite model predictions after being trained for 50 epochs.<br>
This data was was split into training, validation, and test sets. Although the total number of predicted bounding boxes was very high in this case, many were filtered out.
Boxes predicted with a confidence below the threshold were discarded. Where two bounding boxes overlapped, the box predicted with a lower confidence was discarded.
Consequently, predictions can be tuned by confidence and the extent to which two bounding boxes overlap, i.e. a small overlap due to close colonies might be acceptable for some applications. In an application where the user sets a limit on the number of colonies to be picked (n), up to n target colonies would be picked in order from high to low confidence.

<a href=https://www.youtube.com/channel/UCkWYMoMaR-2BUtU9O6clCAA > YouTube </a> <br>
<table>
<td><img src=car-white-GT.png  width=500 > labelled by an expert, then rotated </td>	
<td><img src=car-white-pred.png  width=500 > predicted colonies </td>	
<tr>
<td><img src=model_50_loss.png  width=500 > </td>	
<td><img src=model_50_box.png  width=500 > </td>	
<tr>
<td><img src=model_50_L2.png  width=500 > </td>	
<td><img src=model_50_LR_GN.png  width=500 > </td>	
</table>


