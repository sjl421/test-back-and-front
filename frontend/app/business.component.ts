import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { BusinessService } from './business.service';


@Component({
    moduleId: module.id,
    selector: 'Business',
    templateUrl: 'templates/businessForm.html',
    providers: [BusinessService],
})

export class BusinessComponent {
    title = 'Business Information';
    businessForm: FormGroup;
    errorMessage: string;
    showOwnerForm = false;
    businessId: string;

    constructor(private businessService: BusinessService, fb: FormBuilder) {
        this.businessForm = fb.group({
            'tax_id': ["", Validators.required],
            'name': ["", Validators.required],
            'address': ["", Validators.required],
            'city': ["", Validators.required],
            'state': ["", Validators.required],
            'postal_code': ["", Validators.required],
            'amount': ["", Validators.required]
        });
    }

    doSave(event) {
        event.preventDefault();
        console.log(this.businessForm.value);
        this.businessService.addBusiness(this.businessForm.value)
                            .subscribe(
                                business => {
                                    console.log(business);
                                    this.businessId = business['tax_id'];
                                    this.showOwnerForm = true;
                                },
                                error => {
                                    console.log(error);
                                    this.businessForm.reset();
                                    this.errorMessage = error;
                            });
    }

    validateBusiness(event) {
        event.preventDefault();
        this.businessService.getBusiness(this.businessForm.value['tax_id'])
                            .subscribe(
                                business => {
                                    console.log(business);
                                    if (business.tax_id != null) {
                                        alert('Business already exists');
                                        this.businessForm.reset();
                                    }
                                },
                                error => {
                                    console.log(error);
                                    this.businessForm.reset();
                                    this.errorMessage = error;
                                }
                            );
    }
}