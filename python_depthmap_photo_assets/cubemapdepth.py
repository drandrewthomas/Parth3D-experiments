"""
cubemapdepth.py - A simple test of using Python 3 to create Wavefront OBJ and MTL files based on an image file, with the vertices scaled to a depth map.
"""

import os
import numpy as np
from PIL import Image

import depthmaps as dm
import cubemapper as cm

def apply_depth_array(mesh, darr, depth, off=0, doback=False):
    wpts = mesh[0][0]
    hpts = mesh[0][1]
    frontverts = mesh[1]
    backverts = mesh[4]
    ind = 0
    for y in range(0, hpts):
        for x in range(0, wpts):
            dep = darr[hpts - 1 - y, x]
            frontverts[ind][2] = frontverts[ind][2] + off - dep
            ind = ind + 1
    if doback:
        ind = 0
        for y in range(0, hpts):
            for x in range(0, wpts):
                dep = darr[hpts - 1 - y, x]
                backverts[ind][2] = backverts[ind][2] + off - dep
                ind = ind + 1
    else:
        for vert in backverts:
            vert[2] = vert[2] + off - depth

'''
Large wpoints and hpoints numbers caused pythonista on ipad mini 4gb to crash! When imported into nomad for some reason may need to smooth over the mesh so it looks ok in remder: due to raster xy vertices not fitting with round shape of depth map ?!?
'''

print('OBJ CUBE MAPPING TEST')
wpoints = int(1630 / 4)
hpoints = int(1630 / 4)
width = 100
depth = 100
thickness = 5

# Use for spiral image into a cone made from sine wave
# as separate RGB and depth images
#imfn = 'spiral.png'
#depfn = 'spiral_depth.png'
#print('Loading image files...')
#rgbim, depim = dm.load(imfn, depfn, maxwid=1000)
#####

# Use for the fallen column sculpture as one RGB-D image, so
# we have to save an RGB-only image for the OBJ/MTL texture.
imfn = 'column_rgbd.jpg'
print('Loading image files...')
rgbim, depim = dm.load(imfn, maxwid=1000)
imfn = 'column.jpg'
rgbim.save(imfn)
#####


imw, imh = rgbim.size
height = (imh / imw) * width

print('Calculating mesh...')
mesh = cm.make_cube_mesh(wpoints, hpoints, width, height, thickness)

print('Applying depth map...')
depim = depim.resize((wpoints, hpoints), Image.LANCZOS)
darr = dm.depth_image_to_array(depim, ch='red')
dm.remap_depth_array(darr, 0, depth)
dm.invert_depth_array(darr)
apply_depth_array(mesh, darr, depth, doback=True)

mtlfn = os.path.splitext(imfn)[0] + '.mtl'
print('Writing MTL to ' + mtlfn + '...')
cm.write_mtl_file(mtlfn, imfn)

objfn = os.path.splitext(imfn)[0] + '.obj'
print('Writing OBJ to ' + objfn + '...')
cm.write_obj_file(objfn, mtlfn, mesh)

print('Finished.')

