"""
This module handles image editing operations using OpenCV.
"""

import pickle
import sys
import os
import logging
import cv2
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.database import fetch_image

logging.basicConfig(level=logging.INFO)

class ImageEditor:
    """
    This class provides functionalities to edit images using OpenCV.
    """

    def __init__(self):
        self.current_points = []
        self.is_drawing = False
        self.is_handicap = False
        self.saved_points = self.load_points()
        self.image_path = fetch_image()
        if self.image_path == 0:
            print("Error fetching image path from database")
            sys.exit(1)
        self.image = self.load_image()
        self.clone = self.image.copy() if self.image is not None else None

    def load_image(self):
        """
        Load an image from the specified path.
        """
        try:
            image = cv2.imread(self.image_path)
            if image is None:
                raise FileNotFoundError(f"Image not found at {self.image_path}")
            print("Image size:", image.shape[1], "x", image.shape[0])
            return image
        except FileNotFoundError as e:
            print(f"Error loading image: {e}")
            return None
        except (ValueError, TypeError) as e:
            print(f"Error resizing image: {e}")
            return None

    def load_points(self):
        """
        Load points from a pickle file.
        """
        try:
            with open("./backend/carSpots2.pkl", "rb") as file_in:
                try:
                    return pickle.load(file_in)
                except EOFError:
                    return []
        except FileNotFoundError:
            return []

    def click_and_draw(self, event, x, y, flags, param):
        """
        Handle mouse events to draw on the image.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.is_handicap = False
            color = (0, 255, 0)
            self.current_points = [(x, y)]
            self.is_drawing = True
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.is_handicap = True
            color = (255, 0, 0)
            self.current_points = [(x, y)]
            self.is_drawing = True
        elif event == cv2.EVENT_MOUSEMOVE:
            color = (255, 0, 0) if self.is_handicap else (0, 255, 0)
            if self.is_drawing:
                cv2.circle(self.image, (x, y), 3, color, -1)
                self.current_points.append((x, y))
        elif event in (cv2.EVENT_LBUTTONUP, cv2.EVENT_RBUTTONUP):
            color = (255, 0, 0) if self.is_handicap else (0, 255, 0)
            self.current_points.append((x, y))
            self.is_drawing = False
            cv2.polylines(self.image, [np.array(self.current_points)], True, color, 2)
            cv2.imshow("image", self.image)
            self.saved_points.append((list(self.current_points), self.is_handicap))

    def save_points(self):
        """
        Save points to a pickle file.
        """
        try:
            with open("./backend/carSpots2.pkl", "wb") as file_out:
                pickle.dump(self.saved_points, file_out)
        except pickle.PickleError as pickle_error:
            print(f"Error saving points: {pickle_error}")

    def run(self):
        """
        Run the image editor.
        """
        for point in self.saved_points:
            if len(point) == 2:
                point_group, is_handicap = point
                color = (255, 0, 0) if is_handicap else (0, 255, 0)
                cv2.polylines(self.image, [np.array(point_group)], True, color, 2)

        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("image", self.click_and_draw)

        while True:
            cv2.imshow("image", self.image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"):
                self.saved_points.clear()
                self.save_points()
                self.image = self.clone.copy()
                for point_group, is_handicap in self.saved_points:
                    color = (255, 0, 0) if is_handicap else (0, 255, 0)
                    cv2.polylines(self.image, [np.array(point_group)], True, color, 2)
            elif key == ord("c"):
                self.save_points()
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    editor = ImageEditor()
    editor.run()
