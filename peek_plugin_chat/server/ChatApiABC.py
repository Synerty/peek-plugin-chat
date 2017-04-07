from abc import ABCMeta, abstractmethod

from rx.subjects import Subject
from typing import Optional


class NewMessage:
    """ New Message

    This class represents a new message that another plugin can send to a user.

    """

    # Message priorities
    PRIORITY_EMERGENCY = 1
    PRIORITY_NORMAL = 2

    def __init__(self,
                 extFromUserId: str,
                 extFromUserName: str,
                 toUserId: str,
                 message: str,
                 priority: int = PRIORITY_NORMAL,
                 onReadPayload: Optional[bytes] = None
                 ):
        """
        :param extFromUserId: The external user id of the user sending the message.
            This doesn't have to match a userId in the peek_plugin_user plugin.
    
        :param extFromUserName: The name of the external user (or system) sending the
            message.
    
        :param toUserId: The peek userId that matches a user in peek_plugin_user plugin.
        
        :param message: The message to send to the user.
        
        :param priority: The priority of this message, some messages may be emergency 
            messages.
        
        :param onReadPayload: (Optional) The payload that will be delivered locally
            on Peek Server when the user has read the message.
            
        """
        # From User
        self.extFromUserId = self._required(extFromUserId, "extFromUserId")
        self.extFromUserName = self._required(extFromUserName, "extFromUserName")

        # To User
        self.toUserId = self._required(toUserId, "toUserId")

        # Message
        self.message = self._required(message, "message")
        self.priority = self._required(priority, "priority")

        # On Read Payload
        self.onReadPayload = onReadPayload

    def _required(self, val, desc):
        if not val:
            raise Exception("%s is not optional" % desc)

        return val


class ReceivedMessage:
    """ Received Message

    This class represents a message received from a user.

    """

    # Message priorities
    PRIORITY_EMERGENCY = 1
    PRIORITY_NORMAL = 2

    def __init__(self,
                 extFromUserId: str,
                 extFromUserName: str,
                 toUserId: str,
                 message: str,
                 priority: int = PRIORITY_NORMAL,
                 onReadPayload: Optional[bytes] = None
                 ):
        """
        :param extFromUserId: The external user id of the user sending the message.
            This doesn't have to match a userId in the peek_plugin_user plugin.

        :param extFromUserName: The name of the external user (or system) sending the
            message.

        :param toUserId: The peek userId that matches a user in peek_plugin_user plugin.

        :param message: The message to send to the user.

        :param priority: The priority of this message, some messages may be emergency 
            messages.

        :param onReadPayload: (Optional) The payload that will be delivered locally
            on Peek Server when the user has read the message.

        """
        # From User
        self.extFromUserId = self._required(extFromUserId, "extFromUserId")
        self.extFromUserName = self._required(extFromUserName, "extFromUserName")

        # To User
        self.toUserId = self._required(toUserId, "toUserId")

        # Message
        self.message = self._required(message, "message")
        self.priority = self._required(priority, "priority")

        # On Read Payload
        self.onReadPayload = onReadPayload

    def _required(self, val, desc):
        if not val:
            raise Exception("%s is not optional" % desc)

        return val


class ChatApiABC(metaclass=ABCMeta):
    @abstractmethod
    def sendMessage(self, newMessage: NewMessage) -> None:
        """ Send a Message

        Send a new chat message to a user.
        
        :param newMessage: The definition of the message to send.
        
        """

    @abstractmethod
    def completeTask(self, extToUserId: str) -> Subject:
        """ Complete a Task
        
        Mark a task as complete. NOTE, This doesn't delete it.
        
        :param extToUserId: The external systems userId, that the plugin wants to 
            observe messages for. This is just identifier unique to the external
            system.
            
        :return: A RxJS Observable that will notify observers when a message arrives
            for that external system.
        
        """