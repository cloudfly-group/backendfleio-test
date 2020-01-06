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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");




var UserDetailsClientsComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserDetailsClientsComponent, _super);
    function UserDetailsClientsComponent(config) {
        var _this = _super.call(this) || this;
        _this.config = config;
        _this.displayedColumns = ['id', 'name'];
        return _this;
    }
    UserDetailsClientsComponent.prototype.ngOnInit = function () {
    };
    UserDetailsClientsComponent.ctorParameters = function () { return [
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] }
    ]; };
    UserDetailsClientsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-user-details-clients',
            template: __webpack_require__(/*! raw-loader!./user-details-clients.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.html"),
            styles: [__webpack_require__(/*! ./user-details-clients.component.scss */ "./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.scss")]
        })
    ], UserDetailsClientsComponent);
    return UserDetailsClientsComponent;
}(_shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");



var UserDetailsOverviewComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserDetailsOverviewComponent, _super);
    function UserDetailsOverviewComponent() {
        return _super.call(this) || this;
    }
    UserDetailsOverviewComponent.prototype.ngOnInit = function () {
    };
    UserDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-user-details-overview',
            template: __webpack_require__(/*! raw-loader!./user-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.html"),
            styles: [__webpack_require__(/*! ./user-details-overview.component.scss */ "./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.scss")]
        })
    ], UserDetailsOverviewComponent);
    return UserDetailsOverviewComponent;
}(_shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/fleio-api/client-user/user/users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");








var UserEditFormComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserEditFormComponent, _super);
    function UserEditFormComponent(formBuilder, usersApi, router, config) {
        var _this = _super.call(this) || this;
        _this.formBuilder = formBuilder;
        _this.usersApi = usersApi;
        _this.router = router;
        _this.config = config;
        _this.country = new _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormControl"]('', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required);
        _this.userForm = _this.formBuilder.group({
            first_name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            last_name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            email: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            username: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            email_as_username: [false],
            password: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            is_active: [true, _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            email_verified: [false, _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
        });
        _this.emailAsUsername = _this.userForm.controls.email_as_username;
        _this.username = _this.userForm.controls.username;
        _this.email = _this.userForm.controls.email;
        return _this;
    }
    UserEditFormComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.objectController.actionCallback = function () { return _this.saveUser(); };
        this.userForm.patchValue(this.object);
        this.emailAsUsername.valueChanges.subscribe(function (emailAsUsername) {
            if (emailAsUsername) {
                _this.usernameValue = _this.username.value;
                _this.username.setValue(_this.email.value);
                _this.username.disable();
            }
            else {
                _this.username.setValue(_this.usernameValue);
                _this.username.enable();
            }
        });
    };
    UserEditFormComponent.prototype.saveUser = function () {
        var _this = this;
        var value = this.userForm.value;
        if (this.username.disabled) {
            value.username = this.username.value;
        }
        if (!value.password) {
            delete value.password;
        }
        var request;
        if (this.object.id) {
            value.id = this.object.id;
            request = this.usersApi.update(value.id, value);
        }
        else {
            request = this.usersApi.create(value);
        }
        request.subscribe(function () {
            _this.router.navigateByUrl(_this.config.getPrevUrl('clients-users/users')).catch(function () { });
        }, function (error) {
            _this.setErrors(error.error);
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["of"])(null);
    };
    UserEditFormComponent.ctorParameters = function () { return [
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"] },
        { type: _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_6__["UsersApiService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] }
    ]; };
    UserEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-user-edit-form',
            template: __webpack_require__(/*! raw-loader!./user-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.html"),
            styles: [__webpack_require__(/*! ./user-edit-form.component.scss */ "./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.scss")]
        })
    ], UserEditFormComponent);
    return UserEditFormComponent;
}(_shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_7__["DetailsFormBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../user-list-ui.service */ "./src/app/reseller/clients-users/users/user-list-ui.service.ts");





var UserCreateComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserCreateComponent, _super);
    function UserCreateComponent(route, userListUIService) {
        return _super.call(this, route, userListUIService, 'create', null) || this;
    }
    UserCreateComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["UserListUIService"] }
    ]; };
    UserCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-user-create',
            template: __webpack_require__(/*! raw-loader!./user-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-create/user-create.component.html"),
            styles: [__webpack_require__(/*! ./user-create.component.scss */ "./src/app/reseller/clients-users/users/user-create/user-create.component.scss")]
        })
    ], UserCreateComponent);
    return UserCreateComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../user-list-ui.service */ "./src/app/reseller/clients-users/users/user-list-ui.service.ts");





var UserDetailsComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserDetailsComponent, _super);
    function UserDetailsComponent(route, userListUIService) {
        return _super.call(this, route, userListUIService, 'details', 'user') || this;
    }
    UserDetailsComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["UserListUIService"] }
    ]; };
    UserDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-user-details',
            template: __webpack_require__(/*! raw-loader!./user-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-details/user-details.component.html"),
            styles: [__webpack_require__(/*! ./user-details.component.scss */ "./src/app/reseller/clients-users/users/user-details/user-details.component.scss")]
        })
    ], UserDetailsComponent);
    return UserDetailsComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../user-list-ui.service */ "./src/app/reseller/clients-users/users/user-list-ui.service.ts");





var UserEditComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserEditComponent, _super);
    function UserEditComponent(route, userListUIService) {
        return _super.call(this, route, userListUIService, 'edit', 'user') || this;
    }
    UserEditComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _user_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["UserListUIService"] }
    ]; };
    UserEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-user-edit',
            template: __webpack_require__(/*! raw-loader!./user-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-edit/user-edit.component.html"),
            styles: [__webpack_require__(/*! ./user-edit.component.scss */ "./src/app/reseller/clients-users/users/user-edit/user-edit.component.scss")]
        })
    ], UserEditComponent);
    return UserEditComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/fleio-api/client-user/user/users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../user-list-ui.service */ "./src/app/reseller/clients-users/users/user-list-ui.service.ts");
/* harmony import */ var _shared_ui_api_app_local_storage_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../shared/ui-api/app-local-storage.service */ "./src/app/shared/ui-api/app-local-storage.service.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");








var UserImpersonateComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserImpersonateComponent, _super);
    function UserImpersonateComponent(route, userListUIService, usersApi, appLocalStorage, config) {
        var _this = _super.call(this, route, userListUIService, 'edit', 'user') || this;
        _this.usersApi = usersApi;
        _this.appLocalStorage = appLocalStorage;
        _this.config = config;
        _this.impersonated = false;
        return _this;
    }
    UserImpersonateComponent.prototype.ngOnInit = function () {
        var _this = this;
        _super.prototype.ngOnInit.call(this);
        this.usersApi.objectPostAction(this.object.id, 'impersonate', {
            action: 'impersonate'
        }).subscribe(function (impersonationData) {
            _this.appLocalStorage.setItem('fleio.flStaffBackend', _this.config.getPanelApiUrl(''));
            _this.appLocalStorage.setItem('fleio.flStaffUrl', _this.config.getPanelHomeUrl());
            if (impersonationData.enduser_panel_url) {
                window.location = impersonationData.enduser_panel_url;
            }
            _this.impersonated = true;
        });
    };
    UserImpersonateComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
        { type: _user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["UserListUIService"] },
        { type: _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_2__["UsersApiService"] },
        { type: _shared_ui_api_app_local_storage_service__WEBPACK_IMPORTED_MODULE_6__["AppLocalStorageService"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_7__["ConfigService"] }
    ]; };
    UserImpersonateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-user-impersonate',
            template: __webpack_require__(/*! raw-loader!./user-impersonate.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.html"),
            styles: [__webpack_require__(/*! ./user-impersonate.component.scss */ "./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.scss")]
        })
    ], UserImpersonateComponent);
    return UserImpersonateComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_3__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/client-user/user/users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var _user_ui_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./user-ui.service */ "./src/app/reseller/clients-users/users/user-ui.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _shared_auth_auth_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/auth/auth.service */ "./src/app/shared/auth/auth.service.ts");










