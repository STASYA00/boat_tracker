import cv2
import numpy as np
import os
import sys
import unittest
import uuid

sys.path.append('../')
from graphics import Graphics

ASSET = "1.mp4"


class GraphicsTest(unittest.TestCase):
    def test_draw(self):
        g = Graphics()
        k = np.ones((500,500,3)) * 255
        bb = [20, 200, 250, 50]
        g.make(k, str(uuid.uuid4())[:6], bb)
        cv2.imwrite("img.png", k)
        self.assertEqual(True, True)
        # check __manually__ that rectangle and label are drawn 

    def test_not_draw(self):
        g = Graphics()
        k = np.ones((500,500,3)) * 255
        bb = [20, 500, 80, 200]
        g.make(k, str(uuid.uuid4())[:6], bb)
        cv2.imwrite("img1.png", k)
        self.assertEqual(True, True)
        # check __manually__ that rectangle and label are not drawn

if __name__ == '__main__':
	unittest.main(verbosity=2)
