import numpy as np
import cv2
from matplotlib import pyplot as plt

def getTagArray(num, tsz):
    # DICT_MXM_N
    # M is number of blocks 4 ... 7
    # N is number os possible tags 50, 100, 250 or 1000
    if tsz == 4:
        dict = cv2.aruco.DICT_4X4_50
    elif tsz == 5:
        dict = cv2.aruco.DICT_5X5_50
    elif tsz == 6:
        dict = cv2.aruco.DICT_6X6_50
    elif tsz == 7:
        dict = cv2.aruco.DICT_7X7_50
    else:
        return False
    tags = cv2.aruco.Dictionary_get(dict)
    pixels = tsz + 2 * 1 # Tag plus border pixels
    tag = np.zeros((pixels, pixels, 1), dtype="uint8")
    cv2.aruco.drawMarker(tags, num, pixels, tag, 1) # 1 is border pixels
    return tag

def makeCubeScad(dx, dy, dz, ox=0, oy=0, oz=0):
    txt = ""
    if ox != 0 or oy != 0 or oz != 0:
        txt += "translate(["
        txt += str(ox) + ", " + str(oy) + ", " + str(oz)
        txt += "]) "
    txt += "cube(["
    txt += str(dx) + ", " + str(dy) + ", " + str(dz)
    txt += "], center=true);"
    return txt

def makeTagScad(tagdat, psz, bmm, sqmm, dmm, adj=0.01, upsidedown=False):
    scad = ""
    tagsz = (psz * sqmm) + (2 * bmm)
    scad += "difference()\r\n{\r\n"
    line = "  "+makeCubeScad(tagsz, tagsz, dmm, 0, 0, dmm/2) + "\r\n"
    scad += line
    start = ((psz / 2) * sqmm) - (sqmm / 2)
    for y in range(0, psz):
        for x in range(0, psz):
            if tagdat[y+1][x+1] > 0:
                if upsidedown:
                    px = start - (x * sqmm)
                else:
                    px = -start + (x * sqmm)
                py = start - (y * sqmm)
                line = "  " + makeCubeScad(sqmm+adj, sqmm+adj, dmm*5, px, py, 0) + "\r\n"
                scad += line
    scad += "}\r\n"
    return scad

tagnum = 11 # Aruco marker number (starts at zero)
tagsize = 4 # Square horizontally and vertically

bordermm = 10 # Quiet area width around marker (mm)
squaremm = 10 # Width and height of each pixel square (mm)
depmm = 0.7 # Depth of tag (mm)

tag = getTagArray(tagnum, tagsize)

scadtxt = makeTagScad(tag, tagsize, bordermm, squaremm, depmm, upsidedown=True)

fname = "aruco_" + str(tagnum) + "_" + str(tagsize) + "x" + str(tagsize) + "_50.scad"
with open(fname, "w") as fp:
    fp.write(scadtxt)

plt.imshow(tag)
plt.title("Aruco tag " + str(tagnum), fontsize=24)
#plt.savefig("arucoplot.png")
plt.show()
