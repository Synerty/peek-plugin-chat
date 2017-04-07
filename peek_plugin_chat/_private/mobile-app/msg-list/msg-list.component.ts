import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {chatBaseUrl, MessageTuple, SendChatMsgActionTuple} from "@peek/peek_plugin_chat/_private";

import {UserService} from "@peek/peek_plugin_user"

import {
    ComponentLifecycleEventEmitter,
    TupleActionPushService,
    TupleDataObserverService,
    TupleSelector
} from "@synerty/vortexjs";

@Component({
    selector: 'plugin-chat-msg-list',
    templateUrl: 'msg-list.component.mweb.html',
    moduleId: module.id
})
export class MsgListComponent extends ComponentLifecycleEventEmitter {

    messages: Array<MessageTuple> = [];

    constructor(private actionService: TupleActionPushService,
                private tupleDataObserver: TupleDataObserverService,
                private router: Router,
                private userService:UserService) {
        super();

        // Create the TupleSelector to tell the obserbable what data we want
        let selector = {};
        selector["userId"] = "userId";
        let tupleSelector = new TupleSelector(MessageTuple.tupleName, selector);

        // Setup a subscription for the data
        let sup = tupleDataObserver.subscribeToTupleSelector(tupleSelector)
            .subscribe((tuples: MessageTuple[]) => {
                // We've got new data, assign it to our class variable
                this.messages = tuples;
            });

        // unsubscribe when this component is destroyed
        // This is a feature of ComponentLifecycleEventEmitter
        this.onDestroyEvent.subscribe(() => sup.unsubscribe());

    }

    mainClicked() {
        this.router.navigate([chatBaseUrl]);
    }

    sendMsgClicked(item) {
        let action = new SendChatMsgActionTuple();
        action.stringIntId = item.id;
        this.actionService.pushAction(action)
            .then(() => {
                alert('success');

            })
            .catch((err) => {
                alert(err);
            });
    }


}