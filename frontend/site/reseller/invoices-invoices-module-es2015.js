(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["invoices-invoices-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.html":
/*!******************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.html ***!
  \******************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.html":
/*!********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.html ***!
  \********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-lg']\"></app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.html":
/*!**************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.html ***!
  \**************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.html":
/*!**************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.html ***!
  \**************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-objects-view [objectsListController]=\"objectListController\"></app-objects-view>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.html":
/*!*************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.html ***!
  \*************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form [formGroup]=\"addPaymentForm\" class=\"fl-content\">\n  <app-form-errors #formErrors [formGroup]=\"addPaymentForm\"></app-form-errors>\n  <div fxLayout=\"column\">\n    <div fxLayout=\"row\" fxLayoutGap=\"10px\">\n      <mat-form-field>\n        <input matInput [matDatepicker]=\"paymentDatePicker\" formControlName=\"date_initiated\"\n               placeholder=\"Payment date\">\n        <mat-datepicker-toggle matSuffix [for]=\"paymentDatePicker\"></mat-datepicker-toggle>\n        <mat-datepicker #paymentDatePicker></mat-datepicker>\n        <mat-error>{{'This field is required!'}}</mat-error>\n      </mat-form-field>\n      <mat-form-field>\n        <mat-select formControlName=\"gateway\" placeholder=\"Gateway\">\n          <mat-option *ngFor=\"let gateway of paymentOptions.gateways\" [value]=\"gateway.id\">\n            {{gateway.display_name}}\n          </mat-option>\n        </mat-select>\n        <mat-error>{{'This field is required!'}}</mat-error>\n      </mat-form-field>\n    </div>\n    <mat-form-field fxFlex=\"auto\">\n      <input matInput placeholder=\"Transaction ID\" type=\"text\"\n             formControlName=\"external_id\" required>\n      <mat-error>{{backendErrors['external_id'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n    <div fxLayout=\"row\">\n      <mat-form-field>\n        <input matInput placeholder=\"Amount\" type=\"number\"\n               formControlName=\"amount\" required>\n        <mat-error>{{'This field is required!' }}</mat-error>\n      </mat-form-field>\n      <mat-form-field>\n        <input matInput placeholder=\"Fee\" type=\"number\"\n               formControlName=\"fee\" required>\n        <mat-error>{{'This field is required!' }}</mat-error>\n      </mat-form-field>\n      <mat-form-field>\n        <mat-select formControlName=\"currency\" placeholder=\"Currency\">\n          <mat-option *ngFor=\"let currency of paymentOptions.currencies\" [value]=\"currency.code\">{{currency.code}}\n          </mat-option>\n        </mat-select>\n      </mat-form-field>\n    </div>\n    <mat-form-field>\n      <input matInput placeholder=\"Extra information\" type=\"text\"\n             formControlName=\"extra_info\">\n      <mat-error>{{backendErrors['extra_info']}}</mat-error>\n    </mat-form-field>\n    <div fxLayout=\"row\">\n      <button (click)=\"addPayment()\" mat-button color=\"primary\">\n        Add payment\n      </button>\n    </div>\n  </div>\n</form>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.html":
/*!*******************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.html ***!
  \*******************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxLayout=\"row\" class=\"full-width\">\n  <div fxFlex=\"auto\">\n    <div>\n      <p class=\"fl-detail\" *ngIf=\"object.is_fiscal\">\n        Fiscal invoice issue date: {{object.fiscal_date | date:'yyyy-MM-dd' }}\n      </p>\n      <p class=\"fl-detail\" *ngIf=\"object.is_fiscal\">\n        Fiscal invoice due date: {{object.fiscal_due_date | date:'yyyy-MM-dd' }}\n      </p>\n      <p class=\"fl-detail\">\n        Proforma issue date: {{object.issue_date | date:'yyyy-MM-dd' }}\n      </p>\n      <p class=\"fl-detail\">\n        Proforma due date: {{object.due_date | date:'yyyy-MM-dd' }}\n      </p>\n      <p class=\"fl-detail\">\n        <a [routerLink]=\"[config.getPanelUrl('clients-users/clients'), object.client.id]\"\n           class=\"active-link\">\n          {{object.company }}\n        </a>\n      </p>\n      <p class=\"fl-detail\">\n        <a [routerLink]=\"[config.getPanelUrl('clients-users/clients'), object.client.id]\"\n           class=\"active-link\">\n          {{object.first_name }} {{object.last_name }}\n        </a>\n      </p>\n      <p class=\"fl-detail\">\n        <a [routerLink]=\"[config.getPanelUrl('clients-users/clients'), object.client.id]\"\n           class=\"active-link\">{{object.address1 }}\n        </a>\n      </p>\n      <p class=\"fl-detail\">\n        <a [routerLink]=\"[config.getPanelUrl('clients-users/clients'), object.client.id]\"\n           class=\"active-link\">{{object.address2 }}\n        </a>\n      </p>\n    </div>\n  </div>\n  <div fxLayoutAlign=\"center center\">\n    <p class=\"fl-detail\" [innerHTML]=\"object.fleio_info\"></p>\n  </div>\n\n</div>\n<div class=\"fl-margin-top\">\n  <h2 class=\"fl-detail\">Items</h2>\n  <hr>\n</div>\n\n<div fxLayout=\"column\">\n  <div>\n    <div fxLayout=\"row\" *ngFor=\"let item of object.items\">\n      <div fxFlex=\"auto\">\n        <div>\n          <span class=\"wrap-text-content\">{{item.description}}</span>\n          <div *ngFor=\"let confOpt of item.configurable_options\">\n            <span class=\"fl-detail\">{{confOpt.display}}</span>\n            <span class=\"fl-detail\" *ngIf=\"!confOpt.is_free\">\n              ({{confOpt.price}} {{object.currency}})\n            </span>\n          </div>\n        </div>\n      </div>\n      <div>\n        <span>{{item.amount}} {{object.currency }}</span>\n      </div>\n    </div>\n  </div>\n\n  <div class=\"fl-margin-top\" fxLayout=\"row\" fxLayoutAlign=\"right right\">\n    <div fxFlex=\"auto\"></div>\n    <div>\n      Sub total: {{object.subtotal | number:'.2' }} {{object.currency}}\n      <br>\n      <span *ngFor=\"let tax of object.taxes\">\n        {{tax.name}} {{tax.amount}} {{object.currency}}\n      </span>\n      <br>\n      Total: {{object.total}} {{object.currency }}\n    </div>\n  </div>\n</div>\n\n<div class=\"fl-margin-top\">\n  <h2 class=\"fl-detail\">Journal</h2>\n  <hr>\n</div>\n\n<div *ngIf=\"!object.journal.length\">\n  No entries found\n</div>\n\n<div fxLayout=\"row\" fxLayoutAlign=\"center center\" *ngFor=\"let journalEntry of object.journal\">\n  <div fxFlex=\"20\">\n    {{journalEntry.date_added | date:'short' }}\n  </div>\n\n  <div fxFlex=\"30\">\n    <span>\n      {{journalEntry.source_info.name}}\n    </span>\n    <br>\n    <span class=\"fl-detail\" *ngIf=\"journalEntry.source_info.invoice\">\n          Invoice {{journalEntry.source_info.invoice}}\n    </span>\n    <span class=\"fl-detail\" *ngIf=\"journalEntry.source_info.transaction\">\n          Transaction {{journalEntry.source_info.transaction}}\n    </span>\n  </div>\n\n  <div fxFlex=\"30\">\n    <span>\n      {{journalEntry.destination_info.name}}\n    </span>\n    <br>\n    <span class=\"fl-detail\" *ngIf=\"journalEntry.destination_info.invoice\">\n        Invoice {{journalEntry.destination_info.invoice}}\n      </span>\n    <span class=\"fl-detail\" *ngIf=\"journalEntry.destination_info.transaction\">\n        Transaction {{journalEntry.destination_info.transaction}}\n      </span>\n  </div>\n\n  <div fxFlex=\"20\">\n    {{journalEntry.destination_amount }} {{journalEntry.destination_currency }}<br>\n  </div>\n\n  <div fxFlex=\"10\">\n    <div *ngIf=\"journalEntry.transaction\">\n      <button mat-icon-button fl-tooltip=\"Delete\" fl-tooltip-direction=\"left\" mat-button\n              (click)=\"deleteTransaction(journalEntry.transaction)\" class=\"md-icon-button fl-float-right\">\n        <mat-icon>delete</mat-icon>\n      </button>\n    </div>\n  </div>\n</div>\n\n<div fxLayout=\"row\" class=\"full-width\">\n  <div fxFlex=\"auto\"></div>\n  <div fxLayout=\"column\">\n    <div class=\"fl-margin-top\">\n      <span class=\"balance-container\">\n        Balance {{object.balance }} {{object.currency }}\n      </span>\n    </div>\n\n    <div class=\"download-button fl-margin-top\">\n      <a mat-button color=\"primary\" href=\"{{downloadPdfUrl}}\" target=\"_blank\">\n        Download PDF\n      </a>\n    </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.html":
/*!*****************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.html ***!
  \*****************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form [formGroup]=\"invoiceForm\">\n  <app-form-errors #formErrors [formGroup]=\"invoiceForm\"></app-form-errors>\n  <div fxLayout=\"column\">\n    <p class=\"fl-subheader\">Select client</p>\n    <mat-form-field>\n      <input matInput placeholder=\"Client\" type=\"text\" formControlName=\"client\" required\n             [matAutocomplete]=\"autocompleteClient\">\n      <mat-autocomplete #autocompleteClient=\"matAutocomplete\" [displayWith]=\"clientDisplay\">\n        <mat-option *ngFor=\"let client of filteredClients$ | async\" [value]=\"client\">\n          {{client.first_name}} {{client.last_name}}\n        </mat-option>\n      </mat-autocomplete>\n      <mat-error>{{'This field is required!'}}</mat-error>\n    </mat-form-field>\n    <mat-form-field>\n      <mat-select formControlName=\"status\" placeholder=\"Status\">\n        <mat-option *ngFor=\"let status of createOptions.invoice_statuses\" [value]=\"status[0]\">\n          {{status[1]}}\n        </mat-option>\n      </mat-select>\n      <mat-error>{{'This field is required!'}}</mat-error>\n    </mat-form-field>\n    <div fxLayout=\"row\">\n      <mat-form-field>\n        <input matInput [matDatepicker]=\"issueDatePicker\" formControlName=\"issue_date\" placeholder=\"Issue date\">\n        <mat-datepicker-toggle matSuffix [for]=\"issueDatePicker\"></mat-datepicker-toggle>\n        <mat-datepicker #issueDatePicker></mat-datepicker>\n        <mat-error>{{'This field is required!'}}</mat-error>\n      </mat-form-field>\n      <mat-form-field>\n        <input matInput [matDatepicker]=\"dueDatePicker\" formControlName=\"due_date\" placeholder=\"Due date\">\n        <mat-datepicker-toggle matSuffix [for]=\"dueDatePicker\"></mat-datepicker-toggle>\n        <mat-datepicker #dueDatePicker></mat-datepicker>\n        <mat-error>{{'This field is required!'}}</mat-error>\n      </mat-form-field>\n    </div>\n    <div fxLayout=\"row\" fxLayoutAlign=\"left center\" fxLayoutGap=\"10px\">\n      <div>\n        <p class=\"fl-subheader\">Invoice items</p>\n      </div>\n      <button mat-mini-fab class=\"add-item-button\" fl-tooltip=\"Add invoice item\" fl-tooltip-direction=\"right\"\n              (click)=\"addInvoiceItem()\">\n        <mat-icon>add</mat-icon>\n      </button>\n    </div>\n    <div formArrayName=\"items\" *ngFor=\"let item of invoiceForm.get('items').controls; let i = index;\">\n      <div [formGroupName]=\"i\">\n        <mat-form-field class=\"full-width\">\n          <textarea matInput rows=\"3\" maxlength=\"255\" placeholder=\"Description\" type=\"text\"\n                    formControlName=\"description\" required>\n          </textarea>\n        </mat-form-field>\n        <div fxLayout=\"row\" fxLayoutGap=\"10px\">\n          <mat-form-field fxFlex=\"66\">\n            <mat-select formControlName=\"item_type\" placeholder=\"Invoice item type\">\n              <mat-option *ngFor=\"let item_type of createOptions.invoice_item_types | keyvalue\"\n                          [value]=\"item_type.key\">\n                {{item_type.value}}\n              </mat-option>\n            </mat-select>\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <mat-form-field fxFlex=\"33\">\n            <input matInput placeholder=\"Amount\" type=\"number\"\n                   formControlName=\"amount\" required>\n            <mat-error>{{'This field is required!' }}</mat-error>\n          </mat-form-field>\n        </div>\n        <div fxLayout=\"row\" fxLayoutAlign=\"left center\" fxLayoutGap=\"10px\">\n          <mat-form-field fxFlex=\"66\">\n            <mat-select formControlName=\"service\" placeholder=\"Service\">\n              <mat-option *ngFor=\"let service of createOptions.services\"\n                          [value]=\"service.id\">\n                {{service.display_name}}\n              </mat-option>\n            </mat-select>\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <mat-checkbox formControlName=\"taxed\" color=\"primary\">\n            Taxed\n          </mat-checkbox>\n        </div>\n      </div>\n    </div>\n  </div>\n</form>\n"

/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.scss":
/*!****************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.scss ***!
  \****************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaW52b2ljZXMvaW52b2ljZS1jcmVhdGUvaW52b2ljZS1jcmVhdGUuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.ts":
/*!**************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.ts ***!
  \**************************************************************************************/
/*! exports provided: InvoiceCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceCreateComponent", function() { return InvoiceCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../invoice-list-ui.service */ "./src/app/reseller/billing/invoices/invoice-list-ui.service.ts");





let InvoiceCreateComponent = class InvoiceCreateComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, invoiceListUIService) {
        super(route, invoiceListUIService, 'create', null);
    }
};
InvoiceCreateComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["InvoiceListUIService"] }
];
InvoiceCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-invoice-create',
        template: __webpack_require__(/*! raw-loader!./invoice-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.html"),
        styles: [__webpack_require__(/*! ./invoice-create.component.scss */ "./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.scss")]
    })
], InvoiceCreateComponent);



