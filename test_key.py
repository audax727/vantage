import os
from dotenv import load_dotenv

load_dotenv(override=True)
print("FLASK_SECRET_KEY is:", os.environ.get("FLASK_SECRET_KEY"))
