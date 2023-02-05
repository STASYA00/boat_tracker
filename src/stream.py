import cv2

class Stream:
    """
    Object that represents the incoming video stream to analyze.
    :params: fname      name of the file to read the stream from, str
    :params: stream     the stream itself, cv2.VideoCapture
    """
    def __init__(self, fname:str=None) -> None:
        self._fname:str = fname
        self._stream = self._load()

    def _load(self):
        """
        Function that initiates a stream.
        returns: stream             a new stream, cv2.VideoCapture
        """
        return cv2.VideoCapture(self.fname)

    def end(self):
        """
        Function that closes the stream.
        returns: None.
        """
        self._stream.release()

    def set_current(self, frame):
        """
        Function that sets the current frame.
        :params: frame          frame number to set the stream to, int, must be >=0 and less than total frame amount
        returns: None
        """
        assert (frame>=0 and frame<self.frames), \
        "Frame number {} does not fall in the range {}..{}".format(frame, 0, self.frames)
        
        self._stream.set(cv2.CAP_PROP_POS_FRAMES, frame)

    @property
    def current_frame(self):
        """
        Function that returns the current frame number, int
        """
        return self._stream.get(cv2.CAP_PROP_POS_FRAMES)

    @property
    def stream(self):
        """
        Function that returns the current stream, cv2.VideoCapture
        """
        return self._stream

    @property
    def frame_rate(self):
        """
        Function that returns the current frame rate, float
        """
        return self._stream.get(cv2.CAP_PROP_FPS)

    @property
    def width(self):
        """
        Function that returns the current stream's width, int
        """
        return self._stream.get(cv2.CAP_PROP_FRAME_WIDTH)

    @property
    def height(self):
        """
        Function that returns the current stream's height, int
        """
        return self._stream.get(cv2.CAP_PROP_FRAME_HEIGHT)

    @property
    def fname(self):
        """
        Function that returns the current stream's filepath, str
        """
        return self._fname

    @property
    def frames(self):
        """
        Function that returns the current stream's total frame amount, int
        """
        return self._stream.get(cv2.CAP_PROP_FRAME_COUNT)