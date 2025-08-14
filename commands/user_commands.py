"""User management commands for Discord Expense Tracker."""
import discord
from discord import app_commands
from discord.ext import commands
from database import get_user_by_discord_id, create_user


class UserCommands(commands.Cog):
    """Discord cog for user-related slash commands."""
    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the UserCommands cog."""
        self.bot = bot

    @app_commands.command(name="register", description="Register with the expense tracking bot")
    async def register(self, interaction: discord.Interaction) -> None:
        """Register a new user with the expense tracking bot."""
        try:
            # Extract user information from Discord interaction
            discord_user_id = interaction.user.id
            display_username = interaction.user.display_name
            
            # Check if user already has an account in our database
            existing_user = get_user_by_discord_id(discord_user_id)
            # If user already exists, show their current information
            if existing_user:
                already_registered_embed = discord.Embed(
                    title="Already Registered! 👋",
                    description=f"You're already registered as **{existing_user.username}**",
                    color=discord.Color.blue()
                )
                already_registered_embed.add_field(
                    name="What's Next?",
                    value="You can now create groups with `/creategroup` or join existing ones!",
                    inline=False
                )
                # Send as ephemeral (private) message to avoid channel spam
                await interaction.response.send_message(embed=already_registered_embed, ephemeral=True)
                return

            # Create new user account in database
            newly_created_user = create_user(discord_id=discord_user_id, username=display_username)
            
            # Create success message embed
            success_embed = discord.Embed(
                title="Welcome to Expense Tracker! 🎉",
                description=f"Successfully registered **{newly_created_user.username}**",
                color=discord.Color.green()
            )
            # Add user information fields to embed
            success_embed.add_field(
                name="User ID",
                value=f"`{newly_created_user.id}`",
                inline=True
            )
            success_embed.add_field(
                name="Registration Date",
                value=f"<t:{int(newly_created_user.created_at.timestamp())}:F>",
                inline=True
            )
            success_embed.add_field(
                name="Next Steps",
                value="• Use `/creategroup` to start a new expense group\n• Wait for someone to create a group and join it",
                inline=False
            )
            success_embed.set_footer(text="You can now track expenses with friends!")
            
            # Send public success message to announce new member
            await interaction.response.send_message(embed=success_embed)
            
        except Exception as registration_error:
            # Handle database or other errors gracefully with user-friendly message
            error_embed = discord.Embed(
                title="Registration Failed ❌",
                description="An error occurred while registering your account.",
                color=discord.Color.red()
            )
            error_embed.add_field(
                name="Error Details",
                value=f"```{str(registration_error)[:1000]}```",
                inline=False
            )
            error_embed.set_footer(text="Please try again or contact support if the issue persists.")
            
            # Send error as ephemeral message to avoid channel clutter
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            
            # Log detailed error for debugging (server-side only)
            print(f"🔥 Registration error for Discord user {interaction.user.id}: {registration_error}")

async def setup(bot: commands.Bot) -> None:
    """Add the UserCommands cog to the bot."""
    await bot.add_cog(UserCommands(bot))