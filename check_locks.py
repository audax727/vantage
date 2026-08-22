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
SELECT pid, usename, state, query, wait_event_type, wait_event, xact_start, query_start
FROM pg_stat_activity
WHERE state = 'active' OR state = 'idle in transaction';
""")
rows = cur.fetchall()
for r in rows:
    print(r)
conn.close()
