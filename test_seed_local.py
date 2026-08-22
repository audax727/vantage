import requests

BASE = "http://127.0.0.1:5000"

s = requests.Session()
# Login
res = s.post(f"{BASE}/login", json={
    "email": "shrikarreddy19@gmail.com",
    "password": "nikenduk"
})
print("Login:", res.status_code, res.text[:200])

# Trigger seed
print("Triggering seed...")
res = s.post(f"{BASE}/api/seed-demo-data")
print("Status:", res.status_code)
print("Response:", res.text)
