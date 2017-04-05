from vortex.Tuple import addTupleType, TupleField
from vortex.TupleAction import TupleActionABC

from peek_plugin_chat._private.PluginNames import chatTuplePrefix


@addTupleType
class SendChatMsgActionTuple(TupleActionABC):
    __tupleType__ = chatTuplePrefix + "SendChatMsgActionTuple"

    stringIntId = TupleField()