import requests

BASE = "http://127.0.0.1:5000"

s = requests.Session()
# Login
res = s.post(f"{BASE}/login", data={
    "email": "shrikarreddy19@gmail.com",
    "password": "nikenduk"
})
print("Login:", res.status_code)

# Get AI report first (needed for the payload)
print("Getting AI report...")
ai = s.get(f"{BASE}/api/analytics/ai_report?days=7")
print("AI Status:", ai.status_code)
if ai.status_code == 200:
    ai_data = ai.json()
else:
    print(ai.text)
    ai_data = {}

# Generate PDF
print("Generating PDF...")
res = s.post(f"{BASE}/api/analytics/report/generate?days=7", json=ai_data)
print("PDF Status:", res.status_code)
if res.status_code != 200:
    print(res.text)
