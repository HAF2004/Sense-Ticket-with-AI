# 🚀 SENSE Bot - Deployment Guide

## 📁 File Structure

```
sense/
├── run.py                    # Entry point for bot
├── app.py                    # Flask dashboard (V2)
├── analysis.py               # AI learning & clustering
├── passenger_wsgi.py         # cPanel integration
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── core/                     # Core system
│   ├── bot.py                # Main bot class
│   └── config.py             # Configuration
├── models/                   # Database models
│   └── database.py           # SQLAlchemy setup
├── modules/                  # Bot Features (Cogs)
│   ├── ai_chat.py            # AI Logic
│   ├── ticketing.py          # Ticket System
│   └── ...
├── handlers/                 # Logic Handlers
│   ├── responses.py          # AI Persona & Responses
│   └── ...
└── templates/
    └── dashboard_v2.html     # Dashboard UI
```

## ✅ Features Checklist

### Bot Features:
- [x] **Ticketing System** - Auto-greet, FAQ, Registration, Role Request
- [x] **Roblox Verification** - Auto-validate via Bloxlink
- [x] **Voice Join** - User 461869476393123842 can trigger voice join
- [x] **AI Learning** - Learns from ALL conversations (Smart Caching)
- [x] **Natural Responses** - "Gw/Lu" slang style, cheerful personality
- [x] **Dashboard Integration** - Heartbeat every 60s
- [x] **DeepSeek AI** - Powered by DeepSeek R1 via OpenRouter

### Dashboard Features:
- [x] **Real-time Bot Status** - Online/Offline indicator
- [x] **Statistics** - Total conversations, actions, unique users
- [x] **Clustering Analysis** - K-Means user behavior grouping
- [x] **Infinite Scroll** - Loads conversations dynamically
- [x] **Control Panel** - Toggle AI per channel

## 🔧 Installation Steps

### 1. Create Folder
```bash
mkdir ~/sense
cd ~/sense
```

### 2. Upload Files
Upload ALL files via cPanel File Manager. Ensure the folder structure matches the one above.

### 3. Create .env File
```bash
cd ~/sense
nano .env
```

Content:
```
DISCORD_BOT_TOKEN=your_discord_token
OPENROUTER_API_KEY=your_openrouter_key
FLASK_SECRET_KEY=random_secret_string
```

### 4. Install Dependencies
```bash
source /home/username/virtualenv/sense/3.10/bin/activate
pip install -r requirements.txt
```

### 5. Run Bot (Terminal)
The bot runs separately from the dashboard.
```bash
cd ~/sense
nohup python run.py &
```

### 6. Check Log
```bash
tail -30 nohup.out
```

### 7. Setup Dashboard (cPanel Python App)
1. **Setup Python App** in cPanel
2. **Python version**: 3.10
3. **Application root**: `sense`
4. **Application URL**: `/sense` (or your domain)
5. **Application startup file**: `passenger_wsgi.py`
6. **Application Entry point**: `application`
7. Click **"Create"** or **"Restart"**

## 🎯 Why Modular Architecture?

### Benefits:
- ✅ **Clean Code**: `run.py` is minimal; logic is split into `modules/` and `handlers/`.
- ✅ **Stability**: Editing one feature doesn't break the whole bot.
- ✅ **Database V2**: Uses SQLAlchemy for robust data management (`bot_data_v2.db`).
- ✅ **Smart AI**: Caches successful responses to handle API downtimes.

## 🧠 AI Learning System

### How It Works:
1. **Log Everything** - Bot logs ALL messages to `bot_data_v2.db`.
2. **DeepSeek R1** - Generates smart, contextual answers.
3. **Smart Caching** - Saves good answers. If API is down, reuses them.
4. **Natural Persona** - Uses slang ("gw", "lu", "wkwk") to blend in.

### Learning Process:
```
User: "game apa yang seru?"
Bot (DeepSeek): "Roblox seru banget bang, cobain deh!"
[Bot saves this answer]

... (Later, if API is down) ...
User: "main apa ya yang asik?"
Bot (Cache): "Roblox seru banget bang, cobain deh! 🤖"
```

## 🔄 Updating Bot

### To Update Responses:
```bash
nano ~/sense/handlers/responses.py
# Edit responses
# Save and exit
pkill -f run.py
nohup python run.py &
```

## 🐛 Troubleshooting

### Bot Not Starting:
```bash
cat nohup.out  # Check error log
```

### Dashboard Not Loading:
```bash
# Restart Python App in cPanel
# Check stderr.log
```

### Bot Not Responding:
```bash
# Check Message Content Intent is enabled in Discord Developer Portal
```

## 🎉 Success!

Your SENSE bot is now fully deployed with the latest features! 💚
