"""
This module is used for streaming YOLO object detection model.
It reads the video feed from the camera and detects vehicles in the feed.
It then calculates the number of free normal and handicap parking spots based on the detected vehicles.
The number of free parking spots is saved to the database.
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
from ultralytics import YOLO
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
NORMAL_POINTS_NP = []
HANDICAP_POINTS_NP = []

def load_resources():
    """
    Load the model, video feed, and pickle file.
    """
    global MODEL, CAPTURE, NORMAL_POINTS_NP, HANDICAP_POINTS_NP
    try:
        MODEL = YOLO("yolov8x.pt")
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
                    HANDICAP_POINTS_NP.append(np.array(point_group))
                else:
                    NORMAL_POINTS_NP.append(np.array(point_group))
    except (FileNotFoundError, pickle.PickleError) as e:
        logging.error("Error loading points: %s", e)
        os._exit(1)

    # Create numpy arrays and calculate centroids for normal and handicap spots
    NORMAL_POINTS_NP[:] = [np.array(point_group) for point_group in NORMAL_POINTS_NP]
    HANDICAP_POINTS_NP[:] = [np.array(point_group) for point_group in HANDICAP_POINTS_NP]

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

# test function to visually showing the if regions are drawn correctly
def draw_polygons(image, points_np, color):

    """Draw polylines on the image based on the provided points."""

    for points in points_np:
        cv2.polylines(image, [points], True, color, 2)


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
    return overlap_ratio >= 0.80

def box_in_regions(box, normal_regions, handicap_regions):
    """
    Check if the centroid of a bounding box is within any of the specified regions.
    """
    box_centroid = (int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2))
    for region in normal_regions:
        if cv2.pointPolygonTest(region, box_centroid, False) >= 0:
            return True
    for region in handicap_regions:
        if cv2.pointPolygonTest(region, box_centroid, False) >= 0:
            return True
    return False


def get_regions_of_interest(frame, points_np):
    """
    This function extracts the regions of interest from the frame based on the provided points.
    """
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    for points in points_np:
        cv2.drawContours(mask, [points], -1, (255), thickness=cv2.FILLED)

    regions_of_interest = []
    scales_and_offsets = []
    for points in points_np:
        roi = cv2.bitwise_and(frame, frame, mask=mask)
        x, y, w, h = cv2.boundingRect(points)
        scale = 2*max(frame.shape[0] / h, frame.shape[1] / w)
        offset = (x, y)
        roi = cv2.resize(roi[y:y+h, x:x+w], None, fx=scale, fy=scale)
        regions_of_interest.append(roi)
        scales_and_offsets.append((scale, offset))
    return regions_of_interest, scales_and_offsets

def main():
    """
    Main function for the program to run.
    """
    frame_interval = 30
    last_frame_time = time.time()

    while CAPTURE.isOpened():
        ret, frame = CAPTURE.read()
        if not ret:
            break
        if time.time() - last_frame_time >= frame_interval:
            last_frame_time = time.time()

            # Get the regions of interest
            normal_regions, normal_scales_and_offsets = get_regions_of_interest(frame, NORMAL_POINTS_NP)
            handicap_regions, handicap_scales_and_offsets = get_regions_of_interest(frame, HANDICAP_POINTS_NP)

            total_normal_cars = 0
            total_handicap_cars = 0
            detected_boxes = []

            # Draw polylines on the frame based on the points
            draw_polygons(frame, NORMAL_POINTS_NP, (0, 255, 0))  # Green color for normal regions
            draw_polygons(frame, HANDICAP_POINTS_NP, (255, 0, 0))  # Red color for handicap regions

            # Process all regions of interest in a batch
            all_regions = normal_regions + handicap_regions
            all_scales_and_offsets = normal_scales_and_offsets + handicap_scales_and_offsets
            all_results = MODEL(all_regions)

            for i, (_, (scale, offset), results) in enumerate(zip(all_regions, all_scales_and_offsets, all_results)):

                #normalwindow = f"Processed Region {i+1}"
                #cv2.namedWindow(normalwindow, cv2.WINDOW_NORMAL)

                # Display the processed region
                #cv2.imshow(normalwindow, all_regions[i])
                for result in results:
                    for detection in result.boxes:
                        class_id = detection.cls.item()
                        conf = detection.conf.item()
                        box = detection.xyxy[0].cpu().numpy()
                        box = box / scale + np.array([offset[0], offset[1], offset[0], offset[1]])
                        if class_id in VEHICLE_CLASSES and conf >= 0.25:
                            if not any(boxes_overlap(box, other_box) for other_box in detected_boxes):
                                in_normal_region = box_in_regions(box, NORMAL_POINTS_NP, [])
                                in_handicap_region = box_in_regions(box, [], HANDICAP_POINTS_NP)
                                if in_normal_region or in_handicap_region:
                                    detected_boxes.append(box)
                                    if in_normal_region:
                                        total_normal_cars += 1
                                    elif in_handicap_region:
                                        total_handicap_cars += 1

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
            logging.info("Available normal parking spots: %s", available_normal_spots)
            logging.info("Available handicap parking spots: %s", available_handicap_spots)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    CAPTURE.release()

if __name__ == "__main__":
    # Load resources in a separate thread
    resources_thread = threading.Thread(target=load_resources)
    resources_thread.start()
    # Wait for the resources to load before running main
    resources_thread.join()
    # main runs in the main thread
    main()
