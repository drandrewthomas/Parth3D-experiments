from PIL import Image

sbs = Image.open("druidscircle.jpg")
sbsw, sbsh = sbs.size

aglw = int(sbsw/2)
agl = Image.new("RGBA",(aglw,sbsh),(255,255,255,255))

sbspix = sbs.load()
aglpix = agl.load()

for y in range(0, sbsh):
    for x in range(0, aglw):
        left = sbspix[x, y]
        right = sbspix[aglw + x, y]
        aglpix[x, y] = (left[0], right[1], right[2])

# Must save BEFORE displaying otherwise
# image file will be zero bytes, at least on
# Pydroid3
agl.save("anaglyph.png")

from matplotlib import pyplot as plt
plt.imshow(agl)
plt.show()
