"""User model for Discord expense tracking.

Represents a Discord user who can participate in expense groups
and track shared expenses.
"""
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, TYPE_CHECKING
from database import Base

# Avoid circular imports
if TYPE_CHECKING:
    from models.expense import Expense
    from models.expense_split import ExpenseSplit
    from models.group_member import GroupMember
    from models.group import Group


class User(Base):
    """Database model for Discord users.
    
    Stores user information and provides relationships to expenses,
    group memberships, and payment history.
    
    Attributes:
        id: Primary key for database operations
        discord_id: Unique Discord user ID (64-bit integer)
        username: Display name from Discord
        created_at: Timestamp when user was first registered
    """
    __tablename__ = "users"
    
    # Primary key for internal database operations
    id = Column(Integer, primary_key=True, index=True)
    
    # Discord user ID (unique 64-bit identifier from Discord API)
    discord_id = Column(BigInteger, unique=True, nullable=False, index=True)
    
    # User's display name from Discord
    username = Column(String(255), nullable=False)
    
    # Timestamp when user first registered with the bot
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships to other models
    # Expenses that this user has paid for
    paid_expenses: List['Expense'] = relationship("Expense", back_populates="payer")
    
    # Individual expense splits that this user owes or is owed
    expense_splits: List['ExpenseSplit'] = relationship("ExpenseSplit", back_populates="user")
    
    # Groups that this user is a member of
    group_memberships: List['GroupMember'] = relationship("GroupMember", back_populates="user")
    
    # Groups that this user has created
    created_groups: List['Group'] = relationship("Group", back_populates="creator")
    
    def __repr__(self) -> str:
        """String representation of User for debugging.
        
        Returns:
            str: Formatted string with key user identifiers
        """
        return f"<User(id={self.id}, discord_id={self.discord_id}, username='{self.username}')>"