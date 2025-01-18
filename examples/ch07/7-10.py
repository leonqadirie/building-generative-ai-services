# services/conversations.py

from entities import Message
from repositories.conversations import ConversationRepository
from sqlalchemy import select


class ConversationService(ConversationRepository):
    async def list_messages(self, conversation_id: int) -> list[Message]:
        result = await self.session.execute(
            select(Message).where(Message.conversation_id == conversation_id)
        )
        return [m for m in result.scalars().all()]


# routers/conversations.py

from database import get_db_session
from entities import Message
from fastapi import APIRouter
from schemas import MessageOut
from services.conversations import ConversationService
from sqlalchemy.ext.asyncio import AsyncSession

# replace every ConversationRepository(db) instances with ConversationService(db)

router = APIRouter()


@router.get("/conversations/{conversation_id}/messages")
async def list_conversation_messages_controller(
    conversation: GetConversationDep,
    session: AsyncSession = Depends(get_db_session),
) -> list[Message]:
    messages = await ConversationService(session).list_messages(conversation.id)
    return [MessageOut.model_validate(m) for m in messages]
