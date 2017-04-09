from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Index
from sqlalchemy.sql.sqltypes import LargeBinary

from peek_plugin_chat._private.PluginNames import chatTuplePrefix
from peek_plugin_chat._private.storage.ChatUserTuple import ChatUserTuple
from peek_plugin_chat._private.storage.DeclarativeBase import DeclarativeBase
from peek_plugin_chat._private.storage.MessageTuple import MessageTuple
from vortex.Tuple import Tuple, addTupleType


@addTupleType
class MessageReadPayloadTuple(Tuple, DeclarativeBase):
    __tupleType__ = chatTuplePrefix + 'MessageReadPayloadTuple'
    __tablename__ = 'MessageReadPayloadTuple'

    id = Column(Integer, primary_key=True, autoincrement=True)

    #: Foreign key to a Message
    messageId = Column(Integer,
                       ForeignKey(MessageTuple.id, ondelete="CASCADE"),
                       nullable=False)

    #: Foreign key to a ChatUser
    chatUserId = Column(Integer,
                        ForeignKey(ChatUserTuple.id, ondelete="CASCADE"),
                        nullable=False)

    onReadPayload = Column(LargeBinary, nullable=False)

    __table_args__ = (
        Index("idx_ChatPayloads", messageId, chatUserId, unique=False),
    )
