import cv2

from enum import Enum

from singleton_meta import SingletonMeta

class TRACKERS(Enum):
    CSRT = 0,
    MOSSE = 1,
    DEEPSORT = 2,
    SORT = 3,
    GOTURN = 4,
    KCF = 5,

def not_implemented():
    return

def test_function():
    print(123)

class TrackerFactory(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._content = {
            #TRACKERS.CSRT: cv2.legacy.TrackerCSRT_create,
            TRACKERS.MOSSE: test_function, # cv2.legacy.TrackerMOSSE_create
            TRACKERS.DEEPSORT: not_implemented,
            TRACKERS.SORT: not_implemented,
            TRACKERS.GOTURN: not_implemented,
            #TRACKERS.KCF: cv2.legacy.TrackersKCF_create,
        }

    def get(self, tracker: int):
        assert tracker in TRACKERS, "wrong Tracker index"
        return self._content[tracker]



class Tracker:
    def __init__(self, tracker_type=TRACKERS.MOSSE):
        self.tracker = None
        self.new()
        self._tracker_type = tracker_type

    def add(self, frame, boxes)->None:
      for box in boxes:
          # box is [x,y,w,h]
          #b = [box[0], box[1], box[2]-box[0], box[3]-box[1]]
          self._tracker.add(TrackerFactory().get(self._tracker_type)(), frame, box[:4])

    def check(self):
        print(self._tracker.getObjects())

    def new(self)->None:
        #self._tracker = cv2.legacy.MultiTracker_create()
        return

    def update(self, frame)->list:
        _, boxes = self._tracker.update(frame)
        return boxes