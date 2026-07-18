import os
import psycopg2
from psycopg2.extras import DictCursor

conn = psycopg2.connect("postgresql://postgres.kipuyfpcabhiwkszncxv:Vantage_123_12@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres", cursor_factory=DictCursor)
cur = conn.cursor()
cur.execute("SELECT name, gst_rate FROM products LIMIT 10")
rows = cur.fetchall()
for r in rows:
    print(r)
