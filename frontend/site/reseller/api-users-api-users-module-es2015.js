(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["api-users-api-users-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.html":
/*!*******************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.html ***!
  \*******************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.html":
/*!*********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.html ***!
  \*********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\"></app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.html":
/*!***************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.html ***!
  \***************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.html":
/*!***************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.html ***!
  \***************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-objects-view [objectsListController]=\"objectListController\"></app-objects-view>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.html":
/*!*********************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.html ***!
  \*********************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<h1 mat-dialog-title>Get OpenRC file for {{data.apiUser.name}}</h1>\n<div mat-dialog-content>\n  <div fxLayout=\"row\" *ngIf=\"regionsResponse && regionsResponse.objects.length\">\n    <mat-form-field fxFlex=\"100\">\n      <mat-label>Region to download file for</mat-label>\n      <mat-select [(ngModel)]=\"selectedRegion\" placeholder=\"Region to download file for\" required>\n        <mat-option *ngFor=\"let region of regionsResponse.objects\" [value]=\"region.id\">\n          {{region.id}}\n        </mat-option>\n      </mat-select>\n      <mat-error>This field is required!</mat-error>\n    </mat-form-field>\n  </div>\n  <div fxLayout=\"row\" class=\"fl-detail\">Note: password will be requested when sourcing file.</div>\n</div>\n<div mat-dialog-actions>\n  <button mat-button (click)=\"close()\">Cancel</button>\n  <button mat-button (click)=\"getOpenRCFile()\" [color]=\"'primary'\">\n    Get file\n  </button>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.html":
/*!********************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.html ***!
  \********************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-fl-backdrop *ngIf=\"loading\" [verticalAlignMiddle]=\"true\"></app-fl-backdrop>\n<form [formGroup]=\"apiUserForm\">\n  <app-form-errors #formErrors [formGroup]=\"apiUserForm\"></app-form-errors>\n  <div fxLayout=\"row\">\n    <mat-form-field fxFlex=\"100\">\n      <input matInput placeholder=\"Project\" aria-label=\"Project\" [matAutocomplete]=\"auto\"\n             formControlName=\"default_project\" required>\n      <mat-autocomplete #auto=\"matAutocomplete\" [displayWith]=\"displayProjectFn\">\n        <mat-option *ngFor=\"let project of createOptions\" [value]=\"project\">\n          <span>{{project.name}}</span>\n        </mat-option>\n      </mat-autocomplete>\n      <mat-error>{{backendErrors['default_project'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n  </div>\n  <div fxLayout=\"row\">\n    <mat-form-field fxFlex=\"100\">\n      <input matInput placeholder=\"Name\" type=\"text\" formControlName=\"name\" required>\n      <mat-error>{{backendErrors['name'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n  </div>\n  <div fxLayout=\"row\">\n    <mat-form-field fxFlex=\"100\">\n      <input matInput placeholder=\"Password\" type=\"password\" maxlength=\"1024\" formControlName=\"password\" required>\n      <mat-error>{{backendErrors['password'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n  </div>\n  <div fxLayout=\"row\">\n    <mat-form-field fxFlex=\"100\">\n      <input matInput placeholder=\"Description\" type=\"text\" maxlength=\"1024\" formControlName=\"description\">\n      <mat-error>{{backendErrors['description'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n  </div>\n</form>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.html":
/*!********************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.html ***!
  \********************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxLayout=\"row\">\n  <div fxLayout=\"column\" fxFlex=\"50\">\n    <p class=\"fl-detail\">ID:&nbsp;{{ object.id }}</p>\n    <p class=\"fl-detail\">Name:&nbsp;{{ object.name }}</p>\n    <p class=\"fl-detail\" *ngIf=\"object.project_name\">Project name:&nbsp;{{ object.project_name }}</p>\n    <p class=\"fl-detail\">Project ID:&nbsp;{{ object.default_project_id }}</p>\n    <p class=\"fl-detail\">Domain ID:&nbsp;{{ object.domain_id }}</p>\n    <p class=\"fl-detail\">Description:&nbsp;{{ object.description }}</p>\n  </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.html":
/*!******************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.html ***!
  \******************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-fl-backdrop *ngIf=\"loading\" [verticalAlignMiddle]=\"true\"></app-fl-backdrop>\n<form [formGroup]=\"apiUserForm\">\n  <app-form-errors #formErrors [formGroup]=\"apiUserForm\"></app-form-errors>\n  <div fxLayout=\"row\">\n    <mat-form-field fxFlex=\"100\">\n      <input matInput placeholder=\"Name\" type=\"text\" formControlName=\"name\" required>\n      <mat-error>{{backendErrors['name'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n  </div>\n  <div fxLayout=\"row\">\n    <mat-form-field fxFlex=\"100\">\n      <input matInput placeholder=\"Password\" type=\"password\" maxlength=\"1024\" formControlName=\"password\">\n      <mat-error>{{backendErrors['password'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n  </div>\n  <div fxLayout=\"row\">\n    <mat-form-field fxFlex=\"100\">\n      <input matInput placeholder=\"Description\" type=\"text\" maxlength=\"1024\" formControlName=\"description\">\n      <mat-error>{{backendErrors['description'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n  </div>\n</form>\n"

/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.scss":
/*!*****************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.scss ***!
  \*****************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2FwaS11c2Vycy9hcGktdXNlci1jcmVhdGUvYXBpLXVzZXItY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.ts":
/*!***************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.ts ***!
  \***************************************************************************************/
/*! exports provided: ApiUserCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserCreateComponent", function() { return ApiUserCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../api-user-list-ui.service */ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts");





let ApiUserCreateComponent = class ApiUserCreateComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, apiUserListUiService) {
        super(route, apiUserListUiService, 'create', null);
    }
};
ApiUserCreateComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ApiUserListUiService"] }
];
ApiUserCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-api-user-create',
        template: __webpack_require__(/*! raw-loader!./api-user-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.html"),
        styles: [__webpack_require__(/*! ./api-user-create.component.scss */ "./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.scss")]
    })
], ApiUserCreateComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.scss":
/*!*******************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.scss ***!
  \*******************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2FwaS11c2Vycy9hcGktdXNlci1kZXRhaWxzL2FwaS11c2VyLWRldGFpbHMuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.ts":
/*!*****************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.ts ***!
  \*****************************************************************************************/
