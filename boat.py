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


class Collection:
    def __init__(self, t=Boat) -> None:
        self._type = t
        self._content = {}

    def add(self, boat:Boat, label:int):
        assert isinstance(boat, self._type), "boat does not belong to the correct collection class {}".format(self._type)
        #if (len([x for x in self._content.values() if x!=boat])==0):
        #print("adding boat {}".format(boat.id))
        self._content[label] = boat

    def remove(self, label):
        del self._content[label]
        
    def get_id(self, label):
        return self._content[label].id 

    @property
    def length(self):
        return len(self._content)

    @property
    def ids(self):
        return [boat.id for boat in self._content.values()]

    
    def contains(self, label):
        return label in self._content