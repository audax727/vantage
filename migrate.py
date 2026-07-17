import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres.kipuyfpcabhiwkszncxv:Vantage_123_12@aws-1-ap-northeast-2.pooler.supabase.com:6543/postgres?pgbouncer=true")

db_url = DATABASE_URL.replace("?pgbouncer=true", "").replace("&pgbouncer=true", "")
if "?" not in db_url:
    db_url += "?sslmode=require"
elif "sslmode" not in db_url:
    db_url += "&sslmode=require"

try:
    conn = psycopg2.connect(db_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    # Add gst_rate to products
    try:
        cur.execute("ALTER TABLE products ADD COLUMN gst_rate NUMERIC NOT NULL DEFAULT 18")
        print("Added gst_rate to products")
    except Exception as e:
        print("Skipped products:", e)
        
    # Add gstin to users
    try:
        cur.execute("ALTER TABLE users ADD COLUMN gstin TEXT")
        print("Added gstin to users")
    except Exception as e:
        print("Skipped users:", e)
        
    # Add cgst_amount and sgst_amount to quotations
    try:
        cur.execute("ALTER TABLE quotations ADD COLUMN cgst_amount NUMERIC NOT NULL DEFAULT 0")
        cur.execute("ALTER TABLE quotations ADD COLUMN sgst_amount NUMERIC NOT NULL DEFAULT 0")
        print("Added tax columns to quotations")
    except Exception as e:
        print("Skipped quotations:", e)
        
    # Add cgst_amount and sgst_amount to sales
    try:
        cur.execute("ALTER TABLE sales ADD COLUMN cgst_amount NUMERIC NOT NULL DEFAULT 0")
        cur.execute("ALTER TABLE sales ADD COLUMN sgst_amount NUMERIC NOT NULL DEFAULT 0")
        print("Added tax columns to sales")
    except Exception as e:
        print("Skipped sales:", e)
        
    conn.close()
    print("Migration complete!")
except Exception as e:
    print("Connection error:", e)
