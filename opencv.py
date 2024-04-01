import cv2
import pickle
import numpy as np
 
# Initialize the list of points and boolean indicating
# whether drawing is being performed or not
current_points = []
is_drawing = False

# Load and resize the image
image_path = "./source/jerenAutot.jpg"
new_size = (1920, 1080)  # New size (width, height)
image = cv2.imread(image_path)
image = cv2.resize(image, new_size)
clone = image.copy()

# Use a context manager for file operations
try:
    with open("carSpots.pkl", "rb") as file:
        saved_points = pickle.load(file)
except FileNotFoundError:
    saved_points = []
 
def click_and_draw(event, x, y, flags, param):
    # grab references to the global variables
    global saved_points, current_points, is_drawing, image
 
    if event == cv2.EVENT_LBUTTONDOWN:
        current_points = [(x, y)]
        is_drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if is_drawing:
            cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
            current_points.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        current_points.append((x, y))
        is_drawing = False
        cv2.polylines(image, [np.array(current_points)], True, (0, 255, 0), 2)
        cv2.imshow("image", image)
        saved_points.append(list(current_points))
 
def save_points():
    with open("carSpots.pkl", "wb") as file:
        pickle.dump(saved_points, file)
 
#image = cv2.imread("./source/jerenAutot.jpg")
#clone = image.copy()
 
for point_group in saved_points:
    cv2.polylines(image, [np.array(point_group)], True, (0, 255, 0), 2)
 
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_draw)
 
while True:
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
 
    if key == ord("r"):
        saved_points.clear()
        save_points()
        image = clone.copy()
        for point_group in saved_points:
            cv2.polylines(image, [np.array(point_group)], True, (0, 255, 0), 2)
    elif key == ord("c"):
        save_points()
        break
 
cv2.destroyAllWindows()