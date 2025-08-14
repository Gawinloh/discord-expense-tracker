"""Discord Expense Tracker Bot

A Discord bot for tracking and splitting expenses among friends,
similar to Splitwise functionality.
"""
import discord
from discord.ext import commands
from typing import Optional
from database import init_db


class SplitBot(commands.Bot):
    """Main Discord bot class for expense tracking functionality.
    
    Inherits from discord.ext.commands.Bot to provide slash command
    support and Discord API integration.
    """
    
    def __init__(self) -> None:
        """Initialize the SplitBot with required intents and settings.
        
        Sets up Discord intents for guild access, message content, and
        initializes the bot with slash command support.
        """
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
        """Event handler called when bot successfully connects to Discord.
        
        Performs startup tasks:
        - Initializes database tables
        - Syncs slash commands with Discord
        - Logs connection status
        """
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
        """Global error handler for legacy text commands.
        
        Note: This handles legacy prefix commands. Slash command errors
        are handled individually in each command implementation.
        
        Args:
            ctx: Command context containing message and channel info
            error: The error that occurred during command execution
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