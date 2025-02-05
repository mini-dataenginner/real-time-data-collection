import asyncio
import websockets
import json
import uuid

UPBIT_WS_URL = "wss://api.upbit.com/websocket/v1"

async def fetch_orderbook(market_codes, level=0):
    async with websockets.connect(UPBIT_WS_URL) as websocket:
        # WebSocket 요청 데이터 구성
        request_data = [
            {"ticket": str(uuid.uuid4())},  # Unique ticket ID
            {
                "type": "orderbook",  # 호가 정보 요청
                "codes": market_codes,  # 마켓 코드 리스트 (대문자로 요청)
                "level": level,  # 호가 모아보기 단위 (기본값: 0)
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
    await fetch_orderbook(market_codes, level=0)  # level=0: 기본 호가

if __name__ == "__main__":
    asyncio.run(main())
