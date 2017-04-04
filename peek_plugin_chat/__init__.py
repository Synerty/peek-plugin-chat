__version__ = '0.0.1'


from peek_plugin_base.server.PluginServerEntryHookABC import PluginServerEntryHookABC
from typing import Type


def peekServerEntryHook() -> Type[PluginServerEntryHookABC]:
    from ._private.server.ServerEntryHook import ServerEntryHook
    return ServerEntryHook
