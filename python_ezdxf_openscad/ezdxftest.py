import math

# CREATE A 2D COG GEOMETRY

opts = [] # Outer points list
ipts = [] # Inner points list
orad = 10 # Outer radius
inset = 1.5 # Inset for cog teeth
irad = 2 # Inner radius
teeth = 25 # Number of teeth on cog
numpts = teeth * 2 # Number of points around cog
for c in range(0, numpts):
    ang = (2 * math.pi) * (c / numpts)
    crad = orad
    if (c % 2) != 0:
        crad = orad - inset
    opts.append([crad*math.sin(ang), crad*math.cos(ang)])
    ipts.append([irad*math.sin(ang), irad*math.cos(ang)])


# EXPORT A DXF FILE WITH LAYERS AND POLYLINES

import ezdxf
doc = ezdxf.new('R2010')
msp = doc.modelspace()
lwp = msp.add_lwpolyline(opts, dxfattribs={'layer': 'outer'})
lwp.closed = True
lwp = msp.add_lwpolyline(ipts, dxfattribs={'layer': 'inner'})
lwp.closed = True
doc.saveas('ezdxftest.dxf')


# PLOT THE 2D GEOMETRY

import matplotlib.pyplot as plt
import numpy as np
xy=np.array(opts)
plt.plot(xy[:,0],xy[:,1], linestyle='solid', marker='o', color='blue')
xy=np.array(ipts)
plt.plot(xy[:,0],xy[:,1], linestyle='solid', marker='o', color="green")
plt.axis('square')
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.title("Example cog",fontsize=30)
plt.xlabel('X',fontsize=25)
plt.ylabel('Y',fontsize=25)
plt.tick_params(labelsize=20)
plt.xticks([-10, -5, 0, 5, 10])
plt.yticks([-10, -5, 0, 5, 10])
plt.show()
