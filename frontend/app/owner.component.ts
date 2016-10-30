import { Component, Input } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { LoanComponent } from './loan.component';


import { OwnerService } from './owner.service';


@Component({
    moduleId: module.id,
    selector: 'Owner',
    templateUrl: 'templates/ownerForm.html',
    providers: [OwnerService]
})

export class OwnerComponent {
    title = 'Owner Information';
    ownerForm: FormGroup;
    errorMessage: string;
    ownerId: string;
    showLoanStatus = false;
    @Input() businessId: string;

    constructor(private ownerService: OwnerService, fb: FormBuilder) {
        this.ownerForm = fb.group({
            'businessId': ["", Validators.required],
            'ssnumber': ["", Validators.required],
            'name': ["", Validators.required],
            'email': ["", Validators.required],
            'address': ["", Validators.required],
            'city': ["", Validators.required],
            'state': ["", Validators.required],
            'postal_code': ["", Validators.required]
        });
    }

    doSave(event) {
        this.ownerForm.value['businessId'] = this.businessId;
        event.preventDefault();
        this.ownerService.addOwner(this.ownerForm.value)
                        .subscribe(
                            owner => {
                                console.log(owner);
                                this.ownerId = owner['ssnumber'];
                                this.showLoanStatus = true;
                            },
                            error => {
                                console.log(error);
                                this.ownerForm.reset();
                                this.errorMessage = error;
                        });
    }
}