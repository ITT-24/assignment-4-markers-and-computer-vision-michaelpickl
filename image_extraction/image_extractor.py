import cv2
import sys
import numpy as np


#command line paramater x and y resolution
if len(sys.argv) != 5:
    print('Usage: Dateiname.py input output resolution_x resolution_y')
    sys.exit(1)

#save resolution as integer
input_path = str(sys.argv[1])
output_path = str(sys.argv[2])
resolution_x = int(sys.argv[3])
resolution_y = int(sys.argv[4])


#list for markers
markers = []

img = cv2.imread(input_path)
img_to_draw = img.copy()
WINDOW_NAME = 'Preview Window'
WINDOW_NAME_RESULT = 'Transform Window'
result_view = False
img_transform = img

cv2.namedWindow(WINDOW_NAME)

# mouse input
def mouse_callback(event, x, y, flags, param):
    global img_to_draw, markers

    if event == cv2.EVENT_LBUTTONDOWN:
        img = cv2.circle(img_to_draw, (x, y), 5, (255, 0, 0), -1)
        cv2.imshow(WINDOW_NAME, img_to_draw)
        markers.append([x, y])
        if len(markers) >= 4:
            transformation()

#perspactive transform of the for points in entered resolution
def transformation():
    global markers, result_view, img_transform
    pt1 = np.array(markers, dtype=np.float32)

    pt2 = np.array([[0, 0], [resolution_x, 0], [resolution_x, resolution_y], [0, resolution_y]], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(pt1, pt2)
 
    img_transform = cv2.warpPerspective(img, matrix, (resolution_x, resolution_y))
    cv2.imshow(WINDOW_NAME_RESULT, img_transform)  
    result_view = True

#resets image and points, quits the transform view
def reset():
    global markers, img_to_draw
    markers = []
    cv2.destroyWindow(WINDOW_NAME_RESULT)
    cv2.imshow(WINDOW_NAME, img)
    img_to_draw = img.copy()
    #cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

#saves the image in the comandline argument output path
def save():
    if (result_view):
        cv2.imwrite(output_path, img_transform)
        print('--------------')
        print('Transformed Image has been saved')
        print('--------------')      

#show img to set markers
cv2.imshow(WINDOW_NAME, img)
cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

# get key inputs
while True:
    key = cv2.waitKey(1)
    if key == ord('s'):
        save()
    elif key == 27:
        reset()
    elif key == ord('q'):
        break

cv2.destroyAllWindows() 