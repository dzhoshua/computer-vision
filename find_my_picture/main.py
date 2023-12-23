import cv2
import time

video = 'output.avi'
cam = cv2.VideoCapture(video)

gray_img = cv2.imread('zlata.png', cv2.IMREAD_GRAYSCALE)

count = 0
images_count = 0

while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        print("--The video is over!--")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    res = cv2.matchTemplate(gray_frame, gray_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    #print(max_val)
    if max_val > 0.9:
        count+=1
    images_count += 1
    

    
print(f"the number of MY pictures: {count}")
print(f"total number of images: {images_count }")
cam.release()
cv2.destroyAllWindows()