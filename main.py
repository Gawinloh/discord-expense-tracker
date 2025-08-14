import asyncio
from bot import SplitBot
from config import Config

async def main():
    try:
        print("Starting bot...")
        Config.validate()
        print("Config validated successfully")
        bot = SplitBot()
        print("Bot instance created")
        await bot.start(Config.DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Error running bot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())