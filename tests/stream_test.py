import os
import sys
import unittest

sys.path.append('../')
from stream import Stream

ASSET = "1.mp4"

class StreamTest(unittest.TestCase):

    def test_fname(self):
        s = Stream(ASSET)
        self.assertEqual(s.fname, ASSET)

    def test_change_fname(self):
        s = Stream(ASSET)
        with self.assertRaises(AttributeError):
            s.fname = "gnome"
    
    def test_width(self):
        s = Stream(ASSET)
        self.assertEqual(s.width, 1280)

    def test_height(self):
        s = Stream(ASSET)
        self.assertEqual(s.height, 720)

    def test_fps(self):
        s = Stream(ASSET)
        self.assertEqual(int(s.frame_rate), 23)

    def test_frames(self):
        s = Stream(ASSET)
        self.assertEqual(int(s.frames), 2879)



if __name__ == '__main__':
	unittest.main(verbosity=2)
