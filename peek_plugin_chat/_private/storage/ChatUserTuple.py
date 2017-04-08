from sqlalchemy import Column
from sqlalchemy import Integer, String, Index
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean

from peek_plugin_chat._private.PluginNames import chatTuplePrefix
from peek_plugin_chat._private.storage.ChatTuple import ChatTuple
from peek_plugin_chat._private.storage.DeclarativeBase import DeclarativeBase
from vortex.Tuple import Tuple, addTupleType, TupleField


@addTupleType
class ChatUserTuple(Tuple, DeclarativeBase):
    __tupleType__ = chatTuplePrefix + 'ChatUserTuple'
    __tablename__ = 'ChatUserTuple'

    id = Column(Integer, primary_key=True, autoincrement=True)

    #: Foreign key to a chat
    chatId = Column(Integer,
                    ForeignKey(ChatTuple.id, ondelete="CASCADE"),
                    nullable=False)

    #: The userId of a user in the chat
    userId = Column(String(2000), nullable=False)
    isUserExternal = Column(Boolean, nullable=False)

    #:  User Name, to be populated before sending to the UI
    userName = TupleField(defaultValue="Unknown")

    __table_args__ = (
        Index("idx_ChatUser_userId", userId, unique=False),
        Index("idx_ChatUser_chatId", chatId, unique=False),
    )
