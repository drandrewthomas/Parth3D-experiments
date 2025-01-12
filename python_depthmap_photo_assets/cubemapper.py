"""
cubemapper.py - A simple test library for creating Wavefront OBJ and MTL files textured with an image front and back, and scaled front to back by a depth map.

As the resulting 3D model is textured it is best to use quad faces, so triangle faces have been removed. Also, software like Blender and Nomad Sculpt do not need normals so they too have been removed.
"""

import os
import math
from PIL import Image


def write_obj_file(objfn, mtlfn, mesh):
    params = mesh[0]
    frontverts = mesh[1]
    frontquads = mesh[2]
    fronttex = mesh[3]
    backverts = mesh[4]
    backquads = mesh[5]
    backtex = mesh[6]
    sides = mesh[7]
    with open(objfn, 'w') as f:
        f.write('# Cube mapped to image texture OBJ example.\n')
        f.write('mtllib ' + mtlfn + '\n')
        f.write('o cubemapped\n')
        f.write('# Vertices\n')
        # Front vertices
        for vert in frontverts:
            vstr = 'v ' + str(vert[0]) + ' '
            vstr = vstr + str(vert[1]) + ' '
            vstr = vstr + str(vert[2]) + '\n'
            f.write(vstr)
        # Rear vertices
        for vert in backverts:
            vstr = 'v ' + str(vert[0]) + ' '
            vstr = vstr + str(vert[1]) + ' '
            vstr = vstr + str(vert[2]) + '\n'
            f.write(vstr)
        f.write('# Texture coordinates\n')
        for tc in fronttex:
            vstr = 'vt ' + str(tc[0]) + ' '
            vstr = vstr + str(tc[1]) + '\n'
            f.write(vstr)
        for tc in backtex:
            vstr = 'vt ' + str(tc[0]) + ' '
            vstr = vstr + str(tc[1]) + '\n'
            f.write(vstr)
        f.write('# Triangle faces\n')
        f.write('g mappedcube\n')
        f.write('usemtl imagetexture\n')
        # Front textured triangles
        for c in range(0, len(frontquads)):
            va, vb, vc, vd = frontquads[c]
            vstr = 'f ' + str(va) + '/' + str(va) + '/ '
            vstr = vstr + str(vb) + '/' + str(vb) + '/ '
            vstr = vstr + str(vc) + '/' + str(vc) + '/ '
            vstr = vstr + str(vd) + '/' + str(vd) + '/\n'
            f.write(vstr)
        # Rear triangles
        nv = len(frontverts)
        for c in range(0, len(backquads)):
            vc, vb, va, vd = backquads[c]
            vstr = 'f ' + str(va + nv) + '/' + str(va) + '/ '
            vstr = vstr + str(vb + nv) + '/' + str(vb) + '/ '
            vstr = vstr + str(vc + nv) + '/' + str(vc) + '/ '
            vstr = vstr + str(vd + nv) + '/' + str(vd) + '/\n'
            f.write(vstr)
        # Side triangles
        for side in sides:
            va = side[0]
            vb = side[1]
            vc = va + nv
            vd = vb + nv
            vstr = 'f ' + str(va) + '/1/ '
            vstr = vstr + str(vc) + '/1/ '
            vstr = vstr + str(vd) + '/1/ '
            vstr = vstr + str(vb) + '/1/\n'
            f.write(vstr)

def write_mtl_file(mtlfn, imfn):
    with open(mtlfn, 'w') as f:
        f.write('# Cube mapped to image texture MTL example.\n')
        f.write('\n')
        f.write('newmtl imagetexture\n')
        f.write('Ns 0.000000\n')
        f.write('Ka 1.000000 1.000000 1.000000\n')
        f.write('Ks 0.000000 0.000000 0.000000\n')
        f.write('Ke 0.000000 0.000000 0.000000\n')
        f.write('Ni 1.450000\n')
        f.write('d 1.000000\n')
        f.write('illum 1\n')
        f.write('map_Kd ' + imfn + '\n')

def make_cube_mesh(wpts, hpts, wid, hgt, thk):
    # Assumes triangle winding is counter-clockwise
    params = [wpts, hpts, wid, hgt, thk]
    frontverts = []
    fronttex = []
    frontquads = []
    backverts = []
    backtex = []
    backquads = []
    sides = []
    wppt = wid / (wpts - 1)
    hppt = hgt / (hpts - 1)
    woff = wid / 2
    hoff = hgt / 2
    for h in range(0, hpts):
        for w in range(0, wpts):
            frontverts.append([(w * wppt) - woff, (h * hppt) - hoff, 0])
            fronttex.append([w / (wpts - 1), h / (hpts - 1)])
            backverts.append([(w * wppt) - woff, (h * hppt) - hoff, -thk])
            backtex.append([w / (wpts - 1), h / (hpts - 1)])
    for h in range(0, hpts - 1):
        for w in range(0, wpts - 1):
            ta = (hpts * h) + w
            tb = (hpts * h) + w + 1
            tc = (hpts * (h + 1)) + w
            td = (hpts * (h + 1)) + w + 1
            frontquads.append([ta + 1, tb + 1, td + 1, tc + 1])
            backquads.append([ta + 1, tb + 1, td + 1, tc + 1])
    for w in range(0, wpts - 1):
        sides.append([w + 1, w + 1 + 1]) # Pt1, Pt2
        sides.append([len(frontverts) - 1 - w + 1, len(frontverts) - 1 - w - 1 + 1])
    for h in range(0, hpts - 1):
        sides.append([(hpts * (h + 1)) + 1, (hpts * h) + 1])
        sides.append([(hpts * h) + (hpts - 1) + 1, (hpts * (h + 1)) + (hpts - 1) + 1])
    return [params, frontverts, frontquads, fronttex, backverts, backquads, backtex, sides]

def image_to_cube(imfn, wpoints, hpoints, width, thickness, onlyimtex=True):
    print('Using image file ' + imfn + '...')
    img = Image.open(imfn)
    imw, imh = img.size
    height = (imh / imw) * width 
    print('Calculating mesh...')
    mesh = make_cube_mesh(wpoints, hpoints, width, height, thickness)
    mtlfn = os.path.splitext(imfn)[0] + '.mtl'
    print('Writing MTL to ' + mtlfn + '...')
    write_mtl_file(mtlfn, imfn, onlyimtex=onlyimtex)
    objfn = os.path.splitext(imfn)[0] + '.obj'
    print('Writing OBJ to ' + objfn + '...')
    write_obj_file(objfn, mtlfn, mesh, thickness, onlyimtex=onlyimtex)
    print('Finished.')

if __name__ == '__main__':
    print('OBJ CUBE MAPPING TEST')
    print('Will not output anything!')

