(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["services-services-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/services/service-details/service-details.component.html":
/*!********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/services/service-details/service-details.component.html ***!
  \********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\"></app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/services/service-edit/service-edit.component.html":
/*!**************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/services/service-edit/service-edit.component.html ***!
  \**************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/services/service-list/service-list.component.html":
/*!**************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/services/service-list/service-list.component.html ***!
  \**************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-objects-view [objectsListController]=\"objectListController\"></app-objects-view>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/services/tabs/service-details-overview/service-details-overview.component.html":
/*!*******************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/services/tabs/service-details-overview/service-details-overview.component.html ***!
  \*******************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxLayout=\"column\">\n  <p class=\"fl-detail\">Product: {{object.product.name || 'n/a'}}</p>\n  <p class=\"fl-detail\">\n    <a class=\"active-link\"\n       routerLink=\"{{config.getPanelUrl('billing/invoices/filtering=items__service:' + object.id)}}\">\n      Related invoices\n    </a>\n  </p>\n  <p class=\"fl-detail\">Billing cycle: {{object.cycle.display_name}}</p>\n  <p class=\"fl-detail\">Created at: {{object.created_at}}</p>\n  <p class=\"fl-detail\">Next due date: {{object.next_due_date}}</p>\n  <p class=\"fl-detail\">Next invoice date: {{object.next_invoice_date}}</p>\n  <p class=\"fl-detail\">\n    Client:\n    <a class=\"active-link\"\n       routerLink=\"{{config.getPanelUrl('clients-users/clients/' + object.client.id)}}\">\n      {{object.client.name}}\n    </a>\n  </p>\n  <p class=\"fl-detail\">Last update: {{object.updated_at}}</p>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/services/tabs/service-edit-form/service-edit-form.component.html":
/*!*****************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/services/tabs/service-edit-form/service-edit-form.component.html ***!
  \*****************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form [formGroup]=\"serviceForm\">\n  <app-form-errors #formErrors [formGroup]=\"serviceForm\"></app-form-errors>\n  <div fxLayout=\"column\">\n    <p class=\"fl-detail\">\n      Client:\n      <a class=\"active-link\"\n         routerLink=\"{{config.getPanelUrl('clients-users/clients/' + object.client.id)}}\">\n        {{object.client.name}}\n      </a>\n    </p>\n    <mat-form-field>\n      <input matInput placeholder=\"Display name\" type=\"text\" formControlName=\"display_name\" required>\n      <mat-error>{{backendErrors['display_name'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n    <p class=\"fl-detail\">Product: {{object.product.name}}</p>\n    <p class=\"fl-detail\">Cycle: {{object.cycle.display_name}}</p>\n    <mat-form-field>\n      <textarea matInput rows=\"3\" maxlength=\"255\"\n                placeholder=\"Notes\" formControlName=\"notes\">\n      </textarea>\n      <mat-error>{{backendErrors['notes']}}</mat-error>\n    </mat-form-field>\n    <mat-form-field>\n      <input matInput placeholder=\"Override price\" type=\"number\" formControlName=\"override_price\">\n      <mat-error>{{backendErrors['override_price']}}</mat-error>\n    </mat-form-field>\n    <div fxLayout=\"row\">\n      <div fxFlex=\"50\">\n        <mat-form-field>\n          <input matInput [matDatepicker]=\"overrideSuspendUntilDatePicker\"\n                 formControlName=\"override_suspend_until\" placeholder=\"Do not suspend until\">\n          <mat-datepicker-toggle matSuffix [for]=\"overrideSuspendUntilDatePicker\"></mat-datepicker-toggle>\n          <mat-datepicker #overrideSuspendUntilDatePicker></mat-datepicker>\n          <mat-error>{{ backendErrors['override_suspend_until']}}</mat-error>\n        </mat-form-field>\n        <button mat-icon-button fl-tooltip=\"Clear do not suspend until date\"\n                (click)=\"serviceForm.controls.override_suspend_until.setValue(undefined)\">\n          <mat-icon>delete</mat-icon>\n        </button>\n      </div>\n      <div fxFlex=\"50\">\n        <mat-form-field>\n          <input matInput [matDatepicker]=\"nextDueDatePicker\"\n                 formControlName=\"next_due_date\" placeholder=\"Next due date\">\n          <mat-datepicker-toggle matSuffix [for]=\"nextDueDatePicker\"></mat-datepicker-toggle>\n          <mat-datepicker #nextDueDatePicker></mat-datepicker>\n          <mat-error>{{ backendErrors['next_due_date']}}</mat-error>\n        </mat-form-field>\n        <button mat-icon-button fl-tooltip=\"Clear next due date\"\n                (click)=\"serviceForm.controls.next_due_date.setValue(undefined)\">\n          <mat-icon>delete</mat-icon>\n        </button>\n      </div>\n    </div>\n    <div fxLayout=\"row\">\n      <div fxFlex=\"50\">\n        <mat-form-field>\n          <input matInput [matDatepicker]=\"nextExpirationDatePicker\"\n                 formControlName=\"next_expiration_date\" placeholder=\"Next expiration date\">\n          <mat-datepicker-toggle matSuffix [for]=\"nextExpirationDatePicker\"></mat-datepicker-toggle>\n          <mat-datepicker #nextExpirationDatePicker></mat-datepicker>\n          <mat-error>{{ backendErrors['next_expiration_date']}}</mat-error>\n        </mat-form-field>\n        <button mat-icon-button fl-tooltip=\"Clear next expiration date\"\n                (click)=\"serviceForm.controls.next_expiration_date.setValue(undefined)\">\n          <mat-icon>delete</mat-icon>\n        </button>\n      </div>\n      <div fxFlex=\"50\">\n        <mat-form-field>\n          <input matInput [matDatepicker]=\"nextInvoiceDatePicker\"\n                 formControlName=\"next_invoice_date\" placeholder=\"Next invoice date\">\n          <mat-datepicker-toggle matSuffix [for]=\"nextInvoiceDatePicker\"></mat-datepicker-toggle>\n          <mat-datepicker #nextInvoiceDatePicker></mat-datepicker>\n          <mat-error>{{ backendErrors['next_invoice_date']}}</mat-error>\n        </mat-form-field>\n        <button mat-icon-button fl-tooltip=\"Clear next invoice date\"\n                (click)=\"serviceForm.controls.next_invoice_date.setValue(undefined)\">\n          <mat-icon>delete</mat-icon>\n        </button>\n      </div>\n    </div>\n  </div>\n</form>\n"

/***/ }),

