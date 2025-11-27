# list_google_models.py
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def list_models():
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("No API Key found")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'models' in data:
                        print("Available Models:")
                        for m in data['models']:
                            if 'generateContent' in m.get('supportedGenerationMethods', []):
                                print(f"- {m['name']}")
                    else:
                        print(data)
                else:
                    print(f"Error: {response.status}")
                    text = await response.text()
                    print(text)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(list_models())
