import socket
import matplotlib.pyplot as plt
import numpy as np
from  skimage.measure import label

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

'''def centroid(labeled, label=1):
  pos = np.where(labeled==label)
  return pos[0].mean(), pos[1].mean()'''


host = "84.237.21.36"
port = 5152

plt.ion()
plt.figure()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b'nope'
    while beat != b'yep':
        sock.send(b"get")
        bts = recvall(sock, 40002)

        img = np.frombuffer(bts[2:], dtype="uint8").reshape(bts[0], bts[1])

        plt.clf()
        plt.imshow(img)

        pos1 = np.unravel_index(np.argmax(img), img.shape)

        img_copy = np.copy(img)
        img_copy[img_copy > 0] = 1
        lbl = label(img_copy)

        lbl_pos1 = lbl[pos1]
        img[lbl == lbl_pos1] = 0

        pos2 = np.unravel_index(np.argmax(img), img.shape)

        
        res = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        sock.send(f"{round(res, 1)}".encode())
        print(sock.recv(4))

        plt.pause(2)

        sock.send(b'beat')
        beat = sock.recv(20)
