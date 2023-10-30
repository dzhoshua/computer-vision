from scipy.ndimage import binary_erosion
from skimage.measure import label
import matplotlib.pyplot as plt
import numpy as np
#прямоугольник
struct1 = np.array([
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
])
#дырка сверху
struct2 = np.array([
    [0, 0, 0, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
])
#дырка справа
struct3 = np.array([
    [1, 1, 1, 0],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 1, 1, 0]
])
#дырка слева
struct4 = np.array([
    [0, 1, 1, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 1, 1, 1]
])
#дырка снизу
struct5 = np.array([
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 0, 0, 0]
])

objects = {"rectangle":struct1, 
           "hole on top":struct2, 
           "hole on right":struct3, 
           "hole on left":struct4, 
           "hole on bottom":struct5}

image = np.load("ps.npy.txt")
lb = label(image)
print("Tonal count:", lb.max())

rect = 0
for name, struct in objects.items():
  b_e = binary_erosion(image, struct)
  lb = label(b_e)
  count = lb.max()
  if rect:
    print(f"{name}: {count - rect}")
  else:
    rect = count
    print(f"{name}: {count}")
