from app.models import User, Conversation, Message
from sqlalchemy.orm import Session


def test_user_model(db: Session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpass",
    )
    db.add(user)
    db.commit()

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashedpass"


def test_conversation_model(db: Session):
    conversation = Conversation()
    db.add(conversation)
    db.commit()

    assert conversation.id is not None


def test_message_model(db: Session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpass",
    )
    conversation = Conversation()
    db.add(user)
    db.add(conversation)
    db.commit()

    message = Message(
        content="Test message",
        sender_id=user.id,
        conversation_id=conversation.id,
    )
    db.add(message)
    db.commit()

    assert message.id is not None
    assert message.content == "Test message"
    assert message.sender_id == user.id
    assert message.conversation_id == conversation.id
