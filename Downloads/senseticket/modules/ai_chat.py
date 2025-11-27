# modules/ai_chat.py
# AI Chat cog with out-of-context filtering and hard-coded rules

import discord
from discord.ext import commands
import random
from models.database import db_manager, Message, AIResponse, ChannelSettings
from core.config import JOIN_SENSE_TEXT, AI_SYSTEM_PROMPT, SPECIAL_USER_ID

class AIChatCog(commands.Cog):
    """
    AI conversation handler with smart filtering
    """
    def __init__(self, bot):
        self.bot = bot
        
    def is_join_question(self, content: str) -> bool:
        """
        Check if message is asking about joining Sense
        """
        lower = content.lower()
        keywords = [
            ('cara', 'gabung', 'sense'),
            ('cara', 'join', 'sense'),
            ('gimana', 'gabung'),
            ('how', 'join', 'sense'),
            ('gabung', 'sense'),
            ('daftar', 'sense')
        ]
        
        return any(all(k in lower for k in combo) for combo in keywords)
    
    def is_out_of_context(self, content: str) -> bool:
        """
        Filter out-of-context messages
        """
        # Heuristic checks
        
        # 1. Too short
        if len(content.strip()) < 3:
            return True
        
        # 2. Only emoji/symbols
        if all(not c.isalnum() for c in content):
            return True
        
        # 3. Only links
        if content.startswith('http') and ' ' not in content:
            return True
        
        # 4. Spam patterns
        spam_patterns = ['?????', '!!!!', 'wwww', 'aaaa']
        if any(pattern in content.lower() for pattern in spam_patterns):
            return True
        
        return False
    
    def should_respond(self, message: discord.Message) -> bool:
        """
        Check if AI should respond to this message
        """
        # Check channel settings
        session = db_manager.get_session()
        try:
            settings = session.query(ChannelSettings).filter_by(
                channel_id=str(message.channel.id)
            ).first()
            
            if settings:
                if not settings.ai_enabled or settings.ai_mode == 'off':
                    return False
                
                if settings.ai_mode == 'mention_only':
                    # Only respond if mentioned
                    is_mentioned = self.bot.user.mentioned_in(message) and not message.mention_everyone
                    is_reply = message.reference and message.reference.resolved and message.reference.resolved.author.id == self.bot.user.id
                    return is_mentioned or is_reply
            else:
                # Default: mention_only
                is_mentioned = self.bot.user.mentioned_in(message) and not message.mention_everyone
                is_reply = message.reference and message.reference.resolved and message.reference.resolved.author.id == self.bot.user.id
                return is_mentioned or is_reply
                
        finally:
            session.close()
        
        return False
    
    async def get_ai_response(self, message: discord.Message, query: str) -> str:
        """
        Get AI response using DeepSeek API with smart context
        """
        try:
            import analysis
            from handlers.gemini_handler import generate_response
            
            # Get context from database
            results = analysis.find_smart_context(query, limit=10, threshold=0.1)
            
            # Try DeepSeek API
            response = await generate_response(query, results)
            if response:
                return response
                
            # Fallback to template logic if API fails
            print("⚠️ DeepSeek API failed, checking cache...")
            
            # Try to find cached response
            cached_response = analysis.find_best_cached_response(query)
            if cached_response:
                print(f"✅ Found cached response: {cached_response[:30]}...")
                return f"{cached_response} 🤖"
            
            print("⚠️ Cache miss, using fallback templates")
            
            if results and len(results) > 0:
                relevant = [r for r in results if r['content'].lower() != query.lower() and len(r['content']) > 3]
                
                if relevant:
                    best = relevant[0]
                    score = best['score']
                    
                    is_question = '?' in query or any(w in query.lower() for w in ['apa', 'siapa', 'kapan', 'dimana', 'kenapa', 'gimana', 'berapa'])
                    
                    # Check keyword relevance
                    query_words = set(query.lower().split())
                    match_words = set(best['content'].lower().split())
                    has_keywords = len(query_words.intersection(match_words)) > 0
                    
                    if is_question:
                        if '?' in best['content']:
                            return random.choice([
                                "hmm gw juga penasaran nih 🤔",
                                "nah itu dia! gw juga lagi cari tau wkwk",
                                "menarik nih, tapi gw belum nemu jawabannya juga sih 😅",
                                "waduh kurang tau juga gw, coba tanya sepuh lain deh 😆",
                                "wah pertanyaan bagus! tapi gw masih blank nih hehe"
                            ])
                        else:
                            if score > 0.5 and has_keywords:
                                return random.choice([
                                    f"oh iya! setau gw sih {best['content']} 😊",
                                    f"{best['content']} kok! beneran deh ✨",
                                    f"yup! {best['content']} 👍",
                                    f"nah iya, {best['content']} kan? bener gak? 😄",
                                    f"kayaknya sih {best['content']} ya, cmiiw! 👀"
                                ])
                            elif score > 0.3 and has_keywords:
                                return random.choice([
                                    f"hmm {best['content']} kali ya? 🤔",
                                    f"kayaknya {best['content']} deh, tapi gw gak yakin 100%",
                                    f"mungkin {best['content']}? coba cek lagi deh",
                                    f"seinget gw sih {best['content']} ya..."
                                ])
                            else:
                                return random.choice([
                                    "hmm gw belum tau nih, sorry ya! 😅",
                                    "wah gw belum pernah denger, menarik sih! ceritain dong",
                                    "aduh kurang paham gw, skip dulu deh wkwk 🏃‍♂️",
                                    "kurang tau euy, mungkin yang lain tau? 🤔"
                                ])
                    else:
                        if score > 0.4 and has_keywords:
                            return random.choice([
                                f"iya! {best['content']} 💯",
                                f"bener banget! {best['content']} 🔥",
                                f"nah setuju! {best['content']} banget sih",
                                f"valid no debat! {best['content']} ✨",
                                f"asli! {best['content']} 👍"
                            ])
                        else:
                            return random.choice([
                                "wah menarik nih! cerita lebih lanjut dong! 😮",
                                "oh gitu ya! baru tau gw hehe, thanks infonya! 🙏",
                                "serius? wah gokil sih kalo gitu 😆",
                                "mantap! lanjutin ceritanya dong, kepo nih 👀"
                            ])
            
            return random.choice([
                "belum ada yang bahas ini sih, tapi gw pengen tau! cerita dong! 😊",
                "hmm belum pernah denger, tapi menarik! lanjutin dong 👀",
                "wah topik baru nih! gw nyimak aja deh hehe 🍿",
                "gimana tuh maksudnya? gw kurang nangkep 😅"
            ])
            
        except Exception as e:
            print(f"AI error: {e}")
            return random.choice([
                "aduh error nih, coba lagi ya! 😅",
                "wah ada masalah, sorry! coba tag lagi 🙏"
            ])
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Handle AI chat responses
        """
        # Skip own messages
        if message.author == self.bot.user:
            return
        
        # Skip bots
        if message.author.bot:
            return
        
        # Check if should respond
        if not self.should_respond(message):
            print(f"[DEBUG] Ignoring message from {message.author}: {message.content[:20]}...")
            return
        
        print(f"[DEBUG] Processing message from {message.author}: {message.content}")
        
        # Extract query
        query = message.content
        for mention in message.mentions:
            query = query.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
        query = query.strip()
        
        if not query:
            await message.reply(random.choice([
                "iya? 😊",
                "ada apa? 👀",
                "yes? ✨"
            ]))
            return
        
        # Hard-coded rule: cara gabung sense
        if self.is_join_question(query):
            await message.reply(JOIN_SENSE_TEXT)
            return
        
        # Check common questions (including registration status)
        from handlers.responses import check_common_question
        is_common, common_response = check_common_question(query.lower())
        if is_common:
            await message.reply(common_response)
            return
        
        # Out-of-context filter
        if self.is_out_of_context(query):
            await message.reply("Ini maksudnya apa? Gue kurang nangkep 😅")
            return
        
        # Get AI response
        response_text = await self.get_ai_response(message, query)
        
        # Send response
        response_msg = await message.reply(response_text)
        
        # Track in database
        session = db_manager.get_session()
        try:
            # Get request message ID
            request_msg = session.query(Message).filter_by(
                discord_message_id=str(message.id)
            ).first()
            
            if request_msg:
                # Manually log the AI response message since logging cog ignores bots
                response_msg_db = Message(
                    discord_message_id=str(response_msg.id),
                    guild_id=str(response_msg.guild.id),
                    channel_id=str(response_msg.channel.id),
                    author_id=str(response_msg.author.id),
                    content=response_msg.content,
                    timestamp=response_msg.created_at,
                    is_bot=True,
                    is_ai_response=True
                )
                session.add(response_msg_db)
                session.flush() # Get ID
                
                # Create AI Response record
                ai_response = AIResponse(
                    request_message_id=request_msg.id,
                    response_message_id=response_msg_db.id,
                    style_tags="ceria,kepo",
                    confidence_score=0.7
                )
                session.add(ai_response)
                session.commit()
        except Exception as e:
            print(f"Error tracking AI response: {e}")
            session.rollback()
        finally:
            session.close()


async def setup(bot):
    """
    Setup function for cog
    """
    await bot.add_cog(AIChatCog(bot))
    print("  🤖 AI Chat cog loaded")
