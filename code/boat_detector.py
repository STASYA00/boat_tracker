import numpy as np
import torch
from enum import Enum

from config import Config
from singleton_meta import SingletonMeta

class MODELS(Enum):
    YOLO3= 0
    YOLO5= 1
    YOLOV5L6= 2
    YOLOV5N= 3
    YOLO7= 4

class ModelStd:
    def __init__(self, name:str, repo:str)-> None:
        self._name = name
        self._repo = repo
    
    def get_value(self) -> tuple:
        return (self._name, self._repo)


class ModelFactory(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._content = {
            MODELS.YOLO3:       ModelStd("yolov3", 'ultralytics/yolov3'),
            MODELS.YOLO5:       ModelStd("yolov5l", 'ultralytics/yolov5'),
            MODELS.YOLOV5L6:    ModelStd("yolov5l6", 'ultralytics/yolov5'),
            MODELS.YOLOV5N:     ModelStd("yolov5n", 'ultralytics/yolov5'),
            MODELS.YOLO7:       ModelStd("yolov7", ''),
        }

    @property
    def content(self) -> dict:
        return self._content

class Bbox:
    """
    Standardization of bbox.
    """
    def yolo2standard(xyxy) -> list:
        w = xyxy[2] - xyxy[0]
        h = xyxy[3] - xyxy[1]
        return [xyxy[0], xyxy[1], w, h]

    # def yolo2standardTensor(xyxy):
    #     if (isinstance(xyxy, torch.Tensor)):
    #         xywh = xyxy.clone()
    #     else:
    #         xywh = np.copy(xyxy)
            
    #     xywh[..., 0] = (xyxy[..., 0] + xyxy[..., 2]) / 2  # x center
    #     xywh[..., 1] = (xyxy[..., 1] + xyxy[..., 3]) / 2  # y center
    #     xywh[..., 2] = xyxy[..., 2] - xyxy[..., 0]  # width
    #     xywh[..., 3] = xyxy[..., 3] - xyxy[..., 1]  # height
    #     return xywh



class BoatDetector:
    def __init__(self, model:MODELS=MODELS.YOLO5) -> None:
        assert isinstance(model, MODELS), "This model is not supported"
        self.name = "generic class"
        self.model_name = model
        self.config = Config()
        self.model = self._load_model()

    def run(self, frame) -> torch.Tensor:
        """
        returns: bbs        bboxes of detected boats in a standard fmt [left, top, w, h]
        """
        return self._run(frame)

    def _load_model(self)-> None:
        m = ModelFactory().content[self.model_name].get_value()
        return torch.hub.load(m[1], m[0]) 

    def _run(self, frame) -> torch.Tensor:
        preds = self.model(frame)
        return self._standardize_preds(preds)

    def _standardize_preds(self, res) -> torch.Tensor:
        """
        Brings the predictions to a standard format [left, top, w, h] - changed; 
        now centerx, centery, w, h, conf, cls : deepsort takes it that way
        """
        res = res.xywh[0]
        res = res[res[:, -1]==self.config.category]
        res = res[res[:, -2]>=self.config.confidence]
        return res
        #return [Bbox.yolo2standard(a) for a in res.xyxy[0].tolist() if (a[-1]==self.config.category and 
                                                                        # a[-2]>=self.config.confidence)]

    
    