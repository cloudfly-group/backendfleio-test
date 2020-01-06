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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../api-user-list-ui.service */ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts");





var ApiUserCreateComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ApiUserCreateComponent, _super);
    function ApiUserCreateComponent(route, apiUserListUiService) {
        return _super.call(this, route, apiUserListUiService, 'create', null) || this;
    }
    ApiUserCreateComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ApiUserListUiService"] }
    ]; };
    ApiUserCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-api-user-create',
            template: __webpack_require__(/*! raw-loader!./api-user-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.html"),
            styles: [__webpack_require__(/*! ./api-user-create.component.scss */ "./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.scss")]
        })
    ], ApiUserCreateComponent);
    return ApiUserCreateComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../api-user-list-ui.service */ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts");





var ApiUserDetailsComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ApiUserDetailsComponent, _super);
    function ApiUserDetailsComponent(route, apiUserListUiService) {
        return _super.call(this, route, apiUserListUiService, 'details', 'apiUser') || this;
    }
    ApiUserDetailsComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ApiUserListUiService"] }
    ]; };
    ApiUserDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-api-user-details',
            template: __webpack_require__(/*! raw-loader!./api-user-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.html"),
            styles: [__webpack_require__(/*! ./api-user-details.component.scss */ "./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.scss")]
        })
    ], ApiUserDetailsComponent);
    return ApiUserDetailsComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../api-user-list-ui.service */ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts");





var ApiUserEditComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ApiUserEditComponent, _super);
    function ApiUserEditComponent(route, apiUserListUiService) {
        return _super.call(this, route, apiUserListUiService, 'edit', 'apiUser') || this;
    }
    ApiUserEditComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ApiUserListUiService"] }
    ]; };
    ApiUserEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-api-user-edit',
            template: __webpack_require__(/*! raw-loader!./api-user-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.html"),
            styles: [__webpack_require__(/*! ./api-user-edit.component.scss */ "./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.scss")]
        })
    ], ApiUserEditComponent);
    return ApiUserEditComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _api_user_ui_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./api-user-ui.service */ "./src/app/reseller/cloud/api-users/api-user-ui.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/api-user/api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");









var ApiUserListUiService = /** @class */ (function () {
    function ApiUserListUiService(router, config, apiUsersApi, matDialog) {
        this.router = router;
        this.config = config;
        this.apiUsersApi = apiUsersApi;
        this.matDialog = matDialog;
    }
    ApiUserListUiService.prototype.getObjectUIService = function (object, permissions, state) {
        return new _api_user_ui_service__WEBPACK_IMPORTED_MODULE_6__["ApiUserUiService"](object, permissions, state, this.router, this.config, this.apiUsersApi, this.matDialog);
    };
    ApiUserListUiService.prototype.getTableData = function (objectList) {
        var e_1, _a;
        var tableData = {
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
        try {
            for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](objectList.objects), _c = _b.next(); !_c.done; _c = _b.next()) {
                var object = _c.value;
                var rowUIService = this.getObjectUIService(object, objectList.permissions, 'table-view');
                var row = {
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
    ApiUserListUiService.prototype.getActions = function (objectList) {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__["RouterLinkAction"]({
                name: 'Create new api user',
                tooltip: 'Create new api user',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('cloud/api-users/create')
            })
        ];
    };
    ApiUserListUiService.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
        { type: _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_7__["ApiUsersApiService"] },
        { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialog"] }
    ]; };
    ApiUserListUiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root',
        })
    ], ApiUserListUiService);
    return ApiUserListUiService;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../api-user-list-ui.service */ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts");






var ApiUserListComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ApiUserListComponent, _super);
    function ApiUserListComponent(route, apiUserListUiService, refreshService) {
        var _this = _super.call(this, route, apiUserListUiService, refreshService, 'apiUsers') || this;
        _this.route = route;
        _this.apiUserListUiService = apiUserListUiService;
        _this.refreshService = refreshService;
        return _this;
    }
    ApiUserListComponent.prototype.ngOnInit = function () {
        _super.prototype.ngOnInit.call(this);
    };
    ApiUserListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["ApiUserListUiService"] },
        { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
    ]; };
    ApiUserListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-api-user-list',
            template: __webpack_require__(/*! raw-loader!./api-user-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.html"),
            styles: [__webpack_require__(/*! ./api-user-list.component.scss */ "./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.scss")]
        })
    ], ApiUserListComponent);
    return ApiUserListComponent;
}(_shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"]));



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
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/api-user/api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");
/* harmony import */ var _tabs_api_user_edit_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/api-user-edit-form/api-user-edit-form.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.ts");
/* harmony import */ var _tabs_api_user_details_overview_api_user_details_overview_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/api-user-details-overview/api-user-details-overview.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.ts");
/* harmony import */ var _tabs_api_user_create_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/api-user-create-form/api-user-edit-form.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _dialogs_api_user_download_openrc_api_user_download_openrc_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./dialogs/api-user-download-openrc/api-user-download-openrc.component */ "./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");














var ApiUserUiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ApiUserUiService, _super);
    function ApiUserUiService(user, permissions, state, router, config, apiUsersApi, matDialog) {
        var _this = _super.call(this, user, permissions, state) || this;
        _this.matDialog = matDialog;
        _this.router = router;
        _this.config = config;
        _this.apiUsersApi = apiUsersApi;
        return _this;
    }
    ApiUserUiService.prototype.getIcon = function () {
        return null;
    };
    ApiUserUiService.prototype.getStatus = function () {
        return null;
    };
    ApiUserUiService.prototype.getTitle = function () {
        switch (this.state) {
            case 'details':
                return {
                    text: "User " + this.object.name,
                };
            case 'edit':
                return {
                    text: "Edit " + this.object.name,
                };
            case 'create':
                return {
                    text: 'Create api user',
                };
            default:
                return {
                    text: "" + this.object.name,
                };
        }
    };
    ApiUserUiService.prototype.getActions = function () {
        var _this = this;
        var actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            name: 'Edit',
            tooltip: 'Edit',
            routerUrl: this.config.getPanelUrl("cloud/api-users/" + this.object.id + "/edit"),
            router: this.router,
        }));
        actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_6__["CallbackAction"]({
            object: this.object,
            icon: { name: 'arrow_downward' },
            tooltip: 'Get OpenRC file',
            name: 'Get OpenRC file',
            callback: function (action) {
                return _this.matDialog.open(_dialogs_api_user_download_openrc_api_user_download_openrc_component__WEBPACK_IMPORTED_MODULE_12__["ApiUserDownloadOpenrcComponent"], {
                    data: { apiUser: _this.object }
                }).afterClosed().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_11__["map"])(function (result) {
                    if (result === false) {
                        return;
                    }
                    return { message: result };
                }));
            }
        }));
        actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["ApiCallAction"]({
            object: this.object,
            icon: { name: 'delete' },
            tooltip: 'Delete',
            name: 'Delete',
            confirmOptions: {
                confirm: true,
                title: 'Delete user',
                message: "Are you sure you want to delete user " + this.object.name + "?"
            },
            apiService: this.apiUsersApi,
            callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["CallType"].Delete,
        }));
        return actions;
    };
    ApiUserUiService.prototype.getCardTags = function () {
        return [];
    };
    ApiUserUiService.prototype.getDetailsLink = function () {
        return this.config.getPanelUrl("cloud/api-users/" + this.object.id);
    };
    ApiUserUiService.prototype.getCardFields = function () {
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
    };
    ApiUserUiService.prototype.getTabs = function () {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Overview',
                        component: _tabs_api_user_details_overview_api_user_details_overview_component__WEBPACK_IMPORTED_MODULE_9__["ApiUserDetailsOverviewComponent"],
                    },
                ];
            case 'edit':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_api_user_edit_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_8__["ApiUserEditFormComponent"],
                    },
                ];
            case 'create':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_api_user_create_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_10__["ApiUserCreateFormComponent"],
                    },
                ];
        }
    };
    ApiUserUiService.prototype.getDetailsActions = function () {
        var actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("cloud/api-users"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_6__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("cloud/api-users"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_6__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    };
    ApiUserUiService.ctorParameters = function () { return [
        { type: undefined },
        { type: undefined },
        { type: String },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] },
        { type: _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_7__["ApiUsersApiService"] },
        { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__["MatDialog"] }
    ]; };
    return ApiUserUiService;
}(_shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__["ObjectUIServiceBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _api_user_list_api_user_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./api-user-list/api-user-list.component */ "./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.ts");
/* harmony import */ var _api_user_create_api_user_create_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./api-user-create/api-user-create.component */ "./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.ts");
/* harmony import */ var _api_user_details_api_user_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./api-user-details/api-user-details.component */ "./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.ts");
/* harmony import */ var _api_user_edit_api_user_edit_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./api-user-edit/api-user-edit.component */ "./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_user_list_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/api-user/api-user-list.resolver */ "./src/app/shared/fleio-api/cloud/api-user/api-user-list.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_user_create_options_resolver__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/api-user/api-user-create-options.resolver */ "./src/app/shared/fleio-api/cloud/api-user/api-user-create-options.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_user_resolver__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/api-user/api-user.resolver */ "./src/app/shared/fleio-api/cloud/api-user/api-user.resolver.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");











