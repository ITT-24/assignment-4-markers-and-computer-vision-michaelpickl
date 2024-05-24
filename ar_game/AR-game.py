import cv2
import cv2.aruco as aruco
import game_window as w
import sys
import numpy as np
import pyglet
from PIL import Image
import hand as h

video_id = 0

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])

rectangle = pyglet.shapes.Rectangle(250, 300, 400, 200, color=(255, 22, 20))

cap = cv2.VideoCapture(video_id)
ret, frame = cap.read()
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
aruco_params = aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

# converts OpenCV image to PIL image and then to pyglet texture
# https://gist.github.com/nkymut/1cb40ea6ae4de0cf9ded7332f1ca0d55
def cv2glet(img, fmt):
    '''Assumes image is in BGR color space. Returns a pyimg object'''
    if fmt == 'GRAY':
        rows, cols = img.shape
        channels = 1
    else:
        rows, cols, channels = img.shape

    raw_img = Image.fromarray(img).tobytes()

    top_to_bottom_flag = -1
    bytes_per_row = channels * cols
    pyimg = pyglet.image.ImageData(width=cols,
                                    height=rows,
                                    fmt=fmt,
                                    data=raw_img,
                                    pitch=top_to_bottom_flag * bytes_per_row)
    return pyimg

# Create a video capture object for the webcam
cap = cv2.VideoCapture(video_id)

WINDOW_WIDTH = frame.shape[1]
WINDOW_HEIGHT = frame.shape[0]

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

@window.event
def on_draw():
    window.clear()
    ret, frame = cap.read()
    transformed_game, transformation_successful = w.get_window(detector, frame, ret)

    if transformation_successful:
        img = cv2glet(transformed_game, 'BGR')
        img.blit(0, 0, 0)
        print('in game')
        # hand.get_player(transformed_game)
        rectangle.draw()
        hand_position = h.detect_hand(transformed_game)

        pyglet_y = window.height - hand_position[1]

        # Optionally, scale the coordinates to match the Pyglet window dimensions
        scaled_x = hand_position[0] * (window.width / frame.shape[1])
        scaled_y = pyglet_y * (window.height / frame.shape[0])
        #this is going to be the knife
        circle = pyglet.shapes.Circle(scaled_x, scaled_y, 100, color=(50, 225, 30))
        circle.draw()


       
        # hier kommt des ganze spiel logik rein
    else:
        # If transformation was unsuccessful, draw the original frame
        img = cv2glet(frame, 'BGR')
        img.blit(0, 0, 0)

pyglet.app.run()
