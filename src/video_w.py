import cv2

from singleton_meta import SingletonMeta

class VideoConfig(metaclass=SingletonMeta):
    """
    Object that holds the configuration for the output.
    :params: width          width of the output, int
    :params: height         height of the output, int
    :params: name           path to the output file, str
    """
    def __init__(self):
        self._width = 1280
        self._height = 720
        self._name = "./out.avi"

    @property
    def width(self)->int:
        """
        Function that returns the desired width of the output, int
        """
        return self._width

    @property
    def height(self)->int:
        """
        Function that returns the desired height of the output, int
        """
        return self._height

    @property
    def name(self)->str:
        """
        Function that returns the path to write the output to, str
        """
        return self._name

class VideoW:
    # not the best naming, but didn't want to confuse with
    # the cv2.VideoWriter 
    """
    Object that is responsible for writing out the output.
    :params: config             parameters for the output, VideoConfig
    :params: frame_rate         frame rate for the output, int
    :params: out                video stream, cv2.VideoWriter
    """
    def __init__(self, frame_rate=10)->None:
        self._config:VideoConfig = VideoConfig()
        self._frame_rate:int|float = frame_rate
        self._out = self._make()

    def write(self, frame)->None:
        """
        Function that writes given frame to the stream.
        :params: frame          frame to write to the stream, np.ndarray(h, w, ch)
        returns: None   
        """
        assert (frame.shape[0]==self._config.height and frame.shape[1]==self._config.width), \
        "Wrong frame size: {}x{} instead of {}x{}".format(frame.shape[0], frame.shape[1],
                                                          self._config.width, self._config.height)
        self._out.write(frame)

    def end(self)->None:
        """
        Function that closes the video stream.
        returns: None
        """
        self._out.release()
        

    def _make(self):
        """
        Function that makes a video stream to stream the output into a file.
        returns: video stream, cv2.VideoWriter
        
        """
        return cv2.VideoWriter(self._config.name, 
                               cv2.VideoWriter_fourcc('M','J','P','G'), 
                               self._frame_rate,
                               (self._config.width, self._config.height))
        
    


