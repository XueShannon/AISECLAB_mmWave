## Basic ideal
In this article, the experimental scene is fixed as an L-shaped corridor to explore how to use FMCW radar to detect human position. 

FMCW radar is a range detection radar that can easily obtain the position of obstacles by reflecting signals. But we can't get the angle of transmission. However, by fixing the radar position and analyzing the length relationship of different reflection paths, the transmitting and receiving angles of each signal can be obtained, so as to calculate the human position.

Then, by analyzing the signal intensity at a fixed distance point, FFT can be used to obtain people's breathing rate. Of course, all this has strict restrictions, people cannot move, and the breathing rate should be regular, and the body should not shake.

## Ideal to our experiment
Compared to the FMCW radar, our radar can adjust the transmission and reception angles, which means we don't have to worry about getting the angles, but this also brings other problems. Since the detection Angle is very small, most of our time will be spent on determining which Angle has the strongest signal strength.