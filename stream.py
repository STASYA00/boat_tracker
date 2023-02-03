import cv2

class Stream:
    def __init__(self, fname:str=None) -> None:
        self.fname = fname
        self._stream = self._load()

    def _load(self):
        return cv2.VideoCapture(self.fname)

    def end(self):
        self._stream.release()

    def set_current(self, frame):
        assert (frame>=0 and frame<self.frames), 
        "Frame number {} does not fall in the range {}..{}".format(frame, 0, self.frames)
        
        self._stream.set(cv2.CAP_PROP_POS_FRAMES, frame)

    @property
    def current_frame(self):
        return self._stream.get(cv2.CAP_PROP_POS_FRAMES)

    @property
    def stream(self):
        return self._stream

    @property
    def frame_rate(self):
        return self._stream.get(cv2.CAP_PROP_POS_FRAMES)

    @property
    def width(self):
        return self._stream.get(cv2.CAP_PROP_FRAME_WIDTH)

    @property
    def height(self):
        return self._stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

    @property
    def frames(self):
        return self._stream.get(cv2.CAP_PROP_FRAME_COUNT)