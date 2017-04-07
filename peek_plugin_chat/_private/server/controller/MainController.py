import logging
from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from twisted.internet.defer import inlineCallbacks
from twisted.internet.task import LoopingCall
from txhttputil.util.DeferUtil import deferToThreadWrap

from peek_plugin_active_task.server.ActiveTaskApiABC import ActiveTaskApiABC
from peek_plugin_chat._private.tuples.SendChatMsgActionTuple import SendChatMsgActionTuple
from peek_plugin_chat.server.ChatApiABC import SendMessage
from vortex.DeferUtil import vortexLogFailure, deferToThreadWrapWithLogger
from vortex.TupleAction import TupleGenericAction, TupleActionABC
from vortex.TupleSelector import TupleSelector
from vortex.VortexFactory import VortexFactory
from vortex.handler.TupleActionProcessor import TupleActionProcessorDelegateABC
from vortex.handler.TupleDataObservableHandler import TupleDataObservableHandler

from peek_plugin_active_task._private.server.EmailUtil import SendEmail
from peek_plugin_active_task._private.storage import Setting
from peek_plugin_active_task._private.storage.Activity import Activity
from peek_plugin_active_task._private.storage.Setting import globalSetting
from peek_plugin_active_task._private.storage.Task import Task
from peek_plugin_active_task._private.storage.TaskAction import TaskAction
from peek_plugin_user.server.UserDbServerApiABC import UserDbServerApiABC

logger = logging.getLogger(__name__)


class MainController(TupleActionProcessorDelegateABC):
    PROCESS_PERIOD = 5.0

    def __init__(self, dbSessionCreator,
                 userPluginApi: UserDbServerApiABC,
                 activeTaskPluginApi: ActiveTaskApiABC,
                 tupleObservable: TupleDataObservableHandler):
        self._ormSessionCreator = dbSessionCreator
        self._userPluginApi = userPluginApi
        self._activeTaskPluginApi = activeTaskPluginApi
        self._tupleObserver = tupleObservable

        self._processLoopingCall = LoopingCall(self._deleteOnDateTime)

    def start(self):
        d = self._processLoopingCall.start(self.PROCESS_PERIOD, now=False)
        d.addErrback(vortexLogFailure, logger)

    def shutdown(self):
        self._processLoopingCall.stop()

    def _notifyOfUpdates(self, userId: str) -> None:
        self._tupleObserver.notifyOfTupleUpdate(
            TupleSelector(tupleName, {"userId": userId})
        )

    def processTupleAction(self, tupleAction: TupleActionABC):
        if isinstance(tupleAction, SendChatMsgActionTuple):
            return self._processSendMessageAction(tupleAction)

        raise Exception("Unhandled tuple action %s" % tupleAction.tupleType())

    @deferToThreadWrapWithLogger(logger)
    def externalMessageQueued(self, toUserId:str):
        """ External Message Sent
        
        This method is used to notify the main controller when a new message has
        been queued from an external system.
        """

    @deferToThreadWrapWithLogger(logger)
    def _processSendMessageAction(self, tupleAction: SendChatMsgActionTuple):
        """ Process Task Update
        
        Process updates to the task from the UI.
        
        """
        '''
        taskId = tupleAction.data["id"]
        session = self._ormSessionCreator()
        try:
            task = session.query(Task).filter(Task.id == taskId).one()
            userId = task.userId
            wasDelivered = task.stateFlags & Task.STATE_DELIVERED
            wasCompleted = task.stateFlags & Task.STATE_COMPLETED

            if tupleAction.data.get("stateFlags") is not None:
                newFlags = tupleAction.data["stateFlags"]
                task.stateFlags = (task.stateFlags | newFlags)

            if tupleAction.data.get("notificationSentFlags") is not None:
                mask = tupleAction.data["notificationSentFlags"]
                task.notificationSentFlags = (task.notificationSentFlags | mask)

            if task.autoComplete & task.stateFlags:
                task.stateFlags = (task.stateFlags | Task.STATE_COMPLETED)

            autoDelete = task.autoDelete
            stateFlags = task.stateFlags
            onDeletedPayload = task.onDeletedPayload

            # Commit the updates.
            session.commit()

            newDelivery = not wasDelivered and (newFlags & Task.STATE_DELIVERED)
            if newDelivery and task.onDeliveredPayload:
                VortexFactory.sendVortexMsgLocally(task.onDeliveredPayload)

            newCompleted = not wasCompleted and (newFlags & Task.STATE_COMPLETED)
            if newCompleted and task.onCompletedPayload:
                VortexFactory.sendVortexMsgLocally(task.onCompletedPayload)

            if autoDelete & stateFlags:
                (session.query(Task)
                 .filter(Task.id == taskId)
                 .delete(synchronize_session=False))
                session.commit()

                if onDeletedPayload:
                    VortexFactory.sendVortexMsgLocally(onDeletedPayload)

            self._notifyObserver(Task.tupleName(), userId)

        except NoResultFound:
            logger.debug("_processTaskUpdate Task %s has already been deleted" % taskId)

        finally:
            session.close()
        '''

    # -------------------------------------------------------
    # Delete Old Messages
    # -------------------------------------------------------
    @deferToThreadWrapWithLogger(logger)
    def _deleteOnDateTime(self):
        session = self._ormSessionCreator()
        usersToNotify = set()

        try:
            activitiesToExpire = (
                session
                    .query(Activity)
                    .filter(Activity.autoDeleteDateTime < datetime.utcnow())
            )

            for activity in activitiesToExpire:
                usersToNotify.add(activity.userId)
                session.delete(activity)

            tasksToExpire = (
                session
                    .query(Task)
                    .filter(Task.autoDeleteDateTime < datetime.utcnow())
            )

            for task in tasksToExpire:
                usersToNotify.add(task.userId)
                session.delete(task)

            session.commit()

        finally:
            session.close()

        for userId in usersToNotify:
            self._notifyObserver(Activity.tupleName(), userId)

