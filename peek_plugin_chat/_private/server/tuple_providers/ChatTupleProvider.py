from twisted.internet.defer import Deferred
from txhttputil.util.DeferUtil import deferToThreadWrap
from typing import Union

from peek_plugin_chat._private.storage.ChatTuple import ChatTuple
from peek_plugin_chat._private.storage.ChatUserTuple import ChatUserTuple
from peek_plugin_chat._private.storage.MessageTuple import MessageTuple
from vortex.Payload import Payload
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleDataObservableHandler import TuplesProviderABC


class ChatTupleProvider(TuplesProviderABC):
    def __init__(self, ormSessionCreator):
        self._ormSessionCreator = ormSessionCreator

    @deferToThreadWrap
    def makeVortexMsg(self, filt: dict,
                      tupleSelector: TupleSelector) -> Union[Deferred, bytes]:

        # Potential filters can be placed here.
        chatId = tupleSelector.selector.get("chatId")

        # Potential filters can be placed here.
        userId = tupleSelector.selector.get("userId")

        session = self._ormSessionCreator()
        try:
            chats = []
            # If one chat id has been specified, then just query for one and
            # it's messages.
            if chatId is not None:
                chat = (session.query(ChatTuple)
                        .filter(ChatTuple.id == chatId)
                        .all())

                if chat:
                    chat = chat[0]
                    chat.messages = (session.query(MessageTuple)
                                     .filter(MessageTuple.chatId == chatId)
                                     .order_by(MessageTuple.dateTime)
                                     .all())

                    chats = [chat]

            # Else the UI is after a list of chats for this user
            else:

                chats = (session.query(ChatTuple)
                         .join(ChatUserTuple, ChatUserTuple.chatId == ChatTuple.id)
                         .filter(ChatUserTuple.userId == userId)
                         .order_by(ChatTuple.lastActivity)
                         .all())

            # Create the vortex message
            msg = Payload(filt, tuples=chats).toVortexMsg()

        finally:
            session.close()

        return msg
