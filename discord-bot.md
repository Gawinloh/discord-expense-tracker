# Splitwise-Clone Discord Bot Development Plan

This document provides a comprehensive, step-by-step guide for building a Discord bot that mimics Splitwise functionality. Each step is designed as a standalone prompt that can be copied and pasted into a code-generating AI.

**Prerequisites:** Python 3.8+, Discord Developer Portal bot token, basic understanding of Discord bots.

**Tech Stack:** Python, discord.py, SQLAlchemy, SQLite

---

## Step 1: Project Setup and Environment Configuration

Create the foundational structure for a Discord bot project with the following requirements:

1. Create a `requirements.txt` file with these dependencies:
   - discord.py>=2.3.0
   - SQLAlchemy>=2.0.0
   - python-dotenv>=1.0.0

2. Create a `.env` file template with placeholder for:
   - DISCORD_TOKEN (bot token from Discord Developer Portal)

3. Create a basic project structure with these files:
   - `main.py` (entry point)
   - `bot.py` (main bot class)
   - `config.py` (configuration management)
   - `database.py` (database setup and connection)
   - `models/` directory with `__init__.py`

4. In `config.py`, create a configuration class that loads environment variables using python-dotenv.

5. In `main.py`, create the entry point that imports and runs the bot.

6. In `bot.py`, create a basic Discord bot class that:
   - Inherits from `discord.ext.commands.Bot`
   - Sets up basic intents (guilds, guild_messages, message_content)
   - Has an `on_ready` event that prints bot connection status
   - Includes error handling for basic command errors

7. Create a `.gitignore` file that excludes `.env`, `*.db`, and `__pycache__/`

The bot should be able to connect to Discord but not have any commands yet.

---

## Step 2: Database Models and Schema Design

Create the database models for the expense tracking system using SQLAlchemy ORM:

1. In `database.py`, set up SQLAlchemy with SQLite:
   - Create database engine with SQLite file `splitwise_bot.db`
   - Create session factory
   - Add function to initialize database tables

2. In `models/` directory, create the following model files:

   **`models/user.py`:**
   - User model with fields: id (primary key), discord_id (unique), username, created_at
   - Include relationship to expenses and group memberships

   **`models/group.py`:**
   - Group model with fields: id (primary key), discord_channel_id (unique), name, created_at, created_by_user_id
   - Include relationship to expenses and members

   **`models/expense.py`:**
   - Expense model with fields: id (primary key), group_id (foreign key), paid_by_user_id (foreign key), amount (decimal), description, created_at
   - Include relationships to group, payer, and expense splits

   **`models/expense_split.py`:**
   - ExpenseSplit model with fields: id (primary key), expense_id (foreign key), user_id (foreign key), amount (decimal)
   - This represents how much each user owes for a specific expense

   **`models/group_member.py`:**
   - GroupMember model with fields: id (primary key), group_id (foreign key), user_id (foreign key), joined_at
   - This is the many-to-many relationship table between users and groups

3. In `models/__init__.py`, import all models and create a function to create all tables.

4. Update `bot.py` to initialize the database when the bot starts up.

All models should use appropriate SQLAlchemy column types, constraints, and relationships. Include proper indexing for frequently queried fields like discord_id and discord_channel_id.

---

## Step 3: User Onboarding (`/register` command)

Create a slash command that allows users to register with the bot:

1. Create `commands/` directory with `__init__.py`

2. Create `commands/user_commands.py` with a `/register` command that:
   - Checks if the user is already registered
   - If not registered, creates a new User record with their Discord ID and username
   - Responds with a confirmation message
   - If already registered, responds with a friendly message indicating they're already registered

3. The command should handle database errors gracefully and provide appropriate error messages.

4. Update `bot.py` to load and sync this command with Discord.

5. Add helper functions in `database.py` for:
   - Getting a user by Discord ID
   - Creating a new user

The command should work in any Discord server where the bot is present and should create user records that persist across different groups/channels.

---

## Step 4: Group Management (`/creategroup` command)

Create functionality to initialize a Discord channel as an expense tracking group:

1. In `commands/group_commands.py`, create a `/creategroup` command that:
   - Takes a required parameter: `name` (string, the name of the group)
   - Checks if the current channel is already a group
   - If not, creates a new Group record linked to the current Discord channel
   - Automatically adds the command user as the first group member
   - Responds with a success message and basic instructions

2. Add helper functions in `database.py` for:
   - Getting a group by Discord channel ID
   - Creating a new group
   - Adding a user to a group (creating GroupMember record)

3. Create `commands/member_commands.py` with:
   - `/join` command that allows other users to join an existing group in the current channel
   - `/leave` command that allows users to leave a group
   - `/members` command that lists all members of the current group

