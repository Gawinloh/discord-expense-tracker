from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from database import Base

class ExpenseSplit(Base):
    __tablename__ = "expense_splits"
    
    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)  # Positive = owes money, Negative = is owed money
    
    # Relationships
    expense = relationship("Expense", back_populates="splits")
    user = relationship("User", back_populates="expense_splits")
    
    def __repr__(self):
        return f"<ExpenseSplit(id={self.id}, expense_id={self.expense_id}, user_id={self.user_id}, amount={self.amount})>"