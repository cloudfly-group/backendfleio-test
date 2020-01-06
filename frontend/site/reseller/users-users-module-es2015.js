(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["users-users-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.html":
/*!**************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.html ***!
  \**************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"fl-content fl-content-min-height\">\n  <div *ngIf=\"!object.clients.length\" fxLayout=\"row\" fxLayoutAlign=\"center center\">\n    <p class=\"fl-detail\">No clients</p>\n  </div>\n  <div *ngIf=\"object.clients\" fxLayout=\"column\">\n    <table class=\"full-width\" mat-table [dataSource]=\"object.clients\">\n      <ng-container matColumnDef=\"id\">\n        <th mat-header-cell *matHeaderCellDef>ID</th>\n        <td mat-cell *matCellDef=\"let client\">\n          <a [routerLink]=\"[config.getPanelUrl('clients-users/clients/'), client.id]\">\n            ID: {{client.id}}\n          </a>\n        </td>\n      </ng-container>\n      <ng-container matColumnDef=\"name\">\n        <th mat-header-cell *matHeaderCellDef>Name</th>\n        <td mat-cell *matCellDef=\"let client\">\n          <a [routerLink]=\"[config.getPanelUrl('clients-users/clients/'), client.id]\">\n            {{client.name}}\n          </a>\n        </td>\n      </ng-container>\n      <tr mat-row *matRowDef=\"let row; columns: displayedColumns;\"></tr>\n    </table>\n  </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.html":
/*!****************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.html ***!
  \****************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxLayout=\"row\" fxLayout.xs=\"column\" class=\"fl-content fl-content-min-height\">\n  <div fxLayout=\"column\" fxFlex=\"50\">\n    <p class=\"fl-detail\">First name:&nbsp;{{ object.first_name }}</p>\n    <p class=\"fl-detail\">Last name:&nbsp;{{ object.last_name }}</p>\n    <p class=\"fl-detail\">Username:&nbsp;{{ object.username }}</p>\n    <p class=\"fl-detail\">Email:&nbsp;{{ object.email }}</p>\n    <p class=\"fl-detail\">ID:&nbsp;{{ object.id }}</p>\n    <p class=\"fl-detail\">Last login:&nbsp;{{ (object.last_login | date) || 'never' }}</p>\n    <p class=\"fl-detail\">Date joined:&nbsp;{{ object.date_joined | date }}</p>\n  </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.html":
/*!**************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.html ***!
  \**************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form [formGroup]=\"userForm\">\n  <app-form-errors #formErrors [formGroup]=\"userForm\"></app-form-errors>\n  <mat-form-field class=\"half-width half-width-spacing\">\n    <input matInput placeholder=\"First name\" type=\"text\" formControlName=\"first_name\" required>\n    <mat-error>{{backendErrors['first_name'] || 'This field is required!' }}</mat-error>\n  </mat-form-field>\n  <mat-form-field class=\"half-width\">\n    <input matInput placeholder=\"Last name\" type=\"text\" formControlName=\"last_name\" required>\n    <mat-error>{{backendErrors['last_name'] || 'This field is required!' }}</mat-error>\n  </mat-form-field>\n  <mat-form-field class=\"half-width half-width-spacing\">\n    <input matInput placeholder=\"Email\" type=\"text\" formControlName=\"email\" required>\n    <mat-error>{{backendErrors['email'] || 'This field is required!' }}</mat-error>\n  </mat-form-field>\n  <mat-form-field class=\"half-width\">\n    <input matInput placeholder=\"User name\" type=\"text\" formControlName=\"username\" required>\n    <mat-error>{{backendErrors['username'] || 'This field is required!' }}</mat-error>\n  </mat-form-field>\n  <mat-checkbox [color]=\"'primary'\" class=\"full-width\" formControlName=\"email_as_username\">\n    Use email as username\n  </mat-checkbox>\n  <mat-form-field class=\"full-width\">\n    <input matInput placeholder=\"Password\" type=\"password\" formControlName=\"password\" required>\n    <mat-error>{{backendErrors['password'] || 'This field is required!' }}</mat-error>\n  </mat-form-field>\n  <div class=\"half-width half-width-spacing checkbox-container\">\n    <mat-checkbox [color]=\"'primary'\" formControlName=\"is_active\">\n      Is active\n    </mat-checkbox>\n  </div>\n  <div class=\"half-width checkbox-container\">\n    <mat-checkbox [color]=\"'primary'\" class=\"half-width\" formControlName=\"email_verified\">\n      Has verified email\n    </mat-checkbox>\n  </div>\n</form>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-create/user-create.component.html":
/*!***************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/clients-users/users/user-create/user-create.component.html ***!
  \***************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-details/user-details.component.html":
/*!*****************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/clients-users/users/user-details/user-details.component.html ***!
  \*****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\"></app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-edit/user-edit.component.html":
/*!***********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/clients-users/users/user-edit/user-edit.component.html ***!
  \***********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.html":
/*!*************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.html ***!
  \*************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<p *ngIf=\"!impersonated\">Impersonating user ...</p>\n<p *ngIf=\"impersonated\">User impersonated, you can access end user panel as the user</p>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-list/user-list.component.html":
/*!***********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/clients-users/users/user-list/user-list.component.html ***!
  \***********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-objects-view [objectsListController]=\"objectListController\"></app-objects-view>\n"

/***/ }),

