"""
makesbs.py - A simple example of loading a left and right image from files and create a side-by-side stereo pair.
"""

import os
from matplotlib import pyplot as plt
from photos3d import sbs as sbsim
from photos3d import image as img

leftfname = os.path.join(".", "imagestoprocess", "left.png")
rightfname = os.path.join(".", "imagestoprocess", "right.png")
left = img.open(leftfname)
right = img.open(rightfname)
sbs = sbsim.create(left, right)
outfname = os.path.join(".", "imagestoprocess", "sbs.png")
sbs.save(outfname)
plt.imshow(sbs)
plt.show()