/***/ "./src/app/reseller/billing/services/service-details/service-details.component.scss":
/*!******************************************************************************************!*\
  !*** ./src/app/reseller/billing/services/service-details/service-details.component.scss ***!
  \******************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvc2VydmljZXMvc2VydmljZS1kZXRhaWxzL3NlcnZpY2UtZGV0YWlscy5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/billing/services/service-details/service-details.component.ts":
/*!****************************************************************************************!*\
  !*** ./src/app/reseller/billing/services/service-details/service-details.component.ts ***!
  \****************************************************************************************/
/*! exports provided: ServiceDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceDetailsComponent", function() { return ServiceDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _service_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../service-list-ui.service */ "./src/app/reseller/billing/services/service-list-ui.service.ts");





let ServiceDetailsComponent = class ServiceDetailsComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, serviceListUIService) {
        super(route, serviceListUIService, 'details', 'service');
    }
};
ServiceDetailsComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _service_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ServiceListUIService"] }
];
ServiceDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-service-details',
        template: __webpack_require__(/*! raw-loader!./service-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/services/service-details/service-details.component.html"),
        styles: [__webpack_require__(/*! ./service-details.component.scss */ "./src/app/reseller/billing/services/service-details/service-details.component.scss")]
    })
], ServiceDetailsComponent);



