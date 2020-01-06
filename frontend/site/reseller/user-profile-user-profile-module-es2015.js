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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/fleio-api/profile/user-profile/user-profile-api.service */ "./src/app/shared/fleio-api/profile/user-profile/user-profile-api.service.ts");
/* harmony import */ var _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");







let UserProfileEditFormComponent = class UserProfileEditFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"] {
    constructor(formBuilder, userProfileApiService, notificationService) {
        super();
        this.formBuilder = formBuilder;
        this.userProfileApiService = userProfileApiService;
        this.notificationService = notificationService;
        this.profileForm = this.formBuilder.group({
            first_name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            last_name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            email: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            mobile_phone_number: [''],
            old_password: [''],
            password: [''],
        });
        this.showOldPasswordText = false;
        this.showPasswordText = false;
        this.phoneNumber = '';
    }
    saveProfile() {
        if (this.profileForm.invalid) {
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["of"])(null);
        }
        const value = this.profileForm.value;
        this.userProfileApiService.putAction('update', value).subscribe(response => {
            if (this.phoneNumberInputComponent.error) {
                this.phoneNumberInputComponent.error = null;
            }
            this.notificationService.showMessage('User profile updated.');
        }, error => {
            this.backendErrors = error.error;
            if (this.backendErrors.mobile_phone_number) {
                this.phoneNumberInputComponent.error = this.backendErrors.mobile_phone_number;
            }
            else {
                this.phoneNumberInputComponent.error = null;
            }
            this.formErrors.setBackendErrors(this.backendErrors);
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["of"])(null);
    }
    onChangedPhone(newNumber) {
        this.profileForm.controls.mobile_phone_number.setValue(newNumber);
    }
    ngOnInit() {
        this.objectController.actionCallback = () => this.saveProfile();
        this.profileForm.patchValue(this.object.user);
        if (this.object.user.mobile_phone_number) {
            this.phoneNumber = this.object.user.mobile_phone_number;
        }
    }
};
UserProfileEditFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
    { type: _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_5__["UserProfileApiService"] },
    { type: _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_6__["NotificationService"] }
];
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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _user_profile_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../user-profile-list-ui.service */ "./src/app/reseller/profile/user-profile/user-profile-list-ui.service.ts");





let UserProfileEditComponent = class UserProfileEditComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, userProfileListUiService) {
        super(route, userProfileListUiService, 'edit', 'userProfile');
    }
};
UserProfileEditComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _user_profile_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["UserProfileListUiService"] }
];
UserProfileEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-user-profile-edit',
        template: __webpack_require__(/*! raw-loader!./user-profile-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.html"),
        styles: [__webpack_require__(/*! ./user-profile-edit.component.scss */ "./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.scss")]
    })
], UserProfileEditComponent);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/fleio-api/profile/user-profile/user-profile-api.service */ "./src/app/shared/fleio-api/profile/user-profile/user-profile-api.service.ts");
/* harmony import */ var _user_profile_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./user-profile-ui.service */ "./src/app/reseller/profile/user-profile/user-profile-ui.service.ts");






let UserProfileListUiService = class UserProfileListUiService {
    constructor(router, config, userProfileApiService) {
        this.router = router;
        this.config = config;
        this.userProfileApiService = userProfileApiService;
    }
    getTableData(objectList) {
        return {
            header: {
                columns: [],
                columnNames: [],
            },
            rows: []
        };
    }
    getObjectUIService(object, permissions, state) {
        return new _user_profile_ui_service__WEBPACK_IMPORTED_MODULE_5__["UserProfileUiService"](object, permissions, state, this.router, this.config, this.userProfileApiService);
    }
    getActions(objectList) {
        return [];
    }
};
UserProfileListUiService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_4__["UserProfileApiService"] }
];
UserProfileListUiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], UserProfileListUiService);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _user_profile_edit_user_profile_edit_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./user-profile-edit/user-profile-edit.component */ "./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.ts");
/* harmony import */ var _shared_fleio_api_profile_user_profile_user_profile_resolver__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/fleio-api/profile/user-profile/user-profile.resolver */ "./src/app/shared/fleio-api/profile/user-profile/user-profile.resolver.ts");





