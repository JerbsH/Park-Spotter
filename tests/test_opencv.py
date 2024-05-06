"""
This module contains unit tests for the ImageEditor class from the opencv module.
"""

import unittest
from unittest import mock
import sys
import os
import cv2
import numpy as np
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.opencv import ImageEditor

class TestImageEditor(unittest.TestCase):
    """
    This class contains unit tests for the ImageEditor class.
    """

    def setUp(self):
        """
        This method sets up the test environment. It is called before each test method is executed.
        """
        self.image_path = "test_image_path"
        self.image = np.array([[255, 255, 255], [255, 255, 255], [255, 255, 255]])
        self.points = [(100, 100), (200, 200), (300, 300)]

    @mock.patch('backend.opencv.fetch_image', return_value="test_image_path")
    def test_init(self, mock_fetch_image):
        """
        Test case for the __init__ method.
        """
        with mock.patch('backend.opencv.ImageEditor.load_image', return_value=self.image):
            editor = ImageEditor()
            self.assertEqual(editor.image_path, self.image_path)
            np.testing.assert_array_equal(editor.image, self.image)

    @mock.patch('backend.opencv.fetch_image', return_value="test_image_path")
    def test_load_image(self, mock_fetch_image):
        """
        Test case for the load_image method.
        """
        with mock.patch('cv2.imread', return_value=self.image):
            editor = ImageEditor()
            loaded_image = editor.load_image()
            np.testing.assert_array_equal(loaded_image, self.image)

    @mock.patch('backend.opencv.fetch_image', return_value="test_image_path")
    def test_load_points(self, mock_fetch_image):
        """
        Test case for the load_points method.
        """
        with mock.patch('pickle.load', return_value=self.points):
            editor = ImageEditor()
            loaded_points = editor.load_points()
            self.assertEqual(loaded_points, self.points)

    @mock.patch('backend.opencv.fetch_image', return_value="test_image_path")
    def test_click_and_draw(self, mock_fetch_image):
        """
        Test case for the click_and_draw method.
        """
        with mock.patch('cv2.circle'), \
             mock.patch('cv2.polylines'), \
             mock.patch('cv2.imshow'):
            editor = ImageEditor()
            editor.click_and_draw(cv2.EVENT_LBUTTONDOWN, 100, 100, None, None)
            self.assertTrue(editor.is_drawing)
            self.assertEqual(editor.current_points, [(100, 100)])

    @mock.patch('backend.opencv.fetch_image', return_value="test_image_path")
    def test_save_points(self, mock_fetch_image):
        """
        Test case for the save_points method.
        """
        with mock.patch('pickle.dump'):
            editor = ImageEditor()
            editor.save_points()

    @mock.patch('backend.opencv.fetch_image', return_value="test_image_path")
    def test_run(self, mock_fetch_image):
        """
        Test case for the run method.
        """
        with mock.patch('cv2.polylines'), \
             mock.patch('cv2.namedWindow'), \
             mock.patch('cv2.setMouseCallback'), \
             mock.patch('cv2.imshow'), \
             mock.patch('cv2.waitKey', return_value=ord('c')), \
             mock.patch('cv2.destroyAllWindows'), \
             mock.patch('backend.opencv.ImageEditor.load_image', return_value=self.image):
            editor = ImageEditor()
            editor.run()

if __name__ == '__main__':
    unittest.main()
