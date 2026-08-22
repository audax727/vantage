import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)
db_url = os.environ.get("DATABASE_URL")

if not db_url:
    print("DATABASE_URL not found in .env")
else:
    print(f"Testing connection to: {db_url[:30]}...")
    try:
        # Clean up URL for psycopg2
        clean_url = db_url.replace("?pgbouncer=true", "").replace("&pgbouncer=true", "")
        if "?" not in clean_url:
            clean_url += "?sslmode=require"
        elif "sslmode" not in clean_url:
            clean_url += "&sslmode=require"
            
        conn = psycopg2.connect(clean_url, connect_timeout=10)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        print("SUCCESS! Database is alive and responding.")
        conn.close()
    except Exception as e:
        print(f"FAILED to connect to database: {e}")
