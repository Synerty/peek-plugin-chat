import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {TitleService} from "@synerty/peek-mobile-util";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {chatBaseUrl, ChatTuple} from "@peek/peek_plugin_chat/_private";

import {UserService} from "@peek/peek_plugin_user";

import {
    ComponentLifecycleEventEmitter,
    TupleActionPushService,
    TupleDataObserverService,
    TupleSelector
} from "@synerty/vortexjs";
import {NewChatDialogData} from "./new-chat/new-chat.component";
import {CreateChatActionTuple} from "@peek/peek_plugin_chat/_private";

@Component({
    selector: 'plugin-chat-chat-list',
    templateUrl: 'chat-list.component.mweb.html',
    moduleId: module.id
})
export class ChatListComponent extends ComponentLifecycleEventEmitter {

    chats: Array<ChatTuple> = [];

    newChatDialogData: NewChatDialogData = null;

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private actionService: TupleActionPushService,
                private tupleDataObserver: TupleDataObserverService,
                private router: Router,
                private userService: UserService,
                titleService: TitleService) {
        super();
        titleService.setTitle("Chats");

        // Create the TupleSelector to tell the observable what data we want
        let tupleSelector = new TupleSelector(ChatTuple.tupleName, {
            userId: userService.loggedInUserDetails.userId
        });

        // Setup a subscription for the data
        let sup = tupleDataObserver.subscribeToTupleSelector(tupleSelector)
            .subscribe((tuples: ChatTuple[]) => {
                // We've got new data, assign it to our class variable
                this.chats = tuples;
            });

        // unsubscribe when this component is destroyed
        // This is a feature of ComponentLifecycleEventEmitter
        this.onDestroyEvent.subscribe(() => sup.unsubscribe());

    }

    // ---- Data manipulation methods

    private createChat(data: NewChatDialogData) {
        let action = new CreateChatActionTuple();
        action.userIds = data.users.map((u) => u.userId);
        action.fromUserId = this.userService.loggedInUserDetails.userId;
        this.actionService.pushAction(action)
            .then(() => {
                this.balloonMsg.showSuccess("Chat Created");
            })
            .catch(err => alert(err));
    }


    // ---- User Input methods
    mainClicked() {
        this.router.navigate([chatBaseUrl]);
    }

    newChatClicked() {
        this.newChatDialogData = new NewChatDialogData();
    }

    chatClicked(chat) {
        this.router.navigate([chatBaseUrl, 'messages', chat.id]);
    }

    // ---- Display methods
    isNewChatDialogShown(): boolean {
        return this.newChatDialogData != null;
    }

    dialogConfirmed(data: NewChatDialogData) {
        this.createChat(data);

        this.newChatDialogData = null;
    }

    dialogCanceled() {
        this.newChatDialogData = null;
    }

}