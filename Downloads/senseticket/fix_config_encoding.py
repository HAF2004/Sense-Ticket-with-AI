# fix_config_encoding.py
import os

def fix_encoding():
    print("🔧 Fixing config.py encoding...")
    
    file_path = 'core/config.py'
    content = ""
    
    try:
        with open(file_path, 'rb') as f:
            raw = f.read()
            # Try decoding as utf-8
            try:
                content = raw.decode('utf-8')
            except UnicodeDecodeError:
                # Fallback to latin-1 or cp1252
                content = raw.decode('cp1252', errors='ignore')
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Ensure it starts with encoding declaration
    if not content.startswith('# -*- coding: utf-8 -*-'):
        content = '# -*- coding: utf-8 -*-\n' + content

    # Write back as strict utf-8
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("✅ config.py fixed!")

if __name__ == "__main__":
    fix_encoding()
