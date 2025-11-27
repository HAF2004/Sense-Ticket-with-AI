# modules/logging.py
# Message logging cog with anti-duplicate

import discord
from discord.ext import commands
from sqlalchemy.exc import IntegrityError
from models.database import db_manager, Message
from datetime import datetime

class LoggingCog(commands.Cog):
    """
    Handles all message logging with anti-duplicate protection
    """
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Log all messages to database with anti-duplicate
        """
        # Skip if:
        # - Message from bot (unless it's AI response)
        # - Message in DM
        if message.guild is None:
            return
        
        if message.author.bot:
            return
        
        # Get database session
        session = db_manager.get_session()
        
        try:
            # Create message record
            msg_record = Message(
                discord_message_id=str(message.id),
                guild_id=str(message.guild.id),
                channel_id=str(message.channel.id),
                author_id=str(message.author.id),
                content=message.content,
                timestamp=message.created_at,
                is_bot=message.author.bot,
                is_ai_response=getattr(message, '_is_ai_response', False)
            )
            
            session.add(msg_record)
            session.commit()
            
        except IntegrityError:
            # Duplicate message (discord_message_id already exists)
            session.rollback()
            # Silently skip - this is expected for duplicate events
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error logging message {message.id}: {e}")
            
        finally:
            session.close()


async def setup(bot):
    """
    Setup function for cog
    """
    await bot.add_cog(LoggingCog(bot))
    print("  📝 Logging cog loaded")
