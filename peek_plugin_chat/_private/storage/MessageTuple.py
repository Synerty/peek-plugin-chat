from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Index
from sqlalchemy.sql.sqltypes import DateTime

from peek_plugin_base.storage.TypeDecorators import PeekVarBinary
from peek_plugin_chat._private.PluginNames import chatTuplePrefix
from peek_plugin_chat._private.storage.ConversationTuple import ConversationTuple
from peek_plugin_chat._private.storage.DeclarativeBase import DeclarativeBase
from vortex.Tuple import Tuple, addTupleType


@addTupleType
class MessageTuple(Tuple, DeclarativeBase):
    __tupleType__ = chatTuplePrefix + 'MessageTuple'
    __tablename__ = 'MessageTuple'

    id = Column(Integer, primary_key=True, autoincrement=True)

    #: Foreign key to a conversation
    convId = Column(Integer,
                    ForeignKey(ConversationTuple.id, ondelete="CASCADE"),
                    nullable=False)

    # Message details
    message = Column(String(2000), nullable=False)
    priority = Column(Integer, nullable=False)

    # User to / from
    fromUserId = Column(String(40), nullable=False)

    # Message state details
    dateTime = Column(DateTime, nullable=False)

    #:  These indicate the message state
    state = Column(Integer, nullable=False)
    STATE_NEW = 1
    STATE_DELIVERED = 2
    STATE_READ = 3

    onReadPayload = Column(PeekVarBinary)

    __table_args__ = (
        Index("idx_ChatMsgTuple_convId", convId, unique=False),
        Index("idx_ChatMsgTuple_dateTime", dateTime, unique=False),
    )