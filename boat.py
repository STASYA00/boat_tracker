class Boat:
    def __init__(self, id):
        self._id = id
        self.vectors = []
        self.coords = (0, 0)

    @property
    def id(self):
        return self._id