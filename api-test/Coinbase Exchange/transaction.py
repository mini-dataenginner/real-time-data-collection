import asyncio
import websockets
import json

WS_URL = "wss://ws-feed.exchange.coinbase.com"

async def websocket_listener():
    subscribe_message = json.dumps({
        "type": "subscribe",
        "channels": [
            {"name": "level2", "product_ids": ["BTC-USD"]},
            {"name": "matches", "product_ids": ["BTC-USD"]}
        ]
    })

    async with websockets.connect(WS_URL) as ws:
        print("✅ Connected to WebSocket")
        print(f"📤 Sending: {subscribe_message}")
        await ws.send(subscribe_message)

        while True:
            response = await ws.recv()
            print(f"📥 Received: {response}")

if __name__ == "__main__":
    asyncio.run(websocket_listener())
