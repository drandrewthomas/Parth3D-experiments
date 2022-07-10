from PIL import Image
from matplotlib import pyplot as plt

def load_image(fn, maxwid=None):
    pim = Image.open(fn)
    if maxwid != None:
        w, h = pim.size
        if w > maxwid:
            asp = w / h
            nh = int(maxwid / asp)
            pim = pim.resize((maxwid, nh), Image.ANTIALIAS)
    if pim.mode == "RGBA":
        pim = pim.convert('RGB')
    return pim

def split_anaglyph(ang, gbmode="av"):
    aglw, aglh = ang.size
    lim = Image.new("RGB", (aglw, aglh), (255,255,255))
    rim = Image.new("RGB", (aglw, aglh), (255,255,255))
    apix = ang.load()
    lpix = lim.load()
    rpix = rim.load()
    for y in range(0, aglh):
        for x in range(0, aglw):
            col = apix[x, y]
            lc = int(col[0])
            lpix[x, y] = (lc, lc, lc)
            if gbmode == "green":
                rc = int(col[1])
            elif gbmode == "blue":
                rc = int(col[2])
            else:
                rc = int((col[1] + col[2]) /2)
            rpix[x, y] = (rc, rc, rc)
    return [lim, rim]

def make_sbs(lim, rim):
    # Both images must be same size!
    w, h = lim.size
    sbsim = Image.new("RGB",(w*2, h), (0,0,0))
    sbsim.paste(lim, (0,0))
    sbsim.paste(rim, (w,0))
    return sbsim

if __name__ == '__main__':
    agl = load_image("enginepart.jpg", 640)
    left, right = split_anaglyph(agl)
    sbs = make_sbs(left, right)
    plt.imshow(sbs)
    plt.show()
