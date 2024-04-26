"""
This module contains unit tests for the streamyolo module.
"""

import os
import sys
import time
import threading
import unittest
from unittest.mock import Mock, patch
import numpy as np
import cv2
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.modules['database'] = Mock()
import backend.streamyolo as streamyolo
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
                sys.exit(0)
            except SystemExit:
                os._exit(0)

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

    @patch('backend.streamyolo.torch.hub.load')
    @patch('backend.streamyolo.cv2.VideoCapture')
    @patch('backend.streamyolo.pickle.load')
    def test_load_resources(self, mock_pickle_load, mock_video_capture, mock_torch_load):
        """
        This method tests the load_resources function.
        """
        mock_torch_load.return_value = 'dummy_model'
        mock_video_capture.return_value.isOpened.return_value = True
        mock_pickle_load.return_value = [('dummy_point_group', 'dummy_is_handicap')]

        streamyolo.load_resources()

        self.assertEqual(streamyolo.MODEL, 'dummy_model')
        self.assertTrue(streamyolo.CAPTURE.isOpened())

    def test_calculate_centroids(self):
        """
        This method tests the calculate_centroids function.
        """
        dummy_data = [np.array([[0, 0], [10, 10]]), np.array([[10, 10], [20, 20]])]
        expected_centroids = [(5, 5), (15, 15)]

        actual_centroids = streamyolo.calculate_centroids(dummy_data)

        self.assertEqual(actual_centroids, expected_centroids)

    @patch('backend.streamyolo.cv2.pointPolygonTest')
    def test_box_in_regions(self, mock_point_polygon_test):
        """
        This method tests the box_in_regions function.
        """
        dummy_box = (5, 5, 15, 15)
        dummy_regions = [np.array([[0, 0], [10, 10]]), np.array([[10, 10], [20, 20]])]
        dummy_handicap_regions = [np.array([[0, 0], [10, 10]])]
        expected_result = [True, True]
        mock_point_polygon_test.return_value = 1

        actual_result = [streamyolo.box_in_regions(dummy_box, region, dummy_handicap_regions) for region in dummy_regions]  # Modify this line

        self.assertEqual(actual_result, expected_result)

if __name__ == '__main__':
    unittest.main()
