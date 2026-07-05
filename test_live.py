import threading
import time
import requests
from app import app

def run_server():
    app.run(port=5001, use_reloader=False)

threading.Thread(target=run_server, daemon=True).start()
time.sleep(2)

try:
    res = requests.post("http://127.0.0.1:5001/signup", json={
        "shop_name": "My Shop",
        "email": "live_test@example.com",
        "password": "password123"
    })
    print(res.status_code)
    print(res.text)
except Exception as e:
    print("Error:", e)
