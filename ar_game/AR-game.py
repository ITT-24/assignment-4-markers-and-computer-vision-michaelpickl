import cv2
import cv2.aruco as aruco
import sys
import pyglet
from PIL import Image
import random
import game_window as w  # This should be the updated game_window module
import hand as h
from pyglet.gl import *

# Set video source
video_id = 2
if len(sys.argv) > 1:
    video_id = int(sys.argv[1])


# Score variable
score = 0

#setup like in the aruco_sample
cap = cv2.VideoCapture(video_id)
ret, frame = cap.read()
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
aruco_params = aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

# size of pyglet window, its the size of the webcam
WINDOW_WIDTH = frame.shape[1]
WINDOW_HEIGHT = frame.shape[0]

# create the  window
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

# AS: sprites have to be created after the window

# create knife sprite
knife_img = pyglet.image.load('images/knife.png')
knife = pyglet.sprite.Sprite(knife_img)
knife.scale = 0.05

# create list of fruit images
fruit_images = ['images/apple.png', 'images/lemon.png', 'images/cherry.png', 'images/pear.png', 'images/strawberry.png']
fruits = []

fruit_batch = pyglet.graphics.Batch()


# tracking states to allow game mechanics
transformation_successful = False
is_drop_fruit_scheduled = False

# converts OpenCV image to PIL image and then to pyglet texture
# https://gist.github.com/nkymut/1cb40ea6ae4de0cf9ded7332f1ca0d55
#from opencv:pyglet
def cv2glet(img, fmt):
    if fmt == 'GRAY':
        rows, cols = img.shape
        channels = 1
    else:
        rows, cols, channels = img.shape
    raw_img = Image.fromarray(img).tobytes()
    top_to_bottom_flag = -1
    bytes_per_row = channels * cols
    pyimg = pyglet.image.ImageData(width=cols, height=rows, fmt=fmt, data=raw_img, pitch=top_to_bottom_flag * bytes_per_row)
    return pyimg

# dropping fruit
def drop_fruit(dt):
    global fruits
    if transformation_successful:  # only drops fruits if transformation is successful
        fruit_image = pyglet.image.load(random.choice(fruit_images))
        fruit_sprite = pyglet.sprite.Sprite(fruit_image, x=random.randint(10, 50), y=window.height, batch=fruit_batch)
        fruit_sprite.scale = 0.5 
        fruits.append(fruit_sprite)

# update fruits -> dropping speed
def update(dt):
    global fruits
    for fruit in fruits:
        fruit.y -= 100 * dt  # adjust speed 
        if fruit.y < 0:
            fruits.remove(fruit)

# schedule the update 
pyglet.clock.schedule_interval(update, 1/60.0)

# check if knife and fruits are colliding
def check_collision():
    global fruits, score
    for fruit in fruits:
        if knife.x < fruit.x + fruit.width and \
           knife.x + knife.width > fruit.x and \
           knife.y < fruit.y + fruit.height and \
           knife.y + knife.height > fruit.y:
            fruits.remove(fruit)
            score += 1

@window.event
def on_draw():
    global transformation_successful, is_drop_fruit_scheduled, knife

    window.clear()
    ret, frame = cap.read()
    if ret:
        #getting the transformed canvas
        transformed_game, transformation_successful = w.get_window(detector, frame, ret)
        #if it worked 
        if transformation_successful:
            img = cv2glet(transformed_game, 'BGR')
            img.blit(0, 0, 0)
            #get hand position
            hand_position = h.detect_hand(transformed_game)
            if hand_position is not None:
                pyglet_y = window.height - hand_position[1]
                scaled_x = hand_position[0] * (window.width / frame.shape[1])
                scaled_y = pyglet_y * (window.height / frame.shape[0])

                knife.x = scaled_x
                knife.y = scaled_y
            knife.draw()

            # Schedule the fruit drop function if it's not already scheduled from chatgpt
            if not is_drop_fruit_scheduled:
                pyglet.clock.schedule_interval(drop_fruit, 1.0)
                is_drop_fruit_scheduled = True

            check_collision()

            # finish text after the score of 20
            if score >= 20:
                finish_label = pyglet.text.Label(
                    'You won!',
                    font_name='Arial',
                    font_size=36,
                    x=window.width // 2,
                    y=window.height // 2,
                    anchor_x='center',
                    anchor_y='center',
                    color=(0, 0, 0, 255)  # Black color
                )
                finish_label.draw()
                fruits.clear()
            
        else:
            #no fruits if there is no transformed img
            img = cv2glet(frame, 'BGR')
            img.blit(0, 0, 0)
            if is_drop_fruit_scheduled:
                pyglet.clock.unschedule(drop_fruit)
                is_drop_fruit_scheduled = False
                fruits.clear()

    # draw fruits
    fruit_batch.draw()

    # score
    score_label = pyglet.text.Label(
        f'Score: {score}',
        font_name='Arial',
        font_size=30,
        x=10, y=window.height - 30,
        anchor_x='left', anchor_y='center',
        color = (0,0,0,255)
    )
    score_label.draw()

pyglet.app.run()
