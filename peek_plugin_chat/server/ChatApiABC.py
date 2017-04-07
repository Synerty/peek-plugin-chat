from abc import ABCMeta, abstractmethod

from rx.subjects import Subject
from typing import Optional


class SendMessage:
    """ New Message

    This class represents a new message that another plugin can send to a user.

    """

    # Message priorities

    #:  Emergency priority for message
    PRIORITY_EMERGENCY = 1
    #:  Normal priority for message
    PRIORITY_NORMAL = 2

    def __init__(self,
                 fromExtUserId: str,
                 fromExtUserName: str,
                 toUserId: str,
                 message: str,
                 priority: int = PRIORITY_NORMAL,
                 onReadPayload: Optional[bytes] = None
                 ):
        """ 
        :param fromExtUserId: The external user id of the user sending the message.
            This doesn't have to match a userId in the peek_plugin_user plugin.
    
        :param fromExtUserName: The name of the external user (or system) sending the
            message.
    
        :param toUserId: The peek userId that matches a user in peek_plugin_user plugin.
        
        :param message: The message to send to the user.
        
        :param priority: The priority of this message, some messages may be emergency 
            messages.
        
        :param onReadPayload: (Optional) The payload that will be delivered locally
            on Peek Server when the user has read the message.
            
        """
        # From User
        self.fromExtUserId = self._required(fromExtUserId, "fromExtUserId")
        self.fromExtUserName = self._required(fromExtUserName, "fromExtUserName")

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

    This class represents a message sent from a peek user to an external system.

    """

    # Message priorities
    PRIORITY_EMERGENCY = SendMessage.PRIORITY_EMERGENCY
    PRIORITY_NORMAL = SendMessage.PRIORITY_NORMAL

    def __init__(self,
                 toExtUserId: str,
                 fromUserId: str,
                 message: str,
                 priority: int,
                 onReadPayload: bytes
                 ):
        """
        :param toExtUserId: The external user id that the message is sent to.

        :param fromUserId: The peek userId sending the message to the 
            external system.

        :param message: The message sent by the peek user.

        :param priority: The priority of this message sent.

        :param onReadPayload: The integrating plugin should deliver this payload locally
            on the server service once the message has been delivered/read externally.

        """
        # From User
        self.toExtUserId = toExtUserId

        # To User
        self.fromUserId = fromUserId

        # Message
        self.message = message
        self.priority = priority

        # On Read Payload
        self.onReadPayload = onReadPayload

    def _required(self, val, desc):
        if not val:
            raise Exception("%s is not optional" % desc)

        return val


class ChatApiABC(metaclass=ABCMeta):
    @abstractmethod
    def sendMessage(self, newMessage: SendMessage) -> None:
        """ Send a Message

        Send a new chat message to a user.
        
        :param newMessage: The definition of the message to send.
        
        """

    @abstractmethod
    def receiveMessages(self, toExtUserId: str) -> Subject:
        """ Complete a Task
        
        Mark a task as complete. NOTE, This doesn't delete it.
        
        .. note:: Integrating plugins must tell the chat plugin when the message
            has been read.
        
        :param toExtUserId: The external systems userId, that the plugin wants to 
            observe messages for. This is just identifier unique to the external
            system.
            
        :return: A RxJS Observable that will notify observers when a message arrives
            for that external system.
        
        """