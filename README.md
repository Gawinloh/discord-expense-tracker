# Discord Expense Tracker Bot

A Discord bot for tracking and splitting expenses among friends, similar to Splitwise. Built as a hobby learning project.

🤖 **This project is entirely written by [Claude Code](https://claude.ai/code)** - Anthropic's AI coding assistant.

## Current Features

- ✅ **User Registration** (`/register`) - Users can sign up with the bot to create their profile

## Planned Features

- 🔄 **Group Management** - Create and manage expense groups in Discord channels
  - `/creategroup` - Initialize a channel as an expense tracking group
  - `/join` - Join an existing group
  - `/leave` - Leave a group
  - `/members` - View group members

- 📝 **Expense Logging** - Track shared expenses
  - `/add` - Add new expenses with automatic splitting
  - Support for equal splits among group members

- 💰 **Balance Tracking** - Monitor debts and credits
  - `/balance` - Check what you owe and what you're owed
  - Real-time balance calculations

- 🤝 **Debt Settlement** - Settle up with friends
  - `/settle` - Record payments between users
  - Interactive confirmation system

- 🎯 **Smart Features**
  - `/simplify` - Calculate minimum transactions to clear all debts
  - `/history` - View expense history
  - Comprehensive error handling and help system

## Development Progress

Currently at **Step 3** of 10 in the development plan:
- ✅ Project setup and database models
- ✅ User registration system
- ⏳ Group management (next up)
- ⏸️ Expense logging, balance tracking, settlement system

## Tech Stack

- **Language:** Python 3.8+
- **Discord Library:** discord.py 2.3+
- **Database:** SQLAlchemy with SQLite
- **Environment:** python-dotenv

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Gawinloh/discord-expense-tracker.git
   cd discord-expense-tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

## License

MIT License - feel free to use this code for your own projects!