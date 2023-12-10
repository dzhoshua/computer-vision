import cv2
import mss.tools
import pyautogui
import numpy as np
import time


game_screen = {"top": 330, "left": 130,"width": 800, "height": 90}
offset_screen = {"top": 350, "left": 196, "width": 65, "height": 45}
upper_bird_screen = {"top": 325, "left": 203, "width": 75, "height": 26}

start = time.time()
after_up_sleep = 0.15
speed = 0.005
count_of_acceletarion = 0

def get_gray_image(screen):
    img = np.array(sct.grab(screen))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    ret, img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    return img

with mss.mss() as sct:
    while True:
        diff = time.time() - start
        if diff >= 16:
            start = time.time()
            count_of_acceletarion +=1
            after_up_sleep -= speed
            offset_screen["width"] += 5
            upper_bird_screen["width"]+=3

            print("yep")
        if count_of_acceletarion == 4:
            speed = 0
          
        img = get_gray_image(game_screen)
        offset = get_gray_image(offset_screen)
        upper_bird = get_gray_image(upper_bird_screen)

        cv2.imshow("game", img)
        cv2.imshow("offset", upper_bird)

        
        # down 
        if upper_bird.mean() != 255.0:
            pyautogui.keyDown('down')
            time.sleep(0.2)
            pyautogui.keyUp('down')
        # jump    
        elif offset.mean() != 255.0:
            #time.sleep(0.01)
            pyautogui.press('up')
            time.sleep(after_up_sleep)
            pyautogui.keyDown('down')
            #time.sleep(0.02)
            pyautogui.keyUp('down')

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

cv2.destroyAllWindows()
        