/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.scss":
/*!******************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.scss ***!
  \******************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaW52b2ljZXMvaW52b2ljZS1kZXRhaWxzL2ludm9pY2UtZGV0YWlscy5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.ts":
/*!****************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.ts ***!
  \****************************************************************************************/
/*! exports provided: InvoiceDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceDetailsComponent", function() { return InvoiceDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../invoice-list-ui.service */ "./src/app/reseller/billing/invoices/invoice-list-ui.service.ts");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");





let InvoiceDetailsComponent = class InvoiceDetailsComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_4__["DetailsBase"] {
    constructor(route, invoiceListUIService) {
        super(route, invoiceListUIService, 'details', 'invoice');
    }
};
InvoiceDetailsComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
    { type: _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_3__["InvoiceListUIService"] }
];
InvoiceDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-invoice-details',
        template: __webpack_require__(/*! raw-loader!./invoice-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.html"),
        styles: [__webpack_require__(/*! ./invoice-details.component.scss */ "./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.scss")]
    })
], InvoiceDetailsComponent);



/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.scss":
/*!************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.scss ***!
  \************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaW52b2ljZXMvaW52b2ljZS1lZGl0L2ludm9pY2UtZWRpdC5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.ts":
/*!**********************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.ts ***!
  \**********************************************************************************/
