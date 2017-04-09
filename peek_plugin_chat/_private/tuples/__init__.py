def loadPrivateTuples():
    """ Load Private Tuples

    In this method, we load the private tuples.
    This registers them so the Vortex can reconstructed them from
    serialised data.

    """
    from . import SendMessageActionTuple
    SendMessageActionTuple.__unused = False

    from . import CreateChatActionTuple
    CreateChatActionTuple.__unused = False

    from . import ChatReadActionTuple
    ChatReadActionTuple.__unused = False
