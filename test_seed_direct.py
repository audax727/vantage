import sys
from app import app, get_db, seed_demo_data
from flask import session

with app.test_request_context():
    # Mock a logged in user session
    # First, let's get the user ID for test@test.com
    db = get_db()
    user = db.execute("SELECT id FROM users WHERE email='test@test.com'").fetchone()
    if not user:
        print("User not found!")
        sys.exit(1)
    
    session["user_id"] = user["id"]
    
    try:
        res = seed_demo_data()
        print("Success:", res)
    except Exception as e:
        import traceback
        traceback.print_exc()
