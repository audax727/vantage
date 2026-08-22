import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.environ.get("GROQ_API_KEY")
headers = {"Authorization": f"Bearer {api_key}"}
r = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
print(r.json())
