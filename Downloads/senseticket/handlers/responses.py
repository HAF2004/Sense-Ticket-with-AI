# handlers/responses.py
# Common question responses untuk bot

RULES_TEXT = """**ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ.**
follow the discord terms of server, meaning that you are fifteen or older. limited cursing, some may be sensitive to excessive swearing, so please be aware of that.

**ɴᴏ ɴꜱꜰᴡ ᴄᴏɴᴛᴇɴᴛ.**
refrain from posting or having conversations abt explicit content.

**ɴᴏ ᴄᴏɴᴛʀᴏᴠᴇʀꜱɪᴀʟ ᴘᴏʟɪᴛɪᴄᴀʟ ᴏʀ ʀᴇʟɪɢɪᴏᴜꜱ ᴅɪꜱᴄᴜꜱꜱɪᴏɴ.**
this isn't a place for those topics between the community.

**ɴᴏ ᴅʀᴀᴍᴀ.**
do not ever include sense or this clan to your personal conflict with others. and also, you'll be banned if we saw u caused some drama in general channel or other text channel.

**ʀᴇꜱᴘᴇᴄᴛ ᴇᴀᴄʜ ᴏᴛʜᴇʀ.**
respect is really important within this server. have some respect to each other members, contributors, staffs and also, content creators. any type of disrespect toward others will not be tolerated. any form of harassment such as blackmailing, doxxing, inappropriate DMs, racism, sexism, body shaming will not be tolerated.

**ᴘᴀᴛɪᴇɴᴄᴇ ᴀɴᴅ ᴄᴏᴍᴘʟᴀɪɴᴛꜱ.**
with some situations, it might take a while to deal things since we want to be able do it right and properly. because of this, please be patient with us. if you think you were wrongly banned or kicked, please message our staff and our contributors with your reasoning on why you think it was wrong."""

COMMON_RESPONSES = {
    'greeting': [
        "yoi, apa kabar? 👀",
        "halo bang! lagi ngapain?",
        "woy! ada apa nih? 🤙",
        "yoo! seneng liat lu disini 💚",
        "halo! sehat kan? ✨",
        "pagi/siang/malem! udah makan belum? wkwk"
    ],
    'identity': [
        "gw Sense! temen ngobrol lu disini 🤙",
        "kenalin gw Sense, bot paling asik di server ini (katanya sih) wkwk",
        "gw Sense! salam kenal ya! 🤝",
        "nama gw Sense, lagi belajar jadi anak gaul nih bjir 😆"
    ],
    'capability': [
        "gw bisa bantu jawab pertanyaan lu, atau sekedar nemenin gabut wkwk 🔍",
        "gw lagi belajar banyak hal nih dari kalian! makin sering diajak ngobrol makin pinter gw 📚",
        "gw punya ingatan tajam (caching) lho, jadi bisa inget obrolan kita sebelumnya! keren kan? 🧠"
    ],
    'status': [
        "baik parah! lu gimana? ada cerita seru ga? 😊",
        "aman jaya! lagi semangat 45 nih! lu sendiri? 💪",
        "gacor kang! lagi excited belajar hal baru 🌟",
        "sehat walafiat! penasaran nih lu lagi ngapain? 👀",
        "alhamdulillah baik! lu apa kabar? 💚"
    ],
    'thanks': [
        "yoi santai aja! seneng bisa bantu! 😊",
        "siap bang! kapan-kapan tanya lagi ya! ✨",
        "gas! gw seneng kok kalo bisa bantu 💚",
        "aman! anytime kalo butuh bantuan! 🙌",
        "wkwk sama-sama! 😄"
    ],
    'empty': [
        "yoi? ada yang bisa gw bantu? 😊",
        "kenapa bang? penasaran gw hehe 👀",
        "yes? mau nanya apa? ✨",
        "hmm? ada yang mau diceritain? 💬",
        "kenapa tuh? ada apa? 🤔"
    ],
    'curious': [
        "wah menarik tuh! cerita lagi dong! 😮",
        "oh ya? terus gimana kelanjutannya? 👀",
        "seru bjir! gw penasaran banget 🤩",
        "wah gokil! lanjutin ceritanya dong ✨"
    ],
    'registration_status_open': [
        "Gas daftar! Lagi OPEN MEMBER nih sekarang! 🎉",
        "Woy open member tuh! Buruan sikat sebelum tutup! ✨",
        "Udah buka nih registrasinya! Gaskeun daftar! 🔥",
        "Yoi! Registrasi lagi buka sekarang! Join sini! 💚"
    ],
    'registration_status_close': [
        "Waduh belum buka bang, masih CLOSE member sekarang 😊",
        "Masih tutup euy! Tunggu info selanjutnya ya 💚",
        "Belum open nih! Sabar ya, pantengin terus infonya ✨",
        "Nope, masih tutup! Belum buka pendaftaran 🗓️"
    ],
    'registration_status_default': [
        "Registrasi biasanya cuma buka weekend (Sabtu-Minggu) 📅\nCoba cek lagi pas weekend ya!",
        "Member baru cuma dibuka Sabtu-Minggu aja biasanya 💚",
        "Buka member cuma akhir pekan (Sat-Sun) setau gw ✨",
        "Weekend only bang! Sabtu & Minggu aja buka registrasi 🗓️"
    ],
    'crowd_status_high': [
        "Rame bet gila! 🔥",
        "Lagi rame parah nih! Seru banget chatnya 😆",
        "Waduh rame banget! Sampe pusing bacanya wkwk 🤪",
        "Hype abis! Rame polll ✨"
    ],
    'crowd_status_medium': [
        "Lumayan rame kok! Asik buat ngobrol 😊",
        "Not bad lah, ada aja yang chat 👍",
        "Lumayan nih, gak sepi-sepi amat hehe",
        "Sedeng lah, enak buat santai ☕"
    ],
    'crowd_status_low': [
        "Lagi sepi nyenyet... pada kemana ya? 🤔",
        "Sepi banget kayak hati jomblo wkwk 🤣",
        "Hening... krik krik 🦗",
        "Lagi pada sibuk real life kayaknya, sepi beut 😴"
    ],
    'fun_handsome': [
        "Ya jelas yang baca pesan ini dong! 😎",
        "Hmm... kayaknya lu deh? wkwk 😆",
        "Semua member Sense kece-kece kok! ✨",
        "Admin lah, valid no debat! 👑",
        "Gak ada yang ngalahin Sense dong (canda deng) 🤖✌️"
    ]
}

