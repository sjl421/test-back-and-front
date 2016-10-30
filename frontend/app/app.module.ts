import { NgModule } from '@angular/core';
import { BrowserModule} from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule, JsonpModule} from '@angular/http';


import { AppComponent } from './app.component';
import { BusinessComponent } from './business.component';
import { OwnerComponent } from './owner.component';
import { LoanComponent } from './loan.component';


import './rxjs-extensions';


@NgModule({
    imports: [ 
        BrowserModule,
        FormsModule,
        ReactiveFormsModule,
        HttpModule,
        JsonpModule
    ],
    declarations: [
        AppComponent,
        BusinessComponent,
        OwnerComponent,
        LoanComponent
    ],
    bootstrap: [
        AppComponent
    ]
})

export class AppModule {}
