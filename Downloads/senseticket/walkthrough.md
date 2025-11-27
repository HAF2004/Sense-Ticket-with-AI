# Deployment Guide: Monitoring & Clustering

I have implemented the monitoring system, K-Means clustering analysis, and the web dashboard.

## 1. Install Dependencies
You need to install the new libraries on your server (and locally if testing).
```bash
pip install -r requirements.txt
```
This will install `flask`, `pandas`, and `scikit-learn`.

## 2. Database Setup
The database `bot_data.db` will be automatically created when you run the bot or the web app for the first time.

## 3. Running the Bot
Run your bot as usual. It will now log every message and button click to the database.
```bash
python bot.py
```

## 4. Web Dashboard (Arenhost / cPanel)
I have configured `passenger_wsgi.py` to serve the new Flask dashboard.
- **If your domain points to this folder**: The dashboard should appear at your main URL (e.g., `cafie.my.id`).
- **If you want to keep your existing frontend**: You might need to configure cPanel to serve this Python app on a subdomain (e.g., `monitor.cafie.my.id`) or a specific route, OR move your existing frontend files into the `templates` folder and integrate them into `app.py`.

### Local Testing
To test the dashboard on your computer:
```bash
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

## Features
- **Dashboard**: Shows total stats and recent activity.
- **Clustering**: Groups users into clusters based on their chat topics (Toxic, Help, Confused) and activity level.
- **Visuals**: Uses Chart.js to display cluster distribution.

## 5. Voice Join Fix
I have fixed the `voice_join` module.
- **Functionality**: When the user with ID `461869476393123842` tags the bot, the bot will join their voice channel.
- **Usage**:
    1. Join a voice channel.
    2. Tag the bot (e.g., `@SenseBot`).
    3. The bot should join your channel and reply.
- **Note**: This feature is restricted to the specific user ID configured in `core/config.py`.

## 6. Admin Commands
I have added an admin module for managing the bot.
- **Shutdown**: `!shutdown` (or `!turnoff`, `!stopbot`)
    - **Usage**: Only the configured special user can use this command to safely shut down the bot.
    - **Response**: The bot will say goodbye and terminate the process.
