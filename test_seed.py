import requests

BASE = "https://vantage-hbmr.onrender.com"

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
