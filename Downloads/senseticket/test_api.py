# test_api.py
import asyncio
import os
from dotenv import load_dotenv
from handlers.gemini_handler import generate_response

# Load environment variables
load_dotenv()

async def test_connection():
    print("[INFO] Testing Google Gemini API connection...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in .env file")
        return

    print(f"[INFO] API Key found: {api_key[:10]}...")
    
    query = "Jelaskan secara singkat apa itu Discord dalam 1 kalimat."
    print(f"\n[INFO] Sending query: '{query}'")
    
    try:
        response = await generate_response(query)
        
        if response:
            print("\n[SUCCESS] API Connection SUCCESS!")
            print(f"Response:\n{response}")
        else:
            print("\n[FAILURE] API Connection FAILED.")
            print("Response was empty. Check your API key or quota.")
            
    except Exception as e:
        print(f"\n[ERROR] Exception occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
