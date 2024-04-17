"""
This module contains unit tests for the streamyolo module.
"""

import os
import sys
import time
import threading
import unittest
from unittest.mock import Mock
import cv2
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.modules['database'] = Mock()
from backend.streamyolo import boxes_overlap


class TestStreamYolo(unittest.TestCase):
    """
    This class contains unit tests for the streamyolo module.
    """
    stop_event = threading.Event()

    @classmethod
    def setUpClass(cls):
        video_path = os.getenv('SECURE_URL')

        def open_video_stream():
            start_time = time.time()
            while time.time() - start_time < 5:
                if cls.stop_event.is_set():
                    break
                cls.cap = cv2.VideoCapture(video_path)
                if cls.cap.isOpened():
                    return True
                cls.cap.release()
                time.sleep(0.1)
            return False

        video_thread = threading.Thread(target=open_video_stream)
        video_thread.start()
        video_thread.join(timeout=5)

        if video_thread.is_alive():
            cls.stop_event.set()
            print("Could not open video file. Exiting tests.")
            try:
                sys.exit(1)
            except SystemExit:
                os._exit(1)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'cap') and cls.cap.isOpened():
            cls.cap.release()

    def test_boxes_overlap(self):
        """
        This method tests the boxes_overlap function with various test cases.
        """

        # Test case: boxes do not overlap
        box1 = [0, 0, 1, 1]
        box2 = [2, 2, 3, 3]
        self.assertFalse(boxes_overlap(box1, box2))

        # Test case: boxes overlap but less than 50%
        box1 = [0, 0, 2, 2]
        box2 = [1, 1, 3, 3]
        self.assertFalse(boxes_overlap(box1, box2))

        # Test case: boxes overlap by 50%
        box1 = [0, 0, 2, 2]
        box2 = [1, 0, 3, 2]
        self.assertTrue(boxes_overlap(box1, box2))

        # Test case: boxes overlap more than 50%
        box1 = [0, 0, 2, 2]
        box2 = [0, 0, 2, 1]
        self.assertTrue(boxes_overlap(box1, box2))

if __name__ == '__main__':
    unittest.main()
