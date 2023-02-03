import cv2

from singleton_meta import SingletonMeta

class GraphicsConfig(metaclass=SingletonMeta):
    def __init__(self):
        self._color = [0,0,0]
        self._stroke = 3
        self._name = "#{}"
        self._font = cv2.FONT_HERSHEY_SIMPLEX
        self._fontscale = 2

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
    def font(self):
        return self._font

    @property
    def fontscale(self):
        return self._fontscale


class Graphics:
    def __init__(self):
        self.config = GraphicsConfig()
        self.thr = 0.3

    def make(self, frame, boat, bb):

        return self._make(frame, boat, bb)

    def _check(self, y, bb):
        if (bb[1] < y and bb[3] < y):
            return True
        elif (bb[3]>y):
            p = (bb[3] - y) / (bb[3] - bb[1])
            return p < self.thr
        return False

    def _make(self, frame, label, bb):
        # box is [x,y,w,h]
        if (self._check(frame.shape[0]*0.5, bb)):
            print("passed")
            p1 = (int(bb[0]), int(bb[1]))
            p2 = (int(bb[0] + bb[2]), int(bb[1] + bb[3]))

            orig = (p1[0], p1[1] - 5)
            cv2.rectangle(frame, p1, p2, self.config.color, self.config.stroke)
            cv2.putText(frame, self.config.name.format(label), orig, 
                        self.config.font, self.config.fontscale, self.config.color)
        return frame