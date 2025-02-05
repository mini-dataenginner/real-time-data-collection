import asyncio
import json
import websockets

async def listen_ticker():
    # Coinbase Market Data의 WebSocket URI
    uri = "wss://ws-feed.exchange.coinbase.com"

    async with websockets.connect(uri) as websocket:
        # 구독 메시지: ticker 채널에서 ETH-USD의 데이터를 요청
        subscribe_message = json.dumps({
            "type": "subscribe",
            "channels": [
                {
                    "name": "ticker",
                    "product_ids": ["ETH-USD"]
                }
            ]
        })
        
        await websocket.send(subscribe_message)
        print("Subscribed to ticker channel for ETH-USD.")

        # 무한 루프로 수신되는 메시지를 처리
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(data)

if __name__ == '__main__':
    try:
        asyncio.run(listen_ticker())
    except KeyboardInterrupt:
        print("종료합니다.")
