from txhttputil.util.DeferUtil import deferToThreadWrap
from typing import Union

from twisted.internet.defer import Deferred

from vortex.Payload import Payload
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC

from peek_plugin_chat._private.storage.ChatMsgTuple import ChatMsgTuple


class ChatMsgTupleProvider(TuplesProviderABC):
    def __init__(self, ormSessionCreator):
        self._ormSessionCreator = ormSessionCreator

    @deferToThreadWrap
    def makeVortexMsg(self, filt: dict,
                      tupleSelector: TupleSelector) -> Union[Deferred, bytes]:
        # Potential filters can be placed here.
        userId = tupleSelector.selector["userId"]

        session = self._ormSessionCreator()
        try:
            tasks = (session.query(ChatMsgTuple)
                .filter(ChatMsgTuple.userId == userId)
                .all()
            )

            # Create the vortex message
            msg = Payload(filt, tuples=tasks).toVortexMsg()

        finally:
            session.close()

        return msg