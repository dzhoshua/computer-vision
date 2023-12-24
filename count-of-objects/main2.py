import cv2
import numpy as np
import zmq

#context = zmq.Context()
#socket = context.socket(zmq.SUB)
#socket.setsockopt(zmq.SUBSCRIBE, b"")
#socket.connect("tcp://192.168.0.105:6556")

frame = cv2.imread("count-of-objects/objects2.png")
frame_for_text = cv2.imread("count-of-objects/objects2.png")

cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Text", cv2.WINDOW_KEEPRATIO)

c = -1
while True:
    squares, circles = 0, 0

    #buffer = socket.recv()
    c += 1
    #arr = np.frombuffer(buffer, np.uint8)
    #frame = cv2.imdecode(arr, -1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    contours = cv2.Canny(gray, 100, 80)
    mask = cv2.dilate(contours, None, iterations=5)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        x, y, w, h = cv2.boundingRect(approx)
        contoured_area = cv2.contourArea(approx)

        if  0.2 < contoured_area / (w * h) < 0.7:
            cv2.putText(frame_for_text, "square", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),2)
            cv2.rectangle(frame_for_text, (x, y), (x + w, y + h), (255, 0, 0), 2)
            squares += 1
        else:
            cv2.putText(frame_for_text, "circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),2)
            cv2.rectangle(frame_for_text, (x, y), (x + w, y + h), (0, 0, 255), 2)
            circles += 1
        
    
    cv2.putText(frame_for_text, f"squares:{squares}  circles:{circles}  ALL:{squares+circles}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2)
    
    cv2.imshow("Text", frame_for_text)
    cv2.imshow("Mask", mask)
    
    key = cv2.waitKey(500)
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()
