"""
dispexample.py - An example script showing how to dreate a disparity plot based on vision patameters.
"""

import math
from PIL import Image
from matplotlib import pyplot as plt


def minmax(data, ind=0):
    dmn = 999999
    dmx = -999999
    h = len(data)
    w = len(data[0])
    for dy in range(0, h):
        for dx in range(0, w):
            d = data[dy][dx][ind]
            if d != None:
                if d < dmn:
                    dmn = d
                elif d > dmx:
                    dmx = d
    return [dmn, dmx]

def makeimage(data, dmn=None, dmx=None, ind=0):
    if dmn == None or dmx == None:
        dmn, dmx = minmax(data)
    h = len(data)
    w = len(data[0])
    im = Image.new("RGB", (w, h), (0,0,0))
    pix = im.load()
    for dy in range(0, h):
        for dx in range(0, w):
            d = data[dy][dx][ind]
            if data[dy][dx][0] == None:
                pix[dx, dy] = (255, 255, 255)
            else:
                if d < 0:
                    b = ((abs(d) / abs(dmn)) * (255 - 100)) + 100
                    pix[dx, dy] = (0, int(b), int(b))
                else:
                    r = ((d / dmx) * (255 - 150)) + 150
                    pix[dx, dy] = (int(r), 0, 0)
    return im

def calcdisparity(degfov, sep, convdist, mindist, xnum=501, ynum=500, scl=1):
    wid = xnum
    if wid % 2 == 0:
        wid = wid + 1
    hgt = ynum
    eyerot = math.atan((sep / 2) / convdist)
    fov = math.radians(degfov)
    disparity = []
    for cy in range(0, hgt):
        ldisp = []
        for cx in range(0, wid):
            x = (cx - int(wid / 2)) * scl
            y = (cy * scl) + (scl / 2)
            dist = math.sqrt(x * x + y * y)
            lang = (math.atan((x + sep / 2) / y) + 1000) - (eyerot + 1000)
            rang = (math.atan((x - sep / 2) / y) + 1000) - (-eyerot + 1000)
            if abs(lang) <= (fov/2) and abs(rang) <= (fov/2) and dist >= mindist:
                dang = (lang + 1000) - (rang + 1000)
            else:
                dang = None
            ldisp.append([dang, lang, rang])
        disparity.append(ldisp)
    return disparity


fov = 120 # Field of view in degrees
sep = 0.065 # Seperation distance between eyes or lenses
conv = 25 # Distance at which eye views convergen(metres)
miny = 1 # Minimum distance for plotting values
xpix = 501 # Number of side offset pixels
ypix = 500 # Number of distance pixels
scl = 0.1 # Metres per pixel
disps = calcdisparity(fov, sep, conv, miny, xpix, ypix, scl) 

img = makeimage(disps)

fig=plt.figure()
extents = [-int(0.1*501/2), int(0.1*501/2), 0.1*500, 0]

plt.imshow(img, extent=extents)
plt.gca().invert_yaxis()
plt.xlabel("Offset (m)", fontsize=10)
plt.ylabel("Distance (m)", fontsize=10)
fig.tight_layout()

#plt.savefig('dispexample.png')

plt.show()
