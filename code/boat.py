import uuid

class Boat:
    """
    Object that represents a boat detected throughout the scene.

    :params: _id        unique id that a boat has, uuid.UUID
    :params: vectors    vectors in the coordinate space that represent approximate position
                        of the object with respect to the moving camera, []
    :params: coords     approximate coordinates of the object in the coordinate space [0..1] 
                        with respect to camera trajectory, tuple, (0,0) when not set
    """
    def __init__(self, id=None)->None:
        self._id = uuid.uuid4()
        if isinstance(id, uuid.UUID):
            self._id = id

        self.vectors = []
        self.coords = (0, 0)

    @property
    def id(self) -> uuid.UUID:
        """
        Function that returns object's id.

        returns: id         id of the object, uuid.UUID
        """
        return self._id


class Collection:
    """
    Object that represents a collection of objects of a particular class.
    Acts as a dictionary with predefined type of value.

    :params: _type      type the value should belong to, type
    :params: _content   dictionary itself
    """
    def __init__(self, t=Boat) -> None:
        self._type = t
        self._content = {}

    def add(self, boat:Boat | any, label:int)-> None:
        """
        Function that adds given object to the collection.

        :params: obj        object to add, Boat or another class object, same as collection's type
        :params: label      dictionary key, in this case deepsort detection label, int

        returns: None
        """
        assert isinstance(boat, self._type), "boat does not belong to the correct collection class {}".format(self._type)
        #if (len([x for x in self._content.values() if x!=boat])==0):
        #print("adding boat {}".format(boat.id))
        self._content[label] = boat

    def remove(self, label)-> None:
        """
        Function that removes a record from the collection by label

        :params: label      dictionary key, in this case deepsort detection label, int

        returns: None
        """
        if label in self._content:
            del self._content[label]
        
    def get_id(self, label)-> uuid.UUID | None:
        """
        Function that gets the id of the element by its label.
        :params: label      dictionary key, in this case deepsort detection label, int

        returns: id         id of the element with the given label or None if the label is not
                            in the collection, UUID
        """
        if label in self._content:
            return self._content[label].id 

    @property
    def length(self) -> int:
        """
        Function that counts the length of the collection.

        returns: length         number of elements in the collection, int
        """
        return len(self._content)

    @property
    def ids(self) -> list:
        """
        Function that returns objects' ids.

        returns: ids            ids of elements in the collection, list of UUID
        """
        return [boat.id for boat in self._content.values()]

    
    def contains(self, label) -> bool:
        """
        Function that checks whether an element with such label exists in 
        the collection.
        :params: label      dictionary key, in this case deepsort detection label, int

        returns: check      result, whether an object exists in the collection, bool
        """
        return label in self._content