/***/ "./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.scss":
/*!************************************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.scss ***!
  \************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2NsaWVudHMtdXNlcnMvdXNlcnMvdGFicy91c2VyLWRldGFpbHMtY2xpZW50cy91c2VyLWRldGFpbHMtY2xpZW50cy5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.ts":
/*!**********************************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.ts ***!
  \**********************************************************************************************************/
/*! exports provided: UserDetailsClientsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserDetailsClientsComponent", function() { return UserDetailsClientsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");




let UserDetailsClientsComponent = class UserDetailsClientsComponent extends _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"] {
    constructor(config) {
        super();
        this.config = config;
        this.displayedColumns = ['id', 'name'];
    }
    ngOnInit() {
    }
};
UserDetailsClientsComponent.ctorParameters = () => [
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] }
];
UserDetailsClientsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-user-details-clients',
        template: __webpack_require__(/*! raw-loader!./user-details-clients.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.html"),
        styles: [__webpack_require__(/*! ./user-details-clients.component.scss */ "./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.scss")]
    })
], UserDetailsClientsComponent);



/***/ }),

/***/ "./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.scss":
/*!**************************************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.scss ***!
  \**************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2NsaWVudHMtdXNlcnMvdXNlcnMvdGFicy91c2VyLWRldGFpbHMtb3ZlcnZpZXcvdXNlci1kZXRhaWxzLW92ZXJ2aWV3LmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.ts":
/*!************************************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.ts ***!
  \************************************************************************************************************/
/*! exports provided: UserDetailsOverviewComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserDetailsOverviewComponent", function() { return UserDetailsOverviewComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");



let UserDetailsOverviewComponent = class UserDetailsOverviewComponent extends _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"] {
    constructor() {
        super();
    }
    ngOnInit() {
    }
};
UserDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-user-details-overview',
        template: __webpack_require__(/*! raw-loader!./user-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.html"),
        styles: [__webpack_require__(/*! ./user-details-overview.component.scss */ "./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.scss")]
    })
], UserDetailsOverviewComponent);



/***/ }),

/***/ "./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.scss":
/*!************************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.scss ***!
  \************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2NsaWVudHMtdXNlcnMvdXNlcnMvdGFicy91c2VyLWVkaXQtZm9ybS91c2VyLWVkaXQtZm9ybS5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.ts":
/*!**********************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.ts ***!
  \**********************************************************************************************/
