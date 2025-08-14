"""Discord bot for expense tracking and splitting."""
import discord
from discord.ext import commands
from database import init_db


class SplitBot(commands.Bot):
    """Main bot class with slash command support."""
    
    def __init__(self) -> None:
        """Initialize bot with Discord intents and settings."""
        # Configure Discord intents for bot functionality
        intents = discord.Intents.default()
        intents.guilds = True  # Required for guild/server access
        intents.guild_messages = True  # Required for message handling
        intents.message_content = True  # Required for message content access
        
        # Initialize parent Bot class with slash command support
        super().__init__(
            command_prefix='!',  # Legacy prefix (not used for slash commands)
            intents=intents,
            help_command=None  # Disable default help command
        )
    
    async def on_ready(self) -> None:
        """Handle bot startup: initialize database and sync commands."""
        # Log successful Discord connection
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} guilds')
        
        # Initialize database tables
        try:
            init_db()
            print('✅ Database initialized successfully')
        except Exception as database_error:
            print(f'❌ Database initialization failed: {database_error}')
            # Consider stopping bot if database fails
        
        # Sync slash commands with Discord API
        try:
            synced_commands = await self.tree.sync()
            print(f'✅ Synced {len(synced_commands)} slash command(s)')
        except Exception as sync_error:
            print(f'❌ Failed to sync commands: {sync_error}')
    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """Handle errors for legacy text commands.
        
        Args:
            ctx: Command context
            error: The error that occurred
        """
        # Ignore unknown commands to reduce spam
        if isinstance(error, commands.CommandNotFound):
            return
        
        # Handle specific command errors with user-friendly messages
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument: {error.param}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Invalid argument provided")
        else:
            # Log unexpected errors for debugging
            print(f'🔥 Unhandled command error: {error}')
            await ctx.send("❌ An error occurred while processing the command")