/***/ }),

/***/ "./src/app/reseller/billing/services/service-edit/service-edit.component.scss":
/*!************************************************************************************!*\
  !*** ./src/app/reseller/billing/services/service-edit/service-edit.component.scss ***!
  \************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvc2VydmljZXMvc2VydmljZS1lZGl0L3NlcnZpY2UtZWRpdC5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/billing/services/service-edit/service-edit.component.ts":
/*!**********************************************************************************!*\
  !*** ./src/app/reseller/billing/services/service-edit/service-edit.component.ts ***!
  \**********************************************************************************/
/*! exports provided: ServiceEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceEditComponent", function() { return ServiceEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _service_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../service-list-ui.service */ "./src/app/reseller/billing/services/service-list-ui.service.ts");





let ServiceEditComponent = class ServiceEditComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, serviceListUIService) {
        super(route, serviceListUIService, 'edit', 'service');
    }
};
ServiceEditComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _service_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ServiceListUIService"] }
];
ServiceEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-service-edit',
        template: __webpack_require__(/*! raw-loader!./service-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/services/service-edit/service-edit.component.html"),
        styles: [__webpack_require__(/*! ./service-edit.component.scss */ "./src/app/reseller/billing/services/service-edit/service-edit.component.scss")]
    })
], ServiceEditComponent);



/***/ }),

/***/ "./src/app/reseller/billing/services/service-list-ui.service.ts":
/*!**********************************************************************!*\
  !*** ./src/app/reseller/billing/services/service-list-ui.service.ts ***!
  \**********************************************************************/
/*! exports provided: ServiceListUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceListUIService", function() { return ServiceListUIService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_fleio_api_billing_services_service_api_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/services/service-api.service */ "./src/app/shared/fleio-api/billing/services/service-api.service.ts");
/* harmony import */ var _service_ui_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./service-ui.service */ "./src/app/reseller/billing/services/service-ui.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");








let ServiceListUIService = class ServiceListUIService {
    constructor(router, config, servicesApiService) {
        this.router = router;
        this.config = config;
        this.servicesApiService = servicesApiService;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_7__["DatePipe"](this.config.locale);
    }
    getObjectUIService(object, permissions, state) {
        return new _service_ui_service__WEBPACK_IMPORTED_MODULE_6__["ServiceUIService"](object, permissions, state, this.router, this.config, this.servicesApiService);
    }
    getTableData(objectList) {
        const tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Name', enableSort: true, fieldName: 'name' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Client', enableSort: true, fieldName: 'client' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Created at', enableSort: true, fieldName: 'created_at' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Next due date', enableSort: true, fieldName: 'next_due_date' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Status', enableSort: true, fieldName: 'status' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Actions, displayName: 'Actions', enableSort: true, fieldName: '(actions)' },
                ],
                columnNames: ['name', 'client', 'created_at', 'next_due_date', 'status', '(actions)'],
                statusColumn: 'name',
            },
            rows: [],
        };
        for (const service of objectList.objects) {
            const rowUIService = this.getObjectUIService(service, objectList.permissions, 'table-view');
            const row = {
                cells: {
                    name: { text: service.display_name },
                    client: {
                        text: service.client.name,
                        url: this.config.getPanelUrl(`clients-users/clients/${service.client.id}`)
                    },
                    created_at: { text: this.datePipe.transform(service.created_at) },
                    next_due_date: { text: this.datePipe.transform(service.next_due_date) },
                    status: { text: service.status.toLocaleUpperCase() },
                },
                icon: rowUIService.getIcon(),
                status: rowUIService.getStatus(),
                actions: rowUIService.getActions(),
                url: rowUIService.getDetailsLink()
            };
            tableData.rows.push(row);
        }
        return tableData;
    }
    getActions(objectList) {
        return null;
    }
};
ServiceListUIService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_billing_services_service_api_service__WEBPACK_IMPORTED_MODULE_5__["ServicesApiService"] }
];
ServiceListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ServiceListUIService);



