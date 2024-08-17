from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    created_at: datetime
    sender_id: int
    conversation_id: int

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    pass


class ConversationCreate(ConversationBase):
    participant_ids: List[int]


class Conversation(ConversationBase):
    id: int
    created_at: datetime
    users: List[User]
    messages: List[Message]

    class Config:
        from_attributes = True


class MessageUpdate(BaseModel):
    content: str
