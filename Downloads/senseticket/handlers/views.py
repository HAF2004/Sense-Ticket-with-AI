# handlers/views.py
# Discord UI Views and Embeds for ticketing system

import discord
from discord.ui import Button, View
from models.database import db_manager
from handlers.roblox_api import extract_roblox_username, get_roblox_user_by_username, check_group_membership_and_role

# Configuration
ROBLOX_GROUP_ID = 35908807
REQUIRED_ROLE_NAME = "💚・Our Lovely Sense Member"
DISCORD_VERIFIED_ROLE_ID = 1431176844279021578
ATTUNED_SOUL_ROLE_ID = 1431246790954451156

COLOR_PRIMARY = 0x5865F2
COLOR_SUCCESS = 0x57F287
COLOR_WARNING = 0xFFC107
COLOR_DANGER = 0xED4245
COLOR_INFO = 0x9B59B6
COLOR_PINK = 0xFFC0CB

def get_main_menu_embed_and_view():
    """Create main menu embed and view"""
    embed = discord.Embed(
        title="✦ SENSE Support Center ✦",
        description="**Welcome to SENSE Support!** 💫\n\nThank you for reaching out. Please select one of the options below:",
        color=COLOR_PRIMARY
    )
    embed.add_field(
        name="",
        value=(
            "```text\n📝 Register Member\nJoin the SENSE community and get registration steps.\n```\n"
            "```text\n❓ Question\nBrowse FAQs and get instant answers to common questions.\n```\n"
            "```text\n✨ Request Role\nVerify your membership and get the Attuned Soul role.\n```\n"
            "```text\n💬 Live Chat\nConnect with a staff member for personalized help.\n```"
        ),
        inline=False
    )
    embed.add_field(name="", value="**Click the button below that matches your need:** ⬇️", inline=False)
    embed.set_footer(text="SENSE Community • Support Team Available 24/7")
    embed.timestamp = discord.utils.utcnow()
    return embed, MainMenuView()

class MainMenuView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji="📝", style=discord.ButtonStyle.primary, row=0, custom_id="main_menu:register")
    async def register_button(self, interaction: discord.Interaction, button: Button):
        db_manager.log_action(interaction.user.id, "Click Register Guide")
        embed = discord.Embed(title="📝 Member Registration Guide", description="**𝜗𝜚⋆₊˚ HOW TO JOIN SENSE CLAN ⋆₊˚𝜗𝜚**\n", color=COLOR_PINK)
        embed.add_field(name="", value="```text\n📌 Step 1: Join Our Roblox Community\n• Change your display name to: username+sense\n• Example: dipsysense\n```", inline=False)
        embed.add_field(name="", value="🔗 [Click to Join Community](https://www.roblox.com/communities/35908807/SENSE-of-our-heart#!/about)", inline=False)
        embed.set_footer(text="Registration: Weekends only (Sat-Sun)")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.edit_message(embed=embed, view=BackToMainView())
    
    @discord.ui.button(emoji="❓", style=discord.ButtonStyle.primary, row=0, custom_id="main_menu:question")
    async def question_button(self, interaction: discord.Interaction, button: Button):
        db_manager.log_action(interaction.user.id, "Click FAQ Menu")
        embed = discord.Embed(title="❓ Frequently Asked Questions", description="Select a question below to get help! 💡\n", color=COLOR_PRIMARY)
        embed.add_field(name="", value=(
            "```text\n1️⃣ How do I join SENSE?\nRegistration schedule and how to become a member\n```\n"
            "```text\n2️⃣ Server Rules\nCommunity guidelines and policies you must follow\n```\n"
            "```text\n3️⃣ Game Tutorial\nGet help from staff for game tutorials and guidance\n```"
        ), inline=False)
        embed.set_footer(text="SENSE Community • Support Available 24/7")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.edit_message(embed=embed, view=QuestionView())
    
    @discord.ui.button(emoji="✨", style=discord.ButtonStyle.primary, row=0, custom_id="main_menu:request_role")
    async def request_role_button(self, interaction: discord.Interaction, button: Button):
        db_manager.log_action(interaction.user.id, "Click Request Role Menu")
        embed = discord.Embed(title="✨ Request Attuned Soul Role", description="**Choose your verification method:**\n", color=COLOR_WARNING)
        embed.add_field(name="", value="```text\n🎮 Automatic Verification\nClick 'Request Attuned Soul' to verify automatically.\nBot will check your SENSE Roblox group membership.\n```", inline=False)
        embed.add_field(name="", value="```text\n✅ Requirements:\n• Must be in SENSE Roblox group\n• Must have role: 💚・Our Lovely Sense Member\n• Discord name must show Roblox username (via Bloxlink)\n```", inline=False)
        embed.set_footer(text="Choose your verification method below")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.edit_message(embed=embed, view=RoleRequestView())
    
    @discord.ui.button(emoji="💬", style=discord.ButtonStyle.primary, row=0, custom_id="main_menu:livechat")
    async def livechat_button(self, interaction: discord.Interaction, button: Button):
        db_manager.log_action(interaction.user.id, "Click Live Chat Request")
        role = interaction.guild.get_role(ATTUNED_SOUL_ROLE_ID)
        embed = discord.Embed(title="💬 Live Chat Support Requested", description="**Support staff has been notified!**\n", color=COLOR_DANGER)
        embed.add_field(name="Staff Notification:", value=f"{role.mention if role else '@Attuned Soul'}", inline=False)
        embed.set_footer(text="Thank you for waiting • SENSE Support")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.send_message(embed=embed, ephemeral=False)

