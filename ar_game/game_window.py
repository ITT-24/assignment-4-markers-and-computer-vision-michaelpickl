import cv2
import numpy as np
import cv2.aruco as aruco

game_corners = []
points = {}


def get_window(detector, frame, ret):
    global game_corners

    if not ret:
        return None, False

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect ArUco markers in the frame
    corners, ids, rejected = detector.detectMarkers(gray)

    # Check if marker is detected
    if ids is not None:
        # Draw lines along the sides of the marker
        aruco.drawDetectedMarkers(frame, corners)

        if len(corners) == 4 and len(ids) == 4:  # check if there are all 4 points in screen
            game_corners = sort_ids(corners, ids)
        if len(game_corners) == 4:
            game_transformed = game_transform(game_corners, frame)
            return game_transformed, True
        
    return frame, False

def sort_ids(corners, ids) -> list:
    global points

    if (len(ids) > 4):
        return [points['left_upper'], points['right_upper'], points['right_down'], points['left_down']]
    elif (len(ids == 4)):
        for i in range(len(ids)):
            id = ids[i][0]
            if id == 0:
                points['left_upper'] = corners[i][0][2]  # inner corner
            elif id == 1:
                points['right_upper'] = corners[i][0][3]
            elif id == 2:
                points['right_down'] = corners[i][0][0]
            elif id == 3:
                points['left_down'] = corners[i][0][1]
        
        return [points['left_upper'], points['right_upper'], points['right_down'], points['left_down']]

def game_transform(corners, frame):
    # https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html
    y, x, channel = frame.shape
    flipped_frame = cv2.flip(frame, 0)
    pt1 = np.array(corners, dtype=np.float32)
    pt2 = np.array([[0, 0], [x, 0], [x, y], [0, y]], dtype=np.float32)
    
    matrix = cv2.getPerspectiveTransform(pt1, pt2)
 
    game_transformed = cv2.warpPerspective(flipped_frame, matrix, (x, y))
    return game_transformed






