# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

White Fox Restaurant Telegram Bot - enables customers to interact with the restaurant via QR code scanning at tables. Features include menu access, waiter/hookah staff calling, bill payment requests, feedback submission, and viewing promotions. Administrators can manage promotional events and broadcast messages.

**Stack:** Python 3.12, pyTelegramBotAPI (telebot), Peewee ORM, SQLite

## Commands

### Development
```bash
pip install -r requirements.txt    # Install dependencies
python main.py                     # Run bot locally
```

### Docker
```bash
docker compose up --build -d       # Build and run
docker compose down                # Stop
```

### Deployment
Push to `main` branch triggers GitHub Actions pipeline that deploys to DigitalOcean.

## Architecture

### Entry Point and Flow
- `main.py` - All Telegram message handlers and callback routing
- Users authenticate by scanning QR codes containing table UUIDs (mapped in `table.json`)
- Session-based: 10-minute timeout after QR scan (`SHUTDOWN_DELEY`)

### Key Modules
- `bot_info.py` - Configuration constants (tokens, delays, external URLs)
- `DB.py` - Peewee models: `User`, `Message` (scheduled broadcasts), `Actions` (promotions)
- `Markup.py` - Telegram keyboard layouts for users and admin interfaces
- `decorators.py` - Rate limiting (`@throttle`), cooldowns (`@colldown_decorator`), session checks (`@start_time`)
- `admin_function_message.py` - Admin CRUD for scheduled/broadcast messages
- `admin_function_action.py` - Admin CRUD for promotions/actions

### Global State (in-memory)
```python
USER = {}         # chat_id -> table number mapping
THROTTLING = {}   # rate limit tracking
CDKEYBORDS = {}   # cooldown tracking
START_TIME = {}   # session start timestamps
```

### Admin Detection
Admins are identified by checking if their Telegram username is in the channel admins list (channel ID in `CHANNEL` env var).

### Data Storage
- SQLite database: `data/database.db`
- User-uploaded photos: `data/photo_folder/` (random 6-char filenames)

## Environment Variables

Required in `.env`:
- `BOT_TOKEN` - Telegram bot API token
- `CHANNEL_TOKEN` - Telegram channel ID for admin detection and notifications

## Rate Limiting

- `THROTTLE_DELEY` (1 sec) - Minimum time between any messages
- `COOLDOWN_DELEY` (1 min) - Cooldown for waiter/hookah calls
- `SHUTDOWN_DELEY` (10 min) - Session timeout after QR scan
