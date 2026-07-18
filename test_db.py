import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url = os.environ.get("DATABASE_URL")
print("URL:", db_url)
try:
    conn = psycopg2.connect(db_url)
    print("SUCCESS")
    conn.close()
except Exception as e:
    print("ERROR:", e)
