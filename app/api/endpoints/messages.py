from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ... import crud, models, schemas
from ..deps import get_current_user, get_db

router = APIRouter()


@router.post("/conversations/", response_model=schemas.Conversation)
def create_conversation(
    conversation: schemas.ConversationCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_conversation(db=db, conversation=conversation)


@router.get("/conversations/", response_model=List[schemas.Conversation])
def read_conversations(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.get_user_conversations(db=db, user_id=current_user.id)


@router.post(
    "/conversations/{conversation_id}/messages/",
    response_model=schemas.Message,
)
def create_message(
    conversation_id: int,
    message: schemas.MessageCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_message(
        db=db,
        message=message,
        sender_id=current_user.id,
        conversation_id=conversation_id,
    )


@router.get(
    "/conversations/{conversation_id}/messages/",
    response_model=List[schemas.Message],
)
def read_conversation_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.get_conversation_messages(
        db=db, conversation_id=conversation_id, skip=skip, limit=limit
    )