/*! exports provided: InvoiceEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceEditComponent", function() { return InvoiceEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../invoice-list-ui.service */ "./src/app/reseller/billing/invoices/invoice-list-ui.service.ts");





let InvoiceEditComponent = class InvoiceEditComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, invoiceListUIService) {
        super(route, invoiceListUIService, 'edit', 'invoice');
    }
};
InvoiceEditComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["InvoiceListUIService"] }
];
InvoiceEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-invoice-edit',
        template: __webpack_require__(/*! raw-loader!./invoice-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.html"),
        styles: [__webpack_require__(/*! ./invoice-edit.component.scss */ "./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.scss")]
    })
], InvoiceEditComponent);



/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoice-list-ui.service.ts":
/*!**********************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoice-list-ui.service.ts ***!
  \**********************************************************************/
/*! exports provided: InvoiceListUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceListUIService", function() { return InvoiceListUIService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _invoice_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./invoice-ui.service */ "./src/app/reseller/billing/invoices/invoice-ui.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/invoices/invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");









let InvoiceListUIService = class InvoiceListUIService {
    constructor(router, config, invoicesApi) {
        this.router = router;
        this.config = config;
        this.invoicesApi = invoicesApi;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_8__["DatePipe"](this.config.locale);
    }
    getObjectUIService(object, permissions, state) {
        return new _invoice_ui_service__WEBPACK_IMPORTED_MODULE_4__["InvoiceUIService"](object, permissions, state, this.router, this.config, this.invoicesApi);
    }
    getTableData(objectList) {
        const tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_7__["ColumnType"].Value, displayName: 'ID', enableSort: true, fieldName: 'display_number' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_7__["ColumnType"].Value, displayName: 'Status', enableSort: true, fieldName: 'status' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_7__["ColumnType"].Value, displayName: 'Issue date', enableSort: true, fieldName: 'issue_date' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_7__["ColumnType"].Value, displayName: 'Total', enableSort: true, fieldName: 'total' },
                ],
                columnNames: ['display_number', 'status', 'issue_date', 'total'],
                statusColumn: 'display_number',
            },
            rows: [],
        };
        for (const invoice of objectList.objects) {
            const rowUIService = this.getObjectUIService(invoice, objectList.permissions, 'table-view');
            const row = {
                cells: {
                    display_number: { text: invoice.display_number },
                    status: { text: invoice.status.toLocaleUpperCase() },
                    issue_date: { text: this.datePipe.transform(invoice.issue_date) },
                    total: { text: `${invoice.total} ${invoice.currency}` },
                },
                icon: rowUIService.getIcon(),
                status: rowUIService.getStatus(),
                actions: rowUIService.getActions(),
                url: rowUIService.getDetailsLink(),
            };
            tableData.rows.push(row);
        }
        return tableData;
    }
    getActions(objectList) {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__["RouterLinkAction"]({
                icon: { name: 'add' },
                name: 'Create',
                tooltip: 'Create new invoice',
                routerUrl: this.config.getPanelUrl(`billing/invoices/create`),
                router: this.router,
            }),
        ];
    }
};
InvoiceListUIService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_6__["InvoicesApiService"] }
];
InvoiceListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], InvoiceListUIService);



