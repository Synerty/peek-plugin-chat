import {addTupleType, Tuple} from "@synerty/vortexjs";
import {chatTuplePrefix} from "../PluginNames";
import {ConversationUserTuple} from "./ConversationUserTuple";
import {MessageTuple} from "./MessageTuple";


@addTupleType
export class ConversationTuple extends Tuple {
    public static readonly tupleName = chatTuplePrefix + "ConversationTuple";

    //  Description of date1
    id: number;

    // Message details
    hasUnreads: boolean;
    lastActivity: Date;

    messages: MessageTuple[];
    users: ConversationUserTuple[];

    constructor() {
        super(ConversationTuple.tupleName)
    }
}