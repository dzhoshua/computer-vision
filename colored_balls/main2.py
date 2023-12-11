import cv2
import random

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, -4)
capture.set(cv2.CAP_PROP_TEMPERATURE, 200)

cv2.namedWindow("Camera")

# color = [(lower), (upper)]
red = [(0, 190, 140), (5, 230, 200)]
yellow = [(20, 100 , 170), (40, 255, 250)]
green = [(50, 150, 100), (80, 220 , 200)]
blue = [(90, 150, 120), (105, 260, 200)]

colors = [red, yellow, green, blue]
random.shuffle(colors)
print(colors)

you_win = False


def find_ball(frame, color):
    mask = cv2.inRange(hsv, color[0], color[1])
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 0), 2)
            cv2.circle(frame, center, 5, (0, 0, 0), -1)
            #print(center)
            return center
    return None



while capture.isOpened():
    ret, frame = capture.read()
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    balls = []
    for color in colors:
        ball = find_ball(frame, color)
        if ball is not None:
            balls.append(ball)

    count = 1
    if len(balls) == len(colors):
        
        prev_frame = None
        
        for i in range(len(balls)):
            if prev_frame is not None:
                if i%2 == 1 and balls[i][0] < prev_frame[0]:
                    count += 1
                elif i%2 == 0 and balls[i][1] > prev_frame[1]:
                    count += 1
            #print(count)
            if count == 4:
                you_win = True
            
            prev_frame = balls[i]

    if you_win:
        cv2.putText(frame, f"YOU WIN!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
        you_win = False
        
    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()