import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

coords1 = [[],[]]
coords2 = [[],[]]
coords3 = [[],[]]

def add_coords(area):
    x, y = area[0].centroid
    coords1[0].append(x)
    coords1[1].append(y)
    
    x, y = area[1].centroid
    coords2[0].append(x)
    coords2[1].append(y)

    x, y = area[2].centroid
    coords3[0].append(x)
    coords3[1].append(y)


for i in range(100):
    img = np.load(f"motion/out/h_{i}.npy")
    lbl = label(img)
    regions = regionprops(lbl)
    sorted_area = sorted(regions, key=lambda r: r.area)
    
    add_coords(sorted_area)

plt.plot(coords1[1], coords1[0], label="first")
plt.plot(coords2[1], coords2[0], label="second")
plt.plot(coords3[1], coords3[0], label="third")
plt.legend()
plt.show()