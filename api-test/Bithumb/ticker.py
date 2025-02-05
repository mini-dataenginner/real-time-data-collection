import asyncio
import websockets
import json

# 빗썸 WebSocket API 엔드포인트
BITTHUMB_WS_URL = "wss://ws-api.bithumb.com/websocket/v1"

# 현재가 구독 함수
async def subscribe_ticker(codes):
    async with websockets.connect(BITTHUMB_WS_URL) as websocket:
        # 구독 메시지 생성
        subscribe_message = [
            {"ticket": "test example"},  # 연결 식별자
            {
                "type": "ticker",        # 데이터 타입: 현재가
                "codes": codes,          # 마켓 코드 리스트
                "isOnlyRealtime": True   # 실시간 데이터만 수신
            },
            {"format": "DEFAULT"}       # 데이터 포맷
        ]
        await websocket.send(json.dumps(subscribe_message))
        print(f"Subscribed to ticker for codes: {codes}")

        # 데이터 수신 루프
        while True:
            try:
                # 서버로부터 메시지 수신
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Ticker data: {json.dumps(data, indent=2)}")
            except Exception as e:
                print(f"Error receiving ticker data: {e}")
                break

# 파일 독립 실행
if __name__ == "__main__":
    # 구독할 마켓 코드 리스트 설정 (대문자 필수)
    codes = ["KRW-BTC"]  # 비트코인
    asyncio.run(subscribe_ticker(codes))
