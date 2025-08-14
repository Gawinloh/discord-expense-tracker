from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False, index=True)
    paid_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    group = relationship("Group", back_populates="expenses")
    payer = relationship("User", back_populates="paid_expenses")
    splits = relationship("ExpenseSplit", back_populates="expense", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Expense(id={self.id}, amount={self.amount}, description='{self.description}')>"