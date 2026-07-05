import sqlite3
db = sqlite3.connect("vantage.db")
print(db.execute("SELECT sql FROM sqlite_master WHERE name='locations'").fetchone()[0])
