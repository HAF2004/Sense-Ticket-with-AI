# fix_env.py
import os

def fix_env():
    print("🔧 Fixing .env file...")
    
    content = ""
    try:
        # Try reading as utf-8 first
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        try:
            # Try reading as utf-16 (powershell default)
            with open('.env', 'r', encoding='utf-16') as f:
                content = f.read()
        except:
            # Fallback to binary and decode ignoring errors
            with open('.env', 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
    
    # Clean up content (remove null bytes if any remain)
    content = content.replace('\x00', '')
    
    # Parse lines
    lines = content.splitlines()
    new_lines = []
    
    api_key = "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"
    key_added = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('OPENROUTER_API_KEY='):
            new_lines.append(f"OPENROUTER_API_KEY={api_key}")
            key_added = True
        elif line.startswith('DEEPSEEK_API_KEY='):
            # Remove deepseek key
            continue
        else:
            new_lines.append(line)
            
    if not key_added:
        new_lines.append(f"OPENROUTER_API_KEY={api_key}")
        
    # Write back as clean UTF-8
    with open('.env', 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
        
    print("✅ .env file fixed and updated!")

if __name__ == "__main__":
    fix_env()
