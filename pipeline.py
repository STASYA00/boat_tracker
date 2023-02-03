
import cv2
from boat_detector import *
from stream import Stream

class Pipeline:
    def __init__(self, value) -> None:
        self.value = value
        self._stream = Stream(self.value)

    def run(self):
        self._stream.set_current(0)
        while self._stream.stream.isOpened():
            _, frame = self._stream.stream.read()
            if not self._run(frame):
                break
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        self._stream.end()
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
