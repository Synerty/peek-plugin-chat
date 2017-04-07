from twisted.internet.defer import Deferred
from txhttputil.util.DeferUtil import deferToThreadWrap
from typing import Union

from peek_plugin_chat._private.storage.ConversationTuple import ConversationTuple
from peek_plugin_chat._private.storage.ConversationUserTuple import ConversationUserTuple
from peek_plugin_chat._private.storage.MessageTuple import MessageTuple
from vortex.Payload import Payload
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC


class ConversationTupleProvider(TuplesProviderABC):
    def __init__(self, ormSessionCreator):
        self._ormSessionCreator = ormSessionCreator

    @deferToThreadWrap
    def makeVortexMsg(self, filt: dict,
                      tupleSelector: TupleSelector) -> Union[Deferred, bytes]:

        # Potential filters can be placed here.
        convId = tupleSelector.selector.get("convId")

        # Potential filters can be placed here.
        userId = tupleSelector.selector.get("userId")

        session = self._ormSessionCreator()
        try:
            convs = []
            # If one conversation id has been specified, then just query for one and
            # it's messages.
            if convId is not None:
                conv = (session.query(ConversationTuple)
                        .filter(ConversationTuple.id == convId)
                        .all())

                if conv:
                    conv = conv[0]
                    conv.messages = (session.query(MessageTuple)
                                     .filter(MessageTuple.convId == convId)
                                     .order_by(MessageTuple.dateTime)
                                     .all())

                    convs = [conv]

            # Else the UI is after a list of conversations for this user
            else:

                convs = (session.query(ConversationTuple)
                         .join(ConversationUserTuple, ConversationUserTuple.convId == ConversationTuple.id)
                         .filter(ConversationUserTuple.id == convId)
                         .order_by(ConversationTuple.lastActivity)
                         .all())

            # Create the vortex message
            msg = Payload(filt, tuples=convs).toVortexMsg()

        finally:
            session.close()

        return msg
