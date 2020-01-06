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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../invoice-list-ui.service */ "./src/app/reseller/billing/invoices/invoice-list-ui.service.ts");





var InvoiceCreateComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](InvoiceCreateComponent, _super);
    function InvoiceCreateComponent(route, invoiceListUIService) {
        return _super.call(this, route, invoiceListUIService, 'create', null) || this;
    }
    InvoiceCreateComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["InvoiceListUIService"] }
    ]; };
    InvoiceCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-invoice-create',
            template: __webpack_require__(/*! raw-loader!./invoice-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.html"),
            styles: [__webpack_require__(/*! ./invoice-create.component.scss */ "./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.scss")]
        })
    ], InvoiceCreateComponent);
    return InvoiceCreateComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../invoice-list-ui.service */ "./src/app/reseller/billing/invoices/invoice-list-ui.service.ts");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");





var InvoiceDetailsComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](InvoiceDetailsComponent, _super);
    function InvoiceDetailsComponent(route, invoiceListUIService) {
        return _super.call(this, route, invoiceListUIService, 'details', 'invoice') || this;
    }
    InvoiceDetailsComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_3__["InvoiceListUIService"] }
    ]; };
    InvoiceDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-invoice-details',
            template: __webpack_require__(/*! raw-loader!./invoice-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.html"),
            styles: [__webpack_require__(/*! ./invoice-details.component.scss */ "./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.scss")]
        })
    ], InvoiceDetailsComponent);
    return InvoiceDetailsComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_4__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../invoice-list-ui.service */ "./src/app/reseller/billing/invoices/invoice-list-ui.service.ts");





var InvoiceEditComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](InvoiceEditComponent, _super);
    function InvoiceEditComponent(route, invoiceListUIService) {
        return _super.call(this, route, invoiceListUIService, 'edit', 'invoice') || this;
    }
    InvoiceEditComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["InvoiceListUIService"] }
    ]; };
    InvoiceEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-invoice-edit',
            template: __webpack_require__(/*! raw-loader!./invoice-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.html"),
            styles: [__webpack_require__(/*! ./invoice-edit.component.scss */ "./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.scss")]
        })
    ], InvoiceEditComponent);
    return InvoiceEditComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _invoice_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./invoice-ui.service */ "./src/app/reseller/billing/invoices/invoice-ui.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/invoices/invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");









var InvoiceListUIService = /** @class */ (function () {
    function InvoiceListUIService(router, config, invoicesApi) {
        this.router = router;
        this.config = config;
        this.invoicesApi = invoicesApi;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_8__["DatePipe"](this.config.locale);
    }
    InvoiceListUIService.prototype.getObjectUIService = function (object, permissions, state) {
        return new _invoice_ui_service__WEBPACK_IMPORTED_MODULE_4__["InvoiceUIService"](object, permissions, state, this.router, this.config, this.invoicesApi);
    };
    InvoiceListUIService.prototype.getTableData = function (objectList) {
        var e_1, _a;
        var tableData = {
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
        try {
            for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](objectList.objects), _c = _b.next(); !_c.done; _c = _b.next()) {
                var invoice = _c.value;
                var rowUIService = this.getObjectUIService(invoice, objectList.permissions, 'table-view');
                var row = {
                    cells: {
                        display_number: { text: invoice.display_number },
                        status: { text: invoice.status.toLocaleUpperCase() },
                        issue_date: { text: this.datePipe.transform(invoice.issue_date) },
                        total: { text: invoice.total + " " + invoice.currency },
                    },
                    icon: rowUIService.getIcon(),
                    status: rowUIService.getStatus(),
                    actions: rowUIService.getActions(),
                    url: rowUIService.getDetailsLink(),
                };
                tableData.rows.push(row);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return tableData;
    };
    InvoiceListUIService.prototype.getActions = function (objectList) {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__["RouterLinkAction"]({
                icon: { name: 'add' },
                name: 'Create',
                tooltip: 'Create new invoice',
                routerUrl: this.config.getPanelUrl("billing/invoices/create"),
                router: this.router,
            }),
        ];
    };
    InvoiceListUIService.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
        { type: _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_6__["InvoicesApiService"] }
    ]; };
    InvoiceListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root',
        })
    ], InvoiceListUIService);
    return InvoiceListUIService;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../invoice-list-ui.service */ "./src/app/reseller/billing/invoices/invoice-list-ui.service.ts");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");






var InvoiceListComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](InvoiceListComponent, _super);
    function InvoiceListComponent(route, invoiceListUIService, refreshService) {
        var _this = _super.call(this, route, invoiceListUIService, refreshService, 'invoices') || this;
        _this.route = route;
        _this.invoiceListUIService = invoiceListUIService;
        _this.refreshService = refreshService;
        return _this;
    }
    InvoiceListComponent.prototype.ngOnInit = function () {
        _super.prototype.ngOnInit.call(this);
    };
    InvoiceListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
        { type: _invoice_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["InvoiceListUIService"] },
        { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_3__["RefreshService"] }
    ]; };
    InvoiceListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-invoice-list',
            template: __webpack_require__(/*! raw-loader!./invoice-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.html"),
            styles: [__webpack_require__(/*! ./invoice-list.component.scss */ "./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.scss")]
        })
    ], InvoiceListComponent);
    return InvoiceListComponent;
}(_shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_5__["ListBase"]));



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
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/object-status */ "./src/app/shared/ui/objects-view/interfaces/object-status.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _tabs_invoice_details_overview_invoice_details_overview_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./tabs/invoice-details-overview/invoice-details-overview.component */ "./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.ts");
/* harmony import */ var _tabs_invoice_details_add_payment_invoice_details_add_payment_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tabs/invoice-details-add-payment/invoice-details-add-payment.component */ "./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.ts");
/* harmony import */ var _tabs_invoice_edit_form_invoice_edit_form_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/invoice-edit-form/invoice-edit-form.component */ "./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.ts");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/invoices/invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");












var InvoiceUIService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](InvoiceUIService, _super);
    function InvoiceUIService(invoice, permissions, state, router, config, invoicesApi) {
        var _this = _super.call(this, invoice, permissions, state) || this;
        _this.router = router;
        _this.config = config;
        _this.invoicesApi = invoicesApi;
        return _this;
    }
    InvoiceUIService.prototype.getIcon = function () {
        return null;
    };
    InvoiceUIService.prototype.getStatus = function () {
        var status = null;
        switch (this.object.status) {
            case 'paid':
                status = { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Paid };
                break;
            case 'cancelled':
                status = { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Cancelled };
                break;
            case 'refunded':
                status = { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Refunded };
                break;
            case 'unpaid':
                if (new Date(this.object.due_date) > new Date()) {
                    status = { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Overdue };
                }
                else {
                    status = { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Unpaid };
                }
                break;
        }
        if (['card-view', 'table-view', 'details'].includes(this.state)) {
            return status;
        }
        return null;
    };
    InvoiceUIService.prototype.getTitle = function () {
        switch (this.state) {
            case 'edit':
                return {
                    text: "Edit invoice " + this.object.display_number,
                    subText: this.object.status.toLocaleUpperCase(),
                };
            case 'create':
                return {
                    text: "Create invoice",
                };
            default:
                return {
                    text: "Proforma " + this.object.display_number,
                    subText: this.object.status.toLocaleUpperCase(),
                };
        }
    };
    InvoiceUIService.prototype.getActions = function () {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                icon: { name: 'edit' },
                name: 'Edit',
                tooltip: 'Edit invoice',
                routerUrl: this.config.getPanelUrl("billing/invoices/" + this.object.id + "/edit"),
                router: this.router,
            }),
            new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_10__["ApiCallAction"]({
                object: this.object,
                icon: { name: 'delete' },
                name: 'Delete',
                tooltip: 'Delete',
                confirmOptions: {
                    confirm: true,
                    title: 'Delete invoice',
                    message: "Are you sure you want to delete invoice " + this.object.display_number,
                },
                apiService: this.invoicesApi,
                callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_10__["CallType"].Delete,
                refreshAfterExecute: false,
                redirectAfterExecute: true,
                redirectUrl: this.config.getPanelUrl('billing/invoices'),
            })
        ];
    };
    InvoiceUIService.prototype.getDetailsActions = function () {
        var actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("billing/invoices"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_9__["CallbackAction"]({ name: 'Create invoice' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("billing/invoices"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_9__["CallbackAction"]({ name: 'Save invoice' }));
                break;
            default:
                break;
        }
        return actions;
    };
    InvoiceUIService.prototype.getCardTags = function () {
        return [];
    };
    InvoiceUIService.prototype.getDetailsLink = function () {
        return this.config.getPanelUrl("billing/invoices/" + this.object.id);
    };
    InvoiceUIService.prototype.getCardFields = function () {
        return [
            {
                name: 'Issue date',
                value: "" + this.object.issue_date
            },
            {
                name: 'Total',
                value: this.object.total + " " + this.object.currency
            },
            {
                name: 'Client',
                value: this.object.client ? "" + this.object.client.name : 'n/a',
            }
        ];
    };
    InvoiceUIService.prototype.getTabs = function () {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Details',
                        component: _tabs_invoice_details_overview_invoice_details_overview_component__WEBPACK_IMPORTED_MODULE_6__["InvoiceDetailsOverviewComponent"],
                    },
                    {
                        tabName: 'Add payment',
                        component: _tabs_invoice_details_add_payment_invoice_details_add_payment_component__WEBPACK_IMPORTED_MODULE_7__["InvoiceDetailsAddPaymentComponent"],
                    },
                ];
            case 'edit':
            case 'create':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_invoice_edit_form_invoice_edit_form_component__WEBPACK_IMPORTED_MODULE_8__["InvoiceEditFormComponent"],
                    }
                ];
            default:
                return null;
        }
    };
    InvoiceUIService.ctorParameters = function () { return [
        { type: undefined },
        { type: undefined },
        { type: String },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
        { type: _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_11__["InvoicesApiService"] }
    ]; };
    return InvoiceUIService;
}(_shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_2__["ObjectUIServiceBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
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















var routes = [
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
                    objectList: function (data) {
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
                getBreadCrumbDetail: function (data) {
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
                getBreadCrumbDetail: function (data) {
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
                getBreadCrumbDetail: function (data) {
                    return data.invoice.display_number;
                },
            },
        }
    },
];
var InvoicesRoutingModule = /** @class */ (function () {
    function InvoicesRoutingModule() {
    }
    InvoicesRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
        })
    ], InvoicesRoutingModule);
    return InvoicesRoutingModule;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _invoice_list_invoice_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoice-list/invoice-list.component */ "./src/app/reseller/billing/invoices/invoice-list/invoice-list.component.ts");
