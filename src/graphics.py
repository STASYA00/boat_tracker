import cv2

from singleton_meta import SingletonMeta

class GraphicsConfig(metaclass=SingletonMeta):
    """
    Object that contains the style of the graphics for the output.

    :params: color          color to use for text and detection [0..255], list [r, g, b]
    :params: stroke         width of stroke to use for the bounding boxes, int
    :params: name           annotation format for a detected object, str
    :params: total_name     annotation format for the total amount of detected objects, str
    :params: font           font to use for the annotations, int
    :params: fontscale      font size to use for the annotations, float or int
    :params: total          option to display the total amount of objects detected, bool
    :params: total_location position of the annotation of the total amount of objects detected, list [int, int]
    """
    def __init__(self)->None:
        self._color:list = [0,0,0]
        self._stroke:int = 2
        self._name:str = "#{}"
        self._total_name:str = "TOTAL: {}"
        self._font:int = cv2.FONT_HERSHEY_SIMPLEX
        self._fontscale:float|int = 0.5
        self._total:bool = True
        self._total_location:list = [30, 30]

    @property
    def color(self):
        """
        Function that returns the color to use for text and detection [0..255], list [r, g, b]
        """
        return self._color

    @property
    def stroke(self):
        """
        Function that returns the width of stroke to use for the bounding boxes, int
        """
        return self._stroke

    @property
    def name(self):
        """
        Function that returns the annotation format for a detected object, str
        """
        return self._name

    @property
    def total_name(self):
        """
        Function that returns the annotation format for the total amount of detected objects, str
        """
        return self._total_name

    @property
    def font(self):
        """
        Function that returns the font to use for the annotations, int
        """
        return self._font

    @property
    def fontscale(self):
        """
        Function that returns the font size to use for the annotations, float or int
        """
        return self._fontscale
    
    @property
    def display_total(self):
        """
        Function that returns whether to display the total amount of objects detected, bool
        """
        return self._total

    @property
    def total_location(self):
        """
        Function that returns the position of the annotation of the total amount of objects detected, list [int, int]
        """
        return self._total_location


class Graphics:
    """
    Object that is responsible for drawing within the frame.
    :params: config         graphics parameters, GraphicsConfig
    :params: thr            threshold not to display any graphics on, float
    """
    def __init__(self):
        self._config = GraphicsConfig()
        self.thr = 0.3

    def make(self, frame, boat:str, bb:list):
        """
        Function that draws a boat annotation within a frame.
        :params: frame          matrix to draw on, np.ndarray(h, w, ch)
        :params: boat           label to annotate the boat with, str
        :params: bb             bounding box to draw, list [left, top, width, height]

        returns frame           annotated frame, np.ndarray(h, w, ch)
        """

        return self._make(frame, boat, bb)

    def _check(self, y:int, bb:list)->bool:
        """
        Function that checks whether a bounding box is within the area that
        is restricted for drawing.
        :params: y              matrix height, int
        :params: bb             bounding box to draw, list [left, top, width, height]

        returns: res            lies within the allowed to draw upon area or not, bool
        """
        if (bb[1] < y and bb[1] + bb[3] < y):
            return True
        elif (bb[1] + bb[3] > y):
            p = (bb[1] + bb[3] - y) / bb[3]
            return p < self.thr
        return False


    def _make(self, frame, label:str, bb:list):
        """
        Function that draws a boat annotation within a frame.
        :params: frame          matrix to draw on, np.ndarray(h, w, ch)
        :params: boat           label to annotate the boat with, str
        :params: bb             bounding box to draw, list [left, top, width, height]

        returns frame           annotated frame, np.ndarray(h, w, ch)
        """
        
        if (self._check(frame.shape[0]*0.5, bb)):
            p1 = (int(bb[0]), int(bb[1]))
            p2 = (int(bb[0] + bb[2]), int(bb[1] + bb[3]))

            orig = (p1[0], p1[1] - 5)
            cv2.rectangle(frame, p1, p2, self._config.color, self._config.stroke)
            cv2.putText(frame, self._config.name.format(label), orig, 
                        self._config.font, self._config.fontscale, self._config.color)
        
        return frame

    def add_total(self, frame, total:int):
        """
        Function that draws a total annotation within a frame.
        :params: frame          matrix to draw on, np.ndarray(h, w, ch)
        :params: total          total number of objects, int

        returns frame           annotated frame, np.ndarray(h, w, ch)
        """
        if (self._config.display_total and total>0):
            cv2.putText(frame, self._config.total_name.format(total), 
                        self._config.total_location, 
                        self._config.font, self._config.fontscale, 
                        self._config.color)
        return frame