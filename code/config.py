from singleton_meta import SingletonMeta

class Config(metaclass=SingletonMeta):
    """
    Object that contains the parameters for the detection algorithm
    :params: category       category of the objects to detect, int
    :params: confidence     min confidence to accept, float
    """
    def __init__(self) -> None:
        self.category = 8 # boat COCO class
        self.confidence = 0.15


class DeepSortConfig(metaclass=SingletonMeta):
    """
    Object that contains the parameters for the deepsort algorithm.
    :params: model          model type to use for deepsort, str
    """
    def __init__(self) -> None:
        self.model = "osnet_x0_25"