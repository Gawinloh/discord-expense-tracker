from sqlalchemy import Column, Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    discord_channel_id = Column(BigInteger, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    creator = relationship("User", back_populates="created_groups")
    expenses = relationship("Expense", back_populates="group")
    members = relationship("GroupMember", back_populates="group")
    
    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}', channel_id={self.discord_channel_id})>"