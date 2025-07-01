import bpy

cst = bpy.data.cameras['Camera_STEREO'].stereo

print("Convergence distance (m): " + str(cst.convergence_distance)) # m
print("Convergence mode: " + cst.convergence_mode) # default OFFAXIS want TOE
print("Interocular distance (m): " + str(cst.interocular_distance)) # m e.g. 0.065
print("Pivot type: " + cst.pivot) # default Left want CENTER

"""
SETTING:
cst.convergence_distance = 0
cst.convergence_mode = "TOE"
cst.interocular_distance = 0.065
cst.pivot = CENTER;
"""
