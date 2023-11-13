from torchvision import models, transforms
from typing import Dict
from PIL import Image
from kserve import Model, ModelServer
import torch
import base64
import io
import json


class MyModel(Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.load()

    def load(self):
        self.ready = True

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        print("payload : ", payload, " ", type(payload))
        payload = payload.decode("utf-8")
        print("decoded : ", payload, " ", type(payload))
        payload = json.loads(payload)
        print("jsonify : ", payload, " ", type(payload))
        result = payload["data"]["number"]
        return {"prediction": result}


if __name__ == "__main__":
    model = MyModel("custom-model")
    ModelServer(workers=1).start([model])
