from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    paid_expenses = relationship("Expense", back_populates="payer")
    expense_splits = relationship("ExpenseSplit", back_populates="user")
    group_memberships = relationship("GroupMember", back_populates="user")
    created_groups = relationship("Group", back_populates="creator")
    
    def __repr__(self):
        return f"<User(id={self.id}, discord_id={self.discord_id}, username='{self.username}')>"