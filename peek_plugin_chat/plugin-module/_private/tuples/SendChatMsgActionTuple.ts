import {addTupleType, Tuple, TupleActionABC} from "@synerty/vortexjs";
import {chatTuplePrefix} from "../PluginNames";

@addTupleType
export class SendChatMsgActionTuple extends TupleActionABC {
    static readonly tupleName = chatTuplePrefix + "SendChatMsgActionTuple";

    stringIntId: number;

    constructor() {
        super(SendChatMsgActionTuple.tupleName)
    }
}