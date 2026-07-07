import re

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('import sqlite3', 'import psycopg2\nimport psycopg2.extras')
code = code.replace('DB_PATH = os.environ.get("DB_PATH", "vantage.db")', 'DATABASE_URL = os.environ.get("DATABASE_URL")')

get_db_old = '''def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db'''

get_db_new = '''class DBWrapper:
    def __init__(self, conn):
        self.conn = conn
        
    def execute(self, query, params=None):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        q = query.replace('?', '%s')
        if params is None:
            cur.execute(q)
        else:
            cur.execute(q, params)
        return cur
        
    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.close()

def get_db():
    if "db" not in g:
        conn = psycopg2.connect(DATABASE_URL)
        g.db = DBWrapper(conn)
    return g.db'''
code = code.replace(get_db_old, get_db_new)

# Fix RETURNING id for all INSERT statements that use cur.lastrowid
# There are several inserts in app.py

# 1. Signup
code = code.replace(
    'VALUES (?,?,?,?,?)",\n        (email, pw_hash, "email", shop_name, datetime.utcnow().isoformat()),\n    )\n    user_id = cur.lastrowid',
    'VALUES (?,?,?,?,?) RETURNING id",\n        (email, pw_hash, "email", shop_name, datetime.utcnow().isoformat()),\n    )\n    user_id = cur.fetchone()["id"]'
)

# 2. Google callback
code = code.replace(
    'VALUES (?,?,?,?,?)",\n            (email, None, "google", userinfo.get("name", "My Shop"), datetime.utcnow().isoformat()),\n        )\n        user_id = cur.lastrowid',
    'VALUES (?,?,?,?,?) RETURNING id",\n            (email, None, "google", userinfo.get("name", "My Shop"), datetime.utcnow().isoformat()),\n        )\n        user_id = cur.fetchone()["id"]'
)

# 3. Product create
code = code.replace(
    'datetime.utcnow().isoformat()),\n        )\n        db.commit()\n        return jsonify({"ok": True, "id": cur.lastrowid})',
    'datetime.utcnow().isoformat()),\n        )\n        pid = cur.fetchone()["id"]\n        db.commit()\n        return jsonify({"ok": True, "id": pid})'
)

# 4. Customer create
code = code.replace(
    'datetime.utcnow().isoformat()),\n        )\n        db.commit()\n        return jsonify({"ok": True, "id": cur.lastrowid})',
    'datetime.utcnow().isoformat()),\n        )\n        cid = cur.fetchone()["id"]\n        db.commit()\n        return jsonify({"ok": True, "id": cid})'
)

# 5. Record sale
code = code.replace(
    'VALUES (?,?,?,?,?,?,?,?)",\n        (user_id, customer_id, channel, total_amount, amount_paid, payment_status, "completed", now),\n    )\n    sale_id = cur.lastrowid',
    'VALUES (?,?,?,?,?,?,?,?) RETURNING id",\n        (user_id, customer_id, channel, total_amount, amount_paid, payment_status, "completed", now),\n    )\n    sale_id = cur.fetchone()["id"]'
)

# Fix schema
schema_old = '''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT,          -- NULL if account was created via Google
    auth_provider TEXT NOT NULL DEFAULT 'email',   -- 'email' or 'google'
    shop_name TEXT NOT NULL DEFAULT 'My Shop',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    is_default INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    location_id INTEGER REFERENCES locations(id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    category TEXT,
    cost_price REAL NOT NULL DEFAULT 0,
    sell_price REAL NOT NULL DEFAULT 0,
    current_stock REAL NOT NULL DEFAULT 0,
    reorder_threshold REAL NOT NULL DEFAULT 5,
    unit TEXT NOT NULL DEFAULT 'pcs',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    customer_id INTEGER REFERENCES customers(id) ON DELETE SET NULL,
    channel TEXT NOT NULL DEFAULT 'in_store',   -- 'in_store' or 'online'
    total_amount REAL NOT NULL,
    amount_paid REAL NOT NULL,
    payment_status TEXT NOT NULL,   -- paid / partial / credit
    status TEXT NOT NULL DEFAULT 'completed',  -- completed / abandoned
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL REFERENCES sales(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    qty REAL NOT NULL,
    price_at_sale REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS ledger_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    sale_id INTEGER REFERENCES sales(id) ON DELETE SET NULL,
    amount_due REAL NOT NULL,
    amount_paid REAL NOT NULL DEFAULT 0,
    date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open'   -- open / settled
);

CREATE TABLE IF NOT EXISTS stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    change_qty REAL NOT NULL,
    reason TEXT NOT NULL,   -- sale / restock / adjustment
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    kind TEXT NOT NULL,     -- payment_reminder / cart_nudge / low_stock
    message TEXT NOT NULL,
    channel TEXT NOT NULL,  -- email / mock
    sent_at TEXT NOT NULL
);'''

schema_new = schema_old.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY').replace('REAL', 'NUMERIC')
code = code.replace(schema_old, schema_new)

init_db_old = '''def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA)
    db.commit()
    db.close()'''
    
init_db_new = '''def init_db():
    if not DATABASE_URL: return
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(SCHEMA)
    conn.commit()
    conn.close()'''
code = code.replace(init_db_old, init_db_new)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("done")
