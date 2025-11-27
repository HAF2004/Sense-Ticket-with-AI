# modules/voice_join.py
# Voice join cog for specific user

import discord
from discord.ext import commands
from core.config import SPECIAL_USER_ID

class VoiceJoinCog(commands.Cog):
    """
    Handles voice join when specific user tags bot
    """
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Join voice channel when specific user mentions bot
        """
        # Check if in guild
        if not message.guild:
            return

        # Check if specific user
        if message.author.id != SPECIAL_USER_ID:
            return
        
        # Check if bot is mentioned
        if not (self.bot.user.mentioned_in(message) and not message.mention_everyone):
            return

        # Check if author is in a voice channel
        if not message.author.voice or not message.author.voice.channel:
            await message.reply("Kamu belum masuk voice channel nih~")
            return

        voice_channel = message.author.voice.channel
        
        # Check if bot is already in a voice channel
        if message.guild.voice_client:
            if message.guild.voice_client.channel != voice_channel:
                await message.guild.voice_client.move_to(voice_channel)
                await message.reply(f"Pindah ke {voice_channel.name} ya~")
            else:
                await message.reply("Aku udah di sini kok~")
        else:
            try:
                await voice_channel.connect()
                await message.reply(f"Hadir di {voice_channel.name}~")
            except Exception as e:
                await message.reply(f"Gak bisa join nih: {e}")


async def setup(bot):
    """
    Setup function for cog
    """
    await bot.add_cog(VoiceJoinCog(bot))
    print("  🔊 Voice Join cog loaded")