var routes = [
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
                    objectList: function (data) {
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
                getBreadCrumbDetail: function () {
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
                getBreadCrumbDetail: function (data) {
                    return "" + data.apiUser.name;
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
                getBreadCrumbDetail: function (data) {
                    return "Edit " + data.apiUser.name;
                },
            },
        }
    },
];
var ApiUsersRoutingModule = /** @class */ (function () {
    function ApiUsersRoutingModule() {
    }
    ApiUsersRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
        })
    ], ApiUsersRoutingModule);
    return ApiUsersRoutingModule;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _api_user_list_api_user_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./api-user-list/api-user-list.component */ "./src/app/reseller/cloud/api-users/api-user-list/api-user-list.component.ts");
/* harmony import */ var _api_user_create_api_user_create_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./api-user-create/api-user-create.component */ "./src/app/reseller/cloud/api-users/api-user-create/api-user-create.component.ts");
/* harmony import */ var _api_user_details_api_user_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./api-user-details/api-user-details.component */ "./src/app/reseller/cloud/api-users/api-user-details/api-user-details.component.ts");
/* harmony import */ var _api_user_edit_api_user_edit_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./api-user-edit/api-user-edit.component */ "./src/app/reseller/cloud/api-users/api-user-edit/api-user-edit.component.ts");
/* harmony import */ var _api_users_routing_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./api-users-routing.module */ "./src/app/reseller/cloud/api-users/api-users-routing.module.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _tabs_api_user_edit_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/api-user-edit-form/api-user-edit-form.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm5/input.es5.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm5/checkbox.es5.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/autocomplete */ "./node_modules/@angular/material/esm5/autocomplete.es5.js");
/* harmony import */ var _tabs_api_user_details_overview_api_user_details_overview_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./tabs/api-user-details-overview/api-user-details-overview.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.ts");
/* harmony import */ var _tabs_api_user_create_form_api_user_edit_form_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./tabs/api-user-create-form/api-user-edit-form.component */ "./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.ts");
/* harmony import */ var _dialogs_api_user_download_openrc_api_user_download_openrc_component__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./dialogs/api-user-download-openrc/api-user-download-openrc.component */ "./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm5/select.es5.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm5/button.es5.js");
/* harmony import */ var _api_user_list_ui_service__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./api-user-list-ui.service */ "./src/app/reseller/cloud/api-users/api-user-list-ui.service.ts");
/* harmony import */ var _shared_ui_ui_module__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ../../../shared/ui/ui.module */ "./src/app/shared/ui/ui.module.ts");
