/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.scss":
/*!************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.scss ***!
  \************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaW52b2ljZXMvaW52b2ljZS1saXN0L2ludm9pY2UtbGlzdC5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.ts":
/*!**********************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.ts ***!
  \**********************************************************************************/
/*! exports provided: InvoiceListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceListComponent", function() { return InvoiceListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../invoice-list-ui.service */ "./src/app/reseller/billing/invoices/invoice-list-ui.service.ts");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");






let InvoiceListComponent = class InvoiceListComponent extends _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_5__["ListBase"] {
    constructor(route, invoiceListUIService, refreshService) {
        super(route, invoiceListUIService, refreshService, 'invoices');
        this.route = route;
        this.invoiceListUIService = invoiceListUIService;
        this.refreshService = refreshService;
    }
    ngOnInit() {
        super.ngOnInit();
    }
};
InvoiceListComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
    { type: _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["InvoiceListUIService"] },
    { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_3__["RefreshService"] }
];
InvoiceListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-invoice-list',
        template: __webpack_require__(/*! raw-loader!./invoice-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.html"),
        styles: [__webpack_require__(/*! ./invoice-list.component.scss */ "./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.scss")]
    })
], InvoiceListComponent);



/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoice-ui.service.ts":
/*!*****************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoice-ui.service.ts ***!
  \*****************************************************************/
/*! exports provided: InvoiceUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceUIService", function() { return InvoiceUIService; });
/* harmony import */ var _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/object-status */ "./src/app/shared/ui/objects-view/interfaces/object-status.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _tabs_invoice_details_overview_invoice_details_overview_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tabs/invoice-details-overview/invoice-details-overview.component */ "./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.ts");
/* harmony import */ var _tabs_invoice_details_add_payment_invoice_details_add_payment_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./tabs/invoice-details-add-payment/invoice-details-add-payment.component */ "./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.ts");
/* harmony import */ var _tabs_invoice_edit_form_invoice_edit_form_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tabs/invoice-edit-form/invoice-edit-form.component */ "./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.ts");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/invoices/invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");











class InvoiceUIService extends _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__["ObjectUIServiceBase"] {
    constructor(invoice, permissions, state, router, config, invoicesApi) {
        super(invoice, permissions, state);
        this.router = router;
        this.config = config;
        this.invoicesApi = invoicesApi;
    }
    getIcon() {
        return null;
    }
    getStatus() {
        let status = null;
        switch (this.object.status) {
            case 'paid':
                status = { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Paid };
                break;
            case 'cancelled':
                status = { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Cancelled };
                break;
            case 'refunded':
                status = { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Refunded };
                break;
            case 'unpaid':
                if (new Date(this.object.due_date) > new Date()) {
                    status = { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Overdue };
                }
                else {
                    status = { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Unpaid };
                }
                break;
        }
        if (['card-view', 'table-view', 'details'].includes(this.state)) {
            return status;
        }
        return null;
    }
    getTitle() {
        switch (this.state) {
            case 'edit':
                return {
                    text: `Edit invoice ${this.object.display_number}`,
                    subText: this.object.status.toLocaleUpperCase(),
                };
            case 'create':
                return {
                    text: `Create invoice`,
                };
            default:
                return {
                    text: `Proforma ${this.object.display_number}`,
                    subText: this.object.status.toLocaleUpperCase(),
                };
        }
    }
    getActions() {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                icon: { name: 'edit' },
                name: 'Edit',
                tooltip: 'Edit invoice',
                routerUrl: this.config.getPanelUrl(`billing/invoices/${this.object.id}/edit`),
                router: this.router,
            }),
            new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_9__["ApiCallAction"]({
                object: this.object,
                icon: { name: 'delete' },
                name: 'Delete',
                tooltip: 'Delete',
                confirmOptions: {
                    confirm: true,
                    title: 'Delete invoice',
                    message: `Are you sure you want to delete invoice ${this.object.display_number}`,
                },
                apiService: this.invoicesApi,
                callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_9__["CallType"].Delete,
                refreshAfterExecute: false,
                redirectAfterExecute: true,
                redirectUrl: this.config.getPanelUrl('billing/invoices'),
            })
        ];
    }
    getDetailsActions() {
        const actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`billing/invoices`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({ name: 'Create invoice' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`billing/invoices`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({ name: 'Save invoice' }));
                break;
            default:
                break;
        }
        return actions;
    }
    getCardTags() {
        return [];
    }
    getDetailsLink() {
        return this.config.getPanelUrl(`billing/invoices/${this.object.id}`);
    }
    getCardFields() {
        return [
            {
                name: 'Issue date',
                value: `${this.object.issue_date}`
            },
            {
                name: 'Total',
                value: `${this.object.total} ${this.object.currency}`
            },
            {
                name: 'Client',
                value: this.object.client ? `${this.object.client.name}` : 'n/a',
            }
        ];
    }
    getTabs() {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Details',
                        component: _tabs_invoice_details_overview_invoice_details_overview_component__WEBPACK_IMPORTED_MODULE_5__["InvoiceDetailsOverviewComponent"],
                    },
                    {
                        tabName: 'Add payment',
                        component: _tabs_invoice_details_add_payment_invoice_details_add_payment_component__WEBPACK_IMPORTED_MODULE_6__["InvoiceDetailsAddPaymentComponent"],
                    },
                ];
            case 'edit':
            case 'create':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_invoice_edit_form_invoice_edit_form_component__WEBPACK_IMPORTED_MODULE_7__["InvoiceEditFormComponent"],
                    }
                ];
            default:
                return null;
        }
    }
}
InvoiceUIService.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] },
    { type: _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_10__["InvoicesApiService"] }
];


