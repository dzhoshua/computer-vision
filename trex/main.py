import cv2
import mss.tools
import pyautogui
import numpy as np
import time


#game_screen = {"top": 330, "left": 130,"width": 800, "height": 90}
offset_screen = {"top": 350, "left": 196, "width": 65, "height": 45}
upper_bird_screen = {"top": 325, "left": 203, "width": 75, "height": 26}

after_up_sleep = 0.16
bird_sleep = 0.3
val = 5
speed = 0.002

def get_gray_image(screen):
    img = np.array(sct.grab(screen))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    ret, img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    return img
start = time.time()
with mss.mss() as sct:
    while True:
        diff = time.time() - start
        if diff >= 15:
            start = time.time()

            if after_up_sleep <= 0.158:
                speed = 0.008
                val = 10
            if 0.11 < after_up_sleep <= 0.145:
                val = 15
            if after_up_sleep<= 0.11:
                speed = 0
                val += 1

            after_up_sleep -= speed
            bird_sleep += 0.005
            offset_screen["width"] += val
            upper_bird_screen["width"] += val
            print("sleep", after_up_sleep)
            print("offset", offset_screen["width"])
            print("bird", upper_bird_screen["width"])
            
        
        offset = get_gray_image(offset_screen)
        upper_bird = get_gray_image(upper_bird_screen)

        # down 
        if upper_bird.mean() != 255.0:
            pyautogui.keyDown('down')
            time.sleep(bird_sleep)
            pyautogui.keyUp('down')
        # jump    
        elif offset.mean() != 255.0:
            pyautogui.press('up')
            time.sleep(after_up_sleep)
            pyautogui.keyDown('down')
            pyautogui.keyUp('down')

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cv2.destroyAllWindows()
