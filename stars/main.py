from scipy.ndimage import binary_erosion
from skimage.measure import label
import matplotlib.pyplot as plt
import numpy as np

struct = np.array([
    [
     [0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0],
     [1, 1, 1, 1, 1],
     [0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0]
     ],
    [
     [1, 0, 0, 0, 1],
     [0, 1, 0, 1, 0],
     [0, 0, 1, 0, 0],
     [0, 1, 0, 1, 0],
     [1, 0, 0, 0, 1]]
                  ])

image = np.load("stars.npy")

plus, cross = 0, 0
for i in range(len(struct)):
    b_e = binary_erosion(image, struct[i])
    lb = label(b_e)
    if i == 0:
      plus = np.max(lb)
    else:
      cross = np.max(lb)
print("'Stars':", plus + cross)
print("Pluses in stars:", plus)
print("Crosses in stars:", cross)
plt.imshow(image)
plt.show()