/*! exports provided: ApiUserDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserDetailsComponent", function() { return ApiUserDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../api-user-list-ui.service */ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts");





let ApiUserDetailsComponent = class ApiUserDetailsComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, apiUserListUiService) {
        super(route, apiUserListUiService, 'details', 'apiUser');
    }
};
ApiUserDetailsComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ApiUserListUiService"] }
];
ApiUserDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-api-user-details',
        template: __webpack_require__(/*! raw-loader!./api-user-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.html"),
        styles: [__webpack_require__(/*! ./api-user-details.component.scss */ "./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.scss")]
    })
], ApiUserDetailsComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.scss":
/*!*************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.scss ***!
  \*************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2FwaS11c2Vycy9hcGktdXNlci1lZGl0L2FwaS11c2VyLWVkaXQuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.ts ***!
  \***********************************************************************************/
/*! exports provided: ApiUserEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserEditComponent", function() { return ApiUserEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../api-user-list-ui.service */ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts");





let ApiUserEditComponent = class ApiUserEditComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, apiUserListUiService) {
        super(route, apiUserListUiService, 'edit', 'apiUser');
    }
};
ApiUserEditComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ApiUserListUiService"] }
];
ApiUserEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-api-user-edit',
        template: __webpack_require__(/*! raw-loader!./api-user-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.html"),
        styles: [__webpack_require__(/*! ./api-user-edit.component.scss */ "./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.scss")]
    })
], ApiUserEditComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts":
/*!**********************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts ***!
  \**********************************************************************/
