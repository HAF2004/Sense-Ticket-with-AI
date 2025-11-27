# modules/admin.py
# Admin commands for bot management

import discord
from discord.ext import commands
from core.config import SPECIAL_USER_ID

class AdminCog(commands.Cog):
    """
    Admin commands for bot management
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown", aliases=["turnoff", "stopbot"])
    async def shutdown(self, ctx):
        """
        Shuts down the bot (Owner only)
        """
        if ctx.author.id != SPECIAL_USER_ID:
            await ctx.reply("Kamu bukan owner aku ya~ 😋")
            return

        await ctx.reply("Baiklah, aku istirahat dulu ya~ Sampai jumpa! 👋")
        print("🛑 Bot shutting down via command...")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
    print("  🛡️ Admin cog loaded")
