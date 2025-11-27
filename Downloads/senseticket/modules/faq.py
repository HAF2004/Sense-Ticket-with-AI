# modules/faq.py
# FAQ system cog

import discord
from discord.ext import commands

class FAQCog(commands.Cog):
    """
    FAQ system - handled by ticketing views
    """
    def __init__(self, bot):
        self.bot = bot
        
    # FAQ is handled through ticketing system views
    # This cog is a placeholder for future FAQ commands


async def setup(bot):
    """
    Setup function for cog
    """
    await bot.add_cog(FAQCog(bot))
    print("  ❓ FAQ cog loaded")
