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

    def _check(self, bb):
        p = (360 - bb[1]) / (bb[3] - bb[1])
        return p < self.thr

    def _make(self, frame, boat, bb):
        # box is [x,y,w,h]
        if (self.check(bb)):
            p1 = (int(bb[0]), int(bb[1]))
            p2 = (int(bb[0] + bb[2]), int(bb[1] + bb[3]))

            cv2.rectangle(frame, p1, p2, self.config.color, self.config.stroke)
            cv2.putText(frame, self.config.name.format(boat.id), p1, 
                        self.config.font, self.config.fontscale, self.config.color)