from peek_plugin_chat._private.PluginNames import chatTuplePrefix
from vortex.Tuple import addTupleType, TupleField
from vortex.TupleAction import TupleActionABC


@addTupleType
class SendChatMsgActionTuple(TupleActionABC):
    __tupleType__ = chatTuplePrefix + "SendChatMsgActionTuple"

    toUserId = TupleField()
    fromUserId = TupleField()
    message = TupleField()
    priority = TupleField()
