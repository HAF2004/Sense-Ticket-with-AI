# handlers/registration_detector.py
# Dynamic registration status detection from chat history

from datetime import datetime, timedelta
from models.database import db_manager, Message
from sqlalchemy import and_

def is_open_statement(text: str) -> bool:
    """
    Detect if text indicates registration is OPEN
    """
    text_lower = text.lower()
    
    # Ignore questions
    if '?' in text:
        return False
    
    # Check for negations (these flip the meaning)
    negations = ['gak', 'ga', 'tidak', 'bukan', 'belum', 'ngga']
    has_negation = any(neg in text_lower for neg in negations)
    
    # OPEN indicators
    open_keywords = [
        ('lagi', 'open', 'member'),
        ('udah', 'open', 'member'),
        ('member', 'lagi', 'buka'),
        ('open', 'member', 'sekarang'),
        ('buka', 'member', 'nih'),
        ('registrasi', 'lagi', 'buka'),
        ('member', 'udah', 'buka'),
        ('sekarang', 'open'),
        ('lagi', 'buka'),
    ]
    
    # Check if any keyword combo matches
    for combo in open_keywords:
        if all(k in text_lower for k in combo):
            # If negation exists, flip the result
            return not has_negation
    
    return False


def is_close_statement(text: str) -> bool:
    """
    Detect if text indicates registration is CLOSED
    """
    text_lower = text.lower()
    
    # Ignore questions
    if '?' in text:
        return False
    
    # Check for negations
    negations = ['gak', 'ga', 'tidak', 'bukan']
    has_negation = any(neg in text_lower for neg in negations)
    
    # CLOSE indicators
    close_keywords = [
        ('lagi', 'close', 'member'),
        ('masih', 'close', 'member'),
        ('member', 'masih', 'tutup'),
        ('close', 'member', 'dulu'),
        ('belum', 'buka', 'member'),
        ('member', 'belum', 'open'),
        ('masih', 'tutup'),
        ('belum', 'open'),
        ('close', 'dulu'),
        ('tutup', 'member'),
    ]
    
    # Check if any keyword combo matches
    for combo in close_keywords:
        if all(k in text_lower for k in combo):
            # If negation exists, flip the result
            return not has_negation
    
    return False


def get_registration_sentiment(days: int = 7, min_threshold: int = 5) -> str:
    """
    Analyze chat history to determine registration status
    
    Args:
        days: Number of days to look back
        min_threshold: Minimum number of messages needed to make determination
    
    Returns:
        'OPEN', 'CLOSE', or 'DEFAULT'
    """
    session = db_manager.get_session()
    
    try:
        # Calculate time threshold
        time_threshold = datetime.utcnow() - timedelta(days=days)
        
        # Query messages from last N days
        messages = session.query(Message).filter(
            and_(
                Message.timestamp >= time_threshold,
                Message.is_bot == False  # Only user messages
            )
        ).all()
        
        # Analyze each message
        open_count = 0
        close_count = 0
        
        for msg in messages:
            content = msg.content
            
            if is_open_statement(content):
                open_count += 1
            elif is_close_statement(content):
                close_count += 1
        
        total_relevant = open_count + close_count
        
        # If not enough data, return default
        if total_relevant < min_threshold:
            return 'DEFAULT'
        
        # Calculate sentiment score
        score = open_count - close_count
        
        if score > 0:
            return 'OPEN'
        elif score < 0:
            return 'CLOSE'
        else:
            # Tie - return default
            return 'DEFAULT'
    
    except Exception as e:
        print(f"Error in get_registration_sentiment: {e}")
        return 'DEFAULT'
    
    finally:
        session.close()


def get_registration_status_details(days: int = 7) -> dict:
    """
    Get detailed information about registration status detection
    Used for admin command
    
    Returns:
        dict with status, confidence, counts, and sample messages
    """
    session = db_manager.get_session()
    
    try:
        time_threshold = datetime.utcnow() - timedelta(days=days)
        
        messages = session.query(Message).filter(
            and_(
                Message.timestamp >= time_threshold,
                Message.is_bot == False
            )
        ).order_by(Message.timestamp.desc()).all()
        
        open_messages = []
        close_messages = []
        
        for msg in messages:
            content = msg.content
            
            if is_open_statement(content):
                open_messages.append({
                    'content': content,
                    'timestamp': msg.timestamp,
                    'user_id': msg.user_id
                })
            elif is_close_statement(content):
                close_messages.append({
                    'content': content,
                    'timestamp': msg.timestamp,
                    'user_id': msg.user_id
                })
        
        total = len(open_messages) + len(close_messages)
        score = len(open_messages) - len(close_messages)
        
        if total >= 5:
            if score > 0:
                status = 'OPEN'
            elif score < 0:
                status = 'CLOSE'
            else:
                status = 'DEFAULT'
        else:
            status = 'DEFAULT'
        
        confidence = (abs(score) / total * 100) if total > 0 else 0
        
        return {
            'status': status,
            'confidence': confidence,
            'open_count': len(open_messages),
            'close_count': len(close_messages),
            'total_count': total,
            'open_samples': open_messages[:3],  # Top 3
            'close_samples': close_messages[:3]  # Top 3
        }
    
    except Exception as e:
        print(f"Error in get_registration_status_details: {e}")
        return {
            'status': 'DEFAULT',
            'confidence': 0,
            'open_count': 0,
            'close_count': 0,
            'total_count': 0,
            'open_samples': [],
            'close_samples': []
        }
    
    finally:
        session.close()


def get_chat_activity(minutes: int = 15) -> str:
    """
    Analyze chat activity in the last N minutes
    Returns: 'HIGH', 'MEDIUM', 'LOW'
    """
    session = db_manager.get_session()
    
    try:
        time_threshold = datetime.utcnow() - timedelta(minutes=minutes)
        
        # Count recent messages
        count = session.query(Message).filter(
            and_(
                Message.timestamp >= time_threshold,
                Message.is_bot == False
            )
        ).count()
        
        if count > 20:
            return 'HIGH'
        elif count > 5:
            return 'MEDIUM'
        else:
            return 'LOW'
            
    except Exception as e:
        print(f"Error in get_chat_activity: {e}")
        return 'LOW'
    
    finally:
        session.close()

