# handlers/utils.py
# Utility functions

def classify_message(content):
    """Classify message into categories"""
    content = content.lower()
    if any(word in content for word in ['fuck', 'shit', 'bitch', 'stupid', 'idiot', 'anjing', 'bangsat', 'tolol']):
        return 'Toxic'
    if any(word in content for word in ['help', 'support', 'admin', 'mod', 'assist', 'bantuan', 'tolong']):
        return 'Help'
    if any(word in content for word in ['how', 'what', 'where', 'why', 'idk', 'confused', 'gimana', 'apa', 'bingung']):
        return 'Confused'
    return 'General'
