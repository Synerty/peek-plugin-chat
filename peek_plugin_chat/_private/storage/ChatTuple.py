from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime, Boolean

from peek_plugin_chat._private.PluginNames import chatTuplePrefix
from peek_plugin_chat._private.storage.DeclarativeBase import DeclarativeBase
from vortex.Tuple import Tuple, addTupleType, TupleField


@addTupleType
class ChatTuple(Tuple, DeclarativeBase):
    __tupleType__ = chatTuplePrefix + 'ChatTuple'
    __tablename__ = 'ChatTuple'

    # This will include the users relationship when serialising the data
    __fieldNames__ = ["users"]

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Message details
    hasUnreads = Column(Boolean, nullable=False)
    lastActivity = Column(DateTime, nullable=False)

    # Use a TupleField instead of a relationship so we can decide when it will
    # include the messages or not.
    messages = TupleField()  # relationship("Message.chatId")

    users = relationship("ChatUserTuple", lazy='joined')
