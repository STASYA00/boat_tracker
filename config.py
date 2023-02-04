from singleton_meta import SingletonMeta

class Config(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.category = 8 # boat COCO class
        self.confidence = 0.15


class DeepSortConfig(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.model = "osnet_x0_25"