/*! exports provided: ApiUserListUiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserListUiService", function() { return ApiUserListUiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _api_user_ui_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./api-user-ui.service */ "./src/app/reseller/cloud/api-users/api-user-ui.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/api-user/api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");









let ApiUserListUiService = class ApiUserListUiService {
    constructor(router, config, apiUsersApi, matDialog) {
        this.router = router;
        this.config = config;
        this.apiUsersApi = apiUsersApi;
        this.matDialog = matDialog;
    }
    getObjectUIService(object, permissions, state) {
        return new _api_user_ui_service__WEBPACK_IMPORTED_MODULE_6__["ApiUserUiService"](object, permissions, state, this.router, this.config, this.apiUsersApi, this.matDialog);
    }
    getTableData(objectList) {
        const tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Name', enableSort: false, fieldName: 'name' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Project', enableSort: false, fieldName: 'project_name' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Actions, displayName: 'Actions', enableSort: false, fieldName: '(actions)' },
                ],
                columnNames: ['name', 'project_name', '(actions)'],
                statusColumn: 'name',
            },
            rows: [],
        };
        for (const object of objectList.objects) {
            const rowUIService = this.getObjectUIService(object, objectList.permissions, 'table-view');
            const row = {
                cells: {
                    name: { text: object.name },
                    project_name: { text: object.project_name },
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
                name: 'Create new api user',
                tooltip: 'Create new api user',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('cloud/api-users/create')
            })
        ];
    }
};
ApiUserListUiService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_7__["ApiUsersApiService"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialog"] }
];
ApiUserListUiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], ApiUserListUiService);



/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.scss":
/*!*************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.scss ***!
  \*************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2FwaS11c2Vycy9hcGktdXNlci1saXN0L2FwaS11c2VyLWxpc3QuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.ts ***!
  \***********************************************************************************/
/*! exports provided: ApiUserListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserListComponent", function() { return ApiUserListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../api-user-list-ui.service */ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts");






let ApiUserListComponent = class ApiUserListComponent extends _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"] {
    constructor(route, apiUserListUiService, refreshService) {
        super(route, apiUserListUiService, refreshService, 'apiUsers');
        this.route = route;
        this.apiUserListUiService = apiUserListUiService;
        this.refreshService = refreshService;
    }
    ngOnInit() {
        super.ngOnInit();
    }
};
ApiUserListComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["ApiUserListUiService"] },
    { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
];
ApiUserListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-api-user-list',
        template: __webpack_require__(/*! raw-loader!./api-user-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.html"),
        styles: [__webpack_require__(/*! ./api-user-list.component.scss */ "./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.scss")]
    })
], ApiUserListComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-user-ui.service.ts":
/*!*****************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-user-ui.service.ts ***!
  \*****************************************************************/
/*! exports provided: ApiUserUiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserUiService", function() { return ApiUserUiService; });
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/api-user/api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");
/* harmony import */ var _tabs_api_user_edit_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tabs/api-user-edit-form/api-user-edit-form.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.ts");
/* harmony import */ var _tabs_api_user_details_overview_api_user_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/api-user-details-overview/api-user-details-overview.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.ts");
/* harmony import */ var _tabs_api_user_create_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/api-user-create-form/api-user-edit-form.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _dialogs_api_user_download_openrc_api_user_download_openrc_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./dialogs/api-user-download-openrc/api-user-download-openrc.component */ "./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");













