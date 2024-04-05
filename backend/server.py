import pickle
import threading
import cv2
import numpy as np
from flask import Flask, jsonify
from backend.opencv import click_and_draw
from backend.yolo import FREE_SPOTS  # Import the FREE_SPOTS variable from yolo.py

app = Flask(__name__)

# Initialize the list of points and boolean indicating
# whether drawing is being performed or not
current_points = []
is_drawing = False

# Load and resize the image
image_path = "./source/jerenAutot.jpg"
new_size = (1917, 1045)  # New size (width, height)
image = cv2.imread(image_path)
image = cv2.resize(image, new_size)
clone = image.copy()

# Use a context manager for file operations
try:
    with open("carSpots.pkl", "rb") as file:
        saved_points = pickle.load(file)
except FileNotFoundError:
    saved_points = []

def save_points():
    with open("carSpots.pkl", "wb") as file:
        pickle.dump(saved_points, file)

@app.route('/free_spots', methods=['GET'])
def get_free_spots():
    return jsonify({'free_spots': FREE_SPOTS})

def run_flask_app():
    app.run(port=8000, debug=True, use_reloader=False)

def run_opencv_window():
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_draw)

    global image, saved_points

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

if __name__ == '__main__':
    # Start the Flask application in a new thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    # Start the OpenCV window in the main thread
    run_opencv_window()
