
import cv2
import sys

from boat import *
from boat_detector import *
from config import DeepSortConfig
from stream import Stream
from video_w import VideoW
from graphics import Graphics

sys.path.append('../deep_sort')

from deep_sort import DeepSort

class Pipeline:
    def __init__(self, value, write=False, show=False) -> None:
        self._boats = Collection()
        self.value = value
        self._stream = Stream(self.value)
        self._out = None 
        self._show = show
        if (write):
            self._out = VideoW(self._stream.frame_rate)

    def run(self):
        f = 0
        self._stream.set_current(f)
        while self._stream.stream.isOpened():
            _, frame = self._stream.stream.read()
            print("Processing frame {}".format(f))
            if not self._run(frame):
                break
            if self._out:
                self._out.write(frame)
            if self._show:
                cv2.imshow("", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            f += 1

        self._stream.end()
        if self._out:
            self._out.end()
        return

    def _run(self, frame) -> bool:
        return True

class Yolo3Pipeline(Pipeline):
    def __init__(self, value) -> None:
        super().__init__(value)
        self._model = BoatDetector(MODELS.YOLO3)

    def _run(self, frame) -> bool:
        res = self._model.run(frame)
        return True

class Yolo5DeepSortPipeline(Pipeline):
    def __init__(self, value, write=False, show=False) -> None:
        super().__init__(value, write, show)
        self._model = BoatDetector()
        self._tracker = DeepSort(DeepSortConfig().model)
        self._graphics = Graphics()

    def _check_seen(self, label):
        r = self._boats.contains(label)
        if not r:
            self._boats.add(Boat(), label)
        return r
    
    def _run(self, frame) -> bool:

        res = self._model.run(frame)
        res = self._tracker.update(res[:, :4], res[:,4], res[:,-1], frame)

        for r in res:
            label = r[4]
            if (label!=1):
                _ = self._check_seen(label)
                r = Bbox.yolo2standard(r)
                self._graphics.make(frame, str(self._boats.get_id(label))[:6], r)

        self._graphics.add_total(frame, self._boats.length)
        
        
        return True

