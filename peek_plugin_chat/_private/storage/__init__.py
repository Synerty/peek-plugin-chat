def loadStorageTuples():
    """ Load Storage Tables

    This method should be called from the "load()" method of the agent, server, worker
    and client entry hook classes.

    This will register the ORM classes as tuples, allowing them to be serialised and
    deserialized by the vortex.

    """

    from . import StringIntTuple
    StringIntTuple.__unused = False

    from . import Setting
    Setting.__unused = False