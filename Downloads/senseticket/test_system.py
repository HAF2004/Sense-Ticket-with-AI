# test_system.py
# System testing script

import sys
import os

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from core import config
        print("  ✅ core.config")
    except Exception as e:
        print(f"  ❌ core.config: {e}")
        return False
    
    try:
        from models import database
        print("  ✅ models.database")
    except Exception as e:
        print(f"  ❌ models.database: {e}")
        return False
    
    try:
        import analysis
        print("  ✅ analysis")
    except Exception as e:
        print(f"  ❌ analysis: {e}")
        return False
    
    return True

def test_database():
    """Test database connection and tables"""
    print("\n🧪 Testing database...")
    
    try:
        from models.database import db_manager, Message, AIResponse, ChannelSettings
        
        # Create tables
        db_manager.create_tables()
        print("  ✅ Tables created")
        
        # Test session
        session = db_manager.get_session()
        count = session.query(Message).count()
        session.close()
        print(f"  ✅ Database connection OK ({count} messages)")
        
        return True
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\n🧪 Testing configuration...")
    
    try:
        from core.config import DISCORD_BOT_TOKEN, DATABASE_URL, JOIN_SENSE_TEXT
        
        if not DISCORD_BOT_TOKEN:
            print("  ⚠️ DISCORD_BOT_TOKEN not set in .env")
            return False
        
        print("  ✅ Bot token configured")
        print(f"  ✅ Database URL: {DATABASE_URL}")
        print("  ✅ Join text configured")
        
        return True
    except Exception as e:
        print(f"  ❌ Config error: {e}")
        return False

def test_cogs():
    """Test if all cogs can be loaded"""
    print("\n🧪 Testing cogs...")
    
    cogs = [
        "modules.logging",
        "modules.ai_chat",
        "modules.ticketing",
        "modules.faq",
        "modules.roles",
        "modules.voice_join"
    ]
    
    all_ok = True
    for cog in cogs:
        try:
            __import__(cog)
            print(f"  ✅ {cog}")
        except Exception as e:
            print(f"  ❌ {cog}: {e}")
            all_ok = False
    
    return all_ok

def test_handlers():
    """Test handlers"""
    print("\n🧪 Testing handlers...")
    
    try:
        from handlers import views, responses, utils, roblox_api
        print("  ✅ All handlers imported")
        return True
    except Exception as e:
        print(f"  ❌ Handlers error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*50)
    print("🚀 SENSE Bot v2 - System Test")
    print("="*50)
    
    results = {
        "Imports": test_imports(),
        "Database": test_database(),
        "Configuration": test_config(),
        "Cogs": test_cogs(),
        "Handlers": test_handlers()
    }
    
    print("\n" + "="*50)
    print("📊 Test Results:")
    print("="*50)
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test:20} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ All tests passed! System is ready.")
    else:
        print("❌ Some tests failed. Please fix errors above.")
    print("="*50)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