/***/ }),

/***/ "./src/app/reseller/billing/services/service-list/service-list.component.scss":
/*!************************************************************************************!*\
  !*** ./src/app/reseller/billing/services/service-list/service-list.component.scss ***!
  \************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvc2VydmljZXMvc2VydmljZS1saXN0L3NlcnZpY2UtbGlzdC5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/billing/services/service-list/service-list.component.ts":
/*!**********************************************************************************!*\
  !*** ./src/app/reseller/billing/services/service-list/service-list.component.ts ***!
  \**********************************************************************************/
/*! exports provided: ServiceListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceListComponent", function() { return ServiceListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _service_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../service-list-ui.service */ "./src/app/reseller/billing/services/service-list-ui.service.ts");






let ServiceListComponent = class ServiceListComponent extends _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"] {
    constructor(route, serviceListUIService, refreshService) {
        super(route, serviceListUIService, refreshService, 'services');
        this.route = route;
        this.serviceListUIService = serviceListUIService;
        this.refreshService = refreshService;
    }
    ngOnInit() {
        super.ngOnInit();
    }
};
ServiceListComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _service_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["ServiceListUIService"] },
    { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
];
ServiceListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-service-list',
        template: __webpack_require__(/*! raw-loader!./service-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/services/service-list/service-list.component.html"),
        styles: [__webpack_require__(/*! ./service-list.component.scss */ "./src/app/reseller/billing/services/service-list/service-list.component.scss")]
    })
], ServiceListComponent);



/***/ }),

/***/ "./src/app/reseller/billing/services/service-ui.service.ts":
/*!*****************************************************************!*\
  !*** ./src/app/reseller/billing/services/service-ui.service.ts ***!
  \*****************************************************************/
/*! exports provided: ServiceUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceUIService", function() { return ServiceUIService; });
/* harmony import */ var _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/object-status */ "./src/app/shared/ui/objects-view/interfaces/object-status.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _shared_fleio_api_billing_services_service_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/services/service-api.service */ "./src/app/shared/fleio-api/billing/services/service-api.service.ts");
/* harmony import */ var _tabs_service_details_overview_service_details_overview_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tabs/service-details-overview/service-details-overview.component */ "./src/app/reseller/billing/services/tabs/service-details-overview/service-details-overview.component.ts");
/* harmony import */ var _tabs_service_edit_form_service_edit_form_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/service-edit-form/service-edit-form.component */ "./src/app/reseller/billing/services/tabs/service-edit-form/service-edit-form.component.ts");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");











