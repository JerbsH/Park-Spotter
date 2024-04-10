"""
This module is used for detecting vehicles in a video stream using YOLOv5 model.
"""
import sys
import os
import time
import logging
import pickle
import cv2
import torch
import numpy as np
from dotenv import load_dotenv
from database import fetch_available_spots, store_free_spots

sys.path.insert(0, './backend')

load_dotenv()

logging.basicConfig(level=logging.INFO)

try:
    MODEL = torch.hub.load('ultralytics/yolov5', 'yolov5x6', pretrained=True)
except IOError as e:
    logging.error("Error loading model: %s", e)
    os._exit(1)

VEHICLE_CLASSES = {2, 3, 7}  # Car, motorcycle, truck

try:
    VIDEO_PATH = os.getenv('SECURE_URL')
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise ValueError("Could not open video file.")
except ValueError as e:
    logging.error("Error opening video file: %s", e)
    os._exit(1)

logging.info(
    "Video size: %sx%s",
    cap.get(cv2.CAP_PROP_FRAME_WIDTH),
    cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
)
logging.info("Frame rate: %s", cap.get(cv2.CAP_PROP_FPS))

try:
    with open("./backend/carSpots2.pkl", "rb") as file:
        POINTS = pickle.load(file)
except FileNotFoundError:
    logging.error("File 'carSpots2.pkl' not found.")
    os._exit(1)
except pickle.PickleError as e:
    logging.error("Error loading points: %s", e)
    os._exit(1)

POINTS_NP = [np.array(point_group) for point_group in POINTS]
ANNOTATED_CENTROIDS = [
    (int(np.mean(point_group[:, 0])), int(np.mean(point_group[:, 1])))
    for point_group in POINTS_NP
]

CENTROID_TO_POINTS = dict(zip(ANNOTATED_CENTROIDS, POINTS_NP))

def boxes_overlap(box1, box2):
    """
    This function checks if two boxes overlap.
    """
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2

    # Determine the coordinates of the intersection rectangle
    x_left = max(x1, x3)
    y_top = max(y1, y3)
    x_right = min(x2, x4)
    y_bottom = min(y2, y4)

    if x_right < x_left or y_bottom < y_top:
        return False  # No overlap

    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # Calculate the area of both boxes
    area_box1 = (x2 - x1) * (y2 - y1)
    area_box2 = (x4 - x3) * (y4 - y3)

    # Calculate the overlap ratio
    overlap_ratio = intersection_area / min(area_box1, area_box2)

    return overlap_ratio >= 0.5  # Overlap if overlap ratio >= 0.5

def main():
    """
    This is the main function.
    """
    frame_interval = 10
    last_frame_time = time.time()

    # Create a resizable window
    #cv2.namedWindow('Video Feed', cv2.WINDOW_NORMAL)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        #for point_group in POINTS_NP:
            #cv2.polylines(frame, [point_group.astype(int)], True, (0, 255, 0), 2)
        #cv2.imshow('Video Feed', frame)

        if time.time() - last_frame_time >= frame_interval:
            last_frame_time = time.time()

            results = MODEL(frame)
            results.print()

            total_cars = 0
            detected_boxes = []

            for *box, conf, cls in results.xyxy[0]:
                class_id = int(cls)
                class_name = MODEL.names[class_id]
                logging.info("Detected a %s with confidence %s", class_name, conf)
                if class_id in VEHICLE_CLASSES and conf >= 0.4:
                    # Check if this box overlaps with any previously detected box
                    if not any(boxes_overlap(box, other_box) for other_box in detected_boxes):
                        detected_boxes.append(box)
                        total_cars += 1

            total_spots = 8  # Total number of parking spots
            free_spots = total_spots - total_cars
            # store free spots to database
            # In your main script
            store_free_spots(free_spots)
            fetch_available_spots()
            #logging.info("Available spots: %s", spots[0])
            logging.info("Total parking spots: %s", total_spots)
            logging.info("Total detected cars: %s", total_cars)
            logging.info("Free parking spots: %s", free_spots)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #results.show()
    cap.release()
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