/*! exports provided: UserEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserEditFormComponent", function() { return UserEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/fleio-api/client-user/user/users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");








let UserEditFormComponent = class UserEditFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_7__["DetailsFormBase"] {
    constructor(formBuilder, usersApi, router, config) {
        super();
        this.formBuilder = formBuilder;
        this.usersApi = usersApi;
        this.router = router;
        this.config = config;
        this.country = new _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormControl"]('', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required);
        this.userForm = this.formBuilder.group({
            first_name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            last_name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            email: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            username: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            email_as_username: [false],
            password: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            is_active: [true, _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            email_verified: [false, _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
        });
        this.emailAsUsername = this.userForm.controls.email_as_username;
        this.username = this.userForm.controls.username;
        this.email = this.userForm.controls.email;
    }
    ngOnInit() {
        this.objectController.actionCallback = () => this.saveUser();
        this.userForm.patchValue(this.object);
        this.emailAsUsername.valueChanges.subscribe(emailAsUsername => {
            if (emailAsUsername) {
                this.usernameValue = this.username.value;
                this.username.setValue(this.email.value);
                this.username.disable();
            }
            else {
                this.username.setValue(this.usernameValue);
                this.username.enable();
            }
        });
    }
    saveUser() {
        const value = this.userForm.value;
        if (this.username.disabled) {
            value.username = this.username.value;
        }
        if (!value.password) {
            delete value.password;
        }
        let request;
        if (this.object.id) {
            value.id = this.object.id;
            request = this.usersApi.update(value.id, value);
        }
        else {
            request = this.usersApi.create(value);
        }
        request.subscribe(() => {
            this.router.navigateByUrl(this.config.getPrevUrl('clients-users/users')).catch(() => { });
        }, (error) => {
            this.setErrors(error.error);
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["of"])(null);
    }
};
UserEditFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"] },
    { type: _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_6__["UsersApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] }
];
UserEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-user-edit-form',
        template: __webpack_require__(/*! raw-loader!./user-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.html"),
        styles: [__webpack_require__(/*! ./user-edit-form.component.scss */ "./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.scss")]
    })
], UserEditFormComponent);



/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-create/user-create.component.scss":
/*!*************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-create/user-create.component.scss ***!
  \*************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2NsaWVudHMtdXNlcnMvdXNlcnMvdXNlci1jcmVhdGUvdXNlci1jcmVhdGUuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-create/user-create.component.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-create/user-create.component.ts ***!
  \***********************************************************************************/
/*! exports provided: UserCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserCreateComponent", function() { return UserCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../user-list-ui.service */ "./src/app/reseller/clients-users/users/user-list-ui.service.ts");





let UserCreateComponent = class UserCreateComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, userListUIService) {
        super(route, userListUIService, 'create', null);
    }
};
UserCreateComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["UserListUIService"] }
];
UserCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-user-create',
        template: __webpack_require__(/*! raw-loader!./user-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-create/user-create.component.html"),
        styles: [__webpack_require__(/*! ./user-create.component.scss */ "./src/app/reseller/clients-users/users/user-create/user-create.component.scss")]
    })
], UserCreateComponent);



/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-details/user-details.component.scss":
/*!***************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-details/user-details.component.scss ***!
  \***************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2NsaWVudHMtdXNlcnMvdXNlcnMvdXNlci1kZXRhaWxzL3VzZXItZGV0YWlscy5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-details/user-details.component.ts":
/*!*************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-details/user-details.component.ts ***!
  \*************************************************************************************/
/*! exports provided: UserDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserDetailsComponent", function() { return UserDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../user-list-ui.service */ "./src/app/reseller/clients-users/users/user-list-ui.service.ts");





let UserDetailsComponent = class UserDetailsComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, userListUIService) {
        super(route, userListUIService, 'details', 'user');
    }
};
UserDetailsComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["UserListUIService"] }
];
UserDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-user-details',
        template: __webpack_require__(/*! raw-loader!./user-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-details/user-details.component.html"),
        styles: [__webpack_require__(/*! ./user-details.component.scss */ "./src/app/reseller/clients-users/users/user-details/user-details.component.scss")]
    })
], UserDetailsComponent);



