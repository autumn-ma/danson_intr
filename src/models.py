from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    title = Column(String, index=True)
    grade = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    chat_log_id = Column(Integer)
    rating = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
