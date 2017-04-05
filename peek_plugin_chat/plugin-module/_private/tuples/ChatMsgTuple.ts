import {addTupleType, Tuple} from "@synerty/vortexjs";
import {chatTuplePrefix} from "../PluginNames";


@addTupleType
export class ChatMsgTuple extends Tuple {
    public static readonly tupleName = chatTuplePrefix + "ChatMsgTuple";

    //  Description of date1
    dict1 : {};

    //  Description of array1
    array1 : any[];

    //  Description of date1
    date1 : Date;

    constructor() {
        super(ChatMsgTuple.tupleName)
    }
}