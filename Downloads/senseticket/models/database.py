# models/database.py
# SQLAlchemy models for SENSE Bot

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime
import os

Base = declarative_base()

class Message(Base):
    """
    Messages table - stores all Discord messages with anti-duplicate
    """
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    discord_message_id = Column(String, unique=True, nullable=False, index=True)  # Anti-duplicate
    guild_id = Column(String, nullable=False, index=True)
    channel_id = Column(String, nullable=False, index=True)
    author_id = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_bot = Column(Boolean, default=False, nullable=False)
    is_ai_response = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    ai_requests = relationship("AIResponse", foreign_keys="AIResponse.request_message_id", back_populates="request_message")
    ai_responses = relationship("AIResponse", foreign_keys="AIResponse.response_message_id", back_populates="response_message")
    
    def __repr__(self):
        return f"<Message(id={self.id}, author={self.author_id}, content='{self.content[:30]}...')>"


class AIResponse(Base):
    """
    AI Responses table - tracks AI conversations with feedback
    """
    __tablename__ = 'ai_responses'
    
    id = Column(Integer, primary_key=True)
    request_message_id = Column(Integer, ForeignKey('messages.id'), nullable=False)
    response_message_id = Column(Integer, ForeignKey('messages.id'), nullable=False)
    style_tags = Column(String)  # "ceria,kepo,short"
    feedback_score = Column(Integer, default=0)  # From reactions: 👍=+1, ❤️=+2, 😂=+1, 👎=-1
    confidence_score = Column(Float)  # AI confidence (0.0-1.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    request_message = relationship("Message", foreign_keys=[request_message_id], back_populates="ai_requests")
    response_message = relationship("Message", foreign_keys=[response_message_id], back_populates="ai_responses")
    
    def __repr__(self):
        return f"<AIResponse(id={self.id}, feedback={self.feedback_score}, confidence={self.confidence_score})>"


class StyleProfile(Base):
    """
    Style Profile table - learns from member conversations
    """
    __tablename__ = 'style_profiles'
    
    id = Column(Integer, primary_key=True)
    period = Column(String, unique=True, nullable=False)  # "2025-W48"
    common_words = Column(JSON)  # {"wkwk": 150, "anjir": 120, ...}
    common_emoji = Column(JSON)  # {"😂": 200, "💀": 150, ...}
    tone_examples = Column(JSON)  # [{content: "...", score: 0.9}, ...]
    total_messages = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<StyleProfile(period={self.period}, messages={self.total_messages})>"


class ChannelSettings(Base):
    """
    Channel Settings table - AI control per channel
    """
    __tablename__ = 'channel_settings'
    
    channel_id = Column(String, primary_key=True)
    guild_id = Column(String, nullable=False)
    ai_enabled = Column(Boolean, default=True, nullable=False)
    ai_mode = Column(String, default='mention_only', nullable=False)  # "off", "mention_only", "free_chat"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<ChannelSettings(channel={self.channel_id}, mode={self.ai_mode})>"


class BotStatus(Base):
    """
    Bot Status table - for dashboard monitoring
    """
    __tablename__ = 'bot_status'
    
    id = Column(Integer, primary_key=True)
    status = Column(String, default='offline')
    last_heartbeat = Column(DateTime)
    
    def __repr__(self):
        return f"<BotStatus(status={self.status}, heartbeat={self.last_heartbeat})>"


class Action(Base):
    """
    Actions table - user interactions (buttons, commands)
    """
    __tablename__ = 'actions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    action_type = Column(String, nullable=False)  # "Click Register", "Click FAQ", etc.
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Action(user={self.user_id}, type={self.action_type})>"


# Database connection and session management
class DatabaseManager:
    """
    Database manager for creating engine and sessions
    """
    def __init__(self, database_url=None):
        if database_url is None:
            # Use absolute path to avoid CWD issues
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, 'bot_data_v2.db')
            database_url = f'sqlite:///{db_path}'
            
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)
        print("✅ Database tables created successfully")
        
    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()
    
    def log_action(self, user_id, action_type):
        """Log user action"""
        session = self.get_session()
        try:
            action = Action(user_id=str(user_id), action_type=action_type)
            session.add(action)
            session.commit()
        except Exception as e:
            print(f"❌ Error logging action: {e}")
            session.rollback()
        finally:
            session.close()

    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(self.engine)
        print("⚠️ All tables dropped")


# Singleton instance
db_manager = DatabaseManager()


if __name__ == "__main__":
    # Create tables when run directly
    db_manager.create_tables()
    print("Database initialized!")
