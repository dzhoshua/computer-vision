import numpy as np
#Номинальное разрешение

for i in range(1, 7):
  max_size = np.loadtxt(f"figure{i}.txt", max_rows=1)
  rows = np.loadtxt(f"figure{i}.txt", skiprows=2)

  sum = np.sum(rows, axis=1)
  if max(sum)==0:
    resolution = 0
  else:
    resolution = max_size/max(sum)
  print(f"Номинальное разрешение figure{i}.txt =", resolution)

# Определить смещение
def determine_the_offset(img):
  y, x = 0, 0
  for row in img:
    y+=1
    if any(row)==1:
      x = np.where(row==1)[0][0]
      break
  return y-1, x

img1 = np.loadtxt("img1.txt", skiprows=2)
img2 = np.loadtxt("img2.txt", skiprows=2)

offset1 = determine_the_offset(img1)
offset2 = determine_the_offset(img2)

#print(offset1, offset2)
print("")
print(f"Смещение: y = {offset2[0]-offset1[0]}, x = {offset2[1]-offset1[1]}")
