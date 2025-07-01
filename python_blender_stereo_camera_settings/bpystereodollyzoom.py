"""
bpydollyzoom.py - A simple dolly zoom render test in Blender. We assume the camera starts with the camera at the correct focal length and positioned at the closest point on the dolly line, with a Y-axis location that is negative, and oriented along the dolly line. Also, the subject is assumed to be close to the Y origin and centred on the X and Z axes. Plus, things like render resolution and camera sensor settings are assumed already properly set. If that's not enough, we also assume that the correct renderer (e.g. cycles or eevee) is already set.
"""

import os
import math
import bpy

def make_linear_dist_list(sd, ed, numfr):
    """
    sd = start distance (m)
    ed = end distance (m)
    numfr = number of elements (frames) to include in list
    """
    dl = []
    stp = (ed -sd) / (numfr - 1)
    for c in range(0, numfr):
        dl.append(sd + c * stp)
    return dl

def make_sin_dist_list(sd, ed, numfr):
    """
    sd = start distance (m)
    ed = end distance (m)
    numfr = number of elements (frames) to include in list
    """
    dl = []
    for c in range(0, numfr):
        ang = (c / (numfr - 1)) * 2 * math.pi
        dd = 1 - ((math.sin(ang + (math.pi / 2)) * 0.5) + 0.5)
        dist = ((ed - sd) * dd) + sd
        dl.append(dist)
    return dl

def make_dfl_stereo_list(dl, icd, ifl, icnd):
    """
    dl = list of distances (m)
    icd = initialisation camera distance (m)
    ifl = initialisation camera focal length (mm)
    icd = initial convergence distance (m)
    """
    dfl = []
    for c in range(0, len(dl)):
        fd = dl[c]
        fl = (fd / icd) * ifl
        cnd = (fd / icd) * icnd
        dfl.append([fd, fl, cnd])
    return dfl

bpy.ops.object.mode_set(mode='OBJECT')
objs = bpy.data.objects
cam = objs['Camera_STEREO']
cpy = cam.location[1]
sfl = cam.data.lens # mm

cst = bpy.data.cameras['Camera_STEREO'].stereo
st_cd = cst.convergence_distance # m
st_cm = cst.convergence_mode # default OFFAXIS want TOE
st_piv = cst.pivot # default Left want CENTER
cst.convergence_mode = "TOE"
cst.pivot = "CENTER";

dollystart = 2
dollylength = 30
framesperdolly = 120
framerepeats = 3

print("Start focal length : " + str(sfl) + "mm")
print("Start distance : " + str(cpy) + "m")
print("End distance : " + str(cpy + dollylength) + "m")
print("Frames to render: " + str(framesperdolly))

dl = make_sin_dist_list(dollystart, dollystart + dollylength, framesperdolly)
dfl = make_dfl_stereo_list(dl, abs(cpy), sfl, st_cd)

renderto = os.path.join(bpy.path.abspath("//"), "renders")

framenum = 0
for fr in range(0, framerepeats):
    for c in range(0, framesperdolly):
        renderpath = os.path.join(renderto, "frame-" + format(framenum, '06d') + ".png")
        print("Rendering frame " + str(framenum + 1) + " of " + str(framesperdolly * framerepeats))
        bpy.context.scene.render.filepath = renderpath
        cp, fl, cnvd = dfl[c]
        cam.location[1] = -cp
        cam.data.lens = fl
        cst.convergence_distance = cnvd
        bpy.ops.render.render(write_still = True)
        framenum = framenum + 1

cam.location[1] = cpy
cam.data.lens = sfl
cst.convergence_distance = st_cd
cst.convergence_mode = st_cm
cst.pivot = st_piv

print("Finished!")