class BackToMainView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="⬅️ Back", style=discord.ButtonStyle.secondary, custom_id="back_to_main:back")
    async def back(self, interaction: discord.Interaction, button: Button):
        embed, view = get_main_menu_embed_and_view()
        await interaction.response.edit_message(embed=embed, view=view)

class QuestionView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(emoji="1️⃣", style=discord.ButtonStyle.primary, row=0, custom_id="question:q1")
    async def q1_button(self, interaction: discord.Interaction, button: Button):
        db_manager.log_action(interaction.user.id, "Click Q1: How to Join")
        embed = discord.Embed(title="📅 Registration Schedule", description="**When can I join SENSE?**\n", color=COLOR_SUCCESS)
        embed.add_field(name="Registration Schedule:", value="• **Open:** Saturdays & Sundays only\n• **Closed:** Monday through Friday", inline=False)
        embed.set_footer(text="Registration • Weekend Only")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.edit_message(embed=embed, view=BackToQuestionView())
    
    @discord.ui.button(emoji="2️⃣", style=discord.ButtonStyle.primary, row=0, custom_id="question:q2")
    async def q2_button(self, interaction: discord.Interaction, button: Button):
        db_manager.log_action(interaction.user.id, "Click Q2: Server Rules")
        from handlers.responses import RULES_TEXT
        await interaction.response.send_message(RULES_TEXT, ephemeral=True)
    
    @discord.ui.button(emoji="3️⃣", style=discord.ButtonStyle.primary, row=0, custom_id="question:q3")
    async def q3_button(self, interaction: discord.Interaction, button: Button):
        db_manager.log_action(interaction.user.id, "Click Q3: Game Tutorial")
        role = interaction.guild.get_role(ATTUNED_SOUL_ROLE_ID)
        embed = discord.Embed(title="🎮 Game Tutorial Request", description="**Tutorial assistance requested!**\n", color=COLOR_PRIMARY)
        embed.add_field(name="Staff Notification:", value=f"{role.mention if role else '@Attuned Soul'}", inline=False)
        embed.set_footer(text="Staff will help you master the game!")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.send_message(embed=embed, ephemeral=False)
    
    @discord.ui.button(label="⬅️ Back", style=discord.ButtonStyle.secondary, row=0, custom_id="question:back")
    async def back(self, interaction: discord.Interaction, button: Button):
        embed, view = get_main_menu_embed_and_view()
        await interaction.response.edit_message(embed=embed, view=view)

