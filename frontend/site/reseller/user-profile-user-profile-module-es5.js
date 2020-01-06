(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["user-profile-user-profile-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.html":
/*!*******************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.html ***!
  \*******************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div [formGroup]=\"profileForm\" fxLayout=\"column\">\n  <app-form-errors #formErrors [formGroup]=\"profileForm\"></app-form-errors>\n  <div fxLayout=\"row\" fxLayout.lt-md=\"column\">\n    <mat-form-field fxFlex=\"48\">\n      <input matInput placeholder=\"First name\" type=\"text\" formControlName=\"first_name\" required>\n      <mat-error>{{backendErrors['first_name'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n    <mat-form-field fxFlex=\"50\" fxFlexOffset=\"2\" fxFlexOffset.lt-md=\"0\">\n      <input matInput placeholder=\"Last name\" type=\"text\" formControlName=\"last_name\" required>\n      <mat-error>{{backendErrors['last_name'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n  </div>\n  <div fxLayout=\"row\" fxLayout.lt-md=\"column\">\n    <mat-form-field fxFlex=\"48\">\n      <input matInput placeholder=\"Email address\" type=\"email\" formControlName=\"email\" required>\n      <mat-error>{{backendErrors['email'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n    <app-phone-input [phoneNumber]=\"phoneNumber\" (changedPhone)=\"onChangedPhone($event)\" fxFlex=\"50\"\n                     fxFlexOffset=\"2\" fxFlexOffset.lt-md=\"0\" #phoneNumberInputComponent>\n    </app-phone-input>\n    <input type=\"hidden\" formControlName=\"mobile_phone_number\">\n  </div>\n  <div fxLayout=\"row\">\n    <mat-form-field fxFlex=\"48\">\n      <input matInput placeholder=\"Old password\"\n             [attr.type]=\"showOldPasswordText ? 'text' : 'password'\" formControlName=\"old_password\">\n      <mat-error>{{backendErrors['old_password'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n    <div>\n      <button (mousedown)=\"showOldPasswordText = true;\"\n              (mouseup)=\"showOldPasswordText = false;\"\n              class=\"fl-margin-top-medium\"\n              mat-icon-button\n              fl-tooltip=\"Hold button to reveal password\">\n        <mat-icon>visibility</mat-icon>\n      </button>\n    </div>\n    <mat-form-field fxFlex=\"50\" fxFlexOffset=\"2\">\n      <input matInput placeholder=\"Password\"\n             [attr.type]=\"showPasswordText ? 'text' : 'password'\" formControlName=\"password\">\n      <mat-error>{{backendErrors['password'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n    <div>\n      <button (mousedown)=\"showPasswordText = true;\"\n              (mouseup)=\"showPasswordText = false;\"\n              class=\"fl-margin-top-medium\"\n              mat-icon-button\n              fl-tooltip=\"Hold button to reveal password\">\n        <mat-icon>visibility</mat-icon>\n      </button>\n    </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.html":
/*!****************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.html ***!
  \****************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.scss":
/*!*****************************************************************************************************************!*\
  !*** ./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.scss ***!
  \*****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3Byb2ZpbGUvdXNlci1wcm9maWxlL3RhYnMvdXNlci1wcm9maWxlLWVkaXQtZm9ybS91c2VyLXByb2ZpbGUtZWRpdC1mb3JtLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.ts":
/*!***************************************************************************************************************!*\
  !*** ./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.ts ***!
  \***************************************************************************************************************/
/*! exports provided: UserProfileEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileEditFormComponent", function() { return UserProfileEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/fleio-api/profile/user-profile/user-profile-api.service */ "./src/app/shared/fleio-api/profile/user-profile/user-profile-api.service.ts");
/* harmony import */ var _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");







var UserProfileEditFormComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserProfileEditFormComponent, _super);
    function UserProfileEditFormComponent(formBuilder, userProfileApiService, notificationService) {
        var _this = _super.call(this) || this;
        _this.formBuilder = formBuilder;
        _this.userProfileApiService = userProfileApiService;
        _this.notificationService = notificationService;
        _this.profileForm = _this.formBuilder.group({
            first_name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            last_name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            email: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            mobile_phone_number: [''],
            old_password: [''],
            password: [''],
        });
        _this.showOldPasswordText = false;
        _this.showPasswordText = false;
        _this.phoneNumber = '';
        return _this;
    }
    UserProfileEditFormComponent.prototype.saveProfile = function () {
        var _this = this;
        if (this.profileForm.invalid) {
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["of"])(null);
        }
        var value = this.profileForm.value;
        this.userProfileApiService.putAction('update', value).subscribe(function (response) {
            if (_this.phoneNumberInputComponent.error) {
                _this.phoneNumberInputComponent.error = null;
            }
            _this.notificationService.showMessage('User profile updated.');
        }, function (error) {
            _this.backendErrors = error.error;
            if (_this.backendErrors.mobile_phone_number) {
                _this.phoneNumberInputComponent.error = _this.backendErrors.mobile_phone_number;
            }
            else {
                _this.phoneNumberInputComponent.error = null;
            }
            _this.formErrors.setBackendErrors(_this.backendErrors);
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["of"])(null);
    };
    UserProfileEditFormComponent.prototype.onChangedPhone = function (newNumber) {
        this.profileForm.controls.mobile_phone_number.setValue(newNumber);
    };
    UserProfileEditFormComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.objectController.actionCallback = function () { return _this.saveProfile(); };
        this.profileForm.patchValue(this.object.user);
        if (this.object.user.mobile_phone_number) {
            this.phoneNumber = this.object.user.mobile_phone_number;
        }
    };
    UserProfileEditFormComponent.ctorParameters = function () { return [
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
        { type: _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_5__["UserProfileApiService"] },
        { type: _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_6__["NotificationService"] }
    ]; };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('phoneNumberInputComponent', { static: false })
    ], UserProfileEditFormComponent.prototype, "phoneNumberInputComponent", void 0);
    UserProfileEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-user-profile-edit-form',
            template: __webpack_require__(/*! raw-loader!./user-profile-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.html"),
            styles: [__webpack_require__(/*! ./user-profile-edit-form.component.scss */ "./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.scss")]
        })
    ], UserProfileEditFormComponent);
    return UserProfileEditFormComponent;
}(_shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"]));



/***/ }),