class ServiceUIService extends _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__["ObjectUIServiceBase"] {
    constructor(service, permissions, state, router, config, servicesApiService) {
        super(service, permissions, state);
        this.router = router;
        this.config = config;
        this.servicesApiService = servicesApiService;
    }
    getIcon() {
        return null;
    }
    getStatus() {
        switch (this.object.status) {
            case 'active':
                return { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Active };
            case 'suspended':
                return { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Suspended };
            case 'deleting':
                return { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Changing, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Error };
            default:
                return { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].None, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].None };
        }
    }
    getTitle() {
        switch (this.state) {
            case 'edit':
                return {
                    text: `Edit ${this.object.display_name}`,
                    subText: this.object.status.toLocaleUpperCase(),
                };
            case 'create':
                return {
                    text: 'Create service',
                };
            case 'details':
            default:
                return {
                    text: `${this.object.display_name}`,
                    subText: this.object.status.toLocaleUpperCase(),
                };
        }
    }
    getActions() {
        const actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            tooltip: 'Edit service',
            name: 'Edit',
            routerUrl: this.config.getPanelUrl(`billing/services/${this.object.id}/edit`),
            router: this.router,
        }));
        switch (this.object.status) {
            case 'active':
                actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["ApiCallAction"]({
                    object: this.object,
                    icon: { name: 'pause' },
                    tooltip: 'Suspend service',
                    name: 'Suspend',
                    confirmOptions: {
                        confirm: true,
                        title: 'Suspend service',
                        message: `Are you sure you want to suspend service ${this.object.display_name} and all associated resources`
                    },
                    apiService: this.servicesApiService,
                    apiAction: 'suspend',
                }));
                break;
            case 'suspended':
                actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["ApiCallAction"]({
                    object: this.object,
                    icon: { name: 'play_arrow' },
                    tooltip: 'Resume service',
                    name: 'Resume',
                    confirmOptions: {
                        confirm: false,
                        title: 'Resume service',
                        message: `Are you sure you want to resume service ${this.object.display_name}`
                    },
                    apiService: this.servicesApiService,
                    apiAction: 'resume',
                }));
                break;
            // case 'terminated':
            //   actions.push(new ApiCallAction(
            //     {
            //       object: this.object,
            //       icon: {name: 'add'},
            //       tooltip: 'Activate service',
            //       name: 'Activate',
            //       confirmOptions: {
            //         confirm: true,
            //         title: 'Activate service',
            //         message: `Activate service ${this.object.display_name}`,
            //       },
            //       apiService: this.servicesApiService,
            //       apiAction: 'activate',
            //     }
            //   ));
            //   break;
        }
        if (this.object.status !== 'terminated') {
            actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["ApiCallAction"]({
                object: this.object,
                icon: { name: 'delete' },
                tooltip: 'Terminate service',
                name: 'Terminate',
                confirmOptions: {
                    confirm: true,
                    title: 'Terminate service',
                    message: `Are you sure you want to terminate service ${this.object.display_name}`,
                },
                apiService: this.servicesApiService,
                apiAction: 'terminate',
            }));
        }
        return actions;
    }
    getDetailsLink() {
        return this.config.getPanelUrl(`billing/services/${this.object.id}`);
    }
    getCardFields() {
        const datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_10__["DatePipe"](this.config.locale);
        const fields = [
            {
                name: 'Client',
                value: this.object.client.name,
            },
            {
                name: 'Created at',
                value: `${datePipe.transform(this.object.created_at)}`,
            },
            {
                name: 'Next due',
                value: `${datePipe.transform(this.object.next_due_date)}`,
            }
        ];
        return fields;
    }
    getTabs() {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Overview',
                        component: _tabs_service_details_overview_service_details_overview_component__WEBPACK_IMPORTED_MODULE_7__["ServiceDetailsOverviewComponent"],
                    },
                ];
            case 'edit':
            case 'create':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_service_edit_form_service_edit_form_component__WEBPACK_IMPORTED_MODULE_8__["ServiceEditFormComponent"],
                    },
                ];
        }
    }
    getCardTags() {
        return [];
    }
    getDetailsActions() {
        const actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`billing/services`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_9__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`billing/services`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_9__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    }
}
ServiceUIService.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] },
    { type: _shared_fleio_api_billing_services_service_api_service__WEBPACK_IMPORTED_MODULE_6__["ServicesApiService"] }
];


/***/ }),

/***/ "./src/app/reseller/billing/services/services-routing.module.ts":
/*!**********************************************************************!*\
  !*** ./src/app/reseller/billing/services/services-routing.module.ts ***!
  \**********************************************************************/
/*! exports provided: ServicesRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServicesRoutingModule", function() { return ServicesRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _service_list_service_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./service-list/service-list.component */ "./src/app/reseller/billing/services/service-list/service-list.component.ts");
/* harmony import */ var _service_details_service_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./service-details/service-details.component */ "./src/app/reseller/billing/services/service-details/service-details.component.ts");
/* harmony import */ var _service_edit_service_edit_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./service-edit/service-edit.component */ "./src/app/reseller/billing/services/service-edit/service-edit.component.ts");
/* harmony import */ var _shared_fleio_api_billing_services_service_list_resolver__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/services/service-list.resolver */ "./src/app/shared/fleio-api/billing/services/service-list.resolver.ts");
/* harmony import */ var _shared_fleio_api_billing_services_service_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/billing/services/service.resolver */ "./src/app/shared/fleio-api/billing/services/service.resolver.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/ui-api/interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");










