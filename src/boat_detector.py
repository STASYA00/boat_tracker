import numpy as np
import torch
from enum import Enum

from config import Config
from singleton_meta import SingletonMeta

class MODELS(Enum):
    """
    Enumerator of different models.
    """
    YOLO3= 0
    YOLO5= 1
    YOLOV5L6= 2
    YOLOV5N= 3
    YOLO7= 4

class ModelStd:
    """
    Placeholder for values to download a model in a standardized way.

    :params: name       name of the model in the hub, str
    :params: repo       name of the repo to download the model from, str
    """
    def __init__(self, name:str, repo:str)-> None:
        self._name = name
        self._repo = repo
    
    def get_value(self) -> tuple:
        """
        Function that returns the values of the model, tuple (name:str, repo:str)
        """
        return (self._name, self._repo)


class ModelFactory(metaclass=SingletonMeta):
    """
    Object that holds the mapping for the models based on their type.

    :params: content        dict containing model mapping: model enum - model placeholder with the values (MODEL: ModelStd())
    """
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
        """
        Function that returns the mapping
        """
        return self._content

class Bbox:
    """
    Standardization of bbox.
    """
    def yolo2standard(xyxy) -> list:
        """
        Function that brings yolo bbox xyxy annotation to standard format [left, top, w, h]
        """
        w = xyxy[2] - xyxy[0]
        h = xyxy[3] - xyxy[1]
        return [xyxy[0], xyxy[1], w, h]



class BoatDetector:
    """
    Object that is responsible for detection process.
    :params: model_name         model to use for detection, one of MODELS, default MODELS.YOLO5
    :params: config             config with the parameters to use, Config
    :params: model              model to perform the detection with

    """
    def __init__(self, model:MODELS=MODELS.YOLO5) -> None:
        assert isinstance(model, MODELS), "This model is not supported"
        
        self.model_name = model
        self._config = Config()
        self._model = self._load_model()

    def run(self, frame) -> torch.Tensor:
        """
        Function that performs detection on a given frame.
        :params: frame      frame to detect the objects within, np.ndarray (h, w, 3)
        returns: bbs        bboxes of detected boats in a standard fmt [left, top, w, h]
        """
        return self._run(frame)

    def _load_model(self)-> None:
        """
        Function that loads a model based on a chosen model type.

        returns: model      loaded model from torch hub
        """
        m = ModelFactory().content[self.model_name].get_value()
        return torch.hub.load(m[1], m[0]) 

    def _run(self, frame) -> torch.Tensor:
        """
        Function that performs detection on a given frame.
        :params: frame      frame to detect the objects within, np.ndarray (h, w, 3)
        returns: bbs        bboxes of detected boats in a standard fmt [left, top, w, h]
        """
        preds = self._model(frame)
        return self._standardize_preds(preds)

    def _standardize_preds(self, res) -> torch.Tensor:
        """
        Brings the predictions to a standard format [left, top, w, h] - changed; 
        now centerx, centery, w, h, conf, cls : deepsort takes it that way.
        Predictions are filtered based on the desired detection category and confidence.
        :params: res        prediction result, Detection
        returns: res        transformed and filtered detections, torch.Tensor
        """
        res = res.xywh[0]
        res = res[res[:, -1]==self._config.category]
        res = res[res[:, -2]>=self._config.confidence]
        return res

    
    