/***/ "./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.scss":
/*!**************************************************************************************************!*\
  !*** ./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.scss ***!
  \**************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3Byb2ZpbGUvdXNlci1wcm9maWxlL3VzZXItcHJvZmlsZS1lZGl0L3VzZXItcHJvZmlsZS1lZGl0LmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.ts":
/*!************************************************************************************************!*\
  !*** ./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.ts ***!
  \************************************************************************************************/
/*! exports provided: UserProfileEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileEditComponent", function() { return UserProfileEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _user_profile_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../user-profile-list-ui.service */ "./src/app/reseller/profile/user-profile/user-profile-list-ui.service.ts");





var UserProfileEditComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserProfileEditComponent, _super);
    function UserProfileEditComponent(route, userProfileListUiService) {
        return _super.call(this, route, userProfileListUiService, 'edit', 'userProfile') || this;
    }
    UserProfileEditComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _user_profile_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["UserProfileListUiService"] }
    ]; };
    UserProfileEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-user-profile-edit',
            template: __webpack_require__(/*! raw-loader!./user-profile-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.html"),
            styles: [__webpack_require__(/*! ./user-profile-edit.component.scss */ "./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.scss")]
        })
    ], UserProfileEditComponent);
    return UserProfileEditComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



/***/ }),

/***/ "./src/app/reseller/profile/user-profile/user-profile-list-ui.service.ts":
/*!*******************************************************************************!*\
  !*** ./src/app/reseller/profile/user-profile/user-profile-list-ui.service.ts ***!
  \*******************************************************************************/
/*! exports provided: UserProfileListUiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileListUiService", function() { return UserProfileListUiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/fleio-api/profile/user-profile/user-profile-api.service */ "./src/app/shared/fleio-api/profile/user-profile/user-profile-api.service.ts");
/* harmony import */ var _user_profile_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./user-profile-ui.service */ "./src/app/reseller/profile/user-profile/user-profile-ui.service.ts");