const routes = [
    {
        path: '',
        component: _service_list_service_list_component__WEBPACK_IMPORTED_MODULE_3__["ServiceListComponent"],
        resolve: {
            services: _shared_fleio_api_billing_services_service_list_resolver__WEBPACK_IMPORTED_MODULE_6__["ServiceListResolver"],
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_9__["AuthGuard"]],
        data: {
            config: {
                feature: 'billing.services',
                search: {
                    show: true,
                    placeholder: 'Search services ...',
                },
                subheader: {
                    objectNamePlural: 'services',
                    objectName: 'service',
                    objectList(data) {
                        return data.services;
                    }
                },
                ordering: {
                    default: {
                        field: 'created_at',
                        display: 'Created at',
                        direction: _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_8__["OrderingDirection"].Descending,
                    },
                    options: [
                        { display: 'Name', field: 'name' },
                        { display: 'Client', field: 'client' },
                        { display: 'Created at', field: 'created_at' },
                        { display: 'Next due date', field: 'next_due_date' },
                        { display: 'Status', field: 'status' },
                    ]
                }
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: ':id',
        component: _service_details_service_details_component__WEBPACK_IMPORTED_MODULE_4__["ServiceDetailsComponent"],
        resolve: {
            service: _shared_fleio_api_billing_services_service_resolver__WEBPACK_IMPORTED_MODULE_7__["ServiceResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.service.name;
                },
            },
        }
    },
    {
        path: ':id/edit',
        component: _service_edit_service_edit_component__WEBPACK_IMPORTED_MODULE_5__["ServiceEditComponent"],
        resolve: {
            service: _shared_fleio_api_billing_services_service_resolver__WEBPACK_IMPORTED_MODULE_7__["ServiceResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.service.name;
                },
            },
        }
    },
];
let ServicesRoutingModule = class ServicesRoutingModule {
};
ServicesRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], ServicesRoutingModule);



/***/ }),

/***/ "./src/app/reseller/billing/services/services.module.ts":
/*!**************************************************************!*\
  !*** ./src/app/reseller/billing/services/services.module.ts ***!
  \**************************************************************/
/*! exports provided: ServicesModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServicesModule", function() { return ServicesModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _service_details_service_details_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./service-details/service-details.component */ "./src/app/reseller/billing/services/service-details/service-details.component.ts");
/* harmony import */ var _service_edit_service_edit_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./service-edit/service-edit.component */ "./src/app/reseller/billing/services/service-edit/service-edit.component.ts");
/* harmony import */ var _service_list_service_list_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./service-list/service-list.component */ "./src/app/reseller/billing/services/service-list/service-list.component.ts");
/* harmony import */ var _services_routing_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./services-routing.module */ "./src/app/reseller/billing/services/services-routing.module.ts");
/* harmony import */ var _tabs_service_details_overview_service_details_overview_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tabs/service-details-overview/service-details-overview.component */ "./src/app/reseller/billing/services/tabs/service-details-overview/service-details-overview.component.ts");
/* harmony import */ var _tabs_service_edit_form_service_edit_form_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/service-edit-form/service-edit-form.component */ "./src/app/reseller/billing/services/tabs/service-edit-form/service-edit-form.component.ts");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm2015/select.js");
/* harmony import */ var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/material/datepicker */ "./node_modules/@angular/material/esm2015/datepicker.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm2015/button.js");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/icon */ "./node_modules/@angular/material/esm2015/icon.js");



















