import os
from dotenv import load_dotenv

# ✅ Manually specify the path to ensure it's loaded
dotenv_path = os.path.join(os.path.dirname(__file__), "api.env")
load_dotenv(dotenv_path)

# Check if API Key loads
api_key = os.getenv("OPENAI_API_KEY")
print("API Key:", api_key)  # Debugging step

if not api_key:
    raise ValueError("API Key not found. Set OPENAI_API_KEY in api.env file.")
