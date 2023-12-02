import cv2
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

pencils_total = 0

for i in range(1, 13):
    path = f"pencils/images/img ({i}).jpg"
    image = cv2.imread(path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(image_gray, 125, 255, cv2.THRESH_BINARY)
    binary = cv2.bitwise_not(binary)
    
    lbl = label(binary)

    pencils = 0
    for region in regionprops(lbl):
        if region.perimeter > 2000 and 30 > (region.major_axis_length / region.minor_axis_length) > 10:
            pencils += 1

    print(f"img({i}): {pencils}")      
    pencils_total += pencils

print(f"Total count: {pencils_total}")