import {CommonModule} from "@angular/common";
import {NgModule} from "@angular/core";
import {Routes} from "@angular/router";
// Import the required classes from VortexJS
import {
    TupleActionPushNameService,
    TupleActionPushOfflineService,
    TupleActionPushService,
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService
} from "@synerty/vortexjs";
// Import a small abstraction library to switch between NativeScript and web
import {PeekModuleFactory} from "@synerty/peek-web-ns/index.web";
// Import the names we need for the
import {
    chatActionProcessorName,
    chatFilt,
    chatObservableName,
    chatTupleOfflineServiceName
} from "@peek/peek_plugin_chat/_private";
// Import the default route component
import {ChatComponent} from "./chat.component";
import {ChatMsgComponent} from "./chat-msg/chat-msg.component";


export function tupleOfflineStorageNameServiceFactory() {
    return new TupleOfflineStorageNameService(chatTupleOfflineServiceName);
}

export function tupleDataObservableNameServiceFactory() {
    return new TupleDataObservableNameService(
        chatObservableName, chatFilt);
}

export function tupleActionPushNameServiceFactory() {
    return new TupleActionPushNameService(
        chatActionProcessorName, chatFilt);
}

// Define the child routes for this plugin
export const pluginRoutes: Routes = [
    {
        path: 'chatmsg',
        component: ChatMsgComponent
    },
    {
        path: '',
        component: ChatComponent
    },
    {
        path: '**',
        component: ChatComponent
    }

];

// Define the root module for this plugin.
// This module is loaded by the lazy loader, what ever this defines is what is started.
// When it first loads, it will look up the routs and then select the component to load.
@NgModule({
    imports: [
        CommonModule,
        PeekModuleFactory.RouterModule.forChild(pluginRoutes)],
    exports: [],
    providers: [
        TupleOfflineStorageService,
        {
            provide: TupleOfflineStorageNameService,
            useFactory: tupleOfflineStorageNameServiceFactory
        },
        TupleDataObserverService,
        TupleDataOfflineObserverService,
        {
            provide: TupleDataObservableNameService,
            useFactory: tupleDataObservableNameServiceFactory
        },
        TupleActionPushOfflineService,
        TupleActionPushService, {
            provide: TupleActionPushNameService,
            useFactory: tupleActionPushNameServiceFactory
        },
    ],
    declarations: [ChatComponent, ChatMsgComponent]
})
export class ChatModule {
}