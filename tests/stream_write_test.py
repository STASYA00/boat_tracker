import cv2
import os
import sys
import unittest

sys.path.append('../')
from stream import Stream
from video_w import VideoW, VideoConfig
ASSET = "1.mp4"

class WriteTest(unittest.TestCase):
    
    def test_file_writing(self):
        v = Stream(ASSET)
        out = VideoW(v.frame_rate)
        v.set_current(0)
        while v.stream.isOpened():
            _, frame = v.stream.read()
            out.write(frame)
            cv2.imshow("test", frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        v.end()
        out.end()
        self.assertTrue(VideoConfig().name[2:] in os.listdir())

    def test_frames(self):
        v = Stream(ASSET)
        out = VideoW(v.frame_rate)
        v.set_current(0)
        while v.stream.isOpened():
            _, frame = v.stream.read()
            out.write(frame)
            cv2.imshow("test", frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        i = v.current_frame
        v.end()
        out.end()
        v = Stream(VideoConfig().name)
        self.assertEqual(i, v.frames)


if __name__ == '__main__':
	unittest.main(verbosity=2)