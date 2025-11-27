# list_models.py
import aiohttp
import asyncio
import json

async def list_models():
    url = "https://openrouter.ai/api/v1/models"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get('data', [])
                    
                    print(f"Found {len(models)} models.")
                    
                    # Filter for Gemini models
                    gemini_models = [m['id'] for m in models if 'gemini' in m['id'].lower()]
                    
                    print("\n--- Gemini Models ---")
                    for m in gemini_models:
                        print(m)
                        
                    # Filter for Llama models
                    llama_models = [m['id'] for m in models if 'llama-3' in m['id'].lower() and 'free' in m['id'].lower()]
                    print("\n--- Free Llama Models ---")
                    for m in llama_models:
                        print(m)
                        
                else:
                    print(f"Error: {response.status}")
                    text = await response.text()
                    print(text)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(list_models())
