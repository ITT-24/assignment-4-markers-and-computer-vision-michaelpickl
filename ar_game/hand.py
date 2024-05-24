import cv2
import numpy as np

position = None

#https://www.youtube.com/watch?v=ddSo8Nb0mTw&t=786s&ab_channel=TechWithTim
def detect_hand(frame):
    global position
    # convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range of skin color in HSV by chatgpt
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # threshold the HSV image to get only skin color
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    #set masks
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # find contours of hand
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # filter contours to find hand region
    hand_contour = None
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            hand_contour = contour
    
    if hand_contour is not None:
        # is used to set an frame around the hand
        # find the bounding box of the hand region
        x, y, w, h = cv2.boundingRect(hand_contour)
        position = (x, y)
        return x, y
    if hand_contour is None:
        return position
    
    

