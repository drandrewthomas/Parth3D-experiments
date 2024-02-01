"""
cubemapper.py - A simple test of using Python 3 to create Wavefront OBJ and MTL files based on an image file, so the image is set as a texture for use in 3D modelling software. It was created specifically for use in Nomad Sculpt to allow adding images/photos to scenes, including cropping out unwanted areas and some sculpting.

To use, set the image file name and parameters at the bottom of the code and run 'python cubemapper.py' in your terminal or console. The image file, OBJ file and MTL file can then be imported into Nomad Sculpt together.
"""

import os
import math
from PIL import Image


def write_obj_file(objfn, mtlfn, mesh, ythk, onlyimtex=True):
    params = mesh[0]
    vertices = mesh[1]
    triangles = mesh[2]
    sides = mesh[3]
    texcoords = mesh[4]
    with open(objfn, 'w') as f:
        f.write('# Cube mapped to image texture OBJ example.\n')
        f.write('mtllib ' + mtlfn + '\n')
        f.write('o cubemapped\n')
        f.write('# Vertices\n')
        # Front vertices
        for vert in vertices:
            vstr = 'v ' + str(vert[0]) + ' '
            vstr = vstr + str(vert[1]) + ' '
            vstr = vstr + str(vert[2]) + '\n'
            f.write(vstr)
        # Rear vertices
        for vert in vertices:
            vstr = 'v ' + str(vert[0]) + ' '
            vstr = vstr + str(vert[1]) + ' '
            vstr = vstr + str(vert[2]-ythk) + '\n'
            f.write(vstr)
        f.write('# Vertex normals\n')
        f.write('vn 0 0 -1\n') # Front
        f.write('vn 0 0 1\n') # Back
        f.write('vn 0 1 0\n') # Top
        f.write('vn 1 0 0\n') # Right
        f.write('vn 0 -1 0\n') # Bottom
        f.write('vn -1 0 0\n') # Left
        f.write('# Texture coordinates\n')
        for tc in texcoords:
            vstr = 'vt ' + str(tc[0]) + ' '
            vstr = vstr + str(tc[1]) + '\n'
            f.write(vstr)
        f.write('# Triangle faces\n')
        f.write('g mappedcube\n')
        f.write('usemtl imagetexture\n')
        # Front textured triangles
        for c in range(0, len(triangles)):
            va, vb, vc = triangles[c]
            vstr = 'f ' + str(va) + '/' + str(va) + '/1' + ' '
            vstr = vstr + str(vb) + '/' + str(vb) + '/1' + ' '
            vstr = vstr + str(vc) + '/' + str(vc) + '/1' + '\n'
            f.write(vstr)
        # Rear triangles
        nv = len(vertices)
        for c in range(0, len(triangles)):
            vc, vb, va = triangles[c]
            vstr = 'f ' + str(va + nv) + '/' + str(va) + '/2 '
            vstr = vstr + str(vb + nv) + '/' + str(vb) + '/2 '
            vstr = vstr + str(vc + nv) + '/' + str(vc) + '/2\n'
            f.write(vstr)
        if not onlyimtex:
            f.write('usemtl noimagetexture\n')
        # Side triangles
        for side in sides:
            if onlyimtex: # Don't use non-image texture
                sep = '/1/'
            else:
                sep = '//'
            va = side[0]
            vb = side[1]
            vc = va + nv
            vd = vb + nv
            nn = side[2]
            vstr = 'f ' + str(vc) + sep + str(nn) + ' '
            vstr = vstr + str(vb) + sep + str(nn) + ' '
            vstr = vstr + str(va) + sep + str(nn) + '\n'
            f.write(vstr)
            vstr = 'f ' + str(vd) + sep + str(nn) + ' '
            vstr = vstr + str(vb) + sep + str(nn) + ' '
            vstr = vstr + str(vc) + sep + str(nn) + '\n'
            f.write(vstr)

def write_mtl_file(mtlfn, imfn, onlyimtex):
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
        if not onlyimtex:
            f.write('\n')
            f.write('newmtl noimagetexture\n')
            f.write('Ns 0.000000\n')
            f.write('Ka 1.000000 1.000000 1.000000\n')
            f.write('Kd 0.000000 0.000000 0.000000\n')
            f.write('Ks 0.000000 0.000000 0.000000\n')
            f.write('Ke 0.000000 0.000000 0.000000\n')
            f.write('Ni 1.450000\n')
            f.write('d 1.000000\n')
            f.write('illum 1\n')

def make_cube_mesh(wpts, hpts, wid, hgt):
    # Assumes triangle winding is counter-clockwise
    params = [wpts, hpts, wid, hgt]
    vertices = []
    texcoords = []
    triangles = []
    sides = []
    wppt = wid / (wpts - 1)
    hppt = hgt / (hpts - 1)
    woff = wid / 2
    hoff = hgt / 2
    for h in range(0, hpts):
        for w in range(0, wpts):
            vertices.append([(w * wppt) - woff, (h * hppt) - hoff, 0])
            texcoords.append([w / (wpts - 1), h / (hpts - 1)])
    for h in range(0, hpts - 1):
        for w in range(0, wpts - 1):
            ta = (hpts * h) + w
            tb = (hpts * h) + w + 1
            tc = (hpts * (h + 1)) + w
            td = (hpts * (h + 1)) + w + 1
            triangles.append([ta + 1, tb + 1, tc + 1])
            triangles.append([tc + 1, tb + 1, td + 1])
    for w in range(0, wpts - 1):
        sides.append([w + 1, w + 1 + 1, 3]) # Pt1, Pt2, Normal index
        sides.append([len(vertices) - 1 - w + 1, len(vertices) - 1 - w - 1 + 1, 5])
    for h in range(0, hpts - 1):
        sides.append([(hpts * (h + 1)) + 1, (hpts * h) + 1, 4])
        sides.append([(hpts * h) + (hpts - 1) + 1, (hpts * (h + 1)) + (hpts - 1) + 1, 6])
    return [params, vertices, triangles, sides, texcoords]

def image_to_cube(imfn, wpoints, hpoints, width, thickness, onlyimtex=True):
    print('Using image file ' + imfn + '...')
    img = Image.open(imfn)
    imw, imh = img.size
    height = (imh / imw) * width 
    print('Calculating mesh...')
    mesh = make_cube_mesh(wpoints, hpoints, width, height)
    mtlfn = os.path.splitext(imfn)[0] + '.mtl'
    print('Writing MTL to ' + mtlfn + '...')
    write_mtl_file(mtlfn, imfn, onlyimtex=onlyimtex)
    objfn = os.path.splitext(imfn)[0] + '.obj'
    print('Writing OBJ to ' + objfn + '...')
    write_obj_file(objfn, mtlfn, mesh, thickness, onlyimtex=onlyimtex)
    print('Finished.')

if __name__ == '__main__':
    print('OBJ CUBE MAPPING TEST')
    wpoints = 11
    hpoints = 11
    width = 100
    thickness = 5
    imfn = 'brunel.jpg'
    image_to_cube(imfn, wpoints, hpoints, width, thickness)

