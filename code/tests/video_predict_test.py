import cv2
import os
import sys
import unittest
import uuid

sys.path.append('../')
from boat_detector import BoatDetector, MODELS
from graphics import Graphics
from stream import Stream
from video_w import VideoW, VideoConfig
ASSET = "2.mp4"

# integration test

class WriteTest(unittest.TestCase):
    
    def test_file_writing(self):
        v = Stream(ASSET)
        out = VideoW(v.frame_rate)
        d = BoatDetector(MODELS.YOLO5)
        g = Graphics()
        

        v.set_current(0)
        while v.stream.isOpened():
            _, frame = v.stream.read()
            res = d.run(frame)
            for r in res:
                g.make(frame, str(uuid.uuid4())[:6], r)
            out.write(frame)
            cv2.imshow("test", frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        v.end()
        out.end()
        self.assertTrue(VideoConfig().name[2:] in os.listdir())


if __name__ == '__main__':
	unittest.main(verbosity=2)