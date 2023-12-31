from typing import Dict
from kserve import Model, ModelServer
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
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")
            print("decoded : ", payload, " ", type(payload))
        if isinstance(payload, str):
            payload = json.loads(payload)
            print("jsonify : ", payload, " ", type(payload))
        result = payload["data"]["number"]
        return {"number": result}


if __name__ == "__main__":
    model = MyModel("comp1")
    ModelServer(workers=1).start([model])
