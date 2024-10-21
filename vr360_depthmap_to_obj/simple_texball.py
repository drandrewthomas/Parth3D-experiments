import math
from PIL import Image


# IMAGE OPERATIONS

def load_image(fn, maxwid=None):
    im = Image.open(fn)
    if maxwid != None:
        w, h = im.size
        print("Original image size is " + str(w) + " x " + str(h))
        if w > maxwid:
            asp = w / h
            nh = int(maxwid / asp)
            #im = im.resize((maxwid, nh), Image.Resampling.LANCZOS)
            im = im.resize((maxwid, nh))
            print("Image resized to " + str(maxwid) + " x " + str(nh))
    im = im.convert('RGB')
    return im

def get_sphere_texture_coords(imw, imh):
    tcs = []
    tcs.append([0.5, 1])
    for y in range(1, imh - 1):
        ty = 1 - (y / (imh - 1))
        for x in range(0, imw):
            tx = 1 - (x / (imw - 1))
            tcs.append([tx, ty])
    tcs.append([0.5, 0])
    return tcs


# SPHERE 3D CONSTRUCTION

def sphere_with_seam(latincs, longincs):
    '''
    With a seam we get a sphere where the vertical edge
    is duplicated so that we can texture it properly.
    '''
    # Create half circle cross section
    xs = []
    xs.append([0, 1])
    ainc = math.pi / (latincs - 1)
    for c in range(1, latincs - 1):
        x = math.sin(c * ainc)
        y = math.cos(c * ainc)
        xs.append([x, y])
    xs.append([0, -1])
    vertices = []
    faces = []
    numpts = latincs
    # Create vertices
    for c in range(0, numpts):
        y = xs[c][0]
        z = xs[c][1]
        if c == 0 or c == (numpts - 1):
            vertices.append([0, 0, z])
        else:
            for xincs in range(0, longincs):
                pangle = (xincs / (longincs - 1)) * (2 * math.pi)
                vertices.append([y * math.sin(pangle), y * math.cos(pangle), z])
    ev = len(vertices) - 1
    # Create faces
    for c in range(0, numpts):
        for xincs in range(0, longincs - 1):
            if c==0:
                tl = 0
                bl = ((c + 1) * longincs) + xincs - longincs + 1
                if xincs < (longincs - 1):
                    br = ((c + 1) * longincs) + xincs + 1 - longincs + 1
                else:
                    br = ((c + 1) * longincs) + xincs + 1 - longincs + 1 - longincs
                faces.append([tl, br, bl])
            elif c == (numpts - 1):
                tl = (ev - longincs) + xincs
                if xincs < (longincs - 1):
                    tr = tl + 1
                else:
                    tr = ev - longincs
                bl = ev
                faces.append([tl, tr, bl])
            elif c < (numpts - 2):
                tl = (c * longincs) + xincs - longincs + 1
                bl = ((c + 1) * longincs) + xincs - longincs + 1
                if xincs < (longincs - 1):
                    tr = (c * longincs) + xincs + 1 - longincs + 1
                    br = ((c + 1) * longincs) + xincs + 1 - longincs + 1
                faces.append([tl, tr, br, bl])
    return [vertices, faces]


# DEPTH ADJUSTMENT

def adjust_sphere_depth(verts, dim, wrad, brad):
    """
    Adjust radius EXCEPT at zenith (top) and nadir (bottom).
    wrad is the radius for white pixels (i.e NEAREST DISTANCE).
    brad similarly is for black pixels (i.e. FARTHEST DISTANCE).
    """
    nverts = []
    dw, dh = dm.size
    dpix = dim.load()
    # Calculate depth for top / zenith vertex
    col = dpix[int(dw / 2), 0]
    din = 1 - (float(col[0]) / 256)
    dep = (din * (brad - wrad)) + wrad
    nverts.append([verts[0][0] * dep, verts[0][1] * dep, verts[0][2] * dep]) 
    # Calculate depth for all vertices between top and bottom ones
    for y in range(1, dh - 1):
        for x in range(0, dw):
            col = dpix[(dw - 1) - x, y]
            din = 1 - (float(col[0]) / 256)
            dep = (din * (brad - wrad)) + wrad
            ind = 1 + ((y - 1) * dw) + x
            nverts.append([verts[ind][0] * dep, verts[ind][1] * dep, verts[ind][2] * dep]) 
    # Calculate depth for bottom / nadir vertex
    col = dpix[int(dw / 2), dh - 1]
    din = 1 - (float(col[0]) / 256)
    dep = (din * (brad - wrad)) + wrad
    nverts.append([verts[-1][0] * dep, verts[-1][1] * dep, verts[-1][2] * dep]) 
    # Now smooth the seam by averaging
    for y in range(1, dh - 1):
        ind0 = 1 + ((y - 1) * dw)
        ind1 = 1 + ((y - 1) * dw) + (dw - 1)
        vec0 = nverts[ind0]
        vec1 = nverts[ind1]
        nverts[ind0] = [(vec0[0] + vec1[0]) /2, (vec0[1] + vec1[1]) /2, (vec0[2] + vec1[2]) /2]
        nverts[ind1] = nverts[ind0]
    return nverts


# RUN THE EXAMPLE CODE

if __name__ == '__main__':
    import objfile as obj
    srad = 2
    erad = 15
    print("Simple Textured Ball to OBJ test.")
    dm = load_image("simpletexball_depth.jpg", maxwid=304) # 5% of RGB width
    dw, dh = dm.size
    verts, tris = sphere_with_seam(dh, dw)
    verts = adjust_sphere_depth(verts, dm, srad, erad)
    texcoords = get_sphere_texture_coords(dw, dh)
    obj.write_obj_file("simpletexball", "simpletexball", verts, tris, None, texcoords, swapyz=True)
    obj.write_mtl_file("simpletexball", "simpletexball_rgb.jpg")
    print("Finished.")
    
