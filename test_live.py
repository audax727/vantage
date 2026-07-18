import requests

# Test against LIVE Render server
BASE = "https://vantage-hbmr.onrender.com"

s = requests.Session()

# Login
res = s.post(f"{BASE}/login", json={
    "email": "shrikarreddy19@gmail.com",
    "password": "nikenduk"
})
print("Login:", res.status_code, res.text[:200])

# Get ledger
res = s.get(f"{BASE}/api/ledger")
print("Ledger:", res.status_code)
ledger = res.json()
print("Ledger entries:", len(ledger))

if ledger:
    customer_id = ledger[0]["customer_id"]
    print(f"\nTesting send-now for customer_id={customer_id}...")
    res = s.post(
        f"{BASE}/api/ledger/reminders/{customer_id}/send-now",
        json={"override_email": "shrikareddy578@gmail.com"}
    )
    print("Status:", res.status_code)
    print("Response:", res.text)
else:
    print("No ledger entries found")