class ApiUserUiService extends _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_0__["ObjectUIServiceBase"] {
    constructor(user, permissions, state, router, config, apiUsersApi, matDialog) {
        super(user, permissions, state);
        this.matDialog = matDialog;
        this.router = router;
        this.config = config;
        this.apiUsersApi = apiUsersApi;
    }
    getIcon() {
        return null;
    }
    getStatus() {
        return null;
    }
    getTitle() {
        switch (this.state) {
            case 'details':
                return {
                    text: `User ${this.object.name}`,
                };
            case 'edit':
                return {
                    text: `Edit ${this.object.name}`,
                };
            case 'create':
                return {
                    text: 'Create api user',
                };
            default:
                return {
                    text: `${this.object.name}`,
                };
        }
    }
    getActions() {
        const actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_1__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            name: 'Edit',
            tooltip: 'Edit',
            routerUrl: this.config.getPanelUrl(`cloud/api-users/${this.object.id}/edit`),
            router: this.router,
        }));
        actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_5__["CallbackAction"]({
            object: this.object,
            icon: { name: 'arrow_downward' },
            tooltip: 'Get OpenRC file',
            name: 'Get OpenRC file',
            callback: action => {
                return this.matDialog.open(_dialogs_api_user_download_openrc_api_user_download_openrc_component__WEBPACK_IMPORTED_MODULE_11__["ApiUserDownloadOpenrcComponent"], {
                    data: { apiUser: this.object }
                }).afterClosed().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_10__["map"])(result => {
                    if (result === false) {
                        return;
                    }
                    return { message: result };
                }));
            }
        }));
        actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_4__["ApiCallAction"]({
            object: this.object,
            icon: { name: 'delete' },
            tooltip: 'Delete',
            name: 'Delete',
            confirmOptions: {
                confirm: true,
                title: 'Delete user',
                message: `Are you sure you want to delete user ${this.object.name}?`
            },
            apiService: this.apiUsersApi,
            callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_4__["CallType"].Delete,
        }));
        return actions;
    }
    getCardTags() {
        return [];
    }
    getDetailsLink() {
        return this.config.getPanelUrl(`cloud/api-users/${this.object.id}`);
    }
    getCardFields() {
        return [
            {
                name: 'Id',
                value: this.object.id
            },
            {
                name: 'Project',
                value: this.object.project_name || this.object.default_project_id
            }
        ];
    }
    getTabs() {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Overview',
                        component: _tabs_api_user_details_overview_api_user_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["ApiUserDetailsOverviewComponent"],
                    },
                ];
            case 'edit':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_api_user_edit_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_7__["ApiUserEditFormComponent"],
                    },
                ];
            case 'create':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_api_user_create_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["ApiUserCreateFormComponent"],
                    },
                ];
        }
    }
    getDetailsActions() {
        const actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_1__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`cloud/api-users`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_5__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_1__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`cloud/api-users`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_5__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    }
}
ApiUserUiService.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_6__["ApiUsersApiService"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_12__["MatDialog"] }
];


/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-users-routing.module.ts":
/*!**********************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-users-routing.module.ts ***!
  \**********************************************************************/
/*! exports provided: ApiUsersRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUsersRoutingModule", function() { return ApiUsersRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _api_user_list_api_user_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./api-user-list/api-user-list.component */ "./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.ts");
/* harmony import */ var _api_user_create_api_user_create_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./api-user-create/api-user-create.component */ "./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.ts");
/* harmony import */ var _api_user_details_api_user_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./api-user-details/api-user-details.component */ "./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.ts");
/* harmony import */ var _api_user_edit_api_user_edit_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./api-user-edit/api-user-edit.component */ "./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_user_list_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/api-user/api-user-list.resolver */ "./src/app/shared/fleio-api/cloud/api-user/api-user-list.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_user_create_options_resolver__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/api-user/api-user-create-options.resolver */ "./src/app/shared/fleio-api/cloud/api-user/api-user-create-options.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_user_resolver__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/api-user/api-user.resolver */ "./src/app/shared/fleio-api/cloud/api-user/api-user.resolver.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");











