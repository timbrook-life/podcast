import json
import os
import pika
from functools import wraps
from flask import request
from jose import jwt
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()

with open("/var/run/secrets/rsa.jwk.pub") as json_file:
    key = json.load(json_file)


def require_valid_token():
    def _decorator(func):
        @wraps(func)
        def _inner(*args, **kwargs):
            token = request.cookies.get("token")
            jwt.decode(token, key)
            return func(*args, **kwargs)

        return _inner

    return _decorator


class AsyncProccessor:

    SYMBOL_MAP = {"calulate_duration": "async.DurationPayload"}

    def __init__(self, key: str) -> None:
        self.routing_key = f"async.{key}"
        self.sym = self.SYMBOL_MAP[key]
        self.serialize = _sym_db.GetSymbol(self.sym).SerializeToString

    def dispatch(self, data: object, token: str) -> None:
        credentials = pika.PlainCredentials("user", os.environ.get("AMQT_PASSWORD"))
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="rabbitmq.production.svc.cluster.local", credentials=credentials
            )
        )
        channel = connection.channel()
        body = self.serialize(data).decode("utf-8")
        channel.basic_publish(
            exchange="amq.topic",
            routing_key=self.routing_key,
            body=body,
            properties=pika.BasicProperties(
                headers={"X-Proto-Symbol": self.sym, "X-Auth-Token": token}
            ),
        )

