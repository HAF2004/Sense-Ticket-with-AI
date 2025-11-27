# utils/maintenance.py
# Maintenance utilities for SENSE Bot

from models.database import db_manager, Message, AIResponse, StyleProfile, ChannelSettings
from datetime import datetime, timedelta
from sqlalchemy import func

class MaintenanceTools:
    """
    Utility tools for bot maintenance
    """
    
    @staticmethod
    def get_stats():
        """Get system statistics"""
        session = db_manager.get_session()
        
        try:
            stats = {
                'total_messages': session.query(Message).count(),
                'total_ai_responses': session.query(AIResponse).count(),
                'unique_users': session.query(func.count(func.distinct(Message.author_id))).scalar(),
                'database_size': 'N/A'  # Can be calculated if needed
            }
            
            # Today's stats
            today = datetime.utcnow().date()
            today_start = datetime.combine(today, datetime.min.time())
            
            stats['messages_today'] = session.query(Message).filter(
                Message.timestamp >= today_start
            ).count()
            
            stats['ai_responses_today'] = session.query(Message).filter(
                Message.is_ai_response == True,
                Message.timestamp >= today_start
            ).count()
            
            return stats
            
        finally:
            session.close()
    
    @staticmethod
    def cleanup_old_data(days=90):
        """
        Clean up data older than specified days
        """
        session = db_manager.get_session()
        
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Count messages to delete
            old_messages = session.query(Message).filter(
                Message.timestamp < cutoff_date
            ).count()
            
            print(f"Found {old_messages} messages older than {days} days")
            
            # Delete old messages (cascade will handle AI responses)
            deleted = session.query(Message).filter(
                Message.timestamp < cutoff_date
            ).delete()
            
            session.commit()
            print(f"✅ Deleted {deleted} old messages")
            
            return deleted
            
        except Exception as e:
            session.rollback()
            print(f"❌ Cleanup failed: {e}")
            return 0
            
        finally:
            session.close()
    
    @staticmethod
    def reset_channel_settings(channel_id):
        """Reset channel settings to default"""
        session = db_manager.get_session()
        
        try:
            settings = session.query(ChannelSettings).filter_by(
                channel_id=channel_id
            ).first()
            
            if settings:
                settings.ai_enabled = True
                settings.ai_mode = 'mention_only'
                settings.updated_at = datetime.utcnow()
                session.commit()
                print(f"✅ Reset settings for channel {channel_id}")
            else:
                print(f"⚠️ No settings found for channel {channel_id}")
                
        except Exception as e:
            session.rollback()
            print(f"❌ Reset failed: {e}")
            
        finally:
            session.close()
    
    @staticmethod
    def export_conversations_csv(output_file='conversations.csv'):
        """Export conversations to CSV"""
        session = db_manager.get_session()
        
        try:
            import csv
            
            messages = session.query(Message).order_by(Message.timestamp).all()
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Author', 'Channel', 'Content', 'Timestamp', 'Is AI'])
                
                for msg in messages:
                    writer.writerow([
                        msg.id,
                        msg.author_id,
                        msg.channel_id,
                        msg.content,
                        msg.timestamp,
                        msg.is_ai_response
                    ])
            
            print(f"✅ Exported {len(messages)} messages to {output_file}")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            
        finally:
            session.close()
    
    @staticmethod
    def print_stats():
        """Print formatted statistics"""
        stats = MaintenanceTools.get_stats()
        
        print("\n" + "="*50)
        print("📊 SENSE Bot Statistics")
        print("="*50)
        print(f"Total Messages:        {stats['total_messages']:,}")
        print(f"Total AI Responses:    {stats['total_ai_responses']:,}")
        print(f"Unique Users:          {stats['unique_users']:,}")
        print(f"Messages Today:        {stats['messages_today']:,}")
        print(f"AI Responses Today:    {stats['ai_responses_today']:,}")
        print("="*50 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python utils/maintenance.py stats              - Show statistics")
        print("  python utils/maintenance.py cleanup [days]     - Cleanup old data")
        print("  python utils/maintenance.py export [file]      - Export to CSV")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "stats":
        MaintenanceTools.print_stats()
    
    elif command == "cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 90
        MaintenanceTools.cleanup_old_data(days)
    
    elif command == "export":
        output = sys.argv[2] if len(sys.argv) > 2 else 'conversations.csv'
        MaintenanceTools.export_conversations_csv(output)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