const routes = [
    {
        path: '',
        component: _api_user_list_api_user_list_component__WEBPACK_IMPORTED_MODULE_3__["ApiUserListComponent"],
        resolve: {
            apiUsers: _shared_fleio_api_cloud_api_user_api_user_list_resolver__WEBPACK_IMPORTED_MODULE_7__["ApiUserListResolver"]
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_10__["AuthGuard"]],
        data: {
            config: {
                feature: 'openstack.apiusers',
                search: {
                    show: false,
                    placeholder: 'Search api users ...',
                },
                subheader: {
                    objectName: 'api user',
                    objectNamePlural: 'api users',
                    objectList(data) {
                        return data.apiUsers;
                    }
                },
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: 'create',
        component: _api_user_create_api_user_create_component__WEBPACK_IMPORTED_MODULE_4__["ApiUserCreateComponent"],
        resolve: {
            createOptions: _shared_fleio_api_cloud_api_user_api_user_create_options_resolver__WEBPACK_IMPORTED_MODULE_8__["ApiUserCreateOptionsResolver"]
        },
        data: {
            config: {
                getBreadCrumbDetail: () => {
                    return 'Create api user';
                },
            },
        }
    },
    {
        path: ':id',
        component: _api_user_details_api_user_details_component__WEBPACK_IMPORTED_MODULE_5__["ApiUserDetailsComponent"],
        resolve: {
            apiUser: _shared_fleio_api_cloud_api_user_api_user_resolver__WEBPACK_IMPORTED_MODULE_9__["ApiUserResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return `${data.apiUser.name}`;
                },
            },
        }
    },
    {
        path: ':id/edit',
        component: _api_user_edit_api_user_edit_component__WEBPACK_IMPORTED_MODULE_6__["ApiUserEditComponent"],
        resolve: {
            apiUser: _shared_fleio_api_cloud_api_user_api_user_resolver__WEBPACK_IMPORTED_MODULE_9__["ApiUserResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return `Edit ${data.apiUser.name}`;
                },
            },
        }
    },
];
let ApiUsersRoutingModule = class ApiUsersRoutingModule {
};
ApiUsersRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], ApiUsersRoutingModule);



/***/ }),

/***/ "./src/app/reseller/cloud/api-users/api-users.module.ts":
/*!**************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/api-users.module.ts ***!
  \**************************************************************/
/*! exports provided: ApiUsersModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUsersModule", function() { return ApiUsersModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _api_user_list_api_user_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./api-user-list/api-user-list.component */ "./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.ts");
/* harmony import */ var _api_user_create_api_user_create_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./api-user-create/api-user-create.component */ "./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.ts");
/* harmony import */ var _api_user_details_api_user_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./api-user-details/api-user-details.component */ "./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.ts");
/* harmony import */ var _api_user_edit_api_user_edit_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./api-user-edit/api-user-edit.component */ "./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.ts");
/* harmony import */ var _api_users_routing_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./api-users-routing.module */ "./src/app/reseller/cloud/api-users/api-users-routing.module.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _tabs_api_user_edit_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/api-user-edit-form/api-user-edit-form.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm2015/checkbox.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/autocomplete */ "./node_modules/@angular/material/esm2015/autocomplete.js");
/* harmony import */ var _tabs_api_user_details_overview_api_user_details_overview_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./tabs/api-user-details-overview/api-user-details-overview.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.ts");
/* harmony import */ var _tabs_api_user_create_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./tabs/api-user-create-form/api-user-edit-form.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.ts");
/* harmony import */ var _dialogs_api_user_download_openrc_api_user_download_openrc_component__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./dialogs/api-user-download-openrc/api-user-download-openrc.component */ "./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm2015/select.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm2015/button.js");
/* harmony import */ var _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./api-user-list-ui.service */ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts");
/* harmony import */ var _shared_ui_ui_module__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ../../../shared/ui/ui.module */ "./src/app/shared/ui/ui.module.ts");
























