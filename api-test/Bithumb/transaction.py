import asyncio
import websockets
import json

# 빗썸 WebSocket API 엔드포인트
BITTHUMB_WS_URL = "wss://ws-api.bithumb.com/websocket/v1"

# 체결 데이터 구독 함수
async def subscribe_trade(codes):
    async with websockets.connect(BITTHUMB_WS_URL) as websocket:
        # 구독 메시지 생성
        subscribe_message = [
            {"ticket": "test example"},  # 연결 식별용 티켓
            {
                "type": "trade",         # 데이터 타입: 체결
                "codes": codes,          # 마켓 코드 리스트
                "isOnlyRealtime": True   # 실시간 데이터만 수신
            },
            {"format": "DEFAULT"}       # 데이터 포맷
        ]
        await websocket.send(json.dumps(subscribe_message))
        print(f"Subscribed to trade for codes: {codes}")

        # 데이터 수신 루프
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Trade data: {json.dumps(data, indent=2)}")
            except Exception as e:
                print(f"Error receiving trade data: {e}")
                break

# 파일 독립 실행
if __name__ == "__main__":
    # 구독할 마켓 코드 리스트 설정 (대문자 필수)
    codes = ["KRW-BTC"]  # 비트코인
    asyncio.run(subscribe_trade(codes))
