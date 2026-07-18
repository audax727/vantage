import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)
db_url = os.environ.get("DATABASE_URL").replace("?pgbouncer=true", "").replace("&pgbouncer=true", "")
if "?" not in db_url:
    db_url += "?sslmode=require"
elif "sslmode" not in db_url:
    db_url += "&sslmode=require"

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    print("USERS:", rows)
    conn.close()
except Exception as e:
    print(e)
