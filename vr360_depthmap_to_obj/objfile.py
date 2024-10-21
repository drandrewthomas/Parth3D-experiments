"""
objfile.py - A simple library for saving 3D model data to Wavefront OBJ files.
"""

import os
import math


def write_obj_file(objfn, mtlfn, verts, faces, normals=None, tex=None, swapyz=False):
    '''
    Count for normals compared to count for verts and faces identifies whether face or vertex normals are being used.
    '''
    normaltype = 'none'
    if normals:
        if len(normals) == len(faces):
            normaltype = 'face'
        elif len(normals) == len(verts):
            normaltype = 'vertex'
        else:
            print('Error: Normals count does not match vertices or faces!')
            return False
    with open(objfn + '.obj', 'w') as f:
        f.write('# Textured 360-degree depthmap adjusted sphere OBJ example.\n')
        f.write('mtllib ' + mtlfn + '.mtl\n')
        f.write('o texball3d\n')
        # Vertices
        f.write('# Vertices\n')
        for vert in verts:
            vstr = 'v ' + str(vert[0]) + ' '
            if not swapyz:
                vstr = vstr + str(vert[1]) + ' '
                vstr = vstr + str(vert[2]) + '\n'
            else:
                vstr = vstr + str(vert[2]) + ' '
                vstr = vstr + str(vert[1]) + '\n'
            f.write(vstr)
        # Vertex normals
        if normals:
            f.write('# Vertex normals\n')
            for norm in normals:
                vstr = 'vn ' + str(norm[0]) + ' '
                vstr = vstr + str(norm[1]) + ' '
                vstr = vstr + str(norm[2]) + '\n'
                f.write(vstr)
        # Texture coordinates
        if tex:
            f.write('# Texture coordinates\n')
            for tc in tex:
                vstr = 'vt ' + str(tc[0]) + ' '
                vstr = vstr + str(tc[1]) + '\n'
                f.write(vstr)
        # Triangle faces vnum/vtex/vnorm
        f.write('# Triangle faces\n')
        f.write('g texball3d\n')
        f.write('usemtl imagetexture\n')
        for c in range(0, len(faces)):
            vts = []
            # normaltype = 'vertex' or 'face'
            norms = []
            for i in range(0, len(faces[c])):
                if normals:
                    if normaltype == 'vertex':
                        norms.append(str(faces[c][i] + 1))
                    else:
                        norms.append(str(c + 1))
                else:
                    norms.append('')
                if tex:
                    vts.append(str(faces[c][i] + 1))
                else:
                    vts.append('')
            vstr = 'f '
            for i in range(0, len(faces[c])):
                vstr = vstr + str(faces[c][i] + 1) + '/' + vts[i] + '/' + norms[i]
                if i != len(faces[c]) - 1:
                    vstr = vstr + ' '
                else:
                    vstr = vstr + '\n'
            f.write(vstr)

def write_mtl_file(mtlfn, imfn):
    with open(mtlfn + '.mtl', 'w') as f:
        f.write('# Textured depth mapped sphere MTL example.\n')
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

if __name__ == '__main__':
    print('OBJ FILE TEST')

