import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {chatBaseUrl, ChatMsgTuple} from "@peek/peek_plugin_chat/_private";

import {
    ComponentLifecycleEventEmitter,
    TupleActionPushService,
    TupleDataObserverService,
    TupleSelector
} from "@synerty/vortexjs";
import {SendChatMsgActionTuple} from "../../../plugin-module/_private/tuples/SendChatMsgActionTuple";

@Component({
    selector: 'plugin-chat-chat-msg',
    templateUrl: 'chat-msg.component.mweb.html',
    moduleId: module.id
})
export class ChatMsgComponent extends ComponentLifecycleEventEmitter {

    stringInts: Array<ChatMsgTuple> = [];

    constructor(private actionService: TupleActionPushService,
                private tupleDataObserver: TupleDataObserverService,
                private router: Router) {
        super();

        // Create the TupleSelector to tell the obserbable what data we want
        let selector = {};
        selector["userId"] = "userId";
        let tupleSelector = new TupleSelector(ChatMsgTuple.tupleName, selector);

        // Setup a subscription for the data
        let sup = tupleDataObserver.subscribeToTupleSelector(tupleSelector)
            .subscribe((tuples: ChatMsgTuple[]) => {
                // We've got new data, assign it to our class variable
                this.stringInts = tuples;
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