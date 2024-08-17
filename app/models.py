from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), nullable=True, onupdate=func.now()
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    sender_id = Column(Integer, ForeignKey("users.id"))
    conversation_id = Column(Integer, ForeignKey("conversations.id"))

    sender = relationship("User", back_populates="messages")
    conversation = relationship("Conversation", back_populates="messages")


User.messages = relationship("Message", back_populates="sender")
User.conversations = relationship(
    "Conversation", secondary="participants", back_populates="users"
)
Conversation.users = relationship(
    "User", secondary="participants", back_populates="conversations"
)
Conversation.messages = relationship("Message", back_populates="conversation")