/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoices-routing.module.ts":
/*!**********************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoices-routing.module.ts ***!
  \**********************************************************************/
/*! exports provided: InvoicesRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoicesRoutingModule", function() { return InvoicesRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _invoice_list_invoice_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoice-list/invoice-list.component */ "./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.ts");
/* harmony import */ var _invoice_details_invoice_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./invoice-details/invoice-details.component */ "./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.ts");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoice_list_resolver__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/invoices/invoice-list.resolver */ "./src/app/shared/fleio-api/billing/invoices/invoice-list.resolver.ts");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoice_resolver__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/invoices/invoice.resolver */ "./src/app/shared/fleio-api/billing/invoices/invoice.resolver.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/ui-api/interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_filter_types__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/ui-api/interfaces/route-config/filter-types */ "./src/app/shared/ui-api/interfaces/route-config/filter-types.ts");
/* harmony import */ var _invoice_create_invoice_create_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./invoice-create/invoice-create.component */ "./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.ts");
/* harmony import */ var _invoice_edit_invoice_edit_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./invoice-edit/invoice-edit.component */ "./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.ts");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoice_create_options_resolver__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/invoices/invoice-create-options.resolver */ "./src/app/shared/fleio-api/billing/invoices/invoice-create-options.resolver.ts");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoice_edit_options_resolver__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/invoices/invoice-edit-options.resolver */ "./src/app/shared/fleio-api/billing/invoices/invoice-edit-options.resolver.ts");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoice_payment_options_resolver__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/invoices/invoice-payment-options.resolver */ "./src/app/shared/fleio-api/billing/invoices/invoice-payment-options.resolver.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");















const routes = [
    {
        path: '',
        component: _invoice_list_invoice_list_component__WEBPACK_IMPORTED_MODULE_3__["InvoiceListComponent"],
        resolve: {
            invoices: _shared_fleio_api_billing_invoices_invoice_list_resolver__WEBPACK_IMPORTED_MODULE_5__["InvoiceListResolver"]
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_14__["AuthGuard"]],
        data: {
            config: {
                feature: 'billing.invoices',
                search: {
                    show: true,
                    placeholder: 'Search invoices ...',
                },
                ordering: {
                    default: {
                        field: 'client',
                        display: 'Client',
                        direction: _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_7__["OrderingDirection"].Descending
                    },
                    options: [
                        {
                            field: 'status',
                            display: 'Status'
                        },
                        {
                            field: 'issue_date',
                            display: 'Issue date'
                        },
                        {
                            field: 'due_date',
                            display: 'Due date'
                        },
                        {
                            field: 'client',
                            display: 'Client'
                        }
                    ],
                },
                filterOptions: [
                    {
                        field: 'issue_date',
                        display: 'Issue date',
                        type: _shared_ui_api_interfaces_route_config_filter_types__WEBPACK_IMPORTED_MODULE_8__["FilterTypes"].Date
                    },
                    {
                        field: 'due_date',
                        display: 'Due date',
                        type: _shared_ui_api_interfaces_route_config_filter_types__WEBPACK_IMPORTED_MODULE_8__["FilterTypes"].Date
                    },
                    {
                        field: 'total',
                        display: 'Total',
                        type: _shared_ui_api_interfaces_route_config_filter_types__WEBPACK_IMPORTED_MODULE_8__["FilterTypes"].Decimal
                    }
                ],
                subheader: {
                    objectName: 'invoice',
                    objectNamePlural: 'invoices',
                    objectList(data) {
                        return data.invoices;
                    }
                },
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: 'create',
        component: _invoice_create_invoice_create_component__WEBPACK_IMPORTED_MODULE_9__["InvoiceCreateComponent"],
        resolve: {
            createOptions: _shared_fleio_api_billing_invoices_invoice_create_options_resolver__WEBPACK_IMPORTED_MODULE_11__["InvoiceCreateOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return 'Create new invoice';
                },
            },
        }
    },
    {
        path: ':id',
        component: _invoice_details_invoice_details_component__WEBPACK_IMPORTED_MODULE_4__["InvoiceDetailsComponent"],
        resolve: {
            invoice: _shared_fleio_api_billing_invoices_invoice_resolver__WEBPACK_IMPORTED_MODULE_6__["InvoiceResolver"],
            paymentOptions: _shared_fleio_api_billing_invoices_invoice_payment_options_resolver__WEBPACK_IMPORTED_MODULE_13__["InvoicePaymentOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.invoice.display_number;
                },
            },
        },
        runGuardsAndResolvers: 'always',
    },
    {
        path: ':id/edit',
        component: _invoice_edit_invoice_edit_component__WEBPACK_IMPORTED_MODULE_10__["InvoiceEditComponent"],
        resolve: {
            invoice: _shared_fleio_api_billing_invoices_invoice_resolver__WEBPACK_IMPORTED_MODULE_6__["InvoiceResolver"],
            createOptions: _shared_fleio_api_billing_invoices_invoice_edit_options_resolver__WEBPACK_IMPORTED_MODULE_12__["InvoiceEditOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.invoice.display_number;
                },
            },
        }
    },
];
let InvoicesRoutingModule = class InvoicesRoutingModule {
};
InvoicesRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], InvoicesRoutingModule);



/***/ }),

/***/ "./src/app/reseller/billing/invoices/invoices.module.ts":
/*!**************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/invoices.module.ts ***!
  \**************************************************************/
