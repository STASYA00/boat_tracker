
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
    """
    Object that defines a sequence of actions for boat detection based on the objective.
    :params: boats          collection of detected boats, Collection
    :params: value          path to the file to detect the boats from, str
    :params: stream         video stream to detect the boats from, Stream
    :params: out            video stream to write if needed, VideoW | None
    :params: show           an option to display the video on the screen, bool, default False
    :params: write          an option to write the result to a file, bool, default False
    """
    def __init__(self, value:str, write:bool=False, show:bool=False) -> None:
        self._boats:Collection = Collection()
        self.value:str = value
        self._stream:Stream = Stream(self.value)
        self._out:VideoW | None = None 
        self._show:bool = show
        if (write):
            self._out = VideoW(self._stream.frame_rate)

    def run(self) -> None:
        """
        Function to run the pipeline. Runs the videostream and performs a set of actions
        based on the objective.
        """
        f = 0
        self._stream.set_current(f)
        while self._stream.stream.isOpened():
            _, frame = self._stream.stream.read()
            print("Processing frame {}".format(f)) # being user-friendly
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
        """
        Function that processes the video frame by frame. Different for each pipeline.
        :params: frame          matrix to process, np.ndarray(h, w, ch)
        """
        return True

class Yolo3Pipeline(Pipeline):
    """
    Pipeline child object that only does object detections with yolo3.

    :params: model              model to use for object detection, BoatDetector
    """
    def __init__(self, value, write:bool=False, show:bool=False) -> None:
        super().__init__(value, write, show)
        self._model = BoatDetector(MODELS.YOLO3)

    def _run(self, frame) -> bool:
        """
        Function that processes the video frame by frame and detects the boats in each.
        :params: frame          matrix to process, np.ndarray(h, w, ch)
        """
        res = self._model.run(frame)
        return True

class Yolo5DeepSortPipeline(Pipeline):
    def __init__(self, value, write=False, show=False) -> None:
        super().__init__(value, write, show)
        self._model = BoatDetector()
        self._tracker = DeepSort(DeepSortConfig().model)
        self._graphics = Graphics()

    def _check_seen(self, label):
        """
        Function that checks whether a boat has been seen before. If the boat is new it is 
        added to the boat collection.
        :param: label           label from DeepSort, int
        returns: res            result whether a boat has been seen before, bool
        """
        r = self._boats.contains(label)
        if not r:
            self._boats.add(Boat(), label)
        return r
    
    def _run(self, frame) -> bool:
        """
        Function that processes the video frame by frame, detects and tracks the boats in each.
        :params: frame          matrix to process, np.ndarray(h, w, ch)
        """
        res = self._model.run(frame)
        res = self._tracker.update(res[:, :4], res[:,4], res[:,-1], frame)

        for r in res:
            label = r[4]
            if (label!=1): # the boat the camera is on
                _ = self._check_seen(label)
                r = Bbox.yolo2standard(r)
                self._graphics.make(frame, str(self._boats.get_id(label))[:6], r)
                # label is shortened for graphic purposes, but each boat has a unique UUID

        self._graphics.add_total(frame, self._boats.length)  # annotate with the total number of boats detected
        
        
        return True

