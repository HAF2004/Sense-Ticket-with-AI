# update_env_gemini.py
import os

def update_env():
    print("🔧 Updating .env file with Gemini API Key...")
    
    gemini_key = "AIzaSyAVTcbc_ZY9nrHNcdXxOcNr6HT2vSV6NHo"
    
    content = ""
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        try:
            with open('.env', 'r', encoding='utf-16') as f:
                content = f.read()
        except:
            with open('.env', 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
    
    content = content.replace('\x00', '') # Clean null bytes
    lines = content.splitlines()
    new_lines = []
    
    key_added = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('GEMINI_API_KEY='):
            new_lines.append(f"GEMINI_API_KEY={gemini_key}")
            key_added = True
        elif line.startswith('OPENROUTER_API_KEY='):
            continue # Remove OpenRouter key
        elif line.startswith('DEEPSEEK_API_KEY='):
            continue # Remove DeepSeek key
        else:
            new_lines.append(line)
            
    if not key_added:
        new_lines.append(f"GEMINI_API_KEY={gemini_key}")
        
    with open('.env', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
    print("✅ .env file updated successfully!")

if __name__ == "__main__":
    update_env()