var UserListUIService = /** @class */ (function () {
    function UserListUIService(router, config, usersApi, auth) {
        this.router = router;
        this.config = config;
        this.usersApi = usersApi;
        this.auth = auth;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_8__["DatePipe"](config.locale);
    }
    UserListUIService.prototype.getObjectUIService = function (object, permissions, state) {
        return new _user_ui_service__WEBPACK_IMPORTED_MODULE_7__["UserUIService"](object, permissions, state, this.router, this.config, this.usersApi, this.auth);
    };
    UserListUIService.prototype.getTableData = function (objectList) {
        var e_1, _a;
        var tableData = {
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
        try {
            for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](objectList.objects), _c = _b.next(); !_c.done; _c = _b.next()) {
                var object = _c.value;
                var rowUIService = this.getObjectUIService(object, objectList.permissions, 'table-view');
                var user = object;
                var row = {
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
    UserListUIService.prototype.getActions = function (objectList) {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__["RouterLinkAction"]({
                name: 'Create new user',
                tooltip: 'Create new user',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('clients-users/users/create')
            })
        ];
    };
    UserListUIService.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
        { type: _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_6__["UsersApiService"] },
        { type: _shared_auth_auth_service__WEBPACK_IMPORTED_MODULE_9__["AuthService"] }
    ]; };
    UserListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root',
        })
    ], UserListUIService);
    return UserListUIService;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../user-list-ui.service */ "./src/app/reseller/clients-users/users/user-list-ui.service.ts");






var UserListComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserListComponent, _super);
    function UserListComponent(route, userListUIService, refreshService) {
        var _this = _super.call(this, route, userListUIService, refreshService, 'users') || this;
        _this.route = route;
        _this.userListUIService = userListUIService;
        _this.refreshService = refreshService;
        return _this;
    }
    UserListComponent.prototype.ngOnInit = function () {
        _super.prototype.ngOnInit.call(this);
    };
    UserListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _user_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["UserListUIService"] },
        { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
    ]; };
    UserListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-user-list',
            template: __webpack_require__(/*! raw-loader!./user-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/clients-users/users/user-list/user-list.component.html"),
            styles: [__webpack_require__(/*! ./user-list.component.scss */ "./src/app/reseller/clients-users/users/user-list/user-list.component.scss")]
        })
    ], UserListComponent);
    return UserListComponent;
}(_shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"]));



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
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/object-status */ "./src/app/shared/ui/objects-view/interfaces/object-status.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/fleio-api/client-user/user/users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var _tabs_user_details_overview_user_details_overview_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/user-details-overview/user-details-overview.component */ "./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.ts");
/* harmony import */ var _tabs_user_edit_form_user_edit_form_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./tabs/user-edit-form/user-edit-form.component */ "./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.ts");
/* harmony import */ var _tabs_user_details_clients_user_details_clients_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./tabs/user-details-clients/user-details-clients.component */ "./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.ts");
/* harmony import */ var _shared_auth_auth_service__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../../../shared/auth/auth.service */ "./src/app/shared/auth/auth.service.ts");














