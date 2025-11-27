import discord
from discord.ext import commands, tasks
from models.database import db_manager, BotStatus
from datetime import datetime

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.heartbeat.start()

    def cog_unload(self):
        self.heartbeat.cancel()

    @tasks.loop(seconds=60)
    async def heartbeat(self):
        """
        Update bot status in database every 60 seconds
        """
        try:
            session = db_manager.get_session()
            try:
                status = session.query(BotStatus).first()
                if not status:
                    status = BotStatus(
                        status='online',
                        last_heartbeat=datetime.utcnow()
                    )
                    session.add(status)
                else:
                    status.status = 'online'
                    status.last_heartbeat = datetime.utcnow()
                
                session.commit()
                # print("💓 Heartbeat sent")
            except Exception as e:
                print(f"❌ Heartbeat error: {e}")
            finally:
                session.close()
        except Exception as e:
            print(f"❌ Heartbeat task error: {e}")

    @heartbeat.before_loop
    async def before_heartbeat(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Status(bot))
