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

import * as moment from "moment";

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
    messages(): MessageTuple[] {
        if (this.chat != null)
            return this.chat.messages;
        return [];
    }

    haveMessages(): boolean {
        return this.chat != null && this.chat.messages.length !== 0;
    }

    sendEnabled(): boolean {
        return this.newMessageText.length != 0;
    }

    isMessageFromThisUser(msg: MessageTuple): boolean {
        return msg.fromUserId == this.userService.userDetails.userId;
    }

    userDisplayName(msg: MessageTuple): string {
        return this.userService.userDisplayName(msg.fromUserId);
    }

    isNormalPriority(msg: MessageTuple): boolean {
        return msg.priority === MessageTuple.PRIORITY_NORMAL;
    }

    isEmergencyPriority(msg: MessageTuple): boolean {
        return msg.priority === MessageTuple.PRIORITY_EMERGENCY;
    }

    dateTime(msg: MessageTuple) {
        return moment(msg.dateTime).format('HH:MM DD-MMM');
    }

    timePast(msg: MessageTuple) {
        return moment.duration(new Date().getTime() - msg.dateTime.getTime()).humanize();
    }

    // ---- User Input methods
    navToChatsClicked() {
        this.router.navigate([chatBaseUrl, 'chats']);
    }

    sendMsgClicked() {
        this.sendMessage(MessageTuple.PRIORITY_NORMAL);
    }

    sendSosClicked() {
        this.sendMessage(MessageTuple.PRIORITY_EMERGENCY);
    }

    private sendMessage(priority) {
        let action = new SendMessageActionTuple();
        action.chatId = this.chat.id;
        action.fromUserId = this.userService.userDetails.userId;
        action.message = this.newMessageText;
        action.priority = priority;

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