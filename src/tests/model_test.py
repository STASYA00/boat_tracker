import cv2
import sys
import unittest

sys.path.append('../')
from boat_detector import BoatDetector, MODELS

ASSET = "detect_test.jpg"

class BoatDetectorTest(unittest.TestCase):

    def test_detect(self):
        im = cv2.imread(ASSET)
        d = BoatDetector()
        res = d.run(im)
        self.assertTrue(len(res)==1)
        # detects only boat, no other object

    def test_read_yolov3(self):
        im = cv2.imread(ASSET)
        d = BoatDetector(MODELS.YOLO3)
        res = d.run(im)
        print(res)
        self.assertTrue(len(res)==1)
        # detects only boat, no other object

    def test_format(self):
        im = cv2.imread(ASSET)
        d = BoatDetector()
        res = d.run(im)[0]
        self.assertTrue(len(res)==4) # correct format

    def test_w(self):
        im = cv2.imread(ASSET)
        d = BoatDetector()
        res = d.run(im)[0]
        self.assertTrue(res[2]<750 and res[2]>700)

    def test_h(self):
        im = cv2.imread(ASSET)
        d = BoatDetector()
        res = d.run(im)[0]
        self.assertTrue(res[3]>320 and res[3]<330)



if __name__ == '__main__':
	unittest.main(verbosity=2)