var ApiUsersModule = /** @class */ (function () {
    function ApiUsersModule() {
    }
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
    return ApiUsersModule;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");
/* harmony import */ var _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/api-user/api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_region_regions_api_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/region/regions-api.service */ "./src/app/shared/fleio-api/cloud/region/regions-api.service.ts");






var ApiUserDownloadOpenrcComponent = /** @class */ (function () {
    function ApiUserDownloadOpenrcComponent(dialogRef, data, apiUsersApiService, notificationService, regionsApiService) {
        this.dialogRef = dialogRef;
        this.data = data;
        this.apiUsersApiService = apiUsersApiService;
        this.notificationService = notificationService;
        this.regionsApiService = regionsApiService;
    }
    ApiUserDownloadOpenrcComponent.prototype.close = function () {
        this.dialogRef.close(false);
    };
    ApiUserDownloadOpenrcComponent.prototype.getOpenRCFile = function () {
        var _this = this;
        if (!this.selectedRegion) {
            return;
        }
        this.apiUsersApiService.postAction('get_openrc_file_content', {
            user_name: this.data.apiUser.name,
            default_project_id: this.data.apiUser.default_project_id,
            region: this.selectedRegion,
        }).pipe().subscribe(function (responseData) {
            var blob = new Blob([responseData.content], { type: 'application/octet-stream' });
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'openrc';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            _this.dialogRef.close(true);
        });
    };
    ApiUserDownloadOpenrcComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.regionsResponse = null;
        this.regionsApiService.list().pipe().subscribe(function (response) {
            _this.regionsResponse = response;
        });
    };
    ApiUserDownloadOpenrcComponent.ctorParameters = function () { return [
        { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"] },
        { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"],] }] },
        { type: _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_4__["ApiUsersApiService"] },
        { type: _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_3__["NotificationService"] },
        { type: _shared_fleio_api_cloud_region_regions_api_service__WEBPACK_IMPORTED_MODULE_5__["RegionsApiService"] }
    ]; };
    ApiUserDownloadOpenrcComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-api-user-download-openrc',
            template: __webpack_require__(/*! raw-loader!./api-user-download-openrc.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.html"),
            styles: [__webpack_require__(/*! ./api-user-download-openrc.component.scss */ "./src/app/reseller/cloud/api-users/dialogs/api-user-download-openrc/api-user-download-openrc.component.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__param"](1, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"]))
    ], ApiUserDownloadOpenrcComponent);
    return ApiUserDownloadOpenrcComponent;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/api-user/api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");








var ApiUserCreateFormComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ApiUserCreateFormComponent, _super);
    function ApiUserCreateFormComponent(formBuilder, apiUsersApiService, router, config, activatedRoute) {
        var _this = _super.call(this) || this;
        _this.formBuilder = formBuilder;
        _this.apiUsersApiService = apiUsersApiService;
        _this.router = router;
        _this.config = config;
        _this.activatedRoute = activatedRoute;
        _this.apiUserForm = _this.formBuilder.group({
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            default_project: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            password: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            description: [''],
        });
        _this.loading = false;
        return _this;
    }
    ApiUserCreateFormComponent.prototype.saveUser = function () {
        var _this = this;
        var value = this.apiUserForm.value;
        value.default_project = value.default_project.id;
        this.loading = true;
        this.createOrUpdate(this.apiUsersApiService, value).subscribe(function () {
            _this.loading = false;
            _this.router.navigateByUrl(_this.config.getPrevUrl('cloud/api-users')).catch(function () {
                _this.loading = false;
            });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_7__["of"])(null);
    };
    ApiUserCreateFormComponent.prototype.displayProjectFn = function (project) {
        if (project && project.id) {
            return project.name + ' ' + project.id;
        }
        return '';
    };
    ApiUserCreateFormComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.objectController.actionCallback = function () { return _this.saveUser(); };
        this.createOptions = this.activatedRoute.snapshot.data.createOptions;
        if (this.object) {
            this.apiUserForm.patchValue(this.object);
        }
    };
    ApiUserCreateFormComponent.ctorParameters = function () { return [
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
        { type: _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_6__["ApiUsersApiService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] }
    ]; };
    ApiUserCreateFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-api-user-edit-form',
            template: __webpack_require__(/*! raw-loader!./api-user-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.html"),
            styles: [__webpack_require__(/*! ./api-user-edit-form.component.scss */ "./src/app/reseller/cloud/api-users/tabs/api-user-create-form/api-user-edit-form.component.scss")]
        })
    ], ApiUserCreateFormComponent);
    return ApiUserCreateFormComponent;
}(_shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");



var ApiUserDetailsOverviewComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ApiUserDetailsOverviewComponent, _super);
    function ApiUserDetailsOverviewComponent() {
        return _super.call(this) || this;
    }
    ApiUserDetailsOverviewComponent.prototype.ngOnInit = function () {
    };
    ApiUserDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-api-user-details-overview',
            template: __webpack_require__(/*! raw-loader!./api-user-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.html"),
            styles: [__webpack_require__(/*! ./api-user-details-overview.component.scss */ "./src/app/reseller/cloud/api-users/tabs/api-user-details-overview/api-user-details-overview.component.scss")]
        })
    ], ApiUserDetailsOverviewComponent);
    return ApiUserDetailsOverviewComponent;
}(_shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/api-user/api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");








var ApiUserEditFormComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ApiUserEditFormComponent, _super);
    function ApiUserEditFormComponent(formBuilder, apiUsersApiService, router, config) {
        var _this = _super.call(this) || this;
        _this.formBuilder = formBuilder;
        _this.apiUsersApiService = apiUsersApiService;
        _this.router = router;
        _this.config = config;
        _this.apiUserForm = _this.formBuilder.group({
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            password: [null],
            description: [''],
        });
        _this.loading = false;
        return _this;
    }
    ApiUserEditFormComponent.prototype.saveApiUser = function () {
        var _this = this;
        var value = this.apiUserForm.value;
        if (value.password === null) {
            delete value.password;
        }
        this.loading = true;
        this.createOrUpdate(this.apiUsersApiService, value).subscribe(function () {
            _this.loading = false;
            _this.router.navigateByUrl(_this.config.getPrevUrl('cloud/api-users')).catch(function () {
                _this.loading = false;
            });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_7__["of"])(null);
    };
    ApiUserEditFormComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.objectController.actionCallback = function () { return _this.saveApiUser(); };
        if (this.object) {
            this.apiUserForm.patchValue(this.object);
        }
    };
    ApiUserEditFormComponent.ctorParameters = function () { return [
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
        { type: _shared_fleio_api_cloud_api_user_api_users_api_service__WEBPACK_IMPORTED_MODULE_6__["ApiUsersApiService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] }
    ]; };
    ApiUserEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-api-user-edit-form',
            template: __webpack_require__(/*! raw-loader!./api-user-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.html"),
            styles: [__webpack_require__(/*! ./api-user-edit-form.component.scss */ "./src/app/reseller/cloud/api-users/tabs/api-user-edit-form/api-user-edit-form.component.scss")]
        })
    ], ApiUserEditFormComponent);
    return ApiUserEditFormComponent;
}(_shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");





var ApiUserCreateOptionsResolver = /** @class */ (function () {
    function ApiUserCreateOptionsResolver(apiUsersApiService) {
        this.apiUsersApiService = apiUsersApiService;
    }
    ApiUserCreateOptionsResolver.prototype.resolve = function (route, state) {
        return this.apiUsersApiService.createOptions()
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    ApiUserCreateOptionsResolver.ctorParameters = function () { return [
        { type: _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__["ApiUsersApiService"] }
    ]; };
    ApiUserCreateOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ApiUserCreateOptionsResolver);
    return ApiUserCreateOptionsResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");





var ApiUserListResolver = /** @class */ (function () {
    function ApiUserListResolver(apiUsersApiService) {
        this.apiUsersApiService = apiUsersApiService;
    }
    ApiUserListResolver.prototype.resolve = function (route, state) {
        return this.apiUsersApiService.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    ApiUserListResolver.ctorParameters = function () { return [
        { type: _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__["ApiUsersApiService"] }
    ]; };
    ApiUserListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ApiUserListResolver);
    return ApiUserListResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./api-users-api.service */ "./src/app/shared/fleio-api/cloud/api-user/api-users-api.service.ts");





var ApiUserResolver = /** @class */ (function () {
    function ApiUserResolver(apiUsersApiService) {
        this.apiUsersApiService = apiUsersApiService;
    }
    ApiUserResolver.prototype.resolve = function (route, state) {
        return this.apiUsersApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    ApiUserResolver.ctorParameters = function () { return [
        { type: _api_users_api_service__WEBPACK_IMPORTED_MODULE_4__["ApiUsersApiService"] }
    ]; };
    ApiUserResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ApiUserResolver);
    return ApiUserResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var ApiUsersApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ApiUsersApiService, _super);
    function ApiUsersApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('openstack/users')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    ApiUsersApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    ApiUsersApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ApiUsersApiService);
    return ApiUsersApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var RegionsApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](RegionsApiService, _super);
    function RegionsApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('openstack/regions')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    RegionsApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    RegionsApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], RegionsApiService);
    return RegionsApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ })

}]);
//# sourceMappingURL=api-users-api-users-module-es5.js.map