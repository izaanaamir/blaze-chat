from sqlalchemy.orm import Session
from . import models, schemas
from .core.security import get_password_hash, verify_password


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return (
        db.query(models.User).filter(models.User.username == username).first()
    )


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_conversation(db: Session, conversation_id: int):
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.id == conversation_id)
        .first()
    )


def create_conversation(
    db: Session, conversation: schemas.ConversationCreate
):
    db_conversation = models.Conversation()
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)

    for user_id in conversation.participant_ids:
        db_participant = models.Participant(
            user_id=user_id, conversation_id=db_conversation.id
        )
        db.add(db_participant)

    db.commit()
    return db_conversation


def get_user_conversations(db: Session, user_id: int):
    return (
        db.query(models.Conversation)
        .join(models.Participant)
        .filter(models.Participant.user_id == user_id)
        .all()
    )


def create_message(
    db: Session,
    message: schemas.MessageCreate,
    sender_id: int,
    conversation_id: int,
):
    db_message = models.Message(
        **message.dict(), sender_id=sender_id, conversation_id=conversation_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_conversation_messages(
    db: Session, conversation_id: int, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.Message)
        .filter(models.Message.conversation_id == conversation_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