let ApiUsersModule = class ApiUsersModule {
};
ApiUsersModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _api_user_list_api_user_list_component__WEBPACK_IMPORTED_MODULE_3__["ApiUserListComponent"],
            _api_user_create_api_user_create_component__WEBPACK_IMPORTED_MODULE_4__["ApiUserCreateComponent"],
            _api_user_details_api_user_details_component__WEBPACK_IMPORTED_MODULE_5__["ApiUserDetailsComponent"],
            _api_user_edit_api_user_edit_component__WEBPACK_IMPORTED_MODULE_6__["ApiUserEditComponent"],
            _tabs_api_user_edit_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["ApiUserEditFormComponent"],
            _tabs_api_user_details_overview_api_user_details_overview_component__WEBPACK_IMPORTED_MODULE_16__["ApiUserDetailsOverviewComponent"],
            _tabs_api_user_create_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_17__["ApiUserCreateFormComponent"],
            _dialogs_api_user_download_openrc_api_user_download_openrc_component__WEBPACK_IMPORTED_MODULE_18__["ApiUserDownloadOpenrcComponent"],
        ],
        entryComponents: [
            _tabs_api_user_edit_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["ApiUserEditFormComponent"],
            _tabs_api_user_details_overview_api_user_details_overview_component__WEBPACK_IMPORTED_MODULE_16__["ApiUserDetailsOverviewComponent"],
            _tabs_api_user_create_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_17__["ApiUserCreateFormComponent"],
            _dialogs_api_user_download_openrc_api_user_download_openrc_component__WEBPACK_IMPORTED_MODULE_18__["ApiUserDownloadOpenrcComponent"],
        ],
        exports: [
            _dialogs_api_user_download_openrc_api_user_download_openrc_component__WEBPACK_IMPORTED_MODULE_18__["ApiUserDownloadOpenrcComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _api_users_routing_module__WEBPACK_IMPORTED_MODULE_7__["ApiUsersRoutingModule"],
            _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_8__["ObjectsViewModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_10__["ReactiveFormsModule"],
            _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__["ErrorHandlingModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_12__["MatInputModule"],
            _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_13__["MatCheckboxModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_14__["FlexModule"],
            _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_15__["MatAutocompleteModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_19__["MatDialogModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_20__["MatSelectModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_10__["FormsModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_21__["MatButtonModule"],
            _shared_ui_ui_module__WEBPACK_IMPORTED_MODULE_23__["UiModule"],
        ],
        providers: [
            {
                provide: _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_22__["ApiUserListUiService"],
                useClass: _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_22__["ApiUserListUiService"],
                multi: false,
            },
        ]
    })
], ApiUsersModule);



/***/ }),

/***/ "./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.scss":
/*!*******************************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.scss ***!
  \*******************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2FwaS11c2Vycy9kaWFsb2dzL2FwaS11c2VyLWRvd25sb2FkLW9wZW5yYy9hcGktdXNlci1kb3dubG9hZC1vcGVucmMuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.ts":
/*!*****************************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.ts ***!
  \*****************************************************************************************************************/
/*! exports provided: ApiUserDownloadOpenrcComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserDownloadOpenrcComponent", function() { return ApiUserDownloadOpenrcComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");
/* harmony import */ var _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/api-user/api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_region_regions_api_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/region/regions-api.service */ "./src/app/shared/fleio-api/cloud/region/regions-api.service.ts");






