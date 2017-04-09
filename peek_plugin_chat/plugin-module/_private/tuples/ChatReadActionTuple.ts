import {addTupleType, TupleActionABC} from "@synerty/vortexjs";
import {chatTuplePrefix} from "../PluginNames";

@addTupleType
export class ChatReadActionTuple extends TupleActionABC {
    static readonly tupleName = chatTuplePrefix + "ChatReadActionTuple";

    chatUserId: number;
    readDateTime: Date;

    constructor() {
        super(ChatReadActionTuple.tupleName)
    }
}