/* harmony import */ var _invoice_details_invoice_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./invoice-details/invoice-details.component */ "./src/app/reseller/billing/invoices/invoice-details/invoice-details.component.ts");
/* harmony import */ var _invoices_routing_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./invoices-routing.module */ "./src/app/reseller/billing/invoices/invoices-routing.module.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _invoice_create_invoice_create_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./invoice-create/invoice-create.component */ "./src/app/reseller/billing/invoices/invoice-create/invoice-create.component.ts");
/* harmony import */ var _tabs_invoice_details_overview_invoice_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/invoice-details-overview/invoice-details-overview.component */ "./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.ts");
/* harmony import */ var _tabs_invoice_edit_form_invoice_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/invoice-edit-form/invoice-edit-form.component */ "./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.ts");
/* harmony import */ var _tabs_invoice_details_add_payment_invoice_details_add_payment_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/invoice-details-add-payment/invoice-details-add-payment.component */ "./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/icon */ "./node_modules/@angular/material/esm5/icon.es5.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm5/button.es5.js");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/divider */ "./node_modules/@angular/material/esm5/divider.es5.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _invoice_edit_invoice_edit_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./invoice-edit/invoice-edit.component */ "./src/app/reseller/billing/invoices/invoice-edit/invoice-edit.component.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm5/form-field.es5.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm5/input.es5.js");
/* harmony import */ var _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @angular/material/autocomplete */ "./node_modules/@angular/material/esm5/autocomplete.es5.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm5/select.es5.js");
/* harmony import */ var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @angular/material/datepicker */ "./node_modules/@angular/material/esm5/datepicker.es5.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm5/checkbox.es5.js");
























