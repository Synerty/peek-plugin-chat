import {
    animate,
    Component,
    EventEmitter,
    Input,
    Output,
    state,
    style,
    transition,
    trigger
} from "@angular/core";
import {UserListItemTuple, UserService} from "@peek/peek_plugin_user";
import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";

export class NewChatDialogData {

    users: UserListItemTuple[] = [];

    constructor() {

    }

}


@Component({
    moduleId: module.id,
    selector: 'pl-chat-new-chat',
    templateUrl: './new-chat.component.mweb.html',
    animations: [
        trigger('dialogAnimation', [
            state('void', style({
                transform: "translateY(-100%)",
                opacity: 0,
                height: 0
            })),
            state('hidden', style({
                transform: "translateY(-100%)",
                opacity: 0,
                height: 0
            })),
            state('shown', style({})),
            transition('* => *', animate(500))
        ])
    ]
})
export class NewChatComponent extends ComponentLifecycleEventEmitter {

    dialogAnimationState = "shown";

    @Input("data")
    data: NewChatDialogData = null;

    @Output("create")
    confirmEvent: EventEmitter<NewChatDialogData> = new EventEmitter<NewChatDialogData>();

    @Output("cancel")
    cancelEvent: EventEmitter<void> = new EventEmitter<void>();

    cancelled = true;

    users: UserListItemTuple[] = [];
    selectedUserId: string | null;


    constructor(private userService: UserService) {
        super();

        this.users.add(userService.users);
        this.filterOutUser(userService.userDetails.userId);
    }

    private filterOutUser(userId: string) {
        this.users = this.users.filter((i) => i.userId != userId);
    }


    // ---- Display methods
    newButtonEnabled(): boolean {
        return this.selectedUserId != null;
    }

    createButtonEnabled(): boolean {
        return this.data.users.length != 0;
    }


    // ---- User Input methods

    addUserClicked() {
        let user = this.users.filter(u => u.userId === this.selectedUserId)[0];
        this.data.users.push(user);
        this.filterOutUser(this.selectedUserId);
        this.selectedUserId = null;
    }

    /** Confirm Clicked
     * @param emit Emit the events, this is false for web as the animation end fires
     *              the events.
     */
    confirmClicked(emit: boolean) {
        this.dialogAnimationState = "hidden";
        this.cancelled = false;
        emit && this.emitEvents();
    }

    cancelClicked(emit: boolean) {
        this.dialogAnimationState = "hidden";
        emit && this.emitEvents();
    }

    // ---- Dialog event methods
    animationDone(e) {
        if (e.toState !== "hidden")
            return;
        this.emitEvents();
    }

    private emitEvents() {
        if (this.cancelled) {
            this.cancelEvent.emit();
        } else {
            this.confirmEvent.emit(this.data);
        }
    }

}

