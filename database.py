"""Database configuration and utility functions.

Provides SQLAlchemy setup, session management, and CRUD operations
for the Discord Expense Tracker bot.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Optional
from config import Config

# Database engine with SQLite configuration
engine = create_engine(Config.DATABASE_URL, echo=False)

# Session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()

def get_db() -> Session:
    """Create and return a new database session.
    
    Returns:
        Session: SQLAlchemy database session for queries and transactions
        
    Note:
        Caller is responsible for closing the session after use.
    """
    database_session = SessionLocal()
    return database_session

def init_db() -> None:
    """Initialize database by creating all tables.
    
    Imports all model classes to ensure they are registered with
    the Base metadata, then creates all tables in the database.
    
    Raises:
        SQLAlchemyError: If database table creation fails
    """
    # Import all models to register them with Base metadata
    # This ensures all tables are created properly
    from models.user import User
    from models.group import Group  
    from models.expense import Expense
    from models.expense_split import ExpenseSplit
    from models.group_member import GroupMember
    
    # Create all database tables
    Base.metadata.create_all(bind=engine)

def get_user_by_discord_id(discord_id: int) -> Optional['User']:
    """Retrieve a user by their Discord ID.
    
    Args:
        discord_id: The Discord user's unique identifier
        
    Returns:
        Optional[User]: User model instance if found, None otherwise
        
    Note:
        Automatically handles database session cleanup.
    """
    from models.user import User
    database_session = get_db()
    try:
        # Query for user with matching Discord ID
        user = database_session.query(User).filter(User.discord_id == discord_id).first()
        return user
    finally:
        # Always close database session to prevent leaks
        database_session.close()

def create_user(discord_id: int, username: str) -> 'User':
    """Create a new user in the database.
    
    Args:
        discord_id: The Discord user's unique identifier
        username: The user's display name
        
    Returns:
        User: The newly created user model instance
        
    Raises:
        IntegrityError: If discord_id already exists
        SQLAlchemyError: If database operation fails
    """
    from models.user import User
    database_session = get_db()
    try:
        # Create new user instance
        new_user = User(discord_id=discord_id, username=username)
        
        # Add to session and commit to database
        database_session.add(new_user)
        database_session.commit()
        
        # Refresh to get updated fields (like auto-generated ID)
        database_session.refresh(new_user)
        return new_user
    finally:
        # Always close database session
        database_session.close()

def get_group_by_channel_id(channel_id: int) -> Optional['Group']:
    """Retrieve a group by Discord channel ID.
    
    Args:
        channel_id: The Discord channel's unique identifier
        
    Returns:
        Optional[Group]: Group model instance if found, None otherwise
    """
    from models.group import Group
    database_session = get_db()
    try:
        # Query for group with matching Discord channel ID
        group = database_session.query(Group).filter(Group.discord_channel_id == channel_id).first()
        return group
    finally:
        # Always close database session
        database_session.close()

def create_group(channel_id: int, name: str, created_by_user_id: int) -> 'Group':
    """Create a new expense group in the database.
    
    Args:
        channel_id: Discord channel ID where group is created
        name: Human-readable name for the group
        created_by_user_id: Database ID of the user creating the group
        
    Returns:
        Group: The newly created group model instance
        
    Raises:
        IntegrityError: If channel_id already has a group
        SQLAlchemyError: If database operation fails
    """
    from models.group import Group
    database_session = get_db()
    try:
        # Create new group instance
        new_group = Group(
            discord_channel_id=channel_id, 
            name=name, 
            created_by_user_id=created_by_user_id
        )
        
        # Add to session and commit to database
        database_session.add(new_group)
        database_session.commit()
        
        # Refresh to get updated fields
        database_session.refresh(new_group)
        return new_group
    finally:
        # Always close database session
        database_session.close()

def add_user_to_group(user_id: int, group_id: int) -> 'GroupMember':
    """Add a user to an expense group.
    
    Args:
        user_id: Database ID of the user to add
        group_id: Database ID of the group to join
        
    Returns:
        GroupMember: The newly created group membership record
        
    Raises:
        IntegrityError: If user is already a member of the group
        SQLAlchemyError: If database operation fails
    """
    from models.group_member import GroupMember
    database_session = get_db()
    try:
        # Create new group membership record
        new_membership = GroupMember(user_id=user_id, group_id=group_id)
        
        # Add to session and commit to database
        database_session.add(new_membership)
        database_session.commit()
        
        return new_membership
    finally:
        # Always close database session
        database_session.close()