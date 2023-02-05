import unittest
import sys

sys.path.append('../')

from pipeline import Yolo5DeepSortPipeline

ASSET = "1.mp4"

class PipeTest(unittest.TestCase):

    def test(self):

        pipe = Yolo5DeepSortPipeline(ASSET, write=True, show=False)
        pipe.run()
        self.assertEqual(1, 1)



if __name__ == '__main__':
	unittest.main(verbosity=2)