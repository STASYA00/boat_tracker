import cv2

from singleton_meta import SingletonMeta

class VideoConfig(metaclass=SingletonMeta):
    def __init__(self):
        self._width = 1280
        self._height = 720
        self._name = "out.avi"

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def name(self):
        return self._name

class VideoW:
    # not the best naming, but didn't want to confuse with
    # the cv2.VideoWriter 
    def __init__(self, frame_rate=10)->None:
        self.config = VideoConfig()
        self.frame_rate = frame_rate
        self._out = self._make()
        

    def _make(self):
        return cv2.VideoWriter(self.config.name, 
                               cv2.VideoWriter_fourcc('M','J','P','G'), 
                               self.frame_rate,
                               (self.config.width, self.config.height))
        
    def write(self, frame):
        assert (frame.shape[0]==self.width and frame.shape[1]==self.height), 
        "Wrong frame size: {}x{} instead of {}x{}".format(frame.shape[0], frame.shape[1],
                                                          self.width, self.height)
        self._out.write(frame)

    def end(self):
        self._out.release()


