# migrations/migrate_v1_to_v2.py
# Migration script from old SQLite to new schema

import sqlite3
from datetime import datetime
from models.database import db_manager, Message, Action, BotStatus

def migrate_old_to_new():
    """
    Migrate data from old bot_data.db to new schema
    """
    print("🔄 Starting migration from v1 to v2...")
    
    # Connect to old database
    old_conn = sqlite3.connect('bot_data.db')
    old_cursor = old_conn.cursor()
    
    # Get new database session
    session = db_manager.get_session()
    
    try:
        # Migrate conversations to messages
        print("📝 Migrating conversations...")
        old_cursor.execute("SELECT * FROM conversations")
        conversations = old_cursor.fetchall()
        
        migrated_count = 0
        skipped_count = 0
        
        for conv in conversations:
            # conv = (id, user_id, channel_id, content, category, timestamp)
            try:
                message = Message(
                    discord_message_id=f"migrated_{conv[0]}",  # Use old ID with prefix
                    guild_id="unknown",  # Old schema didn't store guild_id
                    channel_id=str(conv[2]),
                    author_id=str(conv[1]),
                    content=conv[3],
                    timestamp=datetime.fromisoformat(conv[5]) if conv[5] else datetime.utcnow(),
                    is_bot=False,
                    is_ai_response=False
                )
                session.add(message)
                migrated_count += 1
            except Exception as e:
                print(f"  ⚠️ Skipped conversation {conv[0]}: {e}")
                skipped_count += 1
        
        session.commit()
        print(f"  ✅ Migrated {migrated_count} conversations ({skipped_count} skipped)")
        
        # Migrate actions
        print("📝 Migrating actions...")
        old_cursor.execute("SELECT * FROM actions")
        actions = old_cursor.fetchall()
        
        migrated_count = 0
        for act in actions:
            # act = (id, user_id, action_type, timestamp)
            try:
                action = Action(
                    user_id=str(act[1]),
                    action_type=act[2],
                    timestamp=datetime.fromisoformat(act[3]) if act[3] else datetime.utcnow()
                )
                session.add(action)
                migrated_count += 1
            except Exception as e:
                print(f"  ⚠️ Skipped action {act[0]}: {e}")
        
        session.commit()
        print(f"  ✅ Migrated {migrated_count} actions")
        
        # Migrate bot status
        print("📝 Migrating bot status...")
        old_cursor.execute("SELECT * FROM bot_status LIMIT 1")
        status = old_cursor.fetchone()
        
        if status:
            bot_status = BotStatus(
                status=status[1] if len(status) > 1 else 'offline',
                last_heartbeat=datetime.fromisoformat(status[2]) if len(status) > 2 and status[2] else None
            )
            session.add(bot_status)
            session.commit()
            print("  ✅ Migrated bot status")
        
        print("\n✅ Migration completed successfully!")
        print(f"📊 Summary:")
        print(f"  - Messages: {session.query(Message).count()}")
        print(f"  - Actions: {session.query(Action).count()}")
        print(f"  - Bot Status: {session.query(BotStatus).count()}")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        session.rollback()
        raise
    finally:
        old_conn.close()
        session.close()


if __name__ == "__main__":
    # Create new tables first
    print("📋 Creating new database schema...")
    db_manager.create_tables()
    
    # Run migration
    migrate_old_to_new()
    
    print("\n🎉 Migration complete! New database is ready.")
    print("💡 Old database (bot_data.db) is preserved for backup.")
