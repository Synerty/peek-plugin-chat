import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {chatBaseUrl, ConversationTuple} from "@peek/peek_plugin_chat/_private";

import {UserService} from "@peek/peek_plugin_user"

import {
    ComponentLifecycleEventEmitter,
    TupleActionPushService,
    TupleDataObserverService,
    TupleSelector
} from "@synerty/vortexjs";

@Component({
    selector: 'plugin-chat-conv-list',
    templateUrl: 'conv-list.component.mweb.html',
    moduleId: module.id
})
export class ConvListComponent extends ComponentLifecycleEventEmitter {

    conversations: Array<ConversationTuple> = [];

    constructor(private actionService: TupleActionPushService,
                private tupleDataObserver: TupleDataObserverService,
                private router: Router,
                private userService:UserService) {
        super();

        // Create the TupleSelector to tell the obserbable what data we want
        let selector = {};
        selector["userId"] = "userId";
        let tupleSelector = new TupleSelector(ConversationTuple.tupleName, selector);

        // Setup a subscription for the data
        let sup = tupleDataObserver.subscribeToTupleSelector(tupleSelector)
            .subscribe((tuples: ConversationTuple[]) => {
                // We've got new data, assign it to our class variable
                this.conversations = tuples;
            });

        // unsubscribe when this component is destroyed
        // This is a feature of ComponentLifecycleEventEmitter
        this.onDestroyEvent.subscribe(() => sup.unsubscribe());

    }

    mainClicked() {
        this.router.navigate([chatBaseUrl]);
    }

    convClicked(item) {

    }


}