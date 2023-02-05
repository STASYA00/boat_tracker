import cv2

from enum import Enum

from singleton_meta import SingletonMeta

class TRACKERS(Enum):
    """
    Collection of trackers to use for object tracking.
    """
    CSRT = 0,
    MOSSE = 1,
    DEEPSORT = 2,
    SORT = 3,
    GOTURN = 4,
    KCF = 5,

def not_implemented():
    """
    function placeholder
    """
    return

def test_function():
    """
    function placeholder
    """
    print(123)

class TrackerFactory(metaclass=SingletonMeta):
    """
    Object that is responsible for producing a tracker based on its type.
    :params: content            mapping of tracker names to their respective functions, dict {TRACKER: func}
    """
    def __init__(self) -> None:
        self._content = {
            #TRACKERS.CSRT: cv2.legacy.TrackerCSRT_create,
            TRACKERS.MOSSE: test_function, # cv2.legacy.TrackerMOSSE_create
            TRACKERS.DEEPSORT: not_implemented,
            TRACKERS.SORT: not_implemented,
            TRACKERS.GOTURN: not_implemented,
            #TRACKERS.KCF: cv2.legacy.TrackersKCF_create,
        }

    def get(self, tracker: int)->function:
        """
        Function that produces a tracker based on the desired tracker type.
        :params: tracker            tracker to produce, one of TRACKERS, int
        """
        assert tracker in TRACKERS, "wrong Tracker index"
        return self._content[tracker]



class Tracker:
    """
    Object that represents a multitracker.
    :params: tracker            multitracker, cv2.MultiTracker | None
    :params: tracker_type       trackers the multitracker will consist of, cv2.tracker
    """
    def __init__(self, tracker_type:int=TRACKERS.MOSSE)->None:
        self._tracker = None
        self.new()
        self._tracker_type = tracker_type

    def add(self, frame, boxes:list)->None:
        """
        Function that adds a tracker to the multitracker.
        :params: frame          frame to start the new tracker from, np.ndarray(h, w, ch)
        :params: boxes          boxes existing in this frame to track in the following ones, list

        returns: None
        """
        if self._tracker:
            for box in boxes:
                # box is [x,y,w,h]
                #b = [box[0], box[1], box[2]-box[0], box[3]-box[1]]
                self._tracker.add(TrackerFactory().get(self._tracker_type)(), frame, box[:4])

    def check(self):
        """
        Function that prints out what the main multitracker consists of, all the tracker objects
        within it. Testing purposes.
        """
        print(self._tracker.getObjects())

    def new(self)->None:
        """
        Function that initiates a new multitracker object.
        """
        #self._tracker = cv2.legacy.MultiTracker_create()
        return

    def update(self, frame)->list:
        """
        Function that updates the predictions of all the trackers within a multitracker.
        :params: frame          frame to update the trackers upon, np.ndarray(h, w, ch)
        returns: res            resulting boxes based on the tracking history and visual features, list
        """
        _, boxes = self._tracker.update(frame)
        return boxes

class DeepSortTracker(Tracker):
    """
    Objects that is a wrapper around the deepsort implementation.
    Not finished due to the conceptual differences with the parent class.
    """
    def __init__(self, tracker_type=TRACKERS.DEEPSORT):
        super().__init__(tracker_type)

    def add(self, frame, boxes)->None:
        """
        This tracker does not consist of multiple trackers, so there is no need
        to add a small tracker for each box or frame.
        """
        return

    def update(self, frame)->list:
        """
        Function that updates the predictions of all the trackers within a multitracker.
        :params: frame          frame to update the trackers upon, np.ndarray(h, w, ch)
        returns: res            resulting boxes based on the tracking history and visual features, list
        """
        _, boxes = self._tracker.update(frame)
        return boxes