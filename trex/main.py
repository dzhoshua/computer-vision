import cv2
import mss.tools
import pyautogui
import numpy as np
import time


game_screen = {"top": 330, "left": 125, "width": 800, "height": 90}
offset_screen = {"top": 330, "left": 178, "width": 75, "height": 65}

def get_gray_image(screen):
    img = np.array(sct.grab(screen))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    ret, img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    return img

with mss.mss() as sct:

    while True:
    #for i in range(1):
        #last_time = time.time()
        
        img = get_gray_image(game_screen)
        offset = get_gray_image(offset_screen)
        
        if offset.mean() != 255.0:
            pyautogui.press('up')
            time.sleep(0.13)
            pyautogui.keyDown('down')
            time.sleep(0.05)
            pyautogui.keyUp('down')

        cv2.imshow("Game", img)
        cv2.imshow("Offset", offset)