let ServicesModule = class ServicesModule {
};
ServicesModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _service_details_service_details_component__WEBPACK_IMPORTED_MODULE_3__["ServiceDetailsComponent"],
            _service_edit_service_edit_component__WEBPACK_IMPORTED_MODULE_4__["ServiceEditComponent"],
            _service_list_service_list_component__WEBPACK_IMPORTED_MODULE_5__["ServiceListComponent"],
            _tabs_service_details_overview_service_details_overview_component__WEBPACK_IMPORTED_MODULE_7__["ServiceDetailsOverviewComponent"],
            _tabs_service_edit_form_service_edit_form_component__WEBPACK_IMPORTED_MODULE_8__["ServiceEditFormComponent"],
        ],
        entryComponents: [
            _tabs_service_details_overview_service_details_overview_component__WEBPACK_IMPORTED_MODULE_7__["ServiceDetailsOverviewComponent"],
            _tabs_service_edit_form_service_edit_form_component__WEBPACK_IMPORTED_MODULE_8__["ServiceEditFormComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _services_routing_module__WEBPACK_IMPORTED_MODULE_6__["ServicesRoutingModule"],
            _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_9__["ErrorHandlingModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_10__["ReactiveFormsModule"],
            _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_11__["ObjectsViewModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_12__["FlexModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_13__["MatFormFieldModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_14__["MatInputModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_15__["MatSelectModule"],
            _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_16__["MatDatepickerModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_17__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_18__["MatIconModule"],
        ]
    })
], ServicesModule);



/***/ }),

/***/ "./src/app/reseller/billing/services/tabs/service-details-overview/service-details-overview.component.scss":
/*!*****************************************************************************************************************!*\
  !*** ./src/app/reseller/billing/services/tabs/service-details-overview/service-details-overview.component.scss ***!
  \*****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvc2VydmljZXMvdGFicy9zZXJ2aWNlLWRldGFpbHMtb3ZlcnZpZXcvc2VydmljZS1kZXRhaWxzLW92ZXJ2aWV3LmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/billing/services/tabs/service-details-overview/service-details-overview.component.ts":
/*!***************************************************************************************************************!*\
  !*** ./src/app/reseller/billing/services/tabs/service-details-overview/service-details-overview.component.ts ***!
  \***************************************************************************************************************/
/*! exports provided: ServiceDetailsOverviewComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceDetailsOverviewComponent", function() { return ServiceDetailsOverviewComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");




let ServiceDetailsOverviewComponent = class ServiceDetailsOverviewComponent extends _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"] {
    constructor(config) {
        super();
        this.config = config;
    }
    ngOnInit() {
    }
};
ServiceDetailsOverviewComponent.ctorParameters = () => [
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] }
];
ServiceDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-service-details-overview',
        template: __webpack_require__(/*! raw-loader!./service-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/services/tabs/service-details-overview/service-details-overview.component.html"),
        styles: [__webpack_require__(/*! ./service-details-overview.component.scss */ "./src/app/reseller/billing/services/tabs/service-details-overview/service-details-overview.component.scss")]
    })
], ServiceDetailsOverviewComponent);



/***/ }),

/***/ "./src/app/reseller/billing/services/tabs/service-edit-form/service-edit-form.component.scss":
/*!***************************************************************************************************!*\
  !*** ./src/app/reseller/billing/services/tabs/service-edit-form/service-edit-form.component.scss ***!
  \***************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvc2VydmljZXMvdGFicy9zZXJ2aWNlLWVkaXQtZm9ybS9zZXJ2aWNlLWVkaXQtZm9ybS5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/billing/services/tabs/service-edit-form/service-edit-form.component.ts":
/*!*************************************************************************************************!*\
  !*** ./src/app/reseller/billing/services/tabs/service-edit-form/service-edit-form.component.ts ***!
  \*************************************************************************************************/
