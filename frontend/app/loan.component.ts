import { Component, Input } from '@angular/core';

import { LoanService } from './loan.service';


@Component({
    moduleId: module.id,
    selector: 'Loan',
    templateUrl: 'templates/loanStatusPage.html',
    providers: [LoanService]
})

export class LoanComponent {
    title = "Loan Status";
    status: string;
    errorMessage: string;
    private showStatus = false;
    private showButton = true;
    @Input() businessId: string;

    constructor(private loanService: LoanService) {}

    getStatus(event) {
        event.preventDefault();
        this.loanService.getLoanStatus(this.businessId)
                        .subscribe(
                            loan_status => {
                                console.log(loan_status);
                                this.status = loan_status['loan_status'];
                                this.showStatus = true;
                                this.showButton = false;
                            },
                            error => {
                                console.log(error);
                                this.errorMessage = error;
                            }
                        );
    }
}