4. Update `bot.py` to load these new command files.

5. Add validation to ensure:
   - Only registered users can create or join groups
   - Users can't join a group they're already in
   - Users can't leave a group if they have unsettled debts (for now, just warn them)

The group should be tied to the specific Discord channel where it was created.

---

## Step 5: Expense Logging (`/add` command with Discord Modal)

Create an intuitive expense logging system using Discord's Modal interface:

1. In `commands/expense_commands.py`, create a `/add` command that:
   - Checks if the current channel has an associated group
   - Checks if the user is a member of the group
   - Opens a Discord Modal with the following fields:
     - Description (required, text input, max 100 characters)
     - Amount (required, text input, placeholder: "0.00")
     - Split type (for now, only "equal" - can be a hidden field set to "equal")

2. Create a Modal class called `AddExpenseModal` that:
   - Validates the amount is a positive decimal number
   - Creates an Expense record with the current user as the payer
   - Calculates equal splits among all group members
   - Creates ExpenseSplit records for each group member
   - Sends a confirmation message with expense details and how much each person owes

3. Add helper functions in `database.py` for:
   - Getting all members of a group
   - Creating an expense
   - Creating expense splits in bulk
   - Calculating equal split amounts (handling remainders by distributing extra cents to the first few people)

4. The expense split calculation should:
   - Divide the total amount equally among all group members
   - Handle remainders (cents) by adding them to the first few splits
   - The person who paid gets a negative split (they are owed money)
   - Everyone else gets positive splits (they owe money)

5. Add error handling for:
   - Invalid amount formats
   - Groups with no members
   - Database errors

The modal should provide a clean, user-friendly interface for adding expenses without cluttering the chat.

---

## Step 6: Balance Checking (`/balance` command)

Create a command that shows a user's current debts and credits within a group:

1. In `commands/balance_commands.py`, create a `/balance` command that:
   - Checks if the current channel has an associated group
   - Checks if the user is a member of the group
   - Calculates the user's net balance with each other group member
   - Displays the results in a formatted embed

2. Add helper functions in `database.py` for:
   - Getting all expense splits for a user in a specific group
   - Calculating net balances between users

3. The balance calculation logic should:
   - Sum all expense splits for the user in the group
   - Group the results by the expense payer to show individual balances
   - Show positive amounts as "You owe [User] $X.XX"
   - Show negative amounts as "[User] owes you $X.XX"
   - Calculate and display the total net balance

4. Create a Discord Embed that:
   - Has a title showing the group name and user's balance
   - Lists each individual balance with other group members
   - Shows the overall net balance at the bottom
   - Uses color coding: red for net debt, green for net credit, blue for balanced

5. Handle edge cases:
   - User has no expenses in the group
   - User is perfectly balanced (owes and is owed $0.00)

The command should provide clear, easy-to-read balance information that helps users understand their financial standing in the group.

---

## Step 7: Settling Debts (`/settle` command with Button Confirmation)

Create a debt settlement system with interactive confirmation:

1. In `commands/settle_commands.py`, create a `/settle` command that:
   - Takes a required parameter: `member` (Discord user mention)
   - Takes a required parameter: `amount` (decimal)
   - Checks if both users are in the current group
   - Calculates if the settlement amount is valid (not more than what's owed)
   - Creates an interactive message with buttons for the other party to confirm or deny

2. Create a `SettlementView` class (Discord View) with:
   - "Confirm" button (green)
   - "Deny" button (red)
   - Timeout handling (5 minutes)
   - Only the mentioned user can interact with the buttons

3. When confirmed, the settlement should:
   - Create a new "settlement" expense with negative amount
   - Create appropriate expense splits to balance the debt
   - Update both users' balances
   - Send confirmation message to the channel

4. Add helper functions in `database.py` for:
   - Calculating current debt between two specific users
   - Creating settlement expenses
   - Validating settlement amounts

5. The settlement process should:
   - Show a preview of what the balances will be after settlement
   - Prevent settlements that would put someone into unexpected debt
   - Handle partial settlements (settling less than the full amount owed)
   - Log the settlement as a special type of expense for history tracking

6. Add comprehensive error handling for:
   - Invalid user mentions
   - Invalid amounts
   - Users not in the group
   - Settlement amounts exceeding actual debt
   - Timeout scenarios

The settlement system should ensure both parties agree before processing any debt resolution.

---

## Step 8: Debt Simplification (`/simplify` command)

Create an algorithm to calculate the minimum number of transactions needed to clear all debts in a group:

1. In `commands/simplify_commands.py`, create a `/simplify` command that:
   - Checks if the current channel has an associated group
   - Calculates all net balances between group members
   - Runs a debt simplification algorithm
   - Displays the minimum transactions needed to settle all debts

2. Create a debt simplification algorithm in `utils/debt_simplifier.py`:
   - Calculate net balance for each user (total owed minus total owing)
   - Separate users into creditors (negative balance) and debtors (positive balance)
   - Use a greedy algorithm to match largest debts with largest credits
   - Return a list of optimal transactions

3. The algorithm should:
   - Handle the case where debts don't balance exactly (shouldn't happen with proper expense tracking)
   - Minimize the number of transactions
   - Preserve the total amount owed by each person
   - Return transactions as (debtor, creditor, amount) tuples

