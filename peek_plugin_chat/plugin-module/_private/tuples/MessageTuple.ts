import {addTupleType, Tuple} from "@synerty/vortexjs";
import {chatTuplePrefix} from "../PluginNames";


@addTupleType
export class MessageTuple extends Tuple {
    public static readonly tupleName = chatTuplePrefix + "MessageTuple";

    //  Description of date1
    id: number;
    chatId: number;

    // Message details
    message: string;
    priority: number;
    public static readonly PRIORITY_EMERGENCY = 1;
    public static readonly PRIORITY_NORMAL = 2;

    // User to / from
    fromUserId: string;

    // Message state details
    dateTime: Date;

    //  These indicate the message state
    state: number;
    public static readonly STATE_NEW = 1;
    public static readonly STATE_DELIVERED = 2;
    public static readonly STATE_READ = 3;

    // onReadPayload = Column(PeekVarBinary)

    constructor() {
        super(MessageTuple.tupleName)
    }
}