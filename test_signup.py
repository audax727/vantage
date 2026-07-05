import json
from app import app
from flask import Flask

# Need to init db in test context
with app.app_context():
    app.config["TESTING"] = True
    client = app.test_client()

    # Try signing up
    res = client.post("/signup", json={
        "shop_name": "Test Shop",
        "email": "testsignup@example.com",
        "password": "password123"
    })
    
    print(res.status_code)
    print(res.data.decode('utf-8'))
