## Colony picker extension for the Opentrons OT-2 liquid handling robot

<a href=https://www.youtube.com/channel/UCkWYMoMaR-2BUtU9O6clCAA > YouTube </a><br>

<img src=graphics/colony-picker.png  width=600 >

The colony picker uses deep learning to detect and classify yeast colonies, then sends their coordinates to the OT-2 robot.
<ol>
	<li> A data set of images was labelled and split into training, validation, and test sets.
	<li> The deep learning model was trained on a desktop PC.
	<li> The trained model was deployed onto a Raspberry Pi.
</ol>