from app import crud
from app.schemas import UserCreate, MessageCreate
from app.models import Conversation


def test_create_user(db):
    user = UserCreate(
        username="testuser", email="test@example.com", password="testpass"
    )
    db_user = crud.create_user(db, user)
    assert db_user.username == "testuser"
    assert db_user.email == "test@example.com"


def test_get_user(db):
    user = UserCreate(
        username="testuser", email="test@example.com", password="testpass"
    )
    db_user = crud.create_user(db, user)

    fetched_user = crud.get_user(db, db_user.id)
    assert fetched_user.id == db_user.id
    assert fetched_user.username == "testuser"


def test_create_message(db):
    user = UserCreate(
        username="testuser", email="test@example.com", password="testpass"
    )
    db_user = crud.create_user(db, user)

    conversation = Conversation()
    db.add(conversation)
    db.commit()

    message = MessageCreate(content="Test message")
    db_message = crud.create_message(db, message, db_user.id, conversation.id)

    assert db_message.content == "Test message"
    assert db_message.sender_id == db_user.id
    assert db_message.conversation_id == conversation.id


def test_get_conversation_messages(db):
    user = UserCreate(
        username="testuser", email="test@example.com", password="testpass"
    )
    db_user = crud.create_user(db, user)

    conversation = Conversation()
    db.add(conversation)
    db.commit()

    message1 = MessageCreate(content="Test message 1")
    message2 = MessageCreate(content="Test message 2")
    crud.create_message(db, message1, db_user.id, conversation.id)
    crud.create_message(db, message2, db_user.id, conversation.id)

    messages = crud.get_conversation_messages(db, conversation.id)
    assert len(messages) == 2
    assert messages[0].content == "Test message 1"
    assert messages[1].content == "Test message 2"
