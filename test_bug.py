import requests

s = requests.Session()
# We need the CSRF token if there's any? No, Flask by default doesn't enforce CSRF unless CSRFProtect is used.
s.post("http://127.0.0.1:5000/login", data={"email": "test@test.com", "password": "password123"})
    
r_seed = s.post("http://127.0.0.1:5000/api/seed-demo-data")
print("Seed status:", r_seed.status_code)
print("Seed text:", r_seed.text[:500])
    
r_gen = s.post("http://127.0.0.1:5000/api/analytics/report/generate?days=7")
print("Generate status:", r_gen.status_code)
print("Generate text:", r_gen.text[:500])
