from peek_plugin_chat._private.PluginNames import chatFilt
from peek_plugin_chat._private.PluginNames import chatObservableName
from peek_plugin_chat._private.server.tuple_providers.ConversationTupleProvider import \
    ConversationTupleProvider
from peek_plugin_chat._private.storage.ConversationTuple import ConversationTuple
from vortex.handler.TupleDataObservableHandler import TupleDataObservableHandler


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
    tupleObservable.addTupleProvider(ConversationTuple.tupleName(),
                                     ConversationTupleProvider(ormSessionCreator))

    return tupleObservable