class BackToQuestionView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="⬅️ Back to FAQ", style=discord.ButtonStyle.secondary, custom_id="back_to_question:back")
    async def back(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(title="❓ Frequently Asked Questions", description="Select a question below to get help! 💡\n", color=COLOR_PRIMARY)
        embed.add_field(name="", value=(
            "```text\n1️⃣ How do I join SENSE?\nRegistration schedule and how to become a member\n```\n"
            "```text\n2️⃣ Server Rules\nCommunity guidelines and policies you must follow\n```\n"
            "```text\n3️⃣ Game Tutorial\nGet help from staff for game tutorials and guidance\n```"
        ), inline=False)
        embed.set_footer(text="SENSE Community • Support Available 24/7")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.edit_message(embed=embed, view=QuestionView())

class RoleRequestView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="👑 Request Attuned Soul", style=discord.ButtonStyle.success, row=0, custom_id="role_request:verify")
    async def verify_roblox_button(self, interaction: discord.Interaction, button: Button):
        db_manager.log_action(interaction.user.id, "Click Verify Roblox")
        await interaction.response.defer(ephemeral=True)
        
        display_name = interaction.user.display_name
        roblox_username = await extract_roblox_username(display_name)
        
        if not roblox_username:
            embed = discord.Embed(title="❌ Cannot Find Roblox Username", description="I couldn't find your Roblox username in your Discord name.\n\n**Please make sure:**\n• You've linked your Roblox account with Bloxlink\n• Your Discord nickname shows your Roblox username\n• Example: `@uppucs` or `uppucs`\n\n💡 Use `/verify` command with Bloxlink to link your account.", color=COLOR_DANGER)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        user_data = await get_roblox_user_by_username(roblox_username)
        if not user_data:
            embed = discord.Embed(title="❌ Roblox Account Not Found", description=f"Couldn't find Roblox account: `{roblox_username}`\n\n**Please check:**\n• Your Discord name matches your Roblox username\n• You've linked with Bloxlink correctly\n• The username is spelled correctly", color=COLOR_DANGER)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        user_id = user_data['id']
        is_verified, role_info = await check_group_membership_and_role(user_id, ROBLOX_GROUP_ID, REQUIRED_ROLE_NAME)
        
        if is_verified:
            role = interaction.guild.get_role(DISCORD_VERIFIED_ROLE_ID)
            if role:
                try:
                    await interaction.user.add_roles(role)
                    embed = discord.Embed(title="✅ Verification Successful!", description=f"**Welcome to SENSE, {user_data['displayName']}!** 💚\n\nYou've been verified and given the Attuned Soul role!", color=COLOR_SUCCESS)
                    embed.add_field(name="✅ Verified Information:", value=f"**Roblox Username:** {user_data['name']}\n**Roblox Display Name:** {user_data['displayName']}\n**Group Role:** {REQUIRED_ROLE_NAME}\n**Discord Role:** {role.mention}", inline=False)
                    embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=150&height=150&format=png")
                    embed.set_footer(text="Verification completed successfully!")
                    embed.timestamp = discord.utils.utcnow()
                    await interaction.followup.send(embed=embed, ephemeral=True)
                except Exception as e:
                    embed = discord.Embed(title="⚠️ Role Error", description=f"Verification passed but couldn't give role: {str(e)}", color=COLOR_DANGER)
                    await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="⚠️ Configuration Error", description="Attuned Soul role not found. Please contact staff.", color=COLOR_DANGER)
                await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="❌ Verification Failed", description=f"**Roblox Account:** {user_data['displayName']} (@{user_data['name']})\n**Reason:** {role_info}\n\n**Requirements:**\n✅ Must join **SENSE of our heart** group\n✅ Must have role: **💚・Our Lovely Sense Member**\n\n🔗 [Join Group Here](https://www.roblox.com/communities/35908807/SENSE-of-our-heart#!/about)", color=COLOR_DANGER)
            embed.set_thumbnail(url=f"https://www.roblox.com/headshot-thumbnail/image?userId={user_id}&width=150&height=150&format=png")
            embed.set_footer(text="Join the group with correct role and try again!")
            embed.timestamp = discord.utils.utcnow()
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="❓ Help!", style=discord.ButtonStyle.secondary, row=0, custom_id="role_request:help")
    async def manual_help_button(self, interaction: discord.Interaction, button: Button):
        db_manager.log_action(interaction.user.id, "Click Manual Help")
        role = interaction.guild.get_role(ATTUNED_SOUL_ROLE_ID)
        embed = discord.Embed(title="❓ Manual Role Request", description="**Staff assistance requested!**\n", color=COLOR_INFO)
        embed.add_field(name="", value=f"```text\n📋 Request Details:\n• Requested by: {interaction.user.display_name}\n• Type: Manual Role Verification\n• Status: 🟡 Pending Staff Review\n```", inline=False)
        embed.add_field(name="", value=f"👥 **Staff Notification:**\n{role.mention if role else '@Attuned Soul'} will assist you shortly.", inline=False)
        embed.set_footer(text="Thank you for your patience!")
        embed.timestamp = discord.utils.utcnow()
        await interaction.response.send_message(content=f"{role.mention if role else '@Attuned Soul'}", embed=embed, ephemeral=False)
    
    @discord.ui.button(label="⬅️ Back", style=discord.ButtonStyle.secondary, row=0, custom_id="role_request:back")
    async def back(self, interaction: discord.Interaction, button: Button):
        embed, view = get_main_menu_embed_and_view()
        await interaction.response.edit_message(embed=embed, view=view)
