import discord
from discord import app_commands
from discord.ext import commands
from database import get_user_by_discord_id, create_user

class UserCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="register", description="Register with the expense tracking bot")
    async def register(self, interaction: discord.Interaction):
        """Register a new user with the bot"""
        try:
            # Get user information
            discord_id = interaction.user.id
            username = interaction.user.display_name
            
            # Check if user is already registered
            existing_user = get_user_by_discord_id(discord_id)
            if existing_user:
                embed = discord.Embed(
                    title="Already Registered! 👋",
                    description=f"You're already registered as **{existing_user.username}**",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="What's Next?",
                    value="You can now create groups with `/creategroup` or join existing ones!",
                    inline=False
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # Create new user
            new_user = create_user(discord_id=discord_id, username=username)
            
            # Send success message
            embed = discord.Embed(
                title="Welcome to Expense Tracker! 🎉",
                description=f"Successfully registered **{new_user.username}**",
                color=discord.Color.green()
            )
            embed.add_field(
                name="User ID",
                value=f"`{new_user.id}`",
                inline=True
            )
            embed.add_field(
                name="Registration Date",
                value=f"<t:{int(new_user.created_at.timestamp())}:F>",
                inline=True
            )
            embed.add_field(
                name="Next Steps",
                value="• Use `/creategroup` to start a new expense group\n• Wait for someone to create a group and join it",
                inline=False
            )
            embed.set_footer(text="You can now track expenses with friends!")
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            # Handle errors gracefully
            embed = discord.Embed(
                title="Registration Failed ❌",
                description="An error occurred while registering your account.",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Error Details",
                value=f"```{str(e)[:1000]}```",
                inline=False
            )
            embed.set_footer(text="Please try again or contact support if the issue persists.")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(f"Registration error for user {interaction.user.id}: {e}")

async def setup(bot):
    await bot.add_cog(UserCommands(bot))