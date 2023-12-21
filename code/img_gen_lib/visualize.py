import matplotlib.pyplot as plt
import cv2
import os


fig = plt.figure()

for stIdx, st in enumerate( [ 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ] ):
  for guiIdx, gui in enumerate( [ 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26 ] ):
        img = cv2.imread( f"./strengthGuidanceNoPrompt/{st}_{gui}/merged.png", cv2.IMREAD_GRAYSCALE )
        ax = fig.add_subplot( 7, 14, stIdx * 14 + 1 + guiIdx )
        ax.imshow( img, cmap = "gray" )
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.set_title( f"{st}_{gui}", fontsize = 5 )

plt.tight_layout()
fig.savefig( "./test.png", dpi = 300 )
plt.show()