/*! exports provided: InvoicesModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoicesModule", function() { return InvoicesModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _invoice_list_invoice_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoice-list/invoice-list.component */ "./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.ts");
/* harmony import */ var _invoice_details_invoice_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./invoice-details/invoice-details.component */ "./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.ts");
/* harmony import */ var _invoices_routing_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./invoices-routing.module */ "./src/app/reseller/billing/invoices/invoices-routing.module.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _invoice_create_invoice_create_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./invoice-create/invoice-create.component */ "./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.ts");
/* harmony import */ var _tabs_invoice_details_overview_invoice_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/invoice-details-overview/invoice-details-overview.component */ "./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.ts");
/* harmony import */ var _tabs_invoice_edit_form_invoice_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/invoice-edit-form/invoice-edit-form.component */ "./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.ts");
/* harmony import */ var _tabs_invoice_details_add_payment_invoice_details_add_payment_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/invoice-details-add-payment/invoice-details-add-payment.component */ "./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/icon */ "./node_modules/@angular/material/esm2015/icon.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm2015/button.js");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/divider */ "./node_modules/@angular/material/esm2015/divider.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _invoice_edit_invoice_edit_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./invoice-edit/invoice-edit.component */ "./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @angular/material/autocomplete */ "./node_modules/@angular/material/esm2015/autocomplete.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm2015/select.js");
/* harmony import */ var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @angular/material/datepicker */ "./node_modules/@angular/material/esm2015/datepicker.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm2015/checkbox.js");
























let InvoicesModule = class InvoicesModule {
};
InvoicesModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _invoice_list_invoice_list_component__WEBPACK_IMPORTED_MODULE_3__["InvoiceListComponent"],
            _invoice_details_invoice_details_component__WEBPACK_IMPORTED_MODULE_4__["InvoiceDetailsComponent"],
            _invoice_create_invoice_create_component__WEBPACK_IMPORTED_MODULE_7__["InvoiceCreateComponent"],
            _tabs_invoice_details_overview_invoice_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["InvoiceDetailsOverviewComponent"],
            _tabs_invoice_edit_form_invoice_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["InvoiceEditFormComponent"],
            _tabs_invoice_details_add_payment_invoice_details_add_payment_component__WEBPACK_IMPORTED_MODULE_10__["InvoiceDetailsAddPaymentComponent"],
            _invoice_edit_invoice_edit_component__WEBPACK_IMPORTED_MODULE_17__["InvoiceEditComponent"],
        ],
        entryComponents: [
            _tabs_invoice_details_overview_invoice_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["InvoiceDetailsOverviewComponent"],
            _tabs_invoice_edit_form_invoice_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["InvoiceEditFormComponent"],
            _tabs_invoice_details_add_payment_invoice_details_add_payment_component__WEBPACK_IMPORTED_MODULE_10__["InvoiceDetailsAddPaymentComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _invoices_routing_module__WEBPACK_IMPORTED_MODULE_5__["InvoicesRoutingModule"],
            _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_6__["ObjectsViewModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_11__["FlexLayoutModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_12__["MatIconModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_13__["MatButtonModule"],
            _angular_material_divider__WEBPACK_IMPORTED_MODULE_14__["MatDividerModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_15__["ReactiveFormsModule"],
            _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_16__["ErrorHandlingModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_18__["MatFormFieldModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_19__["MatInputModule"],
            _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_20__["MatAutocompleteModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_21__["MatSelectModule"],
            _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_22__["MatDatepickerModule"],
            _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_23__["MatCheckboxModule"],
        ]
    })
], InvoicesModule);



/***/ }),

/***/ "./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.scss":
/*!***********************************************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.scss ***!
  \***********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaW52b2ljZXMvdGFicy9pbnZvaWNlLWRldGFpbHMtYWRkLXBheW1lbnQvaW52b2ljZS1kZXRhaWxzLWFkZC1wYXltZW50LmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.ts":
/*!*********************************************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.ts ***!
  \*********************************************************************************************************************/
/*! exports provided: InvoiceDetailsAddPaymentComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceDetailsAddPaymentComponent", function() { return InvoiceDetailsAddPaymentComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../shared/fleio-api/billing/invoices/invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../../../shared/ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");










let InvoiceDetailsAddPaymentComponent = class InvoiceDetailsAddPaymentComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"] {
    constructor(formBuilder, activatedRoute, invoicesApi, notification, refreshService) {
        super();
        this.formBuilder = formBuilder;
        this.activatedRoute = activatedRoute;
        this.invoicesApi = invoicesApi;
        this.notification = notification;
        this.refreshService = refreshService;
        this.addPaymentForm = this.formBuilder.group({
            external_id: [''],
            extra_info: [''],
            date_initiated: [_angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            gateway: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            currency: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            amount: [0, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            fee: [0, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
        });
    }
    ngOnInit() {
        this.paymentOptions = this.activatedRoute.snapshot.data.paymentOptions;
        this.addPaymentForm.patchValue({
            date_initiated: new Date(),
            amount: this.object.balance,
            currency: this.paymentOptions.currencies[0].code,
            gateway: this.paymentOptions.gateways[0].id,
        });
    }
    addPayment() {
        this.validate();
        if (this.addPaymentForm.invalid) {
            Object.keys(this.formGroup.controls).map(name => {
                const control = this.formGroup.controls[name];
                if (control.invalid) {
                    control.markAsTouched();
                }
            });
        }
        else {
            const value = this.addPaymentForm.value;
            value.invoice = this.object.id;
            const request = this.invoicesApi.objectPostAction(this.object.id, 'add_payment_to_invoice', value);
            request.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["catchError"])((error) => {
                if (error.error) {
                    this.setErrors(error.error);
                    return rxjs__WEBPACK_IMPORTED_MODULE_5__["EMPTY"];
                }
                else {
                    throw error;
                }
            })).subscribe(() => {
                this.notification.showMessage('Payment added');
                this.refreshService.refresh();
            });
        }
    }
};
InvoiceDetailsAddPaymentComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
    { type: _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_7__["InvoicesApiService"] },
    { type: _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_8__["NotificationService"] },
    { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_9__["RefreshService"] }
];
InvoiceDetailsAddPaymentComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-invoice-details-add-payment',
        template: __webpack_require__(/*! raw-loader!./invoice-details-add-payment.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.html"),
        styles: [__webpack_require__(/*! ./invoice-details-add-payment.component.scss */ "./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.scss")]
    })
], InvoiceDetailsAddPaymentComponent);