var UserUIService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserUIService, _super);
    function UserUIService(user, permissions, state, router, config, usersApi, auth) {
        var _this = _super.call(this, user, permissions, state) || this;
        _this.auth = auth;
        _this.router = router;
        _this.config = config;
        _this.usersApi = usersApi;
        return _this;
    }
    UserUIService.prototype.getIcon = function () {
        return {
            name: '(gravatar)',
            gravatarEmail: this.object.email,
        };
    };
    UserUIService.prototype.getStatus = function () {
        return {
            type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined,
            value: this.object.is_active ? _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Active : _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Disabled
        };
    };
    UserUIService.prototype.getTitle = function () {
        switch (this.state) {
            case 'details':
                return {
                    text: this.object.first_name + " " + this.object.last_name,
                    subText: this.object.username,
                };
            case 'edit':
                return {
                    text: this.object.first_name + " " + this.object.last_name,
                    subText: this.object.username,
                };
            case 'create':
                return {
                    text: 'Create user',
                };
            default:
                return {
                    text: this.object.first_name + " " + this.object.last_name,
                    subText: this.object.username,
                };
        }
    };
    UserUIService.prototype.getActions = function () {
        var actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            name: 'Edit',
            tooltip: 'Edit',
            routerUrl: this.config.getPanelUrl("clients-users/users/" + this.object.id + "/edit"),
            router: this.router,
        }));
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
            icon: { name: 'face' },
            name: 'Impersonate user',
            noPermissions: this.auth.isImpersonating(),
            tooltip: this.auth.isImpersonating() ?
                'You cannot impersonate another user while impersonating' : 'Impersonate user',
            routerUrl: this.config.getPanelUrl("clients-users/users/" + this.object.id + "/impersonate"),
            router: this.router,
        }));
        actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_6__["ApiCallAction"]({
            object: this.object,
            icon: { name: 'delete' },
            name: 'Delete',
            tooltip: 'Delete',
            confirmOptions: {
                confirm: true,
                title: 'Delete user',
                message: "Are you sure you want to delete user " + this.object.username + "." +
                    'All data will be lost.',
            },
            apiService: this.usersApi,
            callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_6__["CallType"].Delete,
        }));
        return actions;
    };
    UserUIService.prototype.getDetailsLink = function () {
        return this.config.getPanelUrl("clients-users/users/" + this.object.id);
    };
    UserUIService.prototype.getCardFields = function () {
        var datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_7__["DatePipe"](this.config.locale);
        var fields = [
            {
                name: 'Last login',
                value: this.object.last_login ? datePipe.transform(this.object.last_login) : 'never',
            }
        ];
        return fields;
    };
    UserUIService.prototype.getTabs = function () {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Overview',
                        component: _tabs_user_details_overview_user_details_overview_component__WEBPACK_IMPORTED_MODULE_10__["UserDetailsOverviewComponent"],
                    },
                    {
                        tabName: 'Clients',
                        component: _tabs_user_details_clients_user_details_clients_component__WEBPACK_IMPORTED_MODULE_12__["UserDetailsClientsComponent"],
                    },
                ];
            case 'edit':
            case 'create':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_user_edit_form_user_edit_form_component__WEBPACK_IMPORTED_MODULE_11__["UserEditFormComponent"],
                    },
                ];
        }
    };
    UserUIService.prototype.getDetailsActions = function () {
        var actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("clients-users/users"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("clients-users/users"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    };
    UserUIService.prototype.getCardTags = function () {
        var tags = [];
        return tags;
    };
    UserUIService.ctorParameters = function () { return [
        { type: undefined },
        { type: undefined },
        { type: String },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
        { type: _shared_fleio_api_client_user_user_users_api_service__WEBPACK_IMPORTED_MODULE_9__["UsersApiService"] },
        { type: _shared_auth_auth_service__WEBPACK_IMPORTED_MODULE_13__["AuthService"] }
    ]; };
    return UserUIService;
}(_shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_2__["ObjectUIServiceBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_fleio_api_client_user_user_user_list_resolver__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/fleio-api/client-user/user/user-list.resolver */ "./src/app/shared/fleio-api/client-user/user/user-list.resolver.ts");
/* harmony import */ var _user_list_user_list_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./user-list/user-list.component */ "./src/app/reseller/clients-users/users/user-list/user-list.component.ts");
/* harmony import */ var _user_create_user_create_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./user-create/user-create.component */ "./src/app/reseller/clients-users/users/user-create/user-create.component.ts");
/* harmony import */ var _user_details_user_details_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./user-details/user-details.component */ "./src/app/reseller/clients-users/users/user-details/user-details.component.ts");
/* harmony import */ var _shared_fleio_api_client_user_user_user_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/client-user/user/user.resolver */ "./src/app/shared/fleio-api/client-user/user/user.resolver.ts");
/* harmony import */ var _user_edit_user_edit_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./user-edit/user-edit.component */ "./src/app/reseller/clients-users/users/user-edit/user-edit.component.ts");
/* harmony import */ var _user_impersonate_user_impersonate_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./user-impersonate/user-impersonate.component */ "./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/ui-api/interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");












