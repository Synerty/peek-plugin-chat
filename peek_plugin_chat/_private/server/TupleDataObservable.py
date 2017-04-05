from peek_plugin_chat._private.server.tuple_providers.ChatMsgTupleProvider import \
    ChatMsgTupleProvider
from peek_plugin_chat._private.storage.ChatMsgTuple import ChatMsgTuple
from vortex.handler.TupleDataObservableHandler import TupleDataObservableHandler

from peek_plugin_chat._private.PluginNames import chatFilt
from peek_plugin_chat._private.PluginNames import chatObservableName


def makeTupleDataObservableHandler(ormSessionCreator):
    """" Make Tuple Data Observable Handler

    This method creates the observable object, registers the tuple providers and then
    returns it.

    :param ormSessionCreator: A function that returns a SQLAlchemy session when called

    :return: An instance of :code:`TupleDataObservableHandler`

    """
    tupleObservable = TupleDataObservableHandler(
                observableName=chatObservableName,
                additionalFilt=chatFilt)

    # Register TupleProviders here
    tupleObservable.addTupleProvider(ChatMsgTuple.tupleName(),
                                     ChatMsgTupleProvider(ormSessionCreator))

    return tupleObservable