/***/ }),

/***/ "./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.scss":
/*!*****************************************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.scss ***!
  \*****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".balance-container {\n  float: right;\n}\n\n.download-button {\n  float: right;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaW52b2ljZXMvdGFicy9pbnZvaWNlLWRldGFpbHMtb3ZlcnZpZXcvaW52b2ljZS1kZXRhaWxzLW92ZXJ2aWV3LmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9yZXNlbGxlci9iaWxsaW5nL2ludm9pY2VzL3RhYnMvaW52b2ljZS1kZXRhaWxzLW92ZXJ2aWV3L2ludm9pY2UtZGV0YWlscy1vdmVydmlldy5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLFlBQUE7QUNDRjs7QURFQTtFQUNFLFlBQUE7QUNDRiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaW52b2ljZXMvdGFicy9pbnZvaWNlLWRldGFpbHMtb3ZlcnZpZXcvaW52b2ljZS1kZXRhaWxzLW92ZXJ2aWV3LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLmJhbGFuY2UtY29udGFpbmVyIHtcbiAgZmxvYXQ6IHJpZ2h0O1xufVxuXG4uZG93bmxvYWQtYnV0dG9uIHtcbiAgZmxvYXQ6IHJpZ2h0O1xufVxuIiwiLmJhbGFuY2UtY29udGFpbmVyIHtcbiAgZmxvYXQ6IHJpZ2h0O1xufVxuXG4uZG93bmxvYWQtYnV0dG9uIHtcbiAgZmxvYXQ6IHJpZ2h0O1xufSJdfQ== */"

/***/ }),

/***/ "./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.ts":
/*!***************************************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.ts ***!
  \***************************************************************************************************************/
/*! exports provided: InvoiceDetailsOverviewComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceDetailsOverviewComponent", function() { return InvoiceDetailsOverviewComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _shared_fleio_api_billing_transaction_transaction_api_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/fleio-api/billing/transaction/transaction-api.service */ "./src/app/shared/fleio-api/billing/transaction/transaction-api.service.ts");
/* harmony import */ var _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");







let InvoiceDetailsOverviewComponent = class InvoiceDetailsOverviewComponent extends _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"] {
    constructor(config, refreshService, transactionApi, notificationService) {
        super();
        this.config = config;
        this.refreshService = refreshService;
        this.transactionApi = transactionApi;
        this.notificationService = notificationService;
    }
    ngOnInit() {
        this.downloadPdfUrl = this.config.getPanelApiUrl(`billing/invoices/${this.object.id}/download?content_type=pdf`);
    }
    deleteTransaction(transaction) {
        this.notificationService.confirmDialog({
            title: 'Delete transaction',
            message: 'Are you sure you want to delete transaction?'
        }).subscribe(result => {
            if (result === 'yes') {
                this.transactionApi.delete(transaction.id).subscribe(() => {
                    this.refreshService.refresh();
                });
            }
        });
    }
};
InvoiceDetailsOverviewComponent.ctorParameters = () => [
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] },
    { type: _shared_fleio_api_billing_transaction_transaction_api_service__WEBPACK_IMPORTED_MODULE_5__["TransactionsApiService"] },
    { type: _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_6__["NotificationService"] }
];
InvoiceDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-invoice-details-overview',
        template: __webpack_require__(/*! raw-loader!./invoice-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.html"),
        styles: [__webpack_require__(/*! ./invoice-details-overview.component.scss */ "./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.scss")]
    })
], InvoiceDetailsOverviewComponent);



/***/ }),

/***/ "./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.scss":
/*!***************************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.scss ***!
  \***************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaW52b2ljZXMvdGFicy9pbnZvaWNlLWVkaXQtZm9ybS9pbnZvaWNlLWVkaXQtZm9ybS5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.ts":
/*!*************************************************************************************************!*\
  !*** ./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.ts ***!
  \*************************************************************************************************/
/*! exports provided: InvoiceEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceEditFormComponent", function() { return InvoiceEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _shared_fleio_api_client_user_client_clients_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/fleio-api/client-user/client/clients-api.service */ "./src/app/shared/fleio-api/client-user/client/clients-api.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../../../shared/fleio-api/billing/invoices/invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_billing_services_service_api_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../../../shared/fleio-api/billing/services/service-api.service */ "./src/app/shared/fleio-api/billing/services/service-api.service.ts");











