from datetime import datetime

from peek_plugin_chat._private.PluginNames import chatTuplePrefix
from vortex.Tuple import addTupleType, TupleField
from vortex.TupleAction import TupleActionABC


@addTupleType
class ChatReadActionTuple(TupleActionABC):
    __tupleType__ = chatTuplePrefix + "ChatReadActionTuple"

    chatUserId = TupleField(typingType=int)
    readDateTime = TupleField(typingType=datetime)
