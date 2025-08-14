from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import Config

engine = create_engine(Config.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    return db

def init_db():
    # Import models to ensure they're registered with Base
    from models.user import User
    from models.group import Group  
    from models.expense import Expense
    from models.expense_split import ExpenseSplit
    from models.group_member import GroupMember
    Base.metadata.create_all(bind=engine)

def get_user_by_discord_id(discord_id):
    from models.user import User
    db = get_db()
    try:
        return db.query(User).filter(User.discord_id == discord_id).first()
    finally:
        db.close()

def create_user(discord_id, username):
    from models.user import User
    db = get_db()
    try:
        user = User(discord_id=discord_id, username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

def get_group_by_channel_id(channel_id):
    from models.group import Group
    db = get_db()
    try:
        return db.query(Group).filter(Group.discord_channel_id == channel_id).first()
    finally:
        db.close()

def create_group(channel_id, name, created_by_user_id):
    from models.group import Group
    db = get_db()
    try:
        group = Group(discord_channel_id=channel_id, name=name, created_by_user_id=created_by_user_id)
        db.add(group)
        db.commit()
        db.refresh(group)
        return group
    finally:
        db.close()

def add_user_to_group(user_id, group_id):
    from models.group_member import GroupMember
    db = get_db()
    try:
        membership = GroupMember(user_id=user_id, group_id=group_id)
        db.add(membership)
        db.commit()
        return membership
    finally:
        db.close()