/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-edit/user-edit.component.scss":
/*!*********************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-edit/user-edit.component.scss ***!
  \*********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2NsaWVudHMtdXNlcnMvdXNlcnMvdXNlci1lZGl0L3VzZXItZWRpdC5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-edit/user-edit.component.ts":
/*!*******************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-edit/user-edit.component.ts ***!
  \*******************************************************************************/
/*! exports provided: UserEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserEditComponent", function() { return UserEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../user-list-ui.service */ "./src/app/reseller/clients-users/users/user-list-ui.service.ts");





let UserEditComponent = class UserEditComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, userListUIService) {
        super(route, userListUIService, 'edit', 'user');
    }
};
UserEditComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["UserListUIService"] }
];
UserEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-user-edit',
        template: __webpack_require__(/*! raw-loader!./user-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-edit/user-edit.component.html"),
        styles: [__webpack_require__(/*! ./user-edit.component.scss */ "./src/app/reseller/clients-users/users/user-edit/user-edit.component.scss")]
    })
], UserEditComponent);



/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.scss":
/*!***********************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.scss ***!
  \***********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2NsaWVudHMtdXNlcnMvdXNlcnMvdXNlci1pbXBlcnNvbmF0ZS91c2VyLWltcGVyc29uYXRlLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.ts":
/*!*********************************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.ts ***!
  \*********************************************************************************************/
/*! exports provided: UserImpersonateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserImpersonateComponent", function() { return UserImpersonateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/fleio-api/client-user/user/users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../user-list-ui.service */ "./src/app/reseller/clients-users/users/user-list-ui.service.ts");
/* harmony import */ var _shared_ui_api_app_local_storage_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../shared/ui-api/app-local-storage.service */ "./src/app/shared/ui-api/app-local-storage.service.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");








let UserImpersonateComponent = class UserImpersonateComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_3__["DetailsBase"] {
    constructor(route, userListUIService, usersApi, appLocalStorage, config) {
        super(route, userListUIService, 'edit', 'user');
        this.usersApi = usersApi;
        this.appLocalStorage = appLocalStorage;
        this.config = config;
        this.impersonated = false;
    }
    ngOnInit() {
        super.ngOnInit();
        this.usersApi.objectPostAction(this.object.id, 'impersonate', {
            action: 'impersonate'
        }).subscribe(impersonationData => {
            this.appLocalStorage.setItem('fleio.flStaffBackend', this.config.getPanelApiUrl(''));
            this.appLocalStorage.setItem('fleio.flStaffUrl', this.config.getPanelHomeUrl());
            if (impersonationData.enduser_panel_url) {
                window.location = impersonationData.enduser_panel_url;
            }
            this.impersonated = true;
        });
    }
};
UserImpersonateComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
    { type: _user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["UserListUIService"] },
    { type: _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_2__["UsersApiService"] },
    { type: _shared_ui_api_app_local_storage_service__WEBPACK_IMPORTED_MODULE_6__["AppLocalStorageService"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_7__["ConfigService"] }
];
UserImpersonateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-user-impersonate',
        template: __webpack_require__(/*! raw-loader!./user-impersonate.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.html"),
        styles: [__webpack_require__(/*! ./user-impersonate.component.scss */ "./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.scss")]
    })
], UserImpersonateComponent);



/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-list-ui.service.ts":
/*!**********************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-list-ui.service.ts ***!
  \**********************************************************************/
/*! exports provided: UserListUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserListUIService", function() { return UserListUIService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/client-user/user/users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var _user_ui_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./user-ui.service */ "./src/app/reseller/clients-users/users/user-ui.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _shared_auth_auth_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/auth/auth.service */ "./src/app/shared/auth/auth.service.ts");










