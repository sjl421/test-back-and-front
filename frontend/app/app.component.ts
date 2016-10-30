import { Component } from '@angular/core';


@Component({
    selector: 'root',
    template: `
        <h1>{{title}}</h1>
        <Business></Business>
    `
})

export class AppComponent {
    title = 'Lendingfront App';
}