from matplotlib import pyplot as plt
from PIL import Image

# First we load an MPO file

fname = "mpotest.mpo"

pim = Image.open(fname)
pim.seek(0)
lim = pim.copy()
pim.seek(1)
rim = pim.copy()

# Now we can plot the left and right images

fig=plt.figure()
fig.add_subplot(1,2,1)
plt.imshow(lim)
plt.title("Left image")
fig.add_subplot(1,2,2)
plt.imshow(rim)
plt.title("Right image")
fig.tight_layout()
plt.show()

