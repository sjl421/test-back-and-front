import { Injectable } from '@angular/core';

import { Http, Headers, Response, RequestOptions } from '@angular/http';

import { Observable } from 'rxjs';


@Injectable()
export class LoanService {

    private headers = new Headers({'Content-Type': 'multipart/json'});
    private businessServiceUrl = 'http://localhost:8080/api/';
    private options = new RequestOptions({'headers': this.headers});
    
    constructor(private http: Http) {}

    getLoanStatus(businessId): Observable<any> {
        let url = this.businessServiceUrl + 'getloanstatus/' + businessId;
        return this.http.get(url)
                    .map((res:Response) => res.json())
                    .catch(this.handleError);
    }

    private handleError (error: Response | any) {
        let errMsg: string;
        if (error instanceof Response) {
            const body = error.json() || '';
            const err = body.error || JSON.stringify(body);
            errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Promise.reject(errMsg);
    }
}