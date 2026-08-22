import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)
db_url = os.environ.get("DATABASE_URL")
clean_url = db_url.replace("?pgbouncer=true", "").replace("&pgbouncer=true", "")
if "?" not in clean_url: clean_url += "?sslmode=require"
elif "sslmode" not in clean_url: clean_url += "&sslmode=require"
    
conn = psycopg2.connect(clean_url)
cur = conn.cursor()
cur.execute("""
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle in transaction';
""")
conn.commit()
conn.close()
print("Killed idle transactions")