let ApiUserDownloadOpenrcComponent = class ApiUserDownloadOpenrcComponent {
    constructor(dialogRef, data, apiUsersApiService, notificationService, regionsApiService) {
        this.dialogRef = dialogRef;
        this.data = data;
        this.apiUsersApiService = apiUsersApiService;
        this.notificationService = notificationService;
        this.regionsApiService = regionsApiService;
    }
    close() {
        this.dialogRef.close(false);
    }
    getOpenRCFile() {
        if (!this.selectedRegion) {
            return;
        }
        this.apiUsersApiService.postAction('get_openrc_file_content', {
            user_name: this.data.apiUser.name,
            default_project_id: this.data.apiUser.default_project_id,
            region: this.selectedRegion,
        }).pipe().subscribe(responseData => {
            const blob = new Blob([responseData.content], { type: 'application/octet-stream' });
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'openrc';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            this.dialogRef.close(true);
        });
    }
    ngOnInit() {
        this.regionsResponse = null;
        this.regionsApiService.list().pipe().subscribe(response => {
            this.regionsResponse = response;
        });
    }
};
ApiUserDownloadOpenrcComponent.ctorParameters = () => [
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"] },
    { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"],] }] },
    { type: _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_4__["ApiUsersApiService"] },
    { type: _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_3__["NotificationService"] },
    { type: _shared_fleio_api_cloud_region_regions_api_service__WEBPACK_IMPORTED_MODULE_5__["RegionsApiService"] }
];
ApiUserDownloadOpenrcComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-api-user-download-openrc',
        template: __webpack_require__(/*! raw-loader!./api-user-download-openrc.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.html"),
        styles: [__webpack_require__(/*! ./api-user-download-openrc.component.scss */ "./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__param"](1, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"]))
], ApiUserDownloadOpenrcComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.scss":
/*!******************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.scss ***!
  \******************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2FwaS11c2Vycy90YWJzL2FwaS11c2VyLWNyZWF0ZS1mb3JtL2FwaS11c2VyLWVkaXQtZm9ybS5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.ts":
/*!****************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.ts ***!
  \****************************************************************************************************/
/*! exports provided: ApiUserCreateFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserCreateFormComponent", function() { return ApiUserCreateFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/api-user/api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");








let ApiUserCreateFormComponent = class ApiUserCreateFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"] {
    constructor(formBuilder, apiUsersApiService, router, config, activatedRoute) {
        super();
        this.formBuilder = formBuilder;
        this.apiUsersApiService = apiUsersApiService;
        this.router = router;
        this.config = config;
        this.activatedRoute = activatedRoute;
        this.apiUserForm = this.formBuilder.group({
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            default_project: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            password: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            description: [''],
        });
        this.loading = false;
    }
    saveUser() {
        const value = this.apiUserForm.value;
        value.default_project = value.default_project.id;
        this.loading = true;
        this.createOrUpdate(this.apiUsersApiService, value).subscribe(() => {
            this.loading = false;
            this.router.navigateByUrl(this.config.getPrevUrl('cloud/api-users')).catch(() => {
                this.loading = false;
            });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_7__["of"])(null);
    }
    displayProjectFn(project) {
        if (project && project.id) {
            return project.name + ' ' + project.id;
        }
        return '';
    }
    ngOnInit() {
        this.objectController.actionCallback = () => this.saveUser();
        this.createOptions = this.activatedRoute.snapshot.data.createOptions;
        if (this.object) {
            this.apiUserForm.patchValue(this.object);
        }
    }
};
ApiUserCreateFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
    { type: _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_6__["ApiUsersApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] }
];
ApiUserCreateFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-api-user-edit-form',
        template: __webpack_require__(/*! raw-loader!./api-user-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.html"),
        styles: [__webpack_require__(/*! ./api-user-edit-form.component.scss */ "./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.scss")]
    })
], ApiUserCreateFormComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.scss":
/*!******************************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.scss ***!
  \******************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2FwaS11c2Vycy90YWJzL2FwaS11c2VyLWRldGFpbHMtb3ZlcnZpZXcvYXBpLXVzZXItZGV0YWlscy1vdmVydmlldy5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.ts":
/*!****************************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.ts ***!
  \****************************************************************************************************************/
/*! exports provided: ApiUserDetailsOverviewComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserDetailsOverviewComponent", function() { return ApiUserDetailsOverviewComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");



let ApiUserDetailsOverviewComponent = class ApiUserDetailsOverviewComponent extends _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"] {
    constructor() {
        super();
    }
    ngOnInit() {
    }
};
ApiUserDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-api-user-details-overview',
        template: __webpack_require__(/*! raw-loader!./api-user-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.html"),
        styles: [__webpack_require__(/*! ./api-user-details-overview.component.scss */ "./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.scss")]
    })
], ApiUserDetailsOverviewComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.scss":
/*!****************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.scss ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2FwaS11c2Vycy90YWJzL2FwaS11c2VyLWVkaXQtZm9ybS9hcGktdXNlci1lZGl0LWZvcm0uY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.ts":
/*!**************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.ts ***!
  \**************************************************************************************************/
