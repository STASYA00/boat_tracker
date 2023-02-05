import cv2
import sys
import uuid

sys.path.append('../')
from stream import Stream
ASSET = "1.mp4"

class Test:
    def __init__(self):
        self.name = "custom test"

    def run(self):
        v = Stream(ASSET)
        v.set_current(0)
        while v.stream.isOpened():
            _, frame = v.stream.read()
            cv2.imshow("test", frame)
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        v.end()
        return True


if __name__ == '__main__':
    t = Test()
    t.run()