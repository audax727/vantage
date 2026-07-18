import requests

s = requests.Session()
# Assuming we have a user from earlier, e.g. "admin@example.com" or we can sign up one
res = s.post("http://localhost:5000/signup", json={
    "email": "test_session@example.com",
    "password": "password123",
    "shop_name": "Test Shop"
})

res = s.post("http://localhost:5000/login", json={
    "email": "test_session@example.com",
    "password": "password123"
})
print("Login status:", res.status_code)
print("Login cookies:", s.cookies.get_dict())

res2 = s.get("http://localhost:5000/products")
print("Products page status:", res2.status_code)
print("Redirect history:", res2.history)
