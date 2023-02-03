import uuid

class Boat:
    def __init__(self, id=None):
        self._id = uuid.uuid4()
        if isinstance(id, uuid.UUID):
            self._id = id

        self.vectors = []
        self.coords = (0, 0)

    @property
    def id(self):
        return self._id