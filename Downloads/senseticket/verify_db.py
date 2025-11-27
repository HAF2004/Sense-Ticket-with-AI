import sqlite3
import os

DB_FILE = 'bot_data_v2.db'

def verify_database():
    if not os.path.exists(DB_FILE):
        print(f"❌ File {DB_FILE} not found!")
        return

    print(f"🔍 Verifying {DB_FILE}...")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"✅ Connection successful! Found {len(tables)} tables:")
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   - 📄 Table '{table_name}': {count} rows")
            
        conn.close()
        print("\n✅ Database is HEALTHY and readable!")
        
    except sqlite3.DatabaseError as e:
        print(f"\n❌ Database Error: {e}")
        print("The file might be corrupted.")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")

if __name__ == "__main__":
    verify_database()
