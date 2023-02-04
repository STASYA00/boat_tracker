import cv2
import unittest
import sys

sys.path.append('../')
sys.path.append('../deep_sort')

from deep_sort import DeepSort
from config import DeepSortConfig

from boat_detector import BoatDetector
from graphics import Graphics
from stream import Stream
from video_w import VideoW, VideoConfig
#from deep_sort.utils.parser import get_config

ASSET = "2.mp4"

class BoatTest(unittest.TestCase):

    def test_id(self):
        v = Stream(ASSET)
        out = VideoW(v.frame_rate)
        d = BoatDetector()
        g = Graphics()
        d1 = DeepSort(DeepSortConfig().model)

        while v.stream.isOpened():
            _, frame = v.stream.read()
            res = d.run(frame)
            
            res = d1.update(res[:, :4], res[:,4], res[:,-1], frame)
            
            print("res:\t{}".format(res))

            for r in res:
                label = r[4]
                r = [r[0], r[1], r[2]-r[0], r[3]-r[1]]
                print("boat: {}\t{}".format(label, r))
                g.make(frame, str(label) + "_boat", r)
            out.write(frame)
            cv2.imshow("test", frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        v.end()
        out.end()

        self.assertEqual(1, 1)



if __name__ == '__main__':
	unittest.main(verbosity=2)