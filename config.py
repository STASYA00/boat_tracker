from singleton_meta import SingletonMeta

class Config(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.category = 8 # boat COCO class