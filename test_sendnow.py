import requests

s = requests.Session()
# Use the actual account
res = s.post("http://localhost:5000/login", json={
    "email": "audax727@gmail.com",
    "password": "password123"
})
print("Login:", res.status_code, res.text)
