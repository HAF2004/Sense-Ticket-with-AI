# core/bot.py
# Main bot entry point with Cogs architecture

import discord
from discord.ext import commands
import asyncio
from core.config import DISCORD_BOT_TOKEN, TICKET_CATEGORY_ID
from models.database import db_manager

class SenseBot(commands.Bot):
    """
    Main bot class with Cogs architecture
    """
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        intents.message_content = True
        intents.reactions = True  # For feedback tracking
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None  # Custom help
        )
        
        # Initialize database
        db_manager.create_tables()
        
    async def setup_hook(self):
        """
        Load all cogs before bot starts
        """
        print("🔄 Loading cogs...")
        
        # List of cogs to load
        cogs = [
            "modules.logging",      # Message logger (must be first)
            "modules.ticketing",    # Ticketing system
            "modules.faq",          # FAQ system
            "modules.roles",        # Role management + Bloxlink
            "modules.voice_join",   # Voice join for specific user
            "modules.ai_chat",      # AI conversation handler
            "modules.status",       # Heartbeat for dashboard
            "modules.admin",        # Admin commands (shutdown, etc)
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"  ✅ Loaded: {cog}")
            except Exception as e:
                print(f"  ❌ Failed to load {cog}: {e}")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            print(f"✅ Synced {len(synced)} slash command(s)")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")
    
    async def on_ready(self):
        """
        Bot ready event
        """
        print("\n" + "="*50)
        print("✅ SENSE Bot Online - Cogs Architecture")
        print(f"🤖 Bot: {self.user.name}")
        print(f"📋 Servers: {len(self.guilds)}")
        print(f"🧩 Cogs: {len(self.cogs)}")
        print("="*50 + "\n")
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="SENSE Community 💚"
            )
        )


def run_bot():
    """
    Run the bot
    """
    if not DISCORD_BOT_TOKEN:
        raise ValueError("❌ No DISCORD_BOT_TOKEN found in .env file")
    
    bot = SenseBot()
    
    try:
        bot.run(DISCORD_BOT_TOKEN)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot crashed: {e}")


if __name__ == "__main__":
    run_bot()
