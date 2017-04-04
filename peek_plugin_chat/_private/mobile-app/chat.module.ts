import {CommonModule} from "@angular/common";
import {NgModule} from "@angular/core";
import {Routes} from "@angular/router";

// Import a small abstraction library to switch between NativeScript and web
import {PeekModuleFactory} from "@synerty/peek-web-ns/index.web";

// Import the default route component
import {ChatComponent} from "./chat.component";


// Define the child routes for this plugin
export const pluginRoutes: Routes = [
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
    providers: [],
    declarations: [ChatComponent]
})
export class ChatModule
{
}