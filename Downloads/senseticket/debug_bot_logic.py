# debug_bot_logic.py
import asyncio
import sys
import os

# Add root to sys.path
sys.path.append(os.getcwd())

async def test_logic():
    print("🔍 Testing Bot Logic...")
    
    try:
        print("1. Importing modules...")
        import analysis
        from handlers.gemini_handler import generate_response
        print("✅ Imports successful")
        
        query = "buatkan pantun tentang programmer yang lupa makan siang"
        print(f"2. Testing Context Search for: '{query}'")
        
        try:
            results = analysis.find_smart_context(query, limit=5, threshold=0.1)
            print(f"✅ Context found: {len(results)} items")
        except Exception as e:
            print(f"❌ Context search failed: {e}")
            results = []
            
        print("3. Calling Gemini Handler...")
        try:
            response = await generate_response(query, results)
            if response:
                print("✅ Handler returned response:")
                print(response)
            else:
                print("❌ Handler returned None")
        except Exception as e:
            print(f"❌ Handler raised exception: {e}")
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_logic())