def check_common_question(query_lower):
    """
    Check if query matches common questions
    Returns (is_common, response_text)
    """
    import random
    
    # Greeting
    if any(w in query_lower for w in ['hi', 'hello', 'halo', 'hai', 'hey']):
        return True, random.choice(COMMON_RESPONSES['greeting'])
    
    # Identity
    if any(w in query_lower for w in ['siapa kamu', 'kamu siapa', 'who are you', 'nama kamu']):
        return True, random.choice(COMMON_RESPONSES['identity'])
    
    # Capability
    if any(w in query_lower for w in ['bisa apa', 'what can you do', 'fungsi']):
        return True, random.choice(COMMON_RESPONSES['capability'])
    
    # Status
    if any(w in query_lower for w in ['apa kabar', 'how are you', 'kabar']):
        return True, random.choice(COMMON_RESPONSES['status'])
    
    # Thanks
    if any(w in query_lower for w in ['thanks', 'makasih', 'terima kasih', 'thx']):
        return True, random.choice(COMMON_RESPONSES['thanks'])
    
    # How to Join Sense
    if any(w in query_lower for w in ['gabung', 'join', 'daftar', 'register', 'cara masuk', 'how to join', 'cara gabung']):
        join_text = """✨ **Gabung ke Sense & Jadi Bagian dari Sense!** ✨

1️⃣ Join Discord Sense
2️⃣ Follow TikTok Sense
3️⃣ Join Group Resmi
4️⃣ Ubah display name kamu jadi Sense/Senz
  Contoh: dipsysense atau dipsysenz

Kamu siap jadi bagian dari kita? 👀🔥"""
        return True, join_text
    
    # Rules
    if any(w in query_lower for w in ['rules', 'rule', 'aturan', 'peraturan', 'regulation', 'guideline']):
        return True, RULES_TEXT
    
    # Registration Status (open member?) - DYNAMIC DETECTION
    registration_keywords = [
        ('open', 'member'),
        ('buka', 'member'),
        ('udah', 'open'),
        ('kapan', 'open'),
        ('kapan', 'buka'),
        ('member', 'dibuka'),
        ('registrasi', 'buka'),
        ('registration', 'open')
    ]
    if any(all(k in query_lower for k in combo) for combo in registration_keywords):
        # Use dynamic detection from chat history
        from handlers.registration_detector import get_registration_sentiment
        
        status = get_registration_sentiment(days=7, min_threshold=5)
        
        if status == 'OPEN':
            return True, random.choice(COMMON_RESPONSES['registration_status_open'])
        elif status == 'CLOSE':
            return True, random.choice(COMMON_RESPONSES['registration_status_close'])
        else:  # DEFAULT
            return True, random.choice(COMMON_RESPONSES['registration_status_default'])
    
    # Crowd Status (rame gak?)
    crowd_keywords = [
        ('rame', 'gak'),
        ('sepi', 'gak'),
        ('lagi', 'rame'),
        ('lagi', 'sepi'),
        ('server', 'sepi'),
        ('server', 'rame'),
        ('ada', 'orang'),
        ('pada', 'kemana')
    ]
    if any(all(k in query_lower for k in combo) for combo in crowd_keywords):
        from handlers.registration_detector import get_chat_activity
        status = get_chat_activity(minutes=15)
        
        if status == 'HIGH':
            return True, random.choice(COMMON_RESPONSES['crowd_status_high'])
        elif status == 'MEDIUM':
            return True, random.choice(COMMON_RESPONSES['crowd_status_medium'])
        else:
            return True, random.choice(COMMON_RESPONSES['crowd_status_low'])
            

            
    # Fun: Siapa paling ganteng/cantik?
    fun_keywords = [
        ('siapa', 'ganteng'),
        ('siapa', 'cantik'),
        ('siapa', 'paling', 'kece'),
        ('siapa', 'cakep'),
        ('orang', 'ganteng'),
        ('orang', 'cantik')
    ]
    if any(all(k in query_lower for k in combo) for combo in fun_keywords):
        return True, random.choice(COMMON_RESPONSES['fun_handsome'])

    return False, None