const routes = [
    {
        path: 'edit',
        component: _user_profile_edit_user_profile_edit_component__WEBPACK_IMPORTED_MODULE_3__["UserProfileEditComponent"],
        resolve: {
            userProfile: _shared_fleio_api_profile_user_profile_user_profile_resolver__WEBPACK_IMPORTED_MODULE_4__["UserProfileResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: () => {
                    return 'Edit user profile';
                },
            },
        }
    },
];
let UserProfileRoutingModule = class UserProfileRoutingModule {
};
UserProfileRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], UserProfileRoutingModule);



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
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/fleio-api/profile/user-profile/user-profile-api.service */ "./src/app/shared/fleio-api/profile/user-profile/user-profile-api.service.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _tabs_user_profile_edit_form_user_profile_edit_form_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tabs/user-profile-edit-form/user-profile-edit-form.component */ "./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");








class UserProfileUiService extends _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_4__["ObjectUIServiceBase"] {
    constructor(userProfile, permissions, state, router, config, userProfileApiService) {
        super(userProfile, permissions, state);
        this.router = router;
        this.config = config;
        this.userProfileApiService = userProfileApiService;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_2__["DatePipe"](this.config.locale);
    }
    getIcon() {
        return null;
    }
    getStatus() {
        return null;
    }
    getTitle() {
        switch (this.state) {
            case 'edit':
                return {
                    text: `${this.object.user.username}`,
                };
            default:
                return {
                    text: `${this.object.user.username}`,
                    subText: ``,
                };
        }
    }
    getActions() {
        return [];
    }
    getDetailsActions() {
        const actions = [];
        switch (this.state) {
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_6__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(``),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    }
    getCardFields() {
        return [];
    }
    getTabs() {
        switch (this.state) {
            case 'edit':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_user_profile_edit_form_user_profile_edit_form_component__WEBPACK_IMPORTED_MODULE_5__["UserProfileEditFormComponent"],
                    },
                ];
        }
    }
    getCardTags() {
        return [];
    }
}
UserProfileUiService.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_0__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_1__["ConfigService"] },
    { type: _shared_fleio_api_profile_user_profile_user_profile_api_service__WEBPACK_IMPORTED_MODULE_3__["UserProfileApiService"] }
];


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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _user_profile_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./user-profile-routing.module */ "./src/app/reseller/profile/user-profile/user-profile-routing.module.ts");
/* harmony import */ var _user_profile_edit_user_profile_edit_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./user-profile-edit/user-profile-edit.component */ "./src/app/reseller/profile/user-profile/user-profile-edit/user-profile-edit.component.ts");
/* harmony import */ var _tabs_user_profile_edit_form_user_profile_edit_form_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tabs/user-profile-edit-form/user-profile-edit-form.component */ "./src/app/reseller/profile/user-profile/tabs/user-profile-edit-form/user-profile-edit-form.component.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _shared_ui_ui_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/ui/ui.module */ "./src/app/shared/ui/ui.module.ts");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/icon */ "./node_modules/@angular/material/esm2015/icon.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm2015/button.js");















let UserProfileModule = class UserProfileModule {
};
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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let UserProfileApiService = class UserProfileApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('userprofile'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
UserProfileApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
UserProfileApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], UserProfileApiService);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _user_profile_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./user-profile-api.service */ "./src/app/shared/fleio-api/profile/user-profile/user-profile-api.service.ts");





let UserProfileResolver = class UserProfileResolver {
    constructor(userProfileApiService) {
        this.userProfileApiService = userProfileApiService;
    }
    resolve(route, state) {
        return this.userProfileApiService.list().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
UserProfileResolver.ctorParameters = () => [
    { type: _user_profile_api_service__WEBPACK_IMPORTED_MODULE_4__["UserProfileApiService"] }
];
UserProfileResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], UserProfileResolver);



/***/ })

}]);
//# sourceMappingURL=user-profile-user-profile-module-es2015.js.map