var UserProfileListUiService = /** @class */ (function () {
    function UserProfileListUiService(router, config, userProfileApiService) {
        this.router = router;
        this.config = config;
        this.userProfileApiService = userProfileApiService;
    }
    UserProfileListUiService.prototype.getTableData = function (objectList) {
        return {
            header: {
                columns: [],
                columnNames: [],
            },
            rows: []
        };
    };
    UserProfileListUiService.prototype.getObjectUIService = function (object, permissions, state) {
        return new _user_profile_ui_service__WEBPACK_IMPORTED_MODULE_5__["UserProfileUiService"](object, permissions, state, this.router, this.config, this.userProfileApiService);
    };
    UserProfileListUiService.prototype.getActions = function (objectList) {
        return [];
    };
    UserProfileListUiService.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
        { type: _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_4__["UserProfileApiService"] }
    ]; };
    UserProfileListUiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], UserProfileListUiService);
    return UserProfileListUiService;
}());



/***/ }),

/***/ "./src/app/reseller/profile/user-profile/user-profile-routing.module.ts":
/*!******************************************************************************!*\
  !*** ./src/app/reseller/profile/user-profile/user-profile-routing.module.ts ***!
  \******************************************************************************/
/*! exports provided: UserProfileRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileRoutingModule", function() { return UserProfileRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _user_profile_edit_user_profile_edit_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./user-profile-edit/user-profile-edit.component */ "./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.ts");
/* harmony import */ var _shared_fleio_api_profile_user_profile_user_profile_resolver__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/fleio-api/profile/user-profile/user-profile.resolver */ "./src/app/shared/fleio-api/profile/user-profile/user-profile.resolver.ts");





var routes = [
    {
        path: 'edit',
        component: _user_profile_edit_user_profile_edit_component__WEBPACK_IMPORTED_MODULE_3__["UserProfileEditComponent"],
        resolve: {
            userProfile: _shared_fleio_api_profile_user_profile_user_profile_resolver__WEBPACK_IMPORTED_MODULE_4__["UserProfileResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: function () {
                    return 'Edit user profile';
                },
            },
        }
    },
];
var UserProfileRoutingModule = /** @class */ (function () {
    function UserProfileRoutingModule() {
    }
    UserProfileRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
        })
    ], UserProfileRoutingModule);
    return UserProfileRoutingModule;
}());



/***/ }),

/***/ "./src/app/reseller/profile/user-profile/user-profile-ui.service.ts":
/*!**************************************************************************!*\
  !*** ./src/app/reseller/profile/user-profile/user-profile-ui.service.ts ***!
  \**************************************************************************/
/*! exports provided: UserProfileUiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileUiService", function() { return UserProfileUiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/fleio-api/profile/user-profile/user-profile-api.service */ "./src/app/shared/fleio-api/profile/user-profile/user-profile-api.service.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _tabs_user_profile_edit_form_user_profile_edit_form_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./tabs/user-profile-edit-form/user-profile-edit-form.component */ "./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");









var UserProfileUiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserProfileUiService, _super);
    function UserProfileUiService(userProfile, permissions, state, router, config, userProfileApiService) {
        var _this = _super.call(this, userProfile, permissions, state) || this;
        _this.router = router;
        _this.config = config;
        _this.userProfileApiService = userProfileApiService;
        _this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_3__["DatePipe"](_this.config.locale);
        return _this;
    }
    UserProfileUiService.prototype.getIcon = function () {
        return null;
    };
    UserProfileUiService.prototype.getStatus = function () {
        return null;
    };
    UserProfileUiService.prototype.getTitle = function () {
        switch (this.state) {
            case 'edit':
                return {
                    text: "" + this.object.user.username,
                };
            default:
                return {
                    text: "" + this.object.user.username,
                    subText: "",
                };
        }
    };
    UserProfileUiService.prototype.getActions = function () {
        return [];
    };
    UserProfileUiService.prototype.getDetailsActions = function () {
        var actions = [];
        switch (this.state) {
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_7__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(""),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    };
    UserProfileUiService.prototype.getCardFields = function () {
        return [];
    };
    UserProfileUiService.prototype.getTabs = function () {
        switch (this.state) {
            case 'edit':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_user_profile_edit_form_user_profile_edit_form_component__WEBPACK_IMPORTED_MODULE_6__["UserProfileEditFormComponent"],
                    },
                ];
        }
    };
    UserProfileUiService.prototype.getCardTags = function () {
        return [];
    };
    UserProfileUiService.ctorParameters = function () { return [
        { type: undefined },
        { type: undefined },
        { type: String },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_1__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] },
        { type: _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_4__["UserProfileApiService"] }
    ]; };
    return UserProfileUiService;
}(_shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_5__["ObjectUIServiceBase"]));



