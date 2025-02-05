# transaction.py
import asyncio
import json
import websockets

BINANCE_WS_URL = "wss://stream.binance.com:9443/ws"

async def transaction(symbol: str):
    stream_name = f"{symbol.lower()}@aggTrade"
    url = f"{BINANCE_WS_URL}/{stream_name}"

    async with websockets.connect(url) as ws:
        while True:
            try:
                response = await ws.recv()
                data = json.loads(response)

                print(data)
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed. Reconnecting...")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    symbol = "BTCUSDT"  # 원하는 심볼로 변경 가능
    asyncio.run(transaction(symbol))
