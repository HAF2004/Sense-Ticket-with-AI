import os
import sys
from sqlalchemy import create_engine, text
from datetime import datetime

# Setup path
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, 'bot_data_v2.db')
db_url = f'sqlite:///{db_path}'

print(f"📂 Database Path: {db_path}")

if not os.path.exists(db_path):
    print("❌ Database file NOT FOUND!")
    sys.exit(1)

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM bot_status"))
        rows = result.fetchall()
        
        if not rows:
            print("⚠️ Table 'bot_status' is EMPTY.")
        else:
            print(f"✅ Found {len(rows)} status records:")
            for row in rows:
                print(f"   - ID: {row[0]}, Status: {row[1]}, Last Heartbeat: {row[2]}")
                
        # Check current time
        print(f"🕒 Current Server Time: {datetime.utcnow()}")

except Exception as e:
    print(f"❌ Error reading database: {e}")