/*! exports provided: ApiUserEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserEditFormComponent", function() { return ApiUserEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/api-user/api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");








let ApiUserEditFormComponent = class ApiUserEditFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"] {
    constructor(formBuilder, apiUsersApiService, router, config) {
        super();
        this.formBuilder = formBuilder;
        this.apiUsersApiService = apiUsersApiService;
        this.router = router;
        this.config = config;
        this.apiUserForm = this.formBuilder.group({
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            password: [null],
            description: [''],
        });
        this.loading = false;
    }
    saveApiUser() {
        const value = this.apiUserForm.value;
        if (value.password === null) {
            delete value.password;
        }
        this.loading = true;
        this.createOrUpdate(this.apiUsersApiService, value).subscribe(() => {
            this.loading = false;
            this.router.navigateByUrl(this.config.getPrevUrl('cloud/api-users')).catch(() => {
                this.loading = false;
            });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_7__["of"])(null);
    }
    ngOnInit() {
        this.objectController.actionCallback = () => this.saveApiUser();
        if (this.object) {
            this.apiUserForm.patchValue(this.object);
        }
    }
};
ApiUserEditFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
    { type: _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_6__["ApiUsersApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] }
];
ApiUserEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-api-user-edit-form',
        template: __webpack_require__(/*! raw-loader!./api-user-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.html"),
        styles: [__webpack_require__(/*! ./api-user-edit-form.component.scss */ "./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.scss")]
    })
], ApiUserEditFormComponent);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/api-user/api-user-create-options.resolver.ts":
/*!*************************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/api-user/api-user-create-options.resolver.ts ***!
  \*************************************************************************************/
/*! exports provided: ApiUserCreateOptionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserCreateOptionsResolver", function() { return ApiUserCreateOptionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");





let ApiUserCreateOptionsResolver = class ApiUserCreateOptionsResolver {
    constructor(apiUsersApiService) {
        this.apiUsersApiService = apiUsersApiService;
    }
    resolve(route, state) {
        return this.apiUsersApiService.createOptions()
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
ApiUserCreateOptionsResolver.ctorParameters = () => [
    { type: _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__["ApiUsersApiService"] }
];
ApiUserCreateOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ApiUserCreateOptionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/api-user/api-user-list.resolver.ts":
/*!***************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/api-user/api-user-list.resolver.ts ***!
  \***************************************************************************/
/*! exports provided: ApiUserListResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserListResolver", function() { return ApiUserListResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");





let ApiUserListResolver = class ApiUserListResolver {
    constructor(apiUsersApiService) {
        this.apiUsersApiService = apiUsersApiService;
    }
    resolve(route, state) {
        return this.apiUsersApiService.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
ApiUserListResolver.ctorParameters = () => [
    { type: _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__["ApiUsersApiService"] }
];
ApiUserListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ApiUserListResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/api-user/api-user.resolver.ts":
/*!**********************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/api-user/api-user.resolver.ts ***!
  \**********************************************************************/
/*! exports provided: ApiUserResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUserResolver", function() { return ApiUserResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");





let ApiUserResolver = class ApiUserResolver {
    constructor(apiUsersApiService) {
        this.apiUsersApiService = apiUsersApiService;
    }
    resolve(route, state) {
        return this.apiUsersApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
ApiUserResolver.ctorParameters = () => [
    { type: _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__["ApiUsersApiService"] }
];
ApiUserResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ApiUserResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts":
/*!**************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts ***!
  \**************************************************************************/
/*! exports provided: ApiUsersApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiUsersApiService", function() { return ApiUsersApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let ApiUsersApiService = class ApiUsersApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('openstack/users'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
ApiUsersApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
ApiUsersApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ApiUsersApiService);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/region/regions-api.service.ts":
/*!**********************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/region/regions-api.service.ts ***!
  \**********************************************************************/
/*! exports provided: RegionsApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RegionsApiService", function() { return RegionsApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let RegionsApiService = class RegionsApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('openstack/regions'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
RegionsApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
RegionsApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], RegionsApiService);



/***/ })

}]);
//# sourceMappingURL=api-users-api-users-module-es2015.js.map