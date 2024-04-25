import utils.les as les
import numpy as np
import tqdm
import cv2

points = les.GetPointsFromImage( "./images/test.jpg", "./images/output/output.png", penSize = 5 )


img = cv2.imread( "./images/test.jpg" )
img = cv2.resize( img, ( 768, 512 ) )

frames = []
for point in tqdm.tqdm( points ):
    img = cv2.line( img, point[ "p1" ], point[ "p2" ], ( 0, 0, 0 ), 5 )
    frames.append( np.copy( img ) )

vidwriter = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 60, ( 768, 512 ) )
for frame in frames:
    vidwriter.write(frame)
vidwriter.release()