var routes = [
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
                    objectList: function (data) {
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
                getBreadCrumbDetail: function (data) {
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
                getBreadCrumbDetail: function (data) {
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
                getBreadCrumbDetail: function (data) {
                    return "Edit " + data.user.username;
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
                getBreadCrumbDetail: function (data) {
                    return "Impersonating " + data.user.username;
                },
            },
        }
    },
];
var UsersRoutingModule = /** @class */ (function () {
    function UsersRoutingModule() {
    }
    UsersRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
        })
    ], UsersRoutingModule);
    return UsersRoutingModule;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _user_list_user_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./user-list/user-list.component */ "./src/app/reseller/clients-users/users/user-list/user-list.component.ts");
/* harmony import */ var _user_create_user_create_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./user-create/user-create.component */ "./src/app/reseller/clients-users/users/user-create/user-create.component.ts");
/* harmony import */ var _user_details_user_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./user-details/user-details.component */ "./src/app/reseller/clients-users/users/user-details/user-details.component.ts");
/* harmony import */ var _user_edit_user_edit_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./user-edit/user-edit.component */ "./src/app/reseller/clients-users/users/user-edit/user-edit.component.ts");
/* harmony import */ var _users_routing_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./users-routing.module */ "./src/app/reseller/clients-users/users/users-routing.module.ts");
/* harmony import */ var _tabs_user_details_overview_user_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/user-details-overview/user-details-overview.component */ "./src/app/reseller/clients-users/users/tabs/user-details-overview/user-details-overview.component.ts");
/* harmony import */ var _tabs_user_edit_form_user_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/user-edit-form/user-edit-form.component */ "./src/app/reseller/clients-users/users/tabs/user-edit-form/user-edit-form.component.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm5/form-field.es5.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm5/input.es5.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm5/checkbox.es5.js");
/* harmony import */ var _tabs_user_details_clients_user_details_clients_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./tabs/user-details-clients/user-details-clients.component */ "./src/app/reseller/clients-users/users/tabs/user-details-clients/user-details-clients.component.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/table */ "./node_modules/@angular/material/esm5/table.es5.js");
/* harmony import */ var _user_impersonate_user_impersonate_component__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./user-impersonate/user-impersonate.component */ "./src/app/reseller/clients-users/users/user-impersonate/user-impersonate.component.ts");




















var UsersModule = /** @class */ (function () {
    function UsersModule() {
    }
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
    return UsersModule;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _users_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");





var UserListResolver = /** @class */ (function () {
    function UserListResolver(usersApi) {
        this.usersApi = usersApi;
    }
    UserListResolver.prototype.resolve = function (route, state) {
        return this.usersApi.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    UserListResolver.ctorParameters = function () { return [
        { type: _users_api_service__WEBPACK_IMPORTED_MODULE_3__["UsersApiService"] }
    ]; };
    UserListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], UserListResolver);
    return UserListResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _users_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./users-api.service */ "./src/app/shared/fleio-api/client-user/user/users-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");





var UserResolver = /** @class */ (function () {
    function UserResolver(usersApi) {
        this.usersApi = usersApi;
    }
    UserResolver.prototype.resolve = function (route, state) {
        return this.usersApi.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    UserResolver.ctorParameters = function () { return [
        { type: _users_api_service__WEBPACK_IMPORTED_MODULE_3__["UsersApiService"] }
    ]; };
    UserResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], UserResolver);
    return UserResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var UsersApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UsersApiService, _super);
    // noinspection JSUnusedGlobalSymbols
    function UsersApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('users')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    UsersApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    UsersApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], UsersApiService);
    return UsersApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ })

}]);
//# sourceMappingURL=users-users-module-es5.js.map