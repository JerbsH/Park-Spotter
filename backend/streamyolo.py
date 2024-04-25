"""
This module is used for detecting vehicles in a video stream using YOLOv5 model.
"""
import sys
import os
import time
import logging
import pickle
import threading
import cv2
import torch
import numpy as np
from dotenv import load_dotenv
from database import (
    fetch_available_free_spots,
    save_available_free_spots,
    fetch_available_handicap_spots,
    save_available_handicap_spots,
    fetch_total_handicap_spots,
    fetch_total_spots,
)

sys.path.insert(0, './backend')

load_dotenv()

logging.basicConfig(level=logging.INFO)

VEHICLE_CLASSES = {2, 3, 7}  # Car, motorcycle, truck
MODEL = None
CAPTURE = None
POINTS = None
NORMAL_POINTS = []
HANDICAP_POINTS = []

def load_resources():
    """
    Load the model, video feed, and pickle file.
    """
    global MODEL, CAPTURE, POINTS, NORMAL_POINTS, HANDICAP_POINTS
    try:
        MODEL = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
    except IOError as e:
        logging.error("Error loading model: %s", e)
        os._exit(1)

    try:
        video_path = os.getenv('SECURE_URL')
        CAPTURE = cv2.VideoCapture(video_path)
        if not CAPTURE.isOpened():
            raise ValueError("Could not open video file.")
    except ValueError as e:
        logging.error("Error opening video file: %s", e)
        os._exit(1)

    try:
        with open("./backend/carSpots2.pkl", "rb") as file:
            POINTS = pickle.load(file)
            for point_group, is_handicap in POINTS:
                if is_handicap:
                    HANDICAP_POINTS.append(point_group)
                else:
                    NORMAL_POINTS.append(point_group)
    except (FileNotFoundError, pickle.PickleError) as e:
        logging.error("Error loading points: %s", e)
        os._exit(1)


# Create numpy arrays and calculate centroids for normal and handicap spots
NORMAL_POINTS_NP = [np.array(point_group) for point_group in NORMAL_POINTS]
HANDICAP_POINTS_NP = [np.array(point_group) for point_group in HANDICAP_POINTS]

def calculate_centroids(points_np):
    """
    Calculate the centroids of the points.
    """
    return [
        (
            int(np.mean(point_group[:, 0])),
            int(np.mean(point_group[:, 1]))
        )
        for point_group in points_np
    ]

NORMAL_ANNOTATED_CENTROIDS = calculate_centroids(NORMAL_POINTS_NP)
HANDICAP_ANNOTATED_CENTROIDS = calculate_centroids(HANDICAP_POINTS_NP)

NORMAL_CENTROID_TO_POINTS = dict(zip(NORMAL_ANNOTATED_CENTROIDS, NORMAL_POINTS_NP))
HANDICAP_CENTROID_TO_POINTS = dict(zip(HANDICAP_ANNOTATED_CENTROIDS, HANDICAP_POINTS_NP))

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

def box_in_regions(box, regions):
    """
    Check if the centroid of a bounding box is within any of the specified regions.
    """
    box_centroid = (int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2))
    for region in regions:
        if cv2.pointPolygonTest(region, box_centroid, False) >= 0:
            return True
    return False

def main():
    """
    main function for the program to run.
    """
    frame_interval = 10
    last_frame_time = time.time()

    while CAPTURE.isOpened():
        ret, frame = CAPTURE.read()
        if not ret:
            break

        if time.time() - last_frame_time >= frame_interval:
            last_frame_time = time.time()

            results = MODEL(frame)
            results.print()

            total_normal_cars = 0
            total_handicap_cars = 0
            detected_boxes = []
            for *box, conf, cls in results.xyxy[0]:
                class_id = int(cls)
                class_name = MODEL.names[class_id]
                logging.info("Detected a %s with confidence %s", class_name, conf)
                if class_id in VEHICLE_CLASSES and conf >= 0.4:
                    if not any(boxes_overlap(box, other_box) for other_box in detected_boxes):
                        if box_in_regions(box, NORMAL_POINTS_NP):
                            detected_boxes.append(box)
                            total_normal_cars += 1
                        elif box_in_regions(box, HANDICAP_POINTS_NP):
                            detected_boxes.append(box)
                            total_handicap_cars += 1

            # Calculate the number of free normal spots and free handicap spots
            total_normal_spots = fetch_total_spots()
            total_handicap_spots = fetch_total_handicap_spots()
            free_normal_spots = total_normal_spots - total_normal_cars
            free_handicap_spots = total_handicap_spots - total_handicap_cars
            save_available_free_spots(free_normal_spots)
            save_available_handicap_spots(free_handicap_spots)

            available_normal_spots = fetch_available_free_spots()
            available_handicap_spots = fetch_available_handicap_spots()
            # Log the information
            logging.info("Total normal parking spots: %s", total_normal_spots)
            logging.info("Total handicap parking spots: %s", total_handicap_spots)
            logging.info("Total detected normal cars: %s", total_normal_cars)
            logging.info("Total detected handicap cars: %s", total_handicap_cars)
            logging.info("Free normal parking spots: %s", free_normal_spots)
            logging.info("Free handicap parking spots: %s", free_handicap_spots)
            logging.info("Available normal parking spots: %s", available_normal_spots)
            logging.info("Available handicap parking spots: %s", available_handicap_spots)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    CAPTURE.release()

if __name__ == "__main__":
    # Load resources in a separate thread
    resources_thread = threading.Thread(target=load_resources)
    resources_thread.start()
    # Wait for the resources to load before running main
    resources_thread.join()
    # main runs in the main thread
    main()
