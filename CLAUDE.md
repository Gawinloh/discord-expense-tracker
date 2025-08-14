# CLAUDE.md - Project Development Guidelines

This file contains development rules and conventions for the Discord Expense Tracker Bot project, designed for AI-assisted development with Claude Code.

## Coding Rules and Conventions

### Code Style
- **Comments First**: Every function, class, and complex logic block must have clear comments explaining its purpose
- **Docstrings**: All functions and classes require concise, single-line docstrings following Python standards
- **Keep Docstrings Short**: Prefer `"""Get user by Discord ID."""` over verbose multi-line explanations
- **Variable Names**: Use descriptive names (`discord_user_id` not `uid`, `expense_amount` not `amt`)
- **Function Names**: Use action verbs (`create_user`, `calculate_balance`, `validate_amount`)
- **Constants**: Use UPPER_CASE for constants (`DEFAULT_CURRENCY = "USD"`)

### Code Structure
```python
# Example format for functions
def create_expense(group_id: int, amount: Decimal, description: str, paid_by_user_id: int) -> Expense:
    """Create a new expense record and split it equally among group members."""
    # Implementation here...
    
# For complex functions, use inline comments instead of verbose docstrings
def calculate_complex_balance(user_id: int, group_id: int) -> Decimal:
    """Calculate user's net balance in a group."""
    # Get all expense splits for this user in the group
    user_splits = get_user_splits(user_id, group_id)
    
    # Calculate total owed vs total paid
    total_owed = sum(split.amount for split in user_splits if split.amount > 0)
    total_paid = sum(abs(split.amount) for split in user_splits if split.amount < 0)
    
    return total_paid - total_owed
```

### Error Handling
- Always use try-catch blocks for database operations
- Provide user-friendly error messages in Discord responses
- Log detailed errors for debugging but show simple messages to users
- Never expose database errors or sensitive information to Discord users

### Type Hints
- Use type hints for all function parameters and return values
- Import types: `from typing import Optional, List, Dict, Union`
- Use `Optional[Type]` for nullable values

## Git Conventions

### Branching Strategy
- `main` - Production-ready code only
- `dev` - Development branch for ongoing work
- `feature/feature-name` - Individual features (e.g., `feature/group-management`)
- `fix/issue-description` - Bug fixes (e.g., `fix/balance-calculation`)

### Commit Messages
**Format**: `type: brief description (50 chars max)`

**Types**:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code formatting (no logic changes)
- `refactor:` - Code restructuring
- `test:` - Adding or fixing tests
- `chore:` - Maintenance tasks

**Examples**:
```
feat: add group creation command
fix: handle decimal precision in expense splits
docs: update setup instructions in README
refactor: extract balance calculation logic
```

### Commit Guidelines
- **One feature per commit** - Don't mix unrelated changes
- **Working code only** - Every commit should be functional
- **Small commits** - Easier to review and revert if needed
- **Test before commit** - Ensure bot starts and basic commands work

## Security Guidelines

### Environment Variables
- **Never commit `.env` files** - Use `.env.example` templates instead
- Store sensitive data only in environment variables:
  - `DISCORD_TOKEN` - Bot token
  - `DATABASE_URL` - If using external database
  - `SECRET_KEY` - For any encryption/session management

### Discord Security
- **Validate all user inputs** - Sanitize amounts, descriptions, user mentions
- **Rate limiting** - Don't allow spam of expensive operations
- **Permission checks** - Verify users are in groups before allowing actions
- **Error messages** - Don't leak internal state or database structure

### Database Security
- **Use parameterized queries** - SQLAlchemy ORM prevents SQL injection
- **Validate data types** - Ensure amounts are Decimal, IDs are integers
- **No raw SQL** - Use ORM methods only
- **Database backups** - Consider regular backup strategy for production

## Database Conventions

### Model Design
- **Singular names**: `User`, `Group`, `Expense` (not `Users`, `Groups`)
- **Clear relationships**: Use descriptive foreign key names (`paid_by_user_id` not `user_id`)
- **Timestamps**: Include `created_at` for all models, `updated_at` where relevant
- **Soft deletes**: Consider using `is_deleted` flag instead of hard deletes for important data

### Data Types
- **Money amounts**: Always use `Decimal` type, never `Float`
- **IDs**: Use `Integer` primary keys with auto-increment
- **Discord IDs**: Store as `BigInteger` (Discord IDs are 64-bit)
- **Text fields**: Use appropriate lengths (`VARCHAR(100)` for descriptions)

### Naming Conventions
```python
# Table names: snake_case
class ExpenseSplit(Base):
    __tablename__ = 'expense_splits'
    
    # Column names: snake_case
    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey('expenses.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    split_amount = Column(Decimal(10, 2))  # Always specify precision for money
```

## Discord Bot Conventions

### Command Design
- **Slash commands only** - No text commands (`/register` not `!register`)
- **Clear descriptions** - Help users understand what each command does
- **Parameter validation** - Check inputs before database operations
- **Confirmation for destructive actions** - Use buttons/modals for deletes
- **Ephemeral for errors** - Personal error messages shouldn't clutter chat

### Response Patterns
```python
# Success responses - public by default
await interaction.response.send_message(embed=success_embed)

# Error responses - private (ephemeral)
await interaction.response.send_message(embed=error_embed, ephemeral=True)

# Confirmations - use embeds for better formatting
embed = discord.Embed(title="Success", color=discord.Color.green())
```

### Error Handling Pattern
```python
try:
    # Database operation
    result = create_user(discord_id, username)
    # Success response
    await interaction.response.send_message("Success!")
    
except SpecificError as e:
    # Log detailed error
    logger.error(f"User creation failed: {e}")
    # Send user-friendly message
    await interaction.response.send_message("Registration failed. Please try again.", ephemeral=True)
```

## Testing Guidelines

### Manual Testing Checklist
Before each commit, verify:
- [ ] Bot connects to Discord successfully
- [ ] Database initializes without errors
- [ ] Commands sync properly (`/` commands appear in Discord)
- [ ] New features work as expected
- [ ] Error cases are handled gracefully

### Test Commands
```bash
# Start bot locally
python main.py

# Check database
python -c "from database import init_db; init_db(); print('DB OK')"
```

## Development Workflow

### Starting New Features
1. Create feature branch: `git checkout -b feature/feature-name`
2. Update CLAUDE.md if adding new conventions
3. Implement with comprehensive comments
4. Test locally
5. Commit with clear messages
6. Push and create PR (if working in teams)

### Code Review Checklist
- [ ] Code has adequate comments and docstrings
- [ ] Error handling is comprehensive
- [ ] Database operations use proper types
- [ ] Discord responses are user-friendly
- [ ] No sensitive data is exposed
- [ ] Follows naming conventions

## Project-Specific Rules

### Expense Logic
- **Always use Decimal** for money calculations
- **Round to 2 decimal places** for display
- **Handle remainders** in splits by distributing to first few users
- **Validate positive amounts** before creating expenses

### Group Management
- **One group per Discord channel** - Channel ID is unique identifier
- **Auto-add creator** to group when creating
- **Prevent duplicate joins** - Check membership before adding

### Balance Calculations
- **Real-time calculations** - Don't store running balances, calculate from splits
- **Handle edge cases** - Users with no expenses, perfectly balanced users
- **Color coding** - Red for debt, green for credit, blue for balanced

---

**Remember**: This is an AI-assisted project. Always review generated code and test thoroughly before committing!