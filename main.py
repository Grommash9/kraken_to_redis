import os
import ssl
import sys

import orjson
import redis
import websocket
from websocket import WebSocketApp

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
redis_client = redis.Redis(REDIS_HOST, REDIS_PORT, password=REDIS_PASSWORD)


def on_message(ws: WebSocketApp, message: str) -> None:
    json_message = orjson.loads(message)
    if not isinstance(json_message, list):
        return

    if len(json_message) < 2:
        return
    order_book_data = json_message[1]

    for ask in order_book_data.get("a", []):
        redis_client.hset("KRAKEN_BTCUSD_ask", ask[0], ask[1])

    for bids in order_book_data.get("b", []):
        redis_client.hset("KRAKEN_BTCUSD_bid", bids[0], bids[1])


def ws_open(ws):
    ws.send(
        '{"event":"subscribe", "subscription":{"name":"book", "depth":100}, "pair":["BTC/USDT"]}'
    )


def on_error(ws: WebSocketApp, message: str) -> None:
    sys.exit(message)


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "wss://ws.kraken.com/",
        on_error=on_error,
        on_open=ws_open,
        on_message=on_message,
    )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
