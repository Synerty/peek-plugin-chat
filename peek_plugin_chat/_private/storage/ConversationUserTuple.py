from sqlalchemy import Column
from sqlalchemy import Integer, String, Index
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean

from peek_plugin_chat._private.PluginNames import chatTuplePrefix
from peek_plugin_chat._private.storage.ConversationTuple import ConversationTuple
from peek_plugin_chat._private.storage.DeclarativeBase import DeclarativeBase
from vortex.Tuple import Tuple, addTupleType, TupleField


@addTupleType
class ConversationUserTuple(Tuple, DeclarativeBase):
    __tupleType__ = chatTuplePrefix + 'ConversationUserTuple'
    __tablename__ = 'ConversationUserTuple'

    id = Column(Integer, primary_key=True, autoincrement=True)

    #: Foreign key to a conversation
    convId = Column(Integer,
                    ForeignKey(ConversationTuple.id, ondelete="CASCADE"),
                    nullable=False)

    #: The userId of a user in the conversation
    userId = Column(String(2000), nullable=False)
    isUserExternal = Column(Boolean, nullable=False)

    #:  User Name, to be populated before sending to the UI
    userName = TupleField(defaultValue="Unknown")

    __table_args__ = (
        Index("idx_ConvUser_userId", userId, unique=False),
        Index("idx_ConvUser_convId", convId, unique=False),
    )
