import cv2

from singleton_meta import SingletonMeta

class GraphicsConfig(metaclass=SingletonMeta):
    def __init__(self):
        self._color = [0,0,0]
        self._stroke = 2
        self._name = "#{}"
        self._total_name = "TOTAL: {}"
        self._font = cv2.FONT_HERSHEY_SIMPLEX
        self._fontscale = 0.5
        self._total = True
        self._total_location = [30, 30]

    @property
    def color(self):
        return self._color

    @property
    def stroke(self):
        return self._stroke

    @property
    def name(self):
        return self._name

    @property
    def total_name(self):
        return self._total_name

    @property
    def font(self):
        return self._font

    @property
    def fontscale(self):
        return self._fontscale
    
    @property
    def display_total(self):
        return self._total

    @property
    def total_location(self):
        return self._total_location


class Graphics:
    def __init__(self):
        self.config = GraphicsConfig()
        self.thr = 0.3

    def make(self, frame, boat:str, bb:list):

        return self._make(frame, boat, bb)

    def _check(self, y:int, bb:list):
        
        if (bb[1] < y and bb[1] + bb[3] < y):
            return True
        elif (bb[1] + bb[3] > y):
            p = (bb[1] + bb[3] - y) / bb[3]
            return p < self.thr
        return False


    def _make(self, frame, label:str, bb:list):
        # box is [left, top, w, h]
        if (self._check(frame.shape[0]*0.5, bb)):
            p1 = (int(bb[0]), int(bb[1]))
            p2 = (int(bb[0] + bb[2]), int(bb[1] + bb[3]))

            orig = (p1[0], p1[1] - 5)
            cv2.rectangle(frame, p1, p2, self.config.color, self.config.stroke)
            cv2.putText(frame, self.config.name.format(label), orig, 
                        self.config.font, self.config.fontscale, self.config.color)
        
        return frame

    def add_total(self, frame, total:int):
        
        if (self.config.display_total and total>0):
            cv2.putText(frame, self.config.total_name.format(total), 
                        self.config.total_location, 
                        self.config.font, self.config.fontscale, 
                        self.config.color)
        return frame