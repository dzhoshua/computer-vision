import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
    

img = plt.imread(f"shades_and_shapes/balls_and_rects.png")
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
binary = img.mean(2) > 0
lbl = label(binary)

regions = regionprops(lbl)

colors = []
circle, rect = [], []
h = hsv[:, :, 0]

for region in regions:
    pixels = h[region.coords]
    r = h[region.bbox[0]:region.bbox[2], region.bbox[1]:region.bbox[3]]
    #print(r)
    colors.extend(np.unique(r)[1:])
    if r.min() == 0:
        circle.append(r)
    else:
        rect.append(r)

clusters = []
while colors:
    color1 = colors.pop(0)
    clusters.append([color1])
    for color2 in colors.copy():
        if abs(color1 - color2) < 5:
            clusters[-1].append(color2)
            colors.pop(colors.index(color2))


print("total count:", lbl.max())
print("circles count:", len(circle))
print("rects count:", len(rect))
print("\n")
print("SHADE\tCIRCLES\tRECTS")

for cluster in clusters:
    circle_count, rect_count = 0, 0
    mean_shade = int(np.mean(cluster))

    for i in range(len(circle)):
        if (mean_shade-1) <= int(np.max(circle[i])) <= (mean_shade+1):
            circle_count += 1

    for i in range(len(rect)):
        if (mean_shade-1) <= int(np.max(rect[i])) <= (mean_shade+1):
            rect_count += 1

    print(f"{mean_shade}\t{circle_count}\t{rect_count}")

#plt.imshow(lbl)
#plt.show()