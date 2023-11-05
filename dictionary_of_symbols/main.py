import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def filling_factor(region):
  return region.image.mean()

def recognize(region):
  if filling_factor(region) == 1:
    return "-"
  else:
    euler = region.euler_number
    if euler == -1: #B or 8
      if 1 in region.image.mean(0)[:1]:
        return "B"
      else:
        return "8"
    elif euler == 0: #A 0 P D *
      tmp = region.image.copy()
      if 1 in region.image.mean(0)[:1]:
        tmp[-1, :] = 1
        tmp[:, -len(tmp[0])//2:] = 1
        tmp_lb = label(tmp)
        tmp_regions = regionprops(tmp_lb)
        e = tmp_regions[0].euler_number
        if e == -1:
          return "P"
        elif e == 0:
          return "D"

      tmp[-1, :] = 1
      tmp_lb = label(tmp)
      tmp_regions = regionprops(tmp_lb)
      if 1 in region.image.mean(1):
        return '*'
      if tmp_regions[0].euler_number == -1:
        return "A"
      else:
        return "0"

    else: # 1 W X * /
      if 1 in region.image.mean(0):
        if region.eccentricity < 0.5:
          return "*"
        else:
          return "1"
      tmp = region.image.copy()
      tmp[[0,-1], :] = 1
      tmp_lb = label(tmp)
      tmp_regions = regionprops(tmp_lb)
      e = tmp_regions[0].euler_number
      if e == -1:
        return "X"
      elif e == -2:
        return "W"
      if region.eccentricity > 0.5:
        return "/"
      else:
        return "*"

  return "?"

image = plt.imread('symbols.png')
bin = image.mean(2)
bin[bin > 0] = 1
lb = label(bin)
print("count", lb.max())

regions = regionprops(lb)

counts = {}

for region in regions:
  symbol = recognize(region)
  if symbol not in  counts:
    counts[symbol] = 0
  counts[symbol] += 1

print(counts)
print(1 - counts.get("?", 0)/lb.max())