/***/ }),

/***/ "./src/app/reseller/profile/user-profile/user-profile.module.ts":
/*!**********************************************************************!*\
  !*** ./src/app/reseller/profile/user-profile/user-profile.module.ts ***!
  \**********************************************************************/
/*! exports provided: UserProfileModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileModule", function() { return UserProfileModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _user_profile_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./user-profile-routing.module */ "./src/app/reseller/profile/user-profile/user-profile-routing.module.ts");
/* harmony import */ var _user_profile_edit_user_profile_edit_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./user-profile-edit/user-profile-edit.component */ "./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.ts");
/* harmony import */ var _tabs_user_profile_edit_form_user_profile_edit_form_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tabs/user-profile-edit-form/user-profile-edit-form.component */ "./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm5/form-field.es5.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm5/input.es5.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var _shared_ui_ui_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/ui/ui.module */ "./src/app/shared/ui/ui.module.ts");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/icon */ "./node_modules/@angular/material/esm5/icon.es5.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm5/button.es5.js");















var UserProfileModule = /** @class */ (function () {
    function UserProfileModule() {
    }
    UserProfileModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            declarations: [
                _user_profile_edit_user_profile_edit_component__WEBPACK_IMPORTED_MODULE_4__["UserProfileEditComponent"],
                _tabs_user_profile_edit_form_user_profile_edit_form_component__WEBPACK_IMPORTED_MODULE_5__["UserProfileEditFormComponent"]
            ],
            entryComponents: [
                _tabs_user_profile_edit_form_user_profile_edit_form_component__WEBPACK_IMPORTED_MODULE_5__["UserProfileEditFormComponent"]
            ],
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _user_profile_routing_module__WEBPACK_IMPORTED_MODULE_3__["UserProfileRoutingModule"],
                _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_6__["ObjectsViewModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_7__["ReactiveFormsModule"],
                _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_8__["ErrorHandlingModule"],
                _angular_material_form_field__WEBPACK_IMPORTED_MODULE_9__["MatFormFieldModule"],
                _angular_material_input__WEBPACK_IMPORTED_MODULE_10__["MatInputModule"],
                _angular_flex_layout__WEBPACK_IMPORTED_MODULE_11__["FlexModule"],
                _shared_ui_ui_module__WEBPACK_IMPORTED_MODULE_12__["UiModule"],
                _angular_material_icon__WEBPACK_IMPORTED_MODULE_13__["MatIconModule"],
                _angular_material_button__WEBPACK_IMPORTED_MODULE_14__["MatButtonModule"],
            ]
        })
    ], UserProfileModule);
    return UserProfileModule;
}());



/***/ }),

/***/ "./src/app/shared/fleio-api/profile/user-profile/user-profile-api.service.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/profile/user-profile/user-profile-api.service.ts ***!
  \***********************************************************************************/
/*! exports provided: UserProfileApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileApiService", function() { return UserProfileApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var UserProfileApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](UserProfileApiService, _super);
    function UserProfileApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('userprofile')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    UserProfileApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    UserProfileApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], UserProfileApiService);
    return UserProfileApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ }),

/***/ "./src/app/shared/fleio-api/profile/user-profile/user-profile.resolver.ts":
/*!********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/profile/user-profile/user-profile.resolver.ts ***!
  \********************************************************************************/
/*! exports provided: UserProfileResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserProfileResolver", function() { return UserProfileResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _user_profile_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./user-profile-api.service */ "./src/app/shared/fleio-api/profile/user-profile/user-profile-api.service.ts");





var UserProfileResolver = /** @class */ (function () {
    function UserProfileResolver(userProfileApiService) {
        this.userProfileApiService = userProfileApiService;
    }
    UserProfileResolver.prototype.resolve = function (route, state) {
        return this.userProfileApiService.list().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    UserProfileResolver.ctorParameters = function () { return [
        { type: _user_profile_api_service__WEBPACK_IMPORTED_MODULE_4__["UserProfileApiService"] }
    ]; };
    UserProfileResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], UserProfileResolver);
    return UserProfileResolver;
}());



/***/ })

}]);
//# sourceMappingURL=user-profile-user-profile-module-es5.js.map