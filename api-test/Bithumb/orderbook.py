import asyncio
import websockets
import json

# 빗썸 WebSocket API 엔드포인트
BITTHUMB_WS_URL = "wss://ws-api.bithumb.com/websocket/v1"

# 호가 데이터 구독 함수
async def subscribe_orderbook(codes, level=1):
    async with websockets.connect(BITTHUMB_WS_URL) as websocket:
        # 구독 메시지 생성
        subscribe_message = [
            {"ticket": "test example"},  # 연결 식별용 티켓
            {
                "type": "orderbook",     # 데이터 타입: 호가
                "codes": codes,          # 마켓 코드 리스트
                "level": level,          # 호가 모아보기 단위 (기본값: 1)
                "isOnlyRealtime": True   # 실시간 데이터만 수신
            },
            {"format": "DEFAULT"}       # 데이터 포맷
        ]
        await websocket.send(json.dumps(subscribe_message))
        print(f"Subscribed to orderbook for codes: {codes} with level: {level}")

        # 데이터 수신 루프
        while True:
            try:
                # 서버로부터 메시지 수신
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Orderbook data: {json.dumps(data, indent=2)}")
            except Exception as e:
                print(f"Error receiving orderbook data: {e}")
                break

# 파일 독립 실행
if __name__ == "__main__":
    # 구독할 마켓 코드 리스트 설정 (대문자 필수)
    codes = ["KRW-BTC"]  # 비트코인
    level = 10                      # 호가 모아보기 단위 설정(10인 경우는, 10KRW가 1단위, level이 낮을수록 데이터가 많음)
    # 비동기 함수 실행
    asyncio.run(subscribe_orderbook(codes, level))
