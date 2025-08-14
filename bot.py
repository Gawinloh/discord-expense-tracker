import discord
from discord.ext import commands
from database import init_db

class SplitBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.guild_messages = True
        intents.message_content = True
        
        super().__init__(
            command_prefix='!',``
            intents=intents,
            help_command=None
        )
    
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} guilds')
        
        try:
            init_db()
            print('Database initialized successfully')
        except Exception as e:
            print(f'Database initialization failed: {e}')
        
        try:
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(f'Failed to sync commands: {e}')
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument provided")
        else:
            print(f'Unhandled error: {error}')
            await ctx.send("An error occurred while processing the command")