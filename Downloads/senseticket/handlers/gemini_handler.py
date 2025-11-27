# handlers/gemini_handler.py
# Handler for Google Gemini API interactions

import aiohttp
import json
from core.config import GEMINI_API_KEY, GEMINI_MODEL, AI_SYSTEM_PROMPT

async def generate_response(user_query: str, context_messages: list = None) -> str:
    """
    Generate a response using Google Gemini API
    
    Args:
        user_query: The user's message
        context_messages: List of previous messages for context (optional)
        
    Returns:
        str: The AI's response
    """
    if not GEMINI_API_KEY:
        print("[ERROR] Gemini API Key is missing!")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    
    # Prepare the prompt with system instructions and context
    full_prompt = AI_SYSTEM_PROMPT + "\n\n"
    
    # Add context if available
    if context_messages:
        context_str = "\n".join([f"- {msg['content']}" for msg in context_messages])
        full_prompt += f"Konteks percakapan sebelumnya:\n{context_str}\n\n"
    
    # Add user query
    full_prompt += f"User: {user_query}\n\nRespond naturally as Sense:"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": full_prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 150,
            "topP": 0.9,
            "topK": 40
        }
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    # Extract text from Gemini response
                    if 'candidates' in data and len(data['candidates']) > 0:
                        candidate = data['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content']:
                            text = candidate['content']['parts'][0]['text']
                            return text.strip()
                    print(f"[DEBUG] Full API Response: {json.dumps(data)}")
                    return None
                else:
                    error_text = await response.text()
                    print(f"[ERROR] Gemini API Error {response.status}: {error_text}")
                    return None
                    
    except Exception as e:
        print(f"[ERROR] Error calling Gemini API: {e}")
        return None

async def analyze_ticket(content: str) -> dict:
    """
    Analyze ticket content using Gemini API
    Returns JSON with summary, sentiment, urgency, category
    """
    if not GEMINI_API_KEY:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    
    system_prompt = """Analisis pesan tiket berikut dan berikan respons dalam format JSON.
    
    Format JSON yang harus dikembalikan:
    {
        "summary": "Ringkasan 1 kalimat tentang masalah (dalam Bahasa Indonesia)",
        "sentiment": "Status emosional user (Frustrated/Confused/Polite/Angry)",
        "urgency": "Tingkat urgensi (Low/Medium/High)",
        "category": "Kategori masalah (Technical/Account/Report/General)"
    }
    
    Hanya kembalikan JSON murni, tanpa markdown atau formatting lain."""
    
    full_prompt = f"{system_prompt}\n\nPesan tiket:\n{content}\n\nJSON:"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": full_prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.3,  # Low temperature for consistent analysis
            "maxOutputTokens": 200
        }
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'candidates' in data and len(data['candidates']) > 0:
                        candidate = data['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content']:
                            raw_content = candidate['content']['parts'][0]['text'].strip()
                            # Clean up if markdown is present
                            if raw_content.startswith('```json'):
                                raw_content = raw_content.replace('```json', '').replace('```', '').strip()
                            return json.loads(raw_content)
                    return None
                else:
                    print(f"[ERROR] Gemini Analysis Error {response.status}")
                    return None
    except Exception as e:
        print(f"[ERROR] Error analyzing ticket: {e}")
        return None
