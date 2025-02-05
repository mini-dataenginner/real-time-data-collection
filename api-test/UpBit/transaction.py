import asyncio
import websockets
import json
import uuid

UPBIT_WS_URL = "wss://api.upbit.com/websocket/v1"

async def fetch_trades(market_codes):
    async with websockets.connect(UPBIT_WS_URL) as websocket:
        # WebSocket 요청 데이터 구성
        request_data = [
            {"ticket": str(uuid.uuid4())},  # Unique ticket ID
            {
                "type": "trade",  # 체결 데이터 요청
                "codes": market_codes,  # 마켓 코드 리스트 (대문자로 요청)
                "is_only_realtime": True  # 실시간 데이터만 받기
            },
            {"format": "DEFAULT"}  # 기본 포맷 사용
        ]
        
        # 요청 전송
        await websocket.send(json.dumps(request_data))
        
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(data)

async def main():
    market_codes = ["KRW-BTC"]  # 가져오고 싶은 마켓 코드 리스트
    await fetch_trades(market_codes)

if __name__ == "__main__":
    asyncio.run(main())
