import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

def neighbours4(y, x):
    return (y, x+1), (y, x-1), (y-1, x), (y+1, x)

def neighbours8(y, x):
     return neighbours4(y, x) + ((y-1, x+1), (y+1, x+1), (y-1, x-1), (y+1, x-1))

def get_boundaries(labeled, label=1, connectivity=neighbours4):
    pos = np.where(labeled == label)
    bounds = []
    for y, x in zip(*pos):
        for yn, xn in connectivity(y, x):
            if yn < 0 or yn > labeled.shape[0]-1:
                bounds.append((y, x))
                break
            elif xn < 0 or xn > labeled.shape[1]-1: 
                bounds.append((y, x))
                break
            elif labeled[yn, xn] == 0:
                bounds.append((y, x))
                break
    return bounds

def directions(y, x):
  dirs = {
      (y, x + 1): 0,
      (y + 1, x + 1): 1,
      (y + 1, x): 2,
      (y + 1, x - 1): 3,
      (y, x - 1): 4,
      (y - 1, x - 1): 5,
      (y - 1, x): 6,
      (y - 1, x + 1): 7
      }
  return dirs


def chain(labeled, lbl):
    bounds = get_boundaries(labeled, lbl)
    chain = []
    start = bounds[0]
    point = bounds[1]
    while point != start:
        bounds.pop(bounds.index(point))
        dirs = directions(point[0], point[1])
        for direction in dirs.keys():
            if direction in bounds:
                chain.append(dirs[direction])
                point = direction
                break
    chain.append(0)
    return chain

def curvature(chain):
  result = []
  for i in range(len(chain)):
    if i == len(chain)-1:
      result.append(chain[i] - chain[0])
    else:
      result.append(chain[i] - chain[i+1])
  return result

def normalize(chain):
  for i in range(len(chain)):
    chain[i] = chain[i] % 8
  return chain

def is_equal(norm1, norm2):
    norm1_copy = norm1.copy()
    while norm1_copy != norm2:
        for i in range(len(norm1_copy)-2):
          norm1_copy.append(norm1_copy.pop(0))
        #print('norm_copy',norm1_copy)
        if (norm1_copy == norm1) and norm1_copy != norm2:
          return False
    return norm1_copy == norm2


img = np.array([
    [0,0,0,0],
    [0,1,1,0],
    [0,1,1,0],
    [0,1,1,0],
    [0,0,0,0]
])
labeled = label(img)
print(get_boundaries(labeled))
print(chain(labeled, 1))
plt.imshow(labeled)
plt.show()


image = np.load("similar.npy")
labeled = label(image)
for i in range(1, labeled.max() + 1):
  #print(get_boundaries(labeled))
  print(f"Figure{i}:", chain(labeled, i))

plt.imshow(labeled)
plt.show()

fig1 = np.zeros((5,5))
fig1[1:3, 1:-1] = 1
fig2 = fig1.T

labeled = label(fig1)
ch1 = chain(labeled, 1)
print("chain1:",ch1)

labeled2 = label(fig2)
ch2 = chain(labeled2, 1)
print("chain2:",ch2)
c1 = curvature(ch1)
c2 = curvature(ch2)
print(c1)
print(c2)

print(normalize(c1))
print(normalize(c2))
print("fig1 and fig2 are equal:", is_equal(c1, c2))
