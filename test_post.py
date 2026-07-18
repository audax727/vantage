import requests
try:
    r = requests.post("http://127.0.0.1:5000/signup", json={"email": "test@test.com", "password": "password123", "shop_name": "Test Shop"})
    print(r.status_code, r.text)
except Exception as e:
    print(e)