let UserListUIService = class UserListUIService {
    constructor(router, config, usersApi, auth) {
        this.router = router;
        this.config = config;
        this.usersApi = usersApi;
        this.auth = auth;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_8__["DatePipe"](config.locale);
    }
    getObjectUIService(object, permissions, state) {
        return new _user_ui_service__WEBPACK_IMPORTED_MODULE_7__["UserUIService"](object, permissions, state, this.router, this.config, this.usersApi, this.auth);
    }
    getTableData(objectList) {
        const tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Image, displayName: 'Image', enableSort: false, fieldName: '(image)' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Full name', enableSort: false, fieldName: 'full_name' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Username', enableSort: true, fieldName: 'username' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Last login', enableSort: true, fieldName: 'last_login' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Actions, displayName: 'Actions', enableSort: false, fieldName: '(actions)' },
                ],
                columnNames: ['(image)', 'full_name', 'username', 'last_login', '(actions)'],
                statusColumn: '(image)',
            },
            rows: [],
        };
        for (const object of objectList.objects) {
            const rowUIService = this.getObjectUIService(object, objectList.permissions, 'table-view');
            const user = object;
            const row = {
                cells: {
                    full_name: { text: user.full_name },
                    username: { text: user.username },
                    last_login: { text: user.last_login ? this.datePipe.transform(user.last_login) : 'never' },
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
                name: 'Create new user',
                tooltip: 'Create new user',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('clients-users/users/create')
            })
        ];
    }
};
UserListUIService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_6__["UsersApiService"] },
    { type: _shared_auth_auth_service__WEBPACK_IMPORTED_MODULE_9__["AuthService"] }
];
UserListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], UserListUIService);



/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-list/user-list.component.scss":
/*!*********************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-list/user-list.component.scss ***!
  \*********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2NsaWVudHMtdXNlcnMvdXNlcnMvdXNlci1saXN0L3VzZXItbGlzdC5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-list/user-list.component.ts":
/*!*******************************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-list/user-list.component.ts ***!
  \*******************************************************************************/
/*! exports provided: UserListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserListComponent", function() { return UserListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../user-list-ui.service */ "./src/app/reseller/clients-users/users/user-list-ui.service.ts");






let UserListComponent = class UserListComponent extends _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"] {
    constructor(route, userListUIService, refreshService) {
        super(route, userListUIService, refreshService, 'users');
        this.route = route;
        this.userListUIService = userListUIService;
        this.refreshService = refreshService;
    }
    ngOnInit() {
        super.ngOnInit();
    }
};
UserListComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["UserListUIService"] },
    { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
];
UserListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-user-list',
        template: __webpack_require__(/*! raw-loader!./user-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-list/user-list.component.html"),
        styles: [__webpack_require__(/*! ./user-list.component.scss */ "./src/app/reseller/clients-users/users/user-list/user-list.component.scss")]
    })
], UserListComponent);



/***/ }),

/***/ "./src/app/reseller/clients-users/users/user-ui.service.ts":
/*!*****************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/user-ui.service.ts ***!
  \*****************************************************************/
/*! exports provided: UserUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserUIService", function() { return UserUIService; });
/* harmony import */ var _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/object-status */ "./src/app/shared/ui/objects-view/interfaces/object-status.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/client-user/user/users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var _tabs_user_details_overview_user_details_overview_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/user-details-overview/user-details-overview.component */ "./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.ts");
/* harmony import */ var _tabs_user_edit_form_user_edit_form_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/user-edit-form/user-edit-form.component */ "./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.ts");
/* harmony import */ var _tabs_user_details_clients_user_details_clients_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./tabs/user-details-clients/user-details-clients.component */ "./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.ts");
/* harmony import */ var _shared_auth_auth_service__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/auth/auth.service */ "./src/app/shared/auth/auth.service.ts");













