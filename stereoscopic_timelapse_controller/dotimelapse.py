"""
dotimelapse.py - A simple example of processing and compositing stereoscopic 3D timelapse image frames from the Xreal Beam Pro camera app prior to making a movie file from them.

Note that the filename format for the Beam Pro camera images may differ between app versions, so you may need to change the filename date parsing code if you have problems. The same applies if you use this code with images from a different camera.

The image operations here are limited to just making a 2x2 grid with parallel 3D stereoscopic viewing at the top and cross-eyed below. However, it provides a simple framework for adding more sophisticated processing and compositing. But if you don't want that then using FFMPEG to create the 2x2 grid will be much faster than using this Python code.
"""

import glob
import os
from PIL import Image
from photos3d import sbs as sbsim

def get_file_names_list(folder, exts=["jpg", " jpeg", "jps", "png"], justnames=True):
    exl = []
    for ext in exts:
        if ext.lower() not in exl:
            exl.append(ext.lower().strip())
        if ext.upper() not in exl:
            exl.append(ext.upper().strip())
    tflist = [] # Handle duplicates on Windows
    for ex in exl:
        dirpath = os.path.join(".", folder, "*." + ex)
        tflist = tflist + glob.glob(dirpath)
    flist = []
    for tf in tflist:
        tfn = tf
        if justnames:
            tfn = tfn.split(os.sep)[-1]
        if tfn not in flist:
            flist.append(tfn)
    return flist

def sort_beam_pro_file_names_list(flist):
    rfl = []
    for fl in flist:
        hr = int(fl[12:14]) * 60 * 60
        mn = int(fl[14:16]) * 60
        sc = int(fl[16:18])
        rfl.append([hr + mn + sc, fl])
    rfl.sort(key=lambda x: x[0])
    return [row[1] for row in rfl]

def do_output_folder():
    sfold = "." + os.sep + "timelapseoutput"
    if os.path.exists(sfold):
        dlist = get_file_names_list(sfold, exts=["*"], justnames=False)
        for df in dlist:
            os.remove(df)
    else:
        os.mkdir(sfold)

if __name__ == '__main__':
    do_output_folder()
    fns = "." + os.sep + "timelapse" + os.sep
    flist = get_file_names_list(fns, exts=["jpg"], justnames=True)
    flist = sort_beam_pro_file_names_list(flist)
    numim = len(flist)
    f = 0
    for fl in flist:
        print(str(f+1) + " of " + str(numim) + " --> " + fl)
        lim, rim = sbsim.load(fns + fl, maxwid=1280*2, dosplit=True)
        top = sbsim.create(lim, rim)
        bot = sbsim.create(rim, lim)
        sqim = sbsim.create(top, bot, mode="ud")
        fname = "." + os.sep + "timelapseoutput" + os.sep + "frame"
        fname = fname + str(f).rjust(6, '0') + ".jpg"
        sqim.save(fname)
        f = f + 1
    print("Finished!")
    print()

