import logging
from copy import copy
from typing import List

from twisted.internet.defer import inlineCallbacks, succeed

from peek_plugin_active_task.server.ActiveTaskApiABC import ActiveTaskApiABC, NewTask
from peek_plugin_chat._private.PluginNames import chatFilt
from peek_plugin_chat._private.storage.ChatTuple import ChatTuple
from peek_plugin_chat._private.storage.MessageTuple import MessageTuple
from vortex.Payload import Payload
from vortex.PayloadEndpoint import PayloadEndpoint

logger = logging.getLogger(__name__)

_deliverdPayloadFilt = {
    "key": "active.task.message.delivered"
}
_deliverdPayloadFilt.update(chatFilt)


class TaskController:
    def __init__(self, activeTaskPluginApi: ActiveTaskApiABC):
        self._activeTaskPluginApi = activeTaskPluginApi

        assert isinstance(self._activeTaskPluginApi, ActiveTaskApiABC), (
            "Expected instance of ActiveTaskServerApiABC, received %s" % self._activeTaskPluginApi)

        self._deliveredEndpoint = PayloadEndpoint(
            _deliverdPayloadFilt, self._processTaskDelivered)

    def shutdown(self):
        self._deliveredEndpoint.shutdown()
        self._deliveredEndpoint = None
        self._soapController = None

    def _makeUniqueId(self, chatId: int, userId: str):
        return "peek_plugin_chat.new_message.%s.%s" % (userId, chatId)

    def _makeTaskTitle(self, message: MessageTuple):
        if message.priority == MessageTuple.PRIORITY_EMERGENCY:
            return "EMERGENCY SOS CHAT MESSAGE FROM %s" % message.fromUserId

        return "You have a new chat message from %s" % message.fromUserId

    def _makeMessagesRoutePath(self, chatTuple: ChatTuple):
        return "/peek_plugin_chat/messages/%s" % chatTuple.id

    def _shouldNotifyBySound(self, message: MessageTuple):
        return (NewTask.NOTIFY_BY_DEVICE_SOUND
                if message.priority == MessageTuple.PRIORITY_EMERGENCY else
                0)

    def _shouldTaskSendSMS(self, message: MessageTuple):
        return (NewTask.NOTIFY_BY_SMS
                if message.priority == MessageTuple.PRIORITY_EMERGENCY else
                0)

    @inlineCallbacks
    def _processTaskDelivered(self, payload, **kwargs):
        logger.debug("_processTaskDelivered called")
        try:
            # msgId = payload.filt["msgId"]
            # userId = payload.filt["userId"]
            # action = payload.filt["action"]
            # jobId = payload.filt["jobId"]

            yield succeed(True)

        except Exception as e:
            logger.exception(e)

    @inlineCallbacks
    def addTask(self, chat: ChatTuple, message: MessageTuple, userIds: List[str]):

        try:
            filt = copy(_deliverdPayloadFilt)
            filt["chatId"] = chat.id
            onDeliverPayload = Payload(filt=filt).toVortexMsg()

            for userId in userIds:
                newTask = NewTask(
                    uniqueId=self._makeUniqueId(chat.id, userId),
                    userId=userId,
                    title=self._makeTaskTitle(message),
                    displayAs=NewTask.DISPLAY_AS_MESSAGE,
                    routePath=self._makeMessagesRoutePath(chat),
                    onDeliveredPayload=onDeliverPayload,
                    autoDelete=NewTask.AUTO_DELETE_ON_SELECT,
                    overwriteExisting=True,
                    notificationRequiredFlags=self._shouldNotifyBySound(message)
                                              | NewTask.NOTIFY_BY_DEVICE_POPUP
                                              | self._shouldTaskSendSMS(message)
                )

                yield self._activeTaskPluginApi.addTask(newTask)


        except Exception as e:
            logger.exception(e)

    @inlineCallbacks
    def removeTask(self, chatId: int, userId: str):
        try:
            yield self._activeTaskPluginApi.removeTask(self._makeUniqueId(chatId, userId))

        except ValueError:
            # This means it didn't exist.
            pass

        except Exception as e:
            logger.exception(e)
