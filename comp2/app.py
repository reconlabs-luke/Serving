from typing import Dict
from kserve import Model, ModelServer
import json
import boto3
import threading
import os


class MyModel(Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.name = name
        self.load()

    def load(self):
        self.ready = True
        self.sqs_client = boto3.client("sqs")
        self.q_url = self.sqs_client.get_queue_url(
            QueueName="test-q", QueueOwnerAWSAccountId="129231402580"
        )["QueueUrl"]
        self.increase_visibilty_time_timer = None
        self.receipt_handle = None

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        print("payload : ", payload, " ", type(payload))
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")
            print("decoded : ", payload, " ", type(payload))
        if isinstance(payload, str):
            payload = json.loads(payload)
            print("jsonify : ", payload, " ", type(payload))
        if isinstance(payload, dict) and "Body" in payload.keys():
            if "error" in payload:
                raise Exception("의도적인 에러")

            self.receipt_handle = payload["ReceiptHandle"]
            kwargs = {
                "QueueUrl": os.getenv(
                    "QUEUE_URL",
                    "https://sqs.ap-northeast-1.amazonaws.com/129231402580/test-q",
                ),
                "ReceiptHandle": self.receipt_handle,
                "VisibilityTimeout": 20,
            }
            self.increase_visibilty_time_timer = threading.Timer(
                interval=9,
                function=self.sqs_client.change_message_visibility,
                kwargs=kwargs,
            )
            self.increase_visibilty_time_timer.start()

            payload = payload["Body"]
            print("Consumd body : ", payload, " ", type(payload))

        try:
            if isinstance(payload, dict) and "number" in payload.keys():
                x = 10
                y = payload["number"]
                result = x + y
            else:
                result = payload

            import time

            time.sleep(14)
            print("end")
            self.sqs_client.delete_message(
                QueueUrl=self.q_url, ReceiptHandle=self.receipt_handle
            )
        except Exception as e:
            if self.increase_visibilty_time_timer:
                print("visibility timeout increasing stop start")
                self.increase_visibilty_time_timer.cancel()
                print("visibility timeout increasing stop success")
            raise e

        return {"result": result}


if __name__ == "__main__":
    model = MyModel("comp2")
    ModelServer(workers=1).start([model])
