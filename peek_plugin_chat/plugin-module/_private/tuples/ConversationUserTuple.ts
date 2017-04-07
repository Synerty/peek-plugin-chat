import {addTupleType, Tuple} from "@synerty/vortexjs";
import {chatTuplePrefix} from "../PluginNames";


@addTupleType
export class ConversationUserTuple extends Tuple {
    public static readonly tupleName = chatTuplePrefix + "ConversationUserTuple";

    //  Description of date1
    id: number;
    convId: number;

    // User to / from
    userId: string;
    isUserExternal: boolean;

    // Message state details
    userName: string;

    constructor() {
        super(ConversationUserTuple.tupleName)
    }
}