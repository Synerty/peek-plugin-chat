import logging
from datetime import datetime

from twisted.internet.task import LoopingCall

from peek_plugin_active_task._private.storage.Activity import Activity
from peek_plugin_active_task._private.storage.Task import Task
from peek_plugin_active_task.server.ActiveTaskApiABC import ActiveTaskApiABC
from peek_plugin_chat._private.storage.ChatTuple import ChatTuple
from peek_plugin_chat._private.storage.ChatUserTuple import ChatUserTuple
from peek_plugin_chat._private.storage.MessageTuple import MessageTuple
from peek_plugin_chat._private.tuples.CreateChatActionTuple import CreateChatActionTuple
from peek_plugin_chat._private.tuples.SendMessageActionTuple import SendMessageActionTuple
from peek_plugin_user.server.UserDbServerApiABC import UserDbServerApiABC
from vortex.DeferUtil import vortexLogFailure, deferToThreadWrapWithLogger
from vortex.TupleAction import TupleActionABC
from vortex.TupleSelector import TupleSelector
from vortex.handler.TupleActionProcessor import TupleActionProcessorDelegateABC
from vortex.handler.TupleDataObservableHandler import TupleDataObservableHandler

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

    def _notifyOfChatListUpdate(self, userId: str) -> None:
        """ Notify of Chat List Update

        Notify the observer of the data it needs to emit to the users.

        :param userId: The user to notify of all chat updates

        """

        self._tupleObserver.notifyOfTupleUpdate(
            TupleSelector(ChatTuple.tupleType(), {"userId": userId})
        )


    def _notifyOfChatUpdate(self, chatId: int) -> None:
        """ Notify of Chat Update

        Notify the observer of the data it needs to emit to the users.

        :param chatId: The id of the chat that has been updated.

        """

        self._tupleObserver.notifyOfTupleUpdate(
            TupleSelector(ChatTuple.tupleType(), {"chatId": chatId})
        )

    def processTupleAction(self, tupleAction: TupleActionABC):
        if isinstance(tupleAction, SendMessageActionTuple):
            return self._processSendMessageAction(tupleAction)

        if isinstance(tupleAction, CreateChatActionTuple):
            return self._processCreateChatAction(tupleAction)

        raise Exception("Unhandled tuple action %s" % tupleAction.tupleType())

    @deferToThreadWrapWithLogger(logger)
    def externalMessageQueued(self, toUserId: str):
        """ External Message Sent
        
        This method is used to notify the main controller when a new message has
        been queued from an external system.
        """

    @deferToThreadWrapWithLogger(logger)
    def _processSendMessageAction(self, action: SendMessageActionTuple):
        """ Process Task Update
        
        Process updates to the task from the UI.
        
        """
        session = self._ormSessionCreator()

        try:
            chatTuple = (session
                         .query(ChatTuple)
                         .filter(ChatTuple.id == action.chatId)
                         .one())

            # Create the new chat tuple
            messageTuple = MessageTuple()
            messageTuple.chatId = chatTuple.id
            messageTuple.fromUserId = action.fromUserId
            messageTuple.message = action.message
            messageTuple.priority = action.priority
            messageTuple.dateTime = datetime.utcnow()
            messageTuple.state = MessageTuple.STATE_NEW
            session.add(messageTuple)

            chatTuple.lastActivity = datetime.utcnow()
            chatTuple.hasUnreads = True

            # Get the IDs needed for the updates
            userIds = [chatUser.userId for chatUser in chatTuple.users]
            chatId = chatTuple.id

            session.commit()


        finally:
            session.close()

        for userId in userIds:
            self._notifyOfChatListUpdate(userId)

        self._notifyOfChatUpdate(chatId)

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

    @deferToThreadWrapWithLogger(logger)
    def _processCreateChatAction(self, action: CreateChatActionTuple):
        """ Process Create Chat action by user

        Process updates to the task from the UI.

        """
        session = self._ormSessionCreator()

        try:
            # Create the new chat tuple
            chatTuple = ChatTuple()
            chatTuple.lastActivity = datetime.utcnow()
            chatTuple.hasUnreads = False
            session.add(chatTuple)

            for userId in action.userIds + [action.fromUserId]:
                chatUserTuple = ChatUserTuple()
                chatUserTuple.userId = userId
                chatUserTuple.isUserExternal = False
                chatUserTuple.userName = userId

                chatTuple.users.append(chatUserTuple)
                session.add(chatUserTuple)

            session.commit()

            # chatId = chatTuple.id

        finally:
            session.close()

        for userId in action.userIds:
            self._notifyOfChatListUpdate(userId)

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