let InvoiceEditFormComponent = class InvoiceEditFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"] {
    constructor(formBuilder, clientsApi, activatedRoute, invoicesApi, router, config, servicesApi) {
        super();
        this.formBuilder = formBuilder;
        this.clientsApi = clientsApi;
        this.activatedRoute = activatedRoute;
        this.invoicesApi = invoicesApi;
        this.router = router;
        this.config = config;
        this.servicesApi = servicesApi;
        this.invoiceForm = this.formBuilder.group({
            client: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            status: ['unpaid', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            issue_date: [Date.now(), _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            due_date: [Date.now(), _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            items: this.formBuilder.array([]),
        });
        this.client = this.invoiceForm.controls.client;
    }
    ngOnInit() {
        this.objectController.actionCallback = () => this.saveInvoice();
        this.createOptions = this.activatedRoute.snapshot.data.createOptions;
        if (Object.keys(this.object).length > 0) {
            this.invoiceForm.patchValue(this.object);
            if (this.object.items) {
                this.object.items.map(item => this.invoiceForm.controls.items.push(this.initInvoiceItem(item)));
            }
        }
        else {
            this.invoiceForm.patchValue({
                issue_date: new Date(),
                due_date: new Date(),
            });
            const queryParams = this.activatedRoute.snapshot.queryParams;
            if (queryParams.client_id) {
                this.clientsApi.get(queryParams.client_id).subscribe(client => {
                    this.client.setValue(client);
                });
            }
        }
        this.filteredClients$ = this.client.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["startWith"])(''), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(value => {
            return typeof value === 'string' ? value : value.id;
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["mergeMap"])(value => {
            return this.clientsApi.list({
                search: value,
            }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(clientsList => clientsList.objects));
        }));
        if (!this.object.id) {
            this.client.valueChanges.subscribe(client => {
                this.servicesApi.list({
                    client: client.id,
                }).subscribe(services => {
                    this.createOptions.services = services.objects;
                });
            });
        }
    }
    clientDisplay(client) {
        if (client) {
            return client.name ? client.name : `${client.first_name} ${client.last_name}`;
        }
        else {
            return undefined;
        }
    }
    initInvoiceItem(item = null) {
        return this.formBuilder.group({
            description: [item ? item.description : '', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            amount: [item ? item.amount : '', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            item_type: [item ? item.item_type : '', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            service: [item ? item.service : ''],
            taxed: [item ? item.taxed : false],
        });
    }
    addInvoiceItem() {
        const items = this.invoiceForm.controls.items;
        items.push(this.initInvoiceItem());
    }
    saveInvoice() {
        const value = this.invoiceForm.value;
        if (typeof (value.client) === 'object') {
            value.client = value.client.id;
        }
        this.createOrUpdate(this.invoicesApi, value).subscribe(() => {
            this.router.navigateByUrl(this.config.getPrevUrl('billing/invoices')).catch(() => {
            });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["of"])(null);
    }
};
InvoiceEditFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
    { type: _shared_fleio_api_client_user_client_clients_api_service__WEBPACK_IMPORTED_MODULE_6__["ClientsApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["ActivatedRoute"] },
    { type: _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_8__["InvoicesApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_9__["ConfigService"] },
    { type: _shared_fleio_api_billing_services_service_api_service__WEBPACK_IMPORTED_MODULE_10__["ServicesApiService"] }
];
InvoiceEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-invoice-edit-form',
        template: __webpack_require__(/*! raw-loader!./invoice-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.html"),
        styles: [__webpack_require__(/*! ./invoice-edit-form.component.scss */ "./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.scss")]
    })
], InvoiceEditFormComponent);



/***/ }),

/***/ "./src/app/shared/fleio-api/billing/invoices/invoice-create-options.resolver.ts":
/*!**************************************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/invoices/invoice-create-options.resolver.ts ***!
  \**************************************************************************************/
/*! exports provided: InvoiceCreateOptionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceCreateOptionsResolver", function() { return InvoiceCreateOptionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");





let InvoiceCreateOptionsResolver = class InvoiceCreateOptionsResolver {
    constructor(invoicesApi) {
        this.invoicesApi = invoicesApi;
    }
    resolve(route, state) {
        return this.invoicesApi.createOptions().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
InvoiceCreateOptionsResolver.ctorParameters = () => [
    { type: _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__["InvoicesApiService"] }
];
InvoiceCreateOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], InvoiceCreateOptionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/billing/invoices/invoice-edit-options.resolver.ts":
/*!************************************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/invoices/invoice-edit-options.resolver.ts ***!
  \************************************************************************************/
/*! exports provided: InvoiceEditOptionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceEditOptionsResolver", function() { return InvoiceEditOptionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");





let InvoiceEditOptionsResolver = class InvoiceEditOptionsResolver {
    constructor(invoicesApi) {
        this.invoicesApi = invoicesApi;
    }
    resolve(route, state) {
        return this.invoicesApi.objectGetAction(route.params.id, 'invoice_edit_options').pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
InvoiceEditOptionsResolver.ctorParameters = () => [
    { type: _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__["InvoicesApiService"] }
];
InvoiceEditOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], InvoiceEditOptionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/billing/invoices/invoice-list.resolver.ts":
/*!****************************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/invoices/invoice-list.resolver.ts ***!
  \****************************************************************************/
/*! exports provided: InvoiceListResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceListResolver", function() { return InvoiceListResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _invoices_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");



let InvoiceListResolver = class InvoiceListResolver {
    constructor(invoicesApi) {
        this.invoicesApi = invoicesApi;
    }
    resolve(route, state) {
        return this.invoicesApi.list(route.queryParams);
    }
};
InvoiceListResolver.ctorParameters = () => [
    { type: _invoices_api_service__WEBPACK_IMPORTED_MODULE_2__["InvoicesApiService"] }
];
InvoiceListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], InvoiceListResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/billing/invoices/invoice-payment-options.resolver.ts":
/*!***************************************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/invoices/invoice-payment-options.resolver.ts ***!
  \***************************************************************************************/
/*! exports provided: InvoicePaymentOptionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoicePaymentOptionsResolver", function() { return InvoicePaymentOptionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");





let InvoicePaymentOptionsResolver = class InvoicePaymentOptionsResolver {
    constructor(invoicesApi) {
        this.invoicesApi = invoicesApi;
    }
    resolve(route, state) {
        return this.invoicesApi.objectGetAction(route.params.id, 'payment_options').pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
InvoicePaymentOptionsResolver.ctorParameters = () => [
    { type: _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__["InvoicesApiService"] }
];
InvoicePaymentOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], InvoicePaymentOptionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/billing/invoices/invoice.resolver.ts":
/*!***********************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/invoices/invoice.resolver.ts ***!
  \***********************************************************************/
/*! exports provided: InvoiceResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoiceResolver", function() { return InvoiceResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");





let InvoiceResolver = class InvoiceResolver {
    constructor(invoicesApi) {
        this.invoicesApi = invoicesApi;
    }
    resolve(route, state) {
        return this.invoicesApi.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
InvoiceResolver.ctorParameters = () => [
    { type: _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__["InvoicesApiService"] }
];
InvoiceResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], InvoiceResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/billing/transaction/transaction-api.service.ts":
/*!*********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/transaction/transaction-api.service.ts ***!
  \*********************************************************************************/
/*! exports provided: TransactionsApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TransactionsApiService", function() { return TransactionsApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let TransactionsApiService = class TransactionsApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('billing/transactions'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
TransactionsApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
TransactionsApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], TransactionsApiService);



/***/ })

}]);
//# sourceMappingURL=invoices-invoices-module-es2015.js.map