4. Create a Discord Embed that:
   - Shows current net balances for all group members
   - Lists the minimum transactions needed
   - Calculates how many fewer transactions this is compared to settling individually
   - Includes a note that these are suggestions and can be settled using the `/settle` command

5. Add helper functions in `database.py` for:
   - Getting net balances for all users in a group
   - Calculating total unsettled debt in a group

6. Handle edge cases:
   - Group with no expenses
   - Group where all debts are already settled
   - Groups with only one or two members

This feature helps groups minimize the number of actual money transfers needed to clear all debts.

---

## Step 9: Expense History (`/history` command)

Create a command to view recent expense activity in a group:

1. In `commands/history_commands.py`, create a `/history` command that:
   - Takes an optional parameter: `limit` (integer, default 10, max 50)
   - Checks if the current channel has an associated group
   - Retrieves the most recent expenses in the group
   - Displays them in a paginated embed format

2. Add helper functions in `database.py` for:
   - Getting recent expenses for a group with user and split information
   - Formatting expense data for display

3. The history display should:
   - Show expenses in reverse chronological order (newest first)
   - For each expense, display: date, description, amount, who paid, and how it was split
   - Include settlement transactions (marked clearly as settlements)
   - Use Discord embeds for clean formatting

4. Create pagination functionality:
   - If more than 10 expenses, add navigation buttons (Previous/Next)
   - Show current page number and total pages
   - Handle cases where there are fewer expenses than requested

5. The expense formatting should:
   - Show relative timestamps ("2 days ago", "1 hour ago")
   - Display amounts in a consistent currency format
   - Clearly distinguish between regular expenses and settlements
   - Show participant information (who was included in the split)

6. Add filtering capabilities (optional enhancement):
   - Filter by date range
   - Filter by specific users
   - Filter by amount ranges

This command helps users track expense activity and verify that all transactions are being recorded correctly.

---

## Step 10: Final Integration and Error Handling

Complete the bot by adding comprehensive error handling, help commands, and final integration:

1. Create `commands/help_commands.py` with:
   - `/help` command that shows all available commands
   - Command-specific help (e.g., `/help register`)
   - Usage examples for each command

2. Add comprehensive error handling in `bot.py`:
   - Global error handler for slash commands
   - Specific handlers for common errors (user not found, database errors, permission errors)
   - User-friendly error messages
   - Logging system for debugging

3. Create `utils/validators.py` with:
   - Input validation functions for amounts, user mentions, etc.
   - Sanitization functions for user inputs
   - Common validation patterns used across commands

4. Add administrative features in `commands/admin_commands.py`:
   - `/groupinfo` command to show group statistics
   - `/export` command to export group data (optional)
   - Debug commands for troubleshooting (only for bot owner)

5. Create proper logging configuration:
   - Log all bot activities to a file
   - Include user actions, errors, and system events
   - Implement log rotation

6. Add configuration for deployment:
   - Environment-specific settings
   - Production-ready database configuration
   - Error reporting and monitoring

7. Update `main.py` with:
   - Proper startup sequence
   - Graceful shutdown handling
   - Signal handling for clean exits

8. Final testing checklist:
   - Test all commands in various scenarios
   - Test error conditions
   - Verify database integrity
   - Test with multiple concurrent users
   - Validate all mathematical calculations

This final step ensures the bot is robust, user-friendly, and ready for production deployment.

---

## Additional Notes

- Each step should be implemented and tested before proceeding to the next
- Database migrations should be handled carefully if schema changes are needed
- Consider rate limiting for commands that perform heavy database operations
- All monetary calculations should use decimal types to avoid floating-point precision issues
- User privacy and data security should be considered throughout development
- The bot should handle Discord API rate limits gracefully
- Consider implementing backup and data export functionality for groups

This plan provides a complete roadmap for building a fully-functional Splitwise-clone Discord bot with all essential features for group expense tracking and debt management.