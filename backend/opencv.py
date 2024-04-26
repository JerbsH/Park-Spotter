"""
Module for drawing on an image using OpenCV and saving the drawn points.
"""

import pickle
import sys
import cv2
import numpy as np

# Initialize the list of points and boolean indicating
# whether drawing is being performed or not
CURRENT_POINTS = []
IS_DRAWING = False
IS_HANDICAP = False
# code
# Load and resize the image
IMAGE_PATH = "./backend/source/koulu1.png"

try:
    IMAGE = cv2.imread(IMAGE_PATH)
    if IMAGE is None:
        raise FileNotFoundError(f"Image not found at {IMAGE_PATH}")
    print("Image size:", IMAGE.shape[1], "x", IMAGE.shape[0])  # Add this line

except FileNotFoundError as e:
    print(f"Error loading image: {e}")
    sys.exit(1)
except (ValueError, TypeError) as e:
    print(f"Error resizing image: {e}")
    sys.exit(1)

CLONE = IMAGE.copy()

# Use a context manager for file operations
try:
    with open("./backend/carSpots2.pkl", "rb") as file_in:
        try:
            SAVED_POINTS = pickle.load(file_in)
        except EOFError:
            SAVED_POINTS = []
except FileNotFoundError:
    SAVED_POINTS = []

def click_and_draw(event, x, y, flags, param):
    """
    Function to handle mouse events. Draws on the image on mouse drag and saves the points.
    """
    # grab references to the global variables
    global CURRENT_POINTS, IS_DRAWING, IMAGE, SAVED_POINTS, IS_HANDICAP

    if event == cv2.EVENT_LBUTTONDOWN:
        IS_HANDICAP = False
        color = (0, 255, 0)
        CURRENT_POINTS = [(x, y)]
        IS_DRAWING = True
    elif event == cv2.EVENT_RBUTTONDOWN:
        IS_HANDICAP = True
        color = (255, 0, 0)
        CURRENT_POINTS = [(x, y)]
        IS_DRAWING = True
    elif event == cv2.EVENT_MOUSEMOVE:
        color = (255, 0, 0) if IS_HANDICAP else (0, 255, 0)
        if IS_DRAWING:
            cv2.circle(IMAGE, (x, y), 3, color, -1)
            CURRENT_POINTS.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP:
        color = (255, 0, 0) if IS_HANDICAP else (0, 255, 0)
        CURRENT_POINTS.append((x, y))
        IS_DRAWING = False
        cv2.polylines(IMAGE, [np.array(CURRENT_POINTS)], True, color, 2)
        cv2.imshow("image", IMAGE)
        SAVED_POINTS.append((list(CURRENT_POINTS), IS_HANDICAP))

def save_points():
    """
    Function to save the drawn points to a file.
    """
    try:
        with open("./backend/carSpots2.pkl", "wb") as file_out:
            pickle.dump(SAVED_POINTS, file_out)
    except pickle.PickleError as pickle_error:
        print(f"Error saving points: {pickle_error}")

for point in SAVED_POINTS:
    if len(point) == 2:
        point_group, is_handicap = point
        color = (255, 0, 0) if is_handicap else (0, 255, 0)
        cv2.polylines(IMAGE, [np.array(point_group)], True, color, 2)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)  # Make the window resizable
cv2.setMouseCallback("image", click_and_draw)

while True:
    cv2.imshow("image", IMAGE)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        SAVED_POINTS.clear()
        save_points()
        IMAGE = CLONE.copy()
        for point_group, is_handicap in SAVED_POINTS:
            color = (255, 0, 0) if is_handicap else (0, 255, 0)
            cv2.polylines(IMAGE, [np.array(point_group)], True, color, 2)
    elif key == ord("c"):
        save_points()
        break

cv2.destroyAllWindows()
