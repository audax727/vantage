import os
from dotenv import load_dotenv
load_dotenv()
print("KEY:", os.environ.get("GROQ_API_KEY"))
try:
    from groq import Groq
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "hi"}]
    )
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
