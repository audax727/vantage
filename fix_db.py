import os
import psycopg2
from psycopg2.extras import DictCursor
import json

conn = psycopg2.connect("postgresql://postgres.kipuyfpcabhiwkszncxv:Vantage_123_12@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres", cursor_factory=DictCursor)
conn.autocommit = True
cur = conn.cursor()

with open("seed_data.json", "r") as f:
    data = json.load(f)
    
for p in data["products"]:
    name = p["name"]
    gst_rate = p.get("gst_rate", 18.0)
    cur.execute("UPDATE products SET gst_rate = %s WHERE name = %s", (gst_rate, name))

print("Updated GST rates for existing products.")
