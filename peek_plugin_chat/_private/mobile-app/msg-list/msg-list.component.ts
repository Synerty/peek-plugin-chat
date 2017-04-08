import {Component, OnInit} from "@angular/core";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {ActivatedRoute, Params, Router} from "@angular/router";
import {
    chatBaseUrl,
    ChatTuple,
    MessageTuple,
    SendMessageActionTuple
} from "@peek/peek_plugin_chat/_private";

import {TitleService} from "@synerty/peek-mobile-util";
import {UserService} from "@peek/peek_plugin_user";

import {
    ComponentLifecycleEventEmitter,
    TupleActionPushOfflineService,
    TupleActionPushService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleSelector
} from "@synerty/vortexjs";

@Component({
    selector: 'plugin-chat-msg-list',
    templateUrl: 'msg-list.component.mweb.html',
    moduleId: module.id
})
export class MsgListComponent extends ComponentLifecycleEventEmitter implements OnInit {

    chat: ChatTuple = new ChatTuple();

    newMessageText: string = "";

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private actionService: TupleActionPushService,
                private tupleDataObserver: TupleDataObserverService,
                private tupleDataOfflineObserver: TupleDataOfflineObserverService,
                private tupleOfflineAction: TupleActionPushOfflineService,
                private route: ActivatedRoute,
                private router: Router,
                private userService: UserService,
                titleService: TitleService) {
        super();
        titleService.setTitle("Chat");
    }


    // ---- Data manipulation methods
    ngOnInit() {
        this.route.params.subscribe((params: Params) => {
            let chatId = parseInt(params['chatId']);
            this.loadChat(chatId);
        });

    }

    private loadChat(chatId: number) {


        let tupleSelector = new TupleSelector(ChatTuple.tupleName, {chatId: chatId});

        let sup = this.tupleDataOfflineObserver.subscribeToTupleSelector(tupleSelector)
            .subscribe((tuples: ChatTuple[]) => {
                this.chat = tuples[0];

            });
        this.onDestroyEvent.subscribe(() => sup.unsubscribe());

    }

    // ---- Display methods
    haveMessages(): boolean {
        return this.chat != null && this.chat.messages.length !== 0;
    }

    sendEnabled(): boolean {
        return this.newMessageText.length != 0;
    }

    // ---- User Input methods
    mainClicked() {
        this.router.navigate([chatBaseUrl]);
    }

    sendMsgClicked(item) {
        let action = new SendMessageActionTuple();
        action.chatId = this.chat.id;
        action.fromUserId = this.userService.userDetails.userId;
        action.message = this.newMessageText;
        action.priority = MessageTuple.PRIORITY_NORMAL;

        this.actionService.pushAction(action)
            .then(() => {
                this.newMessageText = '';
                this.balloonMsg.showSuccess("Message Sent");

            })
            .catch((err) => {
                alert(err);
            });
    }


}