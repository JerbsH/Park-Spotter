"""
This module contains unit tests for the boxes_overlap function in the streamyolo module.
"""

import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.streamyolo import boxes_overlap  # Import placed at the top of the module

class TestStreamYolo(unittest.TestCase):
    """
    This class contains unit tests for the streamyolo module.
    """

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
