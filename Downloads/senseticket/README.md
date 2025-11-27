# 🤖 SENSE Bot v2

**Production-ready Discord bot with Cogs architecture, AI learning, and dashboard control panel.**

## ✨ Features

### 🎯 Core Features
- ✅ **Modular Cogs Architecture** - Easy to maintain and extend
- ✅ **Anti-Duplicate Messaging** - Efficient storage with UNIQUE constraints
- ✅ **AI Chat with Filtering** - Smart out-of-context detection
- ✅ **Dashboard Control Panel** - Real-time monitoring and control
- ✅ **Channel-Specific AI** - Toggle AI per channel
- ✅ **Feedback Tracking** - Learn from user reactions

### 🎫 Ticketing System
- Auto-greet new tickets
- FAQ menu (Registration, Rules, Tutorial)
- Role request with Bloxlink auto-validation
- Live chat support

### 🤖 AI Features
- Learns from all member conversations
- Natural SimSimi-style responses
- Hard-coded rules for important info
- Out-of-context filtering (spam, links, short messages)
- Keyword relevance checking

### 📊 Dashboard
- Real-time bot status
- Statistics (messages, AI responses, unique users)
- AI conversation logs with feedback
- User clustering analysis
- Infinite scroll conversations
- Control panel API

## 🚀 Quick Start

See [QUICKSTART.md](QUICKSTART.md) for 5-minute deployment guide.

## 📁 Project Structure

```
sense/
├── core/              # Bot core
├── models/            # Database models
├── modules/           # Cogs (modular features)
├── handlers/          # UI components
├── migrations/        # Database migrations
├── utils/             # Maintenance tools
├── templates/         # Dashboard HTML
├── run.py             # Main entry point
└── app_v2.py          # Dashboard server
```

## 🔧 Installation

### Requirements
- Python 3.10+
- Discord Bot Token
- cPanel with Python App support

### Dependencies
```bash
pip install -r requirements.txt
```

Main packages:
- `discord.py` / `py-cord` - Discord API
- `sqlalchemy` - Database ORM
- `flask` - Web dashboard
- `scikit-learn` - AI analysis
- `pandas` - Data processing

## 📖 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick deployment guide
- [DEPLOY_V2.md](DEPLOY_V2.md) - Complete deployment guide
- [Implementation Plan](implementation_plan.md) - Technical specification

## 🧪 Testing

Run system tests:
```bash
python test_system.py
```

## 🛠️ Maintenance

View statistics:
```bash
python utils/maintenance.py stats
```

Cleanup old data:
```bash
python utils/maintenance.py cleanup 90
```

Export conversations:
```bash
python utils/maintenance.py export conversations.csv
```

## 🎯 Configuration

Edit `.env` file:
```env
DISCORD_BOT_TOKEN=your_token_here
DATABASE_URL=sqlite:///bot_data_v2.db
FLASK_SECRET_KEY=your_secret_key
```

Edit `core/config.py` for:
- Role IDs
- Channel IDs
- AI thresholds
- System prompts

## 📡 API Endpoints

### Statistics
```
GET /api/discord/stats
```

### AI Logs
```
GET /api/discord/ai/logs?page=1&per_page=20
```

### Toggle AI
```
POST /api/discord/control/toggle
{
  "channel_id": "123456789",
  "enabled": true,
  "ai_mode": "mention_only"
}
```

### Flush Cache
```
POST /api/discord/control/flush
```

## 🔒 Security

- Bot token in `.env` (never commit)
- Database credentials secured
- API endpoints can be protected with auth
- Channel permissions enforced

## 🤝 Contributing

This is a private bot for SENSE Community.

## 📝 License

Private - SENSE Community

## 🆘 Support

For issues or questions, contact SENSE Community staff.

## 🎉 Credits

Built with ❤️ for SENSE Community

---

**Version:** 2.0.0  
**Last Updated:** 2025-11-27  
**Status:** Production Ready 🚀