/*! exports provided: ServiceEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceEditFormComponent", function() { return ServiceEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_fleio_api_client_user_client_clients_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../shared/fleio-api/client-user/client/clients-api.service */ "./src/app/shared/fleio-api/client-user/client/clients-api.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_billing_services_service_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../shared/fleio-api/billing/services/service-api.service */ "./src/app/shared/fleio-api/billing/services/service-api.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");









let ServiceEditFormComponent = class ServiceEditFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"] {
    constructor(formBuilder, clientsApi, activatedRoute, router, config, servicesApi) {
        super();
        this.formBuilder = formBuilder;
        this.clientsApi = clientsApi;
        this.activatedRoute = activatedRoute;
        this.router = router;
        this.config = config;
        this.servicesApi = servicesApi;
        this.serviceForm = this.formBuilder.group({
            display_name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            cycle: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            notes: [''],
            override_price: [''],
            override_suspend_until: [''],
            next_due_date: [''],
            next_expiration_date: [''],
            next_invoice_date: [''],
        });
    }
    ngOnInit() {
        this.objectController.actionCallback = () => this.saveService();
        this.serviceForm.patchValue(this.object);
    }
    saveService() {
        const value = this.serviceForm.value;
        value.status = this.object.status;
        value.product = this.object.product.id;
        value.cycle = this.object.cycle.id;
        this.createOrUpdate(this.servicesApi, value).subscribe(() => {
            this.router.navigateByUrl(this.config.getPrevUrl('billing/services')).catch(() => {
            });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_8__["of"])(null);
    }
};
ServiceEditFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
    { type: _shared_fleio_api_client_user_client_clients_api_service__WEBPACK_IMPORTED_MODULE_4__["ClientsApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["ActivatedRoute"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_6__["ConfigService"] },
    { type: _shared_fleio_api_billing_services_service_api_service__WEBPACK_IMPORTED_MODULE_7__["ServicesApiService"] }
];
ServiceEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-service-edit-form',
        template: __webpack_require__(/*! raw-loader!./service-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/services/tabs/service-edit-form/service-edit-form.component.html"),
        styles: [__webpack_require__(/*! ./service-edit-form.component.scss */ "./src/app/reseller/billing/services/tabs/service-edit-form/service-edit-form.component.scss")]
    })
], ServiceEditFormComponent);



/***/ }),

/***/ "./src/app/shared/fleio-api/billing/services/service-list.resolver.ts":
/*!****************************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/services/service-list.resolver.ts ***!
  \****************************************************************************/
/*! exports provided: ServiceListResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceListResolver", function() { return ServiceListResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _service_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./service-api.service */ "./src/app/shared/fleio-api/billing/services/service-api.service.ts");





let ServiceListResolver = class ServiceListResolver {
    constructor(servicesApiService) {
        this.servicesApiService = servicesApiService;
    }
    resolve(route, state) {
        return this.servicesApiService.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
ServiceListResolver.ctorParameters = () => [
    { type: _service_api_service__WEBPACK_IMPORTED_MODULE_4__["ServicesApiService"] }
];
ServiceListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ServiceListResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/billing/services/service.resolver.ts":
/*!***********************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/services/service.resolver.ts ***!
  \***********************************************************************/
/*! exports provided: ServiceResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceResolver", function() { return ServiceResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _service_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./service-api.service */ "./src/app/shared/fleio-api/billing/services/service-api.service.ts");





let ServiceResolver = class ServiceResolver {
    constructor(servicesApiService) {
        this.servicesApiService = servicesApiService;
    }
    resolve(route, state) {
        return this.servicesApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
ServiceResolver.ctorParameters = () => [
    { type: _service_api_service__WEBPACK_IMPORTED_MODULE_4__["ServicesApiService"] }
];
ServiceResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ServiceResolver);



/***/ })

}]);
//# sourceMappingURL=services-services-module-es2015.js.map