class UserUIService extends _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__["ObjectUIServiceBase"] {
    constructor(user, permissions, state, router, config, usersApi, auth) {
        super(user, permissions, state);
        this.auth = auth;
        this.router = router;
        this.config = config;
        this.usersApi = usersApi;
    }
    getIcon() {
        return {
            name: '(gravatar)',
            gravatarEmail: this.object.email,
        };
    }
    getStatus() {
        return {
            type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined,
            value: this.object.is_active ? _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Active : _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Disabled
        };
    }
    getTitle() {
        switch (this.state) {
            case 'details':
                return {
                    text: `${this.object.first_name} ${this.object.last_name}`,
                    subText: this.object.username,
                };
            case 'edit':
                return {
                    text: `${this.object.first_name} ${this.object.last_name}`,
                    subText: this.object.username,
                };
            case 'create':
                return {
                    text: 'Create user',
                };
            default:
                return {
                    text: `${this.object.first_name} ${this.object.last_name}`,
                    subText: this.object.username,
                };
        }
    }
    getActions() {
        const actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            name: 'Edit',
            tooltip: 'Edit',
            routerUrl: this.config.getPanelUrl(`clients-users/users/${this.object.id}/edit`),
            router: this.router,
        }));
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
            icon: { name: 'face' },
            name: 'Impersonate user',
            noPermissions: this.auth.isImpersonating(),
            tooltip: this.auth.isImpersonating() ?
                'You cannot impersonate another user while impersonating' : 'Impersonate user',
            routerUrl: this.config.getPanelUrl(`clients-users/users/${this.object.id}/impersonate`),
            router: this.router,
        }));
        actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["ApiCallAction"]({
            object: this.object,
            icon: { name: 'delete' },
            name: 'Delete',
            tooltip: 'Delete',
            confirmOptions: {
                confirm: true,
                title: 'Delete user',
                message: `Are you sure you want to delete user ${this.object.username}.` +
                    'All data will be lost.',
            },
            apiService: this.usersApi,
            callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["CallType"].Delete,
        }));
        return actions;
    }
    getDetailsLink() {
        return this.config.getPanelUrl(`clients-users/users/${this.object.id}`);
    }
    getCardFields() {
        const datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_6__["DatePipe"](this.config.locale);
        const fields = [
            {
                name: 'Last login',
                value: this.object.last_login ? datePipe.transform(this.object.last_login) : 'never',
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
                        component: _tabs_user_details_overview_user_details_overview_component__WEBPACK_IMPORTED_MODULE_9__["UserDetailsOverviewComponent"],
                    },
                    {
                        tabName: 'Clients',
                        component: _tabs_user_details_clients_user_details_clients_component__WEBPACK_IMPORTED_MODULE_11__["UserDetailsClientsComponent"],
                    },
                ];
            case 'edit':
            case 'create':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_user_edit_form_user_edit_form_component__WEBPACK_IMPORTED_MODULE_10__["UserEditFormComponent"],
                    },
                ];
        }
    }
    getDetailsActions() {
        const actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`clients-users/users`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`clients-users/users`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    }
    getCardTags() {
        const tags = [];
        return tags;
    }
}
UserUIService.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] },
    { type: _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_8__["UsersApiService"] },
    { type: _shared_auth_auth_service__WEBPACK_IMPORTED_MODULE_12__["AuthService"] }
];


/***/ }),

/***/ "./src/app/reseller/clients-users/users/users-routing.module.ts":
/*!**********************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/users-routing.module.ts ***!
  \**********************************************************************/
/*! exports provided: UsersRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UsersRoutingModule", function() { return UsersRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_fleio_api_client_user_user_user_list_resolver__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/fleio-api/client-user/user/user-list.resolver */ "./src/app/shared/fleio-api/client-user/user/user-list.resolver.ts");
/* harmony import */ var _user_list_user_list_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./user-list/user-list.component */ "./src/app/reseller/clients-users/users/user-list/user-list.component.ts");
/* harmony import */ var _user_create_user_create_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./user-create/user-create.component */ "./src/app/reseller/clients-users/users/user-create/user-create.component.ts");
/* harmony import */ var _user_details_user_details_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./user-details/user-details.component */ "./src/app/reseller/clients-users/users/user-details/user-details.component.ts");
/* harmony import */ var _shared_fleio_api_client_user_user_user_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/client-user/user/user.resolver */ "./src/app/shared/fleio-api/client-user/user/user.resolver.ts");
/* harmony import */ var _user_edit_user_edit_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./user-edit/user-edit.component */ "./src/app/reseller/clients-users/users/user-edit/user-edit.component.ts");
/* harmony import */ var _user_impersonate_user_impersonate_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./user-impersonate/user-impersonate.component */ "./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/ui-api/interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");












const routes = [
    {
        path: '',
        component: _user_list_user_list_component__WEBPACK_IMPORTED_MODULE_4__["UserListComponent"],
        resolve: {
            users: _shared_fleio_api_client_user_user_user_list_resolver__WEBPACK_IMPORTED_MODULE_3__["UserListResolver"]
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_10__["AuthGuard"]],
        data: {
            config: {
                feature: 'clients&users.users',
                search: {
                    show: true,
                    placeholder: 'Search users ...',
                },
                subheader: {
                    objectName: 'user',
                    objectNamePlural: 'users',
                    objectList(data) {
                        return data.users;
                    }
                },
                ordering: {
                    default: {
                        display: 'Sign-up date',
                        field: 'date_joined',
                        direction: _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__["OrderingDirection"].Descending,
                    },
                    options: [
                        {
                            display: 'Last login',
                            field: 'last_login',
                        },
                        {
                            display: 'Sign-up date',
                            field: 'date_joined',
                        },
                        {
                            display: 'Username',
                            field: 'username',
                        },
                        {
                            display: 'Email',
                            field: 'email',
                        },
                    ]
                }
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: 'create',
        component: _user_create_user_create_component__WEBPACK_IMPORTED_MODULE_5__["UserCreateComponent"],
        resolve: {},
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return 'Create user';
                },
            },
        }
    },
    {
        path: ':id',
        component: _user_details_user_details_component__WEBPACK_IMPORTED_MODULE_6__["UserDetailsComponent"],
        resolve: {
            user: _shared_fleio_api_client_user_user_user_resolver__WEBPACK_IMPORTED_MODULE_7__["UserResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.user.username;
                },
            },
        }
    },
    {
        path: ':id/edit',
        component: _user_edit_user_edit_component__WEBPACK_IMPORTED_MODULE_8__["UserEditComponent"],
        resolve: {
            user: _shared_fleio_api_client_user_user_user_resolver__WEBPACK_IMPORTED_MODULE_7__["UserResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return `Edit ${data.user.username}`;
                },
            },
        }
    },
    {
        path: ':id/impersonate',
        component: _user_impersonate_user_impersonate_component__WEBPACK_IMPORTED_MODULE_9__["UserImpersonateComponent"],
        resolve: {
            user: _shared_fleio_api_client_user_user_user_resolver__WEBPACK_IMPORTED_MODULE_7__["UserResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return `Impersonating ${data.user.username}`;
                },
            },
        }
    },
];
let UsersRoutingModule = class UsersRoutingModule {
};
UsersRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], UsersRoutingModule);



/***/ }),

/***/ "./src/app/reseller/clients-users/users/users.module.ts":
/*!**************************************************************!*\
  !*** ./src/app/reseller/clients-users/users/users.module.ts ***!
  \**************************************************************/
/*! exports provided: UsersModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UsersModule", function() { return UsersModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _user_list_user_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./user-list/user-list.component */ "./src/app/reseller/clients-users/users/user-list/user-list.component.ts");
/* harmony import */ var _user_create_user_create_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./user-create/user-create.component */ "./src/app/reseller/clients-users/users/user-create/user-create.component.ts");
/* harmony import */ var _user_details_user_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./user-details/user-details.component */ "./src/app/reseller/clients-users/users/user-details/user-details.component.ts");
/* harmony import */ var _user_edit_user_edit_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./user-edit/user-edit.component */ "./src/app/reseller/clients-users/users/user-edit/user-edit.component.ts");
/* harmony import */ var _users_routing_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./users-routing.module */ "./src/app/reseller/clients-users/users/users-routing.module.ts");
/* harmony import */ var _tabs_user_details_overview_user_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/user-details-overview/user-details-overview.component */ "./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.ts");
/* harmony import */ var _tabs_user_edit_form_user_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/user-edit-form/user-edit-form.component */ "./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm2015/checkbox.js");
/* harmony import */ var _tabs_user_details_clients_user_details_clients_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./tabs/user-details-clients/user-details-clients.component */ "./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/table */ "./node_modules/@angular/material/esm2015/table.js");
/* harmony import */ var _user_impersonate_user_impersonate_component__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./user-impersonate/user-impersonate.component */ "./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.ts");




















let UsersModule = class UsersModule {
};
UsersModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _user_list_user_list_component__WEBPACK_IMPORTED_MODULE_3__["UserListComponent"],
            _user_create_user_create_component__WEBPACK_IMPORTED_MODULE_4__["UserCreateComponent"],
            _user_details_user_details_component__WEBPACK_IMPORTED_MODULE_5__["UserDetailsComponent"],
            _user_edit_user_edit_component__WEBPACK_IMPORTED_MODULE_6__["UserEditComponent"],
            _tabs_user_details_overview_user_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["UserDetailsOverviewComponent"],
            _tabs_user_edit_form_user_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["UserEditFormComponent"],
            _tabs_user_details_clients_user_details_clients_component__WEBPACK_IMPORTED_MODULE_16__["UserDetailsClientsComponent"],
            _user_impersonate_user_impersonate_component__WEBPACK_IMPORTED_MODULE_19__["UserImpersonateComponent"],
        ],
        entryComponents: [
            _tabs_user_details_overview_user_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["UserDetailsOverviewComponent"],
            _tabs_user_edit_form_user_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["UserEditFormComponent"],
            _tabs_user_details_clients_user_details_clients_component__WEBPACK_IMPORTED_MODULE_16__["UserDetailsClientsComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _users_routing_module__WEBPACK_IMPORTED_MODULE_7__["UsersRoutingModule"],
            _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_10__["ObjectsViewModule"],
            _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__["ErrorHandlingModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_12__["MatFormFieldModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_13__["ReactiveFormsModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_14__["MatInputModule"],
            _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_15__["MatCheckboxModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_17__["FlexLayoutModule"],
            _angular_material_table__WEBPACK_IMPORTED_MODULE_18__["MatTableModule"],
        ]
    })
], UsersModule);



/***/ }),

/***/ "./src/app/shared/fleio-api/client-user/user/user-list.resolver.ts":
/*!*************************************************************************!*\
  !*** ./src/app/shared/fleio-api/client-user/user/user-list.resolver.ts ***!
  \*************************************************************************/
/*! exports provided: UserListResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserListResolver", function() { return UserListResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _users_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");





let UserListResolver = class UserListResolver {
    constructor(usersApi) {
        this.usersApi = usersApi;
    }
    resolve(route, state) {
        return this.usersApi.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
UserListResolver.ctorParameters = () => [
    { type: _users_api_service__WEBPACK_IMPORTED_MODULE_3__["UsersApiService"] }
];
UserListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], UserListResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/client-user/user/user.resolver.ts":
/*!********************************************************************!*\
  !*** ./src/app/shared/fleio-api/client-user/user/user.resolver.ts ***!
  \********************************************************************/
/*! exports provided: UserResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserResolver", function() { return UserResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _users_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");





let UserResolver = class UserResolver {
    constructor(usersApi) {
        this.usersApi = usersApi;
    }
    resolve(route, state) {
        return this.usersApi.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
UserResolver.ctorParameters = () => [
    { type: _users_api_service__WEBPACK_IMPORTED_MODULE_3__["UsersApiService"] }
];
UserResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], UserResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts":
/*!************************************************************************!*\
  !*** ./src/app/shared/fleio-api/client-user/user/users-api.service.ts ***!
  \************************************************************************/
/*! exports provided: UsersApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UsersApiService", function() { return UsersApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let UsersApiService = class UsersApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('users'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
UsersApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
UsersApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], UsersApiService);



/***/ })

}]);
//# sourceMappingURL=users-users-module-es2015.js.map