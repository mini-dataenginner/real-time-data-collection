import asyncio
import websockets
import json
import hmac
import hashlib
import base64
import time
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 새로 발급받은 인증 정보
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
PASSPHRASE    = ""
WS_URL        = "wss://ws-feed-public.sandbox.exchange.coinbase.com"  # 인증이 필요 없는 WebSocket

# **서명 생성 함수 (Node.js 방식과 동일)**
def generate_cb_signature(sign_path):
    timestamp = str(int(time.time()))
    message = f"{timestamp}GET{sign_path}"  # **Node.js 코드와 동일한 메시지 형식 사용**
    hmac_key = base64.b64decode(SECRET_KEY)  # **Base64 디코딩**
    signature = hmac.new(hmac_key, message.encode(), hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode()
    return signature_b64, timestamp

# **WebSocket 메시지 수신**
async def websocket_listener():
    sign_path = "/users/self/verify"
    signature, timestamp = generate_cb_signature(sign_path)

    subscribe_message = json.dumps({
        "type": "subscribe",
        "channels": [
            "level2",
            "heartbeat",
            {
                "name": "ticker",
                "product_ids": ["ETH-BTC"]
            }
        ],
        "signature": signature,
        "key": ACCESS_KEY,
        "passphrase": PASSPHRASE,
        "timestamp": timestamp
    })

    async with websockets.connect(WS_URL) as ws:
        print("✅ Connected to WebSocket")
        print(f"📤 Sending: {subscribe_message}")
        await ws.send(subscribe_message)

        while True:
            response = await ws.recv()
            print(f"📥 Received: {response}")

# **메인 실행**
if __name__ == "__main__":
    asyncio.run(websocket_listener())
