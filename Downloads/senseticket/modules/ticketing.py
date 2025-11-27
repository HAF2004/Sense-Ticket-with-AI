# modules/ticketing.py
# Ticketing system cog

import discord
from discord.ext import commands
from core.config import TICKET_CATEGORY_ID, TICKET_CHANNEL_PREFIX
from handlers import views

class TicketingCog(commands.Cog):
    """
    Handles ticketing system
    """
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """
        Auto-greet new ticket channels
        """
        if not isinstance(channel, discord.TextChannel):
            return
        
        if channel.category_id != TICKET_CATEGORY_ID:
            return
        
        if TICKET_CHANNEL_PREFIX not in channel.name.lower():
            return
        
        # Wait a bit for channel to be ready
        import asyncio
        await asyncio.sleep(2)
        
        # Send greeting with menu
        embed, view = views.get_main_menu_embed_and_view()
        await channel.send(embed=embed, view=view)
        
        print(f"🎫 Auto-greeted ticket channel: {channel.name}")
    
    @discord.app_commands.command(name="sense", description="Open SENSE Support Center")
    async def sense_command(self, interaction: discord.Interaction):
        """
        Slash command to open support menu
        """
        # Check if in ticket channel
        if not (interaction.channel.category_id == TICKET_CATEGORY_ID and 
                TICKET_CHANNEL_PREFIX in interaction.channel.name.lower()):
            embed = discord.Embed(
                title="❌ Invalid Channel",
                description="This command can only be used in ticket channels!",
                color=0xED4245
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Send support menu
        embed, view = views.get_main_menu_embed_and_view()
        await interaction.response.send_message(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Monitor ticket channels for first message analysis
        """
        # Skip bot messages
        if message.author.bot:
            return
            
        # Check if in ticket channel
        if not isinstance(message.channel, discord.TextChannel):
            return
            
        if message.channel.category_id != TICKET_CATEGORY_ID:
            return
            
        if TICKET_CHANNEL_PREFIX not in message.channel.name.lower():
            return
            
        # Check if this is likely the first or second message (heuristic)
        # We don't want to analyze every single chat
        # Ideally we check if an analysis has already been posted, but for now we check message count
        # or just check if it's the first message from this user in this channel
        
        # Simple heuristic: Only analyze if message length > 10 chars (meaningful content)
        if len(message.content) < 10:
            return
            
        # Check if we already analyzed this channel (prevent spam)
        # We can check if the bot has sent an "Analysis" embed recently
        history = []
        async for msg in message.channel.history(limit=10):
            history.append(msg)
        for msg in history:
            if msg.author == self.bot.user and msg.embeds and "Ticket Analysis" in (msg.embeds[0].title or ""):
                return  # Already analyzed
        
        # Trigger Analysis
        from handlers.gemini_handler import analyze_ticket
        
        # Send "Analyzing..." placeholder
        temp_msg = await message.channel.send("🔍 *Analyzing ticket content...*")
        
        analysis = await analyze_ticket(message.content)
        
        if analysis:
            # Create Embed
            color_map = {
                'High': 0xED4245,   # Red
                'Medium': 0xFFC107, # Yellow
                'Low': 0x57F287     # Green
            }
            urgency = analysis.get('urgency', 'Medium')
            color = color_map.get(urgency, 0x5865F2)
            
            embed = discord.Embed(title="🧠 Smart Ticket Analysis", color=color)
            embed.add_field(name="📝 Summary", value=analysis.get('summary', 'N/A'), inline=False)
            embed.add_field(name="🎭 Sentiment", value=analysis.get('sentiment', 'N/A'), inline=True)
            embed.add_field(name="🚨 Urgency", value=urgency, inline=True)
            embed.add_field(name="📂 Category", value=analysis.get('category', 'General'), inline=True)
            embed.set_footer(text="Powered by Google Gemini AI")
            
            await temp_msg.edit(content=None, embed=embed)
        else:
            await temp_msg.delete()


async def setup(bot):
    """
    Setup function for cog
    """
    # Register persistent views
    from handlers.views import MainMenuView, BackToMainView, QuestionView, BackToQuestionView, RoleRequestView
    bot.add_view(MainMenuView())
    bot.add_view(BackToMainView())
    bot.add_view(QuestionView())
    bot.add_view(BackToQuestionView())
    bot.add_view(RoleRequestView())
    
    await bot.add_cog(TicketingCog(bot))
    print("  🎫 Ticketing cog loaded")
    print("  ✅ Persistent views registered")

