'''
obj2scad - A simple piece of code to illustrate how to load vertices
and triangles from an OBJ file and write them to an OpenSCAD file
for use in constructive solid geometry. Note that it cannot handle
quads or ngons, so the 3D model must be triangulated (e.g. in
Blender there's an option for that in the OBJ export file dialog).

OBJ files are assumed to be Y axis up, so Y and Z values are swapped.
Also, the full specifications for the OBJ file format is more
complicated than the code here can handle, so you may get errors with
some files. However, the code has been tested with exported files
from Blender and they seem to work OK.
'''

import random

def load_obj(fname):
    verts = []
    tris = []
    with open(fname, "r") as fp:
        for line in fp:
            line = " ".join(line.strip().split())
            bits=line.split(" ")
            if bits[0] == "v":
                if len(bits) != 4:
                    return [False, "Wrong vertex format (" + line + ")!"]
                v1 = float(bits[1])
                v2 = float(bits[2])
                v3 = float(bits[3])
                verts.append([v1, v2, v3])
            elif bits[0] == "f":
                if len(bits) != 4:
                    return [False, "Wrong number of vertices in face (" + line + ")!"]
                # Faces can just have vertex indices or they can have texture coordinate
                # and face normal indices appended with a slash.
                if bits[1].find("/") > 0:
                    t1 = int(bits[1].split("/")[0]) - 1
                else:
                    t1 = int(bits[1]) - 1
                if bits[2].find("/") > 0:
                    t2 = int(bits[2].split("/")[0]) - 1
                else:
                    t2 = int(bits[2]) - 1
                if bits[3].find("/") > 0:
                    t3 = int(bits[3].split("/")[0]) - 1
                else:
                    t3 = int(bits[3]) - 1
                if t1 < 0 or t2 < 0 or t3 < 0:
                    return [False, "Negative face indices are not supported!"]
                tris.append([t1,t2,t3])
    mv = -1
    for c in range(0, len(tris)):
        if tris[c][0] > mv: mv = tris[c][0]
        if tris[c][1] > mv: mv = tris[c][1]
        if tris[c][2] > mv: mv = tris[c][2]
    if mv > (len(verts) - 1):
        return [False, "Vertex indices don't match number of vertices!"]
    return [verts, tris]

def make_openscad_module_text(verts, tris, mname='object', swapyz=False):
    if len(verts)==0 or len(tris)==0: return False
    mtxt = ""
    mtxt = mtxt + 'module ' + mname + '()\n'
    mtxt = mtxt + '{\n'
    mtxt = mtxt + '  polyhedron(points=['
    for i, v in enumerate(verts):
        if swapyz:
            mtxt = mtxt + '[' + str(v[0]) + ', ' + str(v[2]) + ', ' + str(v[1]) + ']'
        else:
            mtxt = mtxt + '[' + str(v[0]) + ', ' + str(v[1]) + ', ' + str(v[2]) + ']'
        if i < len(verts)-1:
            mtxt = mtxt + ', '
    mtxt = mtxt + '], faces=['
    for i, t in enumerate(tris):
        mtxt = mtxt + '[' + str(t[0]) + ', ' + str(t[1]) + ', ' + str(t[2]) + ']'
        if i < len(tris)-1:
            mtxt = mtxt + ', '
    mtxt = mtxt + ']);\n'
    mtxt = mtxt + '}\n'
    mtxt = mtxt + '\n'
    return mtxt

def add_vertex_jitter(verts, maxrand, axes='xyz'):
    nverts = []
    for vert in verts:
        if 'x' in axes:
            x = vert[0] + ((random.random() * 2 * maxrand) -maxrand)
        if 'y' in axes:
            y = vert[1] + ((random.random() * 2 * maxrand) -maxrand)
        if 'z' in axes:
            z = vert[2] + ((random.random() * 2 * maxrand) -maxrand)
        nverts.append([x, y, z])
    return nverts

if __name__ == "__main__":
    with open("objscadtest.scad", "w") as fp:
        fp.write("difference()\n")
        fp.write("{\n")
        fp.write("  test_cube();\n")
        fp.write("  test_cylinder();\n")
        fp.write("}\n")
        fp.write("\n")
        verts, tris = load_obj("testcube.obj")
        verts = add_vertex_jitter(verts, 0.3)
        ctxt = make_openscad_module_text(verts, tris, "test_cube", swapyz=True)
        fp.write(ctxt)
        verts, tris = load_obj("testcylinder.obj")
        ctxt = make_openscad_module_text(verts, tris, "test_cylinder", swapyz=True)
        fp.write(ctxt)
    print("Finished!")
