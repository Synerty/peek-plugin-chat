import logging

from rx.subjects import Subject

from peek_plugin_chat._private.server.controller.MainController import MainController
from peek_plugin_chat.server.ChatApiABC import ChatApiABC, NewMessage

logger = logging.getLogger(__name__)


class ChatApi(ChatApiABC):
    def __init__(self, ormSessionCreator):
        self._ormSessionCreator = ormSessionCreator
        self._mainController = None

    def setMainController(self, mainController: MainController):
        self._mainController = mainController

    def shutdown(self):
        pass

    def sendMessage(self, newMessage: NewMessage) -> None:
        '''
        # Create the database task from the parameter
        dbTask = Task()
        for name in dbTask.tupleFieldNames():
            if getattr(task, name, None) and name is not "actions":
                setattr(dbTask, name, getattr(task, name))

        # Set the time of the message
        dbTask.dateTime = datetime.utcnow()


        session = self._ormSessionCreator()
        try:
            try:
                oldTask = (
                    session
                        .query(Task)
                        .filter(Task.uniqueId == task.uniqueId)
                        .one()
                )

                if task.overwriteExisting:
                    session.delete(oldTask)
                    session.commit()

                else:
                    raise Exception("Activity with uniqueId %s already exists"
                                    % task.uniqueId)

            except NoResultFound:
                pass

            session.add(dbTask)
            for dbAction in dbTask.actions:
                session.add(dbAction)
            session.commit()
            taskId, userId = dbTask.id, dbTask.userId

        finally:
            session.close()

        self._taskProc.taskAdded(taskId, userId)
        '''

    def receiveMessages(self, toExtUserId: str) -> Subject:
        pass