var InvoicesModule = /** @class */ (function () {
    function InvoicesModule() {
    }
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
    return InvoicesModule;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../shared/fleio-api/billing/invoices/invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../../../shared/ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");










var InvoiceDetailsAddPaymentComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](InvoiceDetailsAddPaymentComponent, _super);
    function InvoiceDetailsAddPaymentComponent(formBuilder, activatedRoute, invoicesApi, notification, refreshService) {
        var _this = _super.call(this) || this;
        _this.formBuilder = formBuilder;
        _this.activatedRoute = activatedRoute;
        _this.invoicesApi = invoicesApi;
        _this.notification = notification;
        _this.refreshService = refreshService;
        _this.addPaymentForm = _this.formBuilder.group({
            external_id: [''],
            extra_info: [''],
            date_initiated: [_angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            gateway: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            currency: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            amount: [0, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            fee: [0, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
        });
        return _this;
    }
    InvoiceDetailsAddPaymentComponent.prototype.ngOnInit = function () {
        this.paymentOptions = this.activatedRoute.snapshot.data.paymentOptions;
        this.addPaymentForm.patchValue({
            date_initiated: new Date(),
            amount: this.object.balance,
            currency: this.paymentOptions.currencies[0].code,
            gateway: this.paymentOptions.gateways[0].id,
        });
    };
    InvoiceDetailsAddPaymentComponent.prototype.addPayment = function () {
        var _this = this;
        this.validate();
        if (this.addPaymentForm.invalid) {
            Object.keys(this.formGroup.controls).map(function (name) {
                var control = _this.formGroup.controls[name];
                if (control.invalid) {
                    control.markAsTouched();
                }
            });
        }
        else {
            var value = this.addPaymentForm.value;
            value.invoice = this.object.id;
            var request = this.invoicesApi.objectPostAction(this.object.id, 'add_payment_to_invoice', value);
            request.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["catchError"])(function (error) {
                if (error.error) {
                    _this.setErrors(error.error);
                    return rxjs__WEBPACK_IMPORTED_MODULE_5__["EMPTY"];
                }
                else {
                    throw error;
                }
            })).subscribe(function () {
                _this.notification.showMessage('Payment added');
                _this.refreshService.refresh();
            });
        }
    };
    InvoiceDetailsAddPaymentComponent.ctorParameters = function () { return [
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
        { type: _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_7__["InvoicesApiService"] },
        { type: _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_8__["NotificationService"] },
        { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_9__["RefreshService"] }
    ]; };
    InvoiceDetailsAddPaymentComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-invoice-details-add-payment',
            template: __webpack_require__(/*! raw-loader!./invoice-details-add-payment.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.html"),
            styles: [__webpack_require__(/*! ./invoice-details-add-payment.component.scss */ "./src/app/reseller/billing/invoices/tabs/invoice-details-add-payment/invoice-details-add-payment.component.scss")]
        })
    ], InvoiceDetailsAddPaymentComponent);
    return InvoiceDetailsAddPaymentComponent;
}(_shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _shared_fleio_api_billing_transaction_transaction_api_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/fleio-api/billing/transaction/transaction-api.service */ "./src/app/shared/fleio-api/billing/transaction/transaction-api.service.ts");
/* harmony import */ var _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");







var InvoiceDetailsOverviewComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](InvoiceDetailsOverviewComponent, _super);
    function InvoiceDetailsOverviewComponent(config, refreshService, transactionApi, notificationService) {
        var _this = _super.call(this) || this;
        _this.config = config;
        _this.refreshService = refreshService;
        _this.transactionApi = transactionApi;
        _this.notificationService = notificationService;
        return _this;
    }
    InvoiceDetailsOverviewComponent.prototype.ngOnInit = function () {
        this.downloadPdfUrl = this.config.getPanelApiUrl("billing/invoices/" + this.object.id + "/download?content_type=pdf");
    };
    InvoiceDetailsOverviewComponent.prototype.deleteTransaction = function (transaction) {
        var _this = this;
        this.notificationService.confirmDialog({
            title: 'Delete transaction',
            message: 'Are you sure you want to delete transaction?'
        }).subscribe(function (result) {
            if (result === 'yes') {
                _this.transactionApi.delete(transaction.id).subscribe(function () {
                    _this.refreshService.refresh();
                });
            }
        });
    };
    InvoiceDetailsOverviewComponent.ctorParameters = function () { return [
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
        { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] },
        { type: _shared_fleio_api_billing_transaction_transaction_api_service__WEBPACK_IMPORTED_MODULE_5__["TransactionsApiService"] },
        { type: _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_6__["NotificationService"] }
    ]; };
    InvoiceDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-invoice-details-overview',
            template: __webpack_require__(/*! raw-loader!./invoice-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.html"),
            styles: [__webpack_require__(/*! ./invoice-details-overview.component.scss */ "./src/app/reseller/billing/invoices/tabs/invoice-details-overview/invoice-details-overview.component.scss")]
        })
    ], InvoiceDetailsOverviewComponent);
    return InvoiceDetailsOverviewComponent;
}(_shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _shared_fleio_api_client_user_client_clients_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/fleio-api/client-user/client/clients-api.service */ "./src/app/shared/fleio-api/client-user/client/clients-api.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../../../shared/fleio-api/billing/invoices/invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_billing_services_service_api_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../../../shared/fleio-api/billing/services/service-api.service */ "./src/app/shared/fleio-api/billing/services/service-api.service.ts");











var InvoiceEditFormComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](InvoiceEditFormComponent, _super);
    function InvoiceEditFormComponent(formBuilder, clientsApi, activatedRoute, invoicesApi, router, config, servicesApi) {
        var _this = _super.call(this) || this;
        _this.formBuilder = formBuilder;
        _this.clientsApi = clientsApi;
        _this.activatedRoute = activatedRoute;
        _this.invoicesApi = invoicesApi;
        _this.router = router;
        _this.config = config;
        _this.servicesApi = servicesApi;
        _this.invoiceForm = _this.formBuilder.group({
            client: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            status: ['unpaid', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            issue_date: [Date.now(), _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            due_date: [Date.now(), _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            items: _this.formBuilder.array([]),
        });
        _this.client = _this.invoiceForm.controls.client;
        return _this;
    }
    InvoiceEditFormComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.objectController.actionCallback = function () { return _this.saveInvoice(); };
        this.createOptions = this.activatedRoute.snapshot.data.createOptions;
        if (Object.keys(this.object).length > 0) {
            this.invoiceForm.patchValue(this.object);
            if (this.object.items) {
                this.object.items.map(function (item) { return _this.invoiceForm.controls.items.push(_this.initInvoiceItem(item)); });
            }
        }
        else {
            this.invoiceForm.patchValue({
                issue_date: new Date(),
                due_date: new Date(),
            });
            var queryParams = this.activatedRoute.snapshot.queryParams;
            if (queryParams.client_id) {
                this.clientsApi.get(queryParams.client_id).subscribe(function (client) {
                    _this.client.setValue(client);
                });
            }
        }
        this.filteredClients$ = this.client.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["startWith"])(''), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(function (value) {
            return typeof value === 'string' ? value : value.id;
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["mergeMap"])(function (value) {
            return _this.clientsApi.list({
                search: value,
            }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(function (clientsList) { return clientsList.objects; }));
        }));
        if (!this.object.id) {
            this.client.valueChanges.subscribe(function (client) {
                _this.servicesApi.list({
                    client: client.id,
                }).subscribe(function (services) {
                    _this.createOptions.services = services.objects;
                });
            });
        }
    };
    InvoiceEditFormComponent.prototype.clientDisplay = function (client) {
        if (client) {
            return client.name ? client.name : client.first_name + " " + client.last_name;
        }
        else {
            return undefined;
        }
    };
    InvoiceEditFormComponent.prototype.initInvoiceItem = function (item) {
        if (item === void 0) { item = null; }
        return this.formBuilder.group({
            description: [item ? item.description : '', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            amount: [item ? item.amount : '', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            item_type: [item ? item.item_type : '', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            service: [item ? item.service : ''],
            taxed: [item ? item.taxed : false],
        });
    };
    InvoiceEditFormComponent.prototype.addInvoiceItem = function () {
        var items = this.invoiceForm.controls.items;
        items.push(this.initInvoiceItem());
    };
    InvoiceEditFormComponent.prototype.saveInvoice = function () {
        var _this = this;
        var value = this.invoiceForm.value;
        if (typeof (value.client) === 'object') {
            value.client = value.client.id;
        }
        this.createOrUpdate(this.invoicesApi, value).subscribe(function () {
            _this.router.navigateByUrl(_this.config.getPrevUrl('billing/invoices')).catch(function () {
            });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["of"])(null);
    };
    InvoiceEditFormComponent.ctorParameters = function () { return [
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
        { type: _shared_fleio_api_client_user_client_clients_api_service__WEBPACK_IMPORTED_MODULE_6__["ClientsApiService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["ActivatedRoute"] },
        { type: _shared_fleio_api_billing_invoices_invoices_api_service__WEBPACK_IMPORTED_MODULE_8__["InvoicesApiService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_9__["ConfigService"] },
        { type: _shared_fleio_api_billing_services_service_api_service__WEBPACK_IMPORTED_MODULE_10__["ServicesApiService"] }
    ]; };
    InvoiceEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-invoice-edit-form',
            template: __webpack_require__(/*! raw-loader!./invoice-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.html"),
            styles: [__webpack_require__(/*! ./invoice-edit-form.component.scss */ "./src/app/reseller/billing/invoices/tabs/invoice-edit-form/invoice-edit-form.component.scss")]
        })
    ], InvoiceEditFormComponent);
    return InvoiceEditFormComponent;
}(_shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");





var InvoiceCreateOptionsResolver = /** @class */ (function () {
    function InvoiceCreateOptionsResolver(invoicesApi) {
        this.invoicesApi = invoicesApi;
    }
    InvoiceCreateOptionsResolver.prototype.resolve = function (route, state) {
        return this.invoicesApi.createOptions().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    InvoiceCreateOptionsResolver.ctorParameters = function () { return [
        { type: _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__["InvoicesApiService"] }
    ]; };
    InvoiceCreateOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], InvoiceCreateOptionsResolver);
    return InvoiceCreateOptionsResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");





var InvoiceEditOptionsResolver = /** @class */ (function () {
    function InvoiceEditOptionsResolver(invoicesApi) {
        this.invoicesApi = invoicesApi;
    }
    InvoiceEditOptionsResolver.prototype.resolve = function (route, state) {
        return this.invoicesApi.objectGetAction(route.params.id, 'invoice_edit_options').pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    InvoiceEditOptionsResolver.ctorParameters = function () { return [
        { type: _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__["InvoicesApiService"] }
    ]; };
    InvoiceEditOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], InvoiceEditOptionsResolver);
    return InvoiceEditOptionsResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _invoices_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");



var InvoiceListResolver = /** @class */ (function () {
    function InvoiceListResolver(invoicesApi) {
        this.invoicesApi = invoicesApi;
    }
    InvoiceListResolver.prototype.resolve = function (route, state) {
        return this.invoicesApi.list(route.queryParams);
    };
    InvoiceListResolver.ctorParameters = function () { return [
        { type: _invoices_api_service__WEBPACK_IMPORTED_MODULE_2__["InvoicesApiService"] }
    ]; };
    InvoiceListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], InvoiceListResolver);
    return InvoiceListResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");





var InvoicePaymentOptionsResolver = /** @class */ (function () {
    function InvoicePaymentOptionsResolver(invoicesApi) {
        this.invoicesApi = invoicesApi;
    }
    InvoicePaymentOptionsResolver.prototype.resolve = function (route, state) {
        return this.invoicesApi.objectGetAction(route.params.id, 'payment_options').pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    InvoicePaymentOptionsResolver.ctorParameters = function () { return [
        { type: _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__["InvoicesApiService"] }
    ]; };
    InvoicePaymentOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], InvoicePaymentOptionsResolver);
    return InvoicePaymentOptionsResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./invoices-api.service */ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");





var InvoiceResolver = /** @class */ (function () {
    function InvoiceResolver(invoicesApi) {
        this.invoicesApi = invoicesApi;
    }
    InvoiceResolver.prototype.resolve = function (route, state) {
        return this.invoicesApi.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    InvoiceResolver.ctorParameters = function () { return [
        { type: _invoices_api_service__WEBPACK_IMPORTED_MODULE_3__["InvoicesApiService"] }
    ]; };
    InvoiceResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], InvoiceResolver);
    return InvoiceResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var TransactionsApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](TransactionsApiService, _super);
    // noinspection JSUnusedGlobalSymbols
    function TransactionsApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('billing/transactions')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    TransactionsApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    TransactionsApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], TransactionsApiService);
    return TransactionsApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ })

}]);
//# sourceMappingURL=invoices-invoices-module-es5.js.map