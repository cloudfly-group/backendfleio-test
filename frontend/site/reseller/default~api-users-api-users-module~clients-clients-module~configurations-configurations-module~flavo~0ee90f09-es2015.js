(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"],{

/***/ "./src/app/shared/ui/objects-view/actions/base-action.ts":
/*!***************************************************************!*\
  !*** ./src/app/shared/ui/objects-view/actions/base-action.ts ***!
  \***************************************************************/
/*! exports provided: BaseAction */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BaseAction", function() { return BaseAction; });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");


class BaseAction {
    constructor(init) {
        this.refreshAfterExecute = true;
        this.redirectAfterExecute = false;
        Object.assign(this, init);
        if (this.noPermissions && !this.tooltip) {
            this.tooltip = 'You don\'t have permissions to perform this action';
        }
    }
    executeImpl() {
        console.warn('Base object action executeImpl method invoked, ' +
            'override this in your derived classes.');
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_0__["of"])({ message: 'Base object action execute method invoked.' }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_1__["delay"])(1000));
    }
    getActiveOptions(executionOptions) {
        const activeOptions = {
            displayConfirmation: true,
            displayMessages: true,
        };
        if (this.options) {
            activeOptions.displayConfirmation =
                activeOptions.displayConfirmation && this.options.displayConfirmation;
            activeOptions.displayMessages = activeOptions.displayMessages && this.options.displayMessages;
        }
        if (executionOptions) {
            activeOptions.displayConfirmation =
                activeOptions.displayConfirmation && executionOptions.displayConfirmation;
            activeOptions.displayMessages = activeOptions.displayMessages && executionOptions.displayMessages;
        }
        return activeOptions;
    }
    execute(notificationService, refreshService, options) {
        this.isRunning = true;
        this.notificationService = notificationService;
        const activeOptions = this.getActiveOptions(options);
        let dialogResult$ = Object(rxjs__WEBPACK_IMPORTED_MODULE_0__["of"])('yes');
        if (this.confirmOptions && this.confirmOptions.confirm && activeOptions.displayConfirmation) {
            dialogResult$ = notificationService.confirmDialog({
                title: this.confirmOptions.title,
                message: this.confirmOptions.message,
            });
        }
        dialogResult$.subscribe(dialogResult => {
            if (dialogResult === 'yes') {
                this.executeImpl().subscribe(result => {
                    this.isRunning = false;
                    if (activeOptions.displayMessages && result) {
                        notificationService.showMessage(result.message);
                    }
                    if (this.refreshAfterExecute) {
                        refreshService.refresh();
                    }
                    if (this.redirectAfterExecute) {
                        refreshService.redirect(this.redirectUrl);
                    }
                });
            }
            else {
                this.isRunning = false;
            }
        });
    }
}
BaseAction.ctorParameters = () => [
    { type: undefined }
];


/***/ }),

/***/ "./src/app/shared/ui/objects-view/actions/callback-action.ts":
/*!*******************************************************************!*\
  !*** ./src/app/shared/ui/objects-view/actions/callback-action.ts ***!
  \*******************************************************************/
/*! exports provided: CallbackAction */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CallbackAction", function() { return CallbackAction; });
/* harmony import */ var _base_action__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base-action */ "./src/app/shared/ui/objects-view/actions/base-action.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");


class CallbackAction extends _base_action__WEBPACK_IMPORTED_MODULE_0__["BaseAction"] {
    constructor(init) {
        super(init);
        if (!this.options) {
            this.options = { displayConfirmation: false, displayMessages: false };
        }
        this.refreshAfterExecute = init ? !!init.refreshAfterExecute : false;
    }
    executeImpl() {
        if (this.callback) {
            return this.callback(this);
        }
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["of"])(null);
    }
}
CallbackAction.ctorParameters = () => [
    { type: undefined }
];


/***/ }),

/***/ "./src/app/shared/ui/objects-view/actions/router-link-action.ts":
/*!**********************************************************************!*\
  !*** ./src/app/shared/ui/objects-view/actions/router-link-action.ts ***!
  \**********************************************************************/
/*! exports provided: RouterLinkAction */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RouterLinkAction", function() { return RouterLinkAction; });
/* harmony import */ var _base_action__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base-action */ "./src/app/shared/ui/objects-view/actions/base-action.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");



class RouterLinkAction extends _base_action__WEBPACK_IMPORTED_MODULE_0__["BaseAction"] {
    constructor(init) {
        super(init);
        if (!this.options) {
            this.options = { displayConfirmation: false, displayMessages: false };
        }
        this.refreshAfterExecute = false;
    }
    executeImpl() {
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["from"])(this.router.navigateByUrl(this.routerUrl)).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["map"])(result => {
            return { message: 'Navigated successfully' };
        }));
    }
}
RouterLinkAction.ctorParameters = () => [
    { type: undefined }
];


/***/ }),

/***/ "./src/app/shared/ui/objects-view/details-base.ts":
/*!********************************************************!*\
  !*** ./src/app/shared/ui/objects-view/details-base.ts ***!
  \********************************************************/
/*! exports provided: DetailsBase */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DetailsBase", function() { return DetailsBase; });
/* harmony import */ var _object_controller__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./object-controller */ "./src/app/shared/ui/objects-view/object-controller.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");



class DetailsBase {
    constructor(route, objectListUIService, state, objectName, additionalObjectNames = null) {
        this.route = route;
        this.objectListUIService = objectListUIService;
        this.state = state;
        this.objectName = objectName;
        this.additionalObjectNames = additionalObjectNames;
    }
    get object() {
        return this.objectController.object;
    }
    ngOnInit() {
        this.objectController = new _object_controller__WEBPACK_IMPORTED_MODULE_0__["ObjectController"](this.route.data.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_1__["map"])((data) => {
            let object;
            let additionalObjects;
            if (this.objectName) {
                object = data[this.objectName];
                if (!object) {
                    console.error(`No object named ${this.objectName} found in router data`);
                }
                if (this.additionalObjectNames) {
                    additionalObjects = {};
                    for (const additionalObjectName of this.additionalObjectNames) {
                        const additionalObject = data[additionalObjectName];
                        if (!additionalObject) {
                            console.error(`No additional object named ${additionalObjectName} found in router data`);
                            console.error(data);
                        }
                        else {
                            additionalObjects[additionalObjectName] = data[additionalObjectName];
                        }
                    }
                }
            }
            else {
                object = {};
            }
            return {
                object,
                additionalObjects,
                permissions: data.permissions,
            };
        })), this.objectListUIService, this.state);
    }
    ngOnDestroy() {
        if (this.objectController) {
            this.objectController.unsubscribe();
            this.objectController = null;
        }
    }
}
DetailsBase.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
    { type: undefined },
    { type: String },
    { type: String },
    { type: undefined }
];


/***/ }),

/***/ "./src/app/shared/ui/objects-view/details-component-base.ts":
/*!******************************************************************!*\
  !*** ./src/app/shared/ui/objects-view/details-component-base.ts ***!
  \******************************************************************/
/*! exports provided: DetailsComponentBase */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DetailsComponentBase", function() { return DetailsComponentBase; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _ui_api_helpers_refresh_timer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../ui-api/helpers/refresh-timer */ "./src/app/shared/ui-api/helpers/refresh-timer.ts");



class DetailsComponentBase {
    constructor() {
        this.tabActive = false;
    }
    ngOnDestroy() {
        if (this.refreshTimer) {
            this.refreshTimer.stop();
            delete this.refreshTimer;
        }
    }
    get object() {
        return this.objectController.object;
    }
    initTabEvents() {
        this.objectController.currentTabIndex$.subscribe(tabIndex => {
            if (tabIndex === this.componentTabIndex) {
                if (!this.tabActive) {
                    this.tabActive = true;
                    this.tabActivated();
                }
            }
            else {
                if (this.tabActive) {
                    this.tabActive = false;
                    this.tabDeactivated();
                }
            }
        });
    }
    setupRefreshTimer(interval) {
        this.initTabEvents();
        this.refreshTimer = new _ui_api_helpers_refresh_timer__WEBPACK_IMPORTED_MODULE_2__["RefreshTimer"](interval, () => {
            this.refreshData();
        }, false);
    }
    boostRefreshTimer(boostIntervals = _ui_api_helpers_refresh_timer__WEBPACK_IMPORTED_MODULE_2__["DEFAULT_BOOST_INTERVALS"]) {
        if (!this.refreshTimer) {
            console.error('refresh timer is not initialized');
            return;
        }
        this.refreshTimer.boost(boostIntervals);
    }
    tabActivated() {
        if (this.refreshTimer) {
            this.refreshData();
            this.refreshTimer.start();
        }
    }
    tabDeactivated() {
        if (this.refreshTimer) {
            this.refreshTimer.stop();
        }
    }
    refreshData() {
    }
}
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], DetailsComponentBase.prototype, "objectController", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], DetailsComponentBase.prototype, "componentTabIndex", void 0);


/***/ }),

/***/ "./src/app/shared/ui/objects-view/details-form-base.ts":
/*!*************************************************************!*\
  !*** ./src/app/shared/ui/objects-view/details-form-base.ts ***!
  \*************************************************************/
/*! exports provided: DetailsFormBase */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DetailsFormBase", function() { return DetailsFormBase; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _details_component_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");





class DetailsFormBase extends _details_component_base__WEBPACK_IMPORTED_MODULE_1__["DetailsComponentBase"] {
    constructor() {
        super(...arguments);
        this.backendErrors = {};
    }
    validate() {
        if (!this.formErrors) {
            console.error('You should declare form errors in your form');
        }
        else {
            if (!this.formGroup) {
                this.formGroup = this.formErrors.formGroup;
            }
        }
    }
    setErrors(backendErrors) {
        this.validate();
        this.backendErrors = backendErrors;
        this.formErrors.setBackendErrors(backendErrors);
    }
    createOrUpdate(api, value, raise = false) {
        this.validate();
        if (this.formGroup.invalid) {
            Object.keys(this.formGroup.controls).map(name => {
                const control = this.formGroup.controls[name];
                if (control.invalid) {
                    control.markAsTouched();
                }
            });
            return rxjs__WEBPACK_IMPORTED_MODULE_4__["EMPTY"];
        }
        let request;
        if (this.object.id) {
            if (value instanceof FormData) {
                throw new Error('Form data not supported on update');
            }
            value.id = this.object.id;
            request = api.update(value.id, value);
        }
        else {
            if (value instanceof FormData) {
                request = api.createWithUpload(value);
            }
            else {
                request = api.create(value);
            }
        }
        return request.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])((error) => {
            if (error.error) {
                this.setErrors(error.error);
                if (raise) {
                    throw error;
                }
                else {
                    return rxjs__WEBPACK_IMPORTED_MODULE_4__["EMPTY"];
                }
            }
            else {
                throw error;
            }
        }));
    }
}
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ViewChild"])('formErrors', { static: false })
], DetailsFormBase.prototype, "formErrors", void 0);


/***/ }),

/***/ "./src/app/shared/ui/objects-view/object-controller.ts":
/*!*************************************************************!*\
  !*** ./src/app/shared/ui/objects-view/object-controller.ts ***!
  \*************************************************************/
/*! exports provided: ObjectController */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ObjectController", function() { return ObjectController; });
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _actions_callback_action__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");


class ObjectController {
    constructor(objectData, objectListUIService, state) {
        this.currentTabIndex = new rxjs__WEBPACK_IMPORTED_MODULE_0__["BehaviorSubject"](0);
        this.currentTabIndex$ = this.currentTabIndex.asObservable();
        this.actionCallback = null;
        this.state = state;
        this.dataSubscription = objectData.subscribe((data) => {
            this.object = data.object;
            this.additionalObjects = data.additionalObjects;
            this.permissions = data.permissions;
            this.objectUIService = objectListUIService.getObjectUIService(this.object, this.permissions, state);
        });
    }
    unsubscribe() {
        if (this.dataSubscription) {
            this.dataSubscription.unsubscribe();
            this.dataSubscription = null;
        }
    }
    setActionCallback(actions) {
        for (const action of actions) {
            if (action instanceof _actions_callback_action__WEBPACK_IMPORTED_MODULE_1__["CallbackAction"] && !action.callback) {
                action.callback = (callbackAction) => {
                    if (this.actionCallback) {
                        return this.actionCallback(callbackAction);
                    }
                    return Object(rxjs__WEBPACK_IMPORTED_MODULE_0__["of"])(null);
                };
            }
        }
        return actions;
    }
    getObjectActions() {
        if (['card-view', 'list-view', 'details'].indexOf(this.state) === -1) {
            return [];
        }
        return this.objectUIService.getActions();
    }
    getSummaryCardData() {
        const detailsLink = this.objectUIService.getDetailsLink();
        return {
            header: {
                title: this.objectUIService.getTitle(),
                icon: this.objectUIService.getIcon(),
                status: this.objectUIService.getStatus(),
                tags: this.objectUIService.getCardTags(),
            },
            detailsLink: {
                enabled: !!detailsLink,
                url: detailsLink,
            },
            fields: this.objectUIService.getCardFields(),
            actions: this.setActionCallback(this.getObjectActions()),
        };
    }
    getDetailsCardData() {
        return {
            header: {
                title: this.objectUIService.getTitle(),
                icon: this.objectUIService.getIcon(),
                status: this.objectUIService.getStatus(),
                tags: this.objectUIService.getCardTags(),
            },
            actions: this.setActionCallback(this.getObjectActions()),
            tabs: this.objectUIService.getTabs(),
            detailsActions: this.setActionCallback(this.objectUIService.getDetailsActions()),
        };
    }
}
ObjectController.ctorParameters = () => [
    { type: rxjs__WEBPACK_IMPORTED_MODULE_0__["Observable"] },
    { type: undefined },
    { type: String }
];


/***/ }),

/***/ "./src/app/shared/ui/objects-view/object-ui-service-base.ts":
/*!******************************************************************!*\
  !*** ./src/app/shared/ui/objects-view/object-ui-service-base.ts ***!
  \******************************************************************/
/*! exports provided: ObjectUIServiceBase */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ObjectUIServiceBase", function() { return ObjectUIServiceBase; });
class ObjectUIServiceBase {
    constructor(object, permissions, state) {
        this.state = state;
        this.setData(object, permissions);
    }
    setData(object, permissions) {
        this.object = object;
        this.permissions = permissions;
    }
    getIcon() {
        console.warn('getIcon must be implemented in derived classes');
        return null;
    }
    getStatus() {
        console.warn('getStatus must be implemented in derived classes');
        return null;
    }
    getTitle() {
        console.warn('getTitle must be implemented in derived classes');
        return null;
    }
    getActions() {
        console.warn('getActions must be implemented in derived classes');
        return [];
    }
    getDetailsLink() {
        console.warn('getDetailsLink must be implemented in derived classes');
        return null;
    }
    getCardFields() {
        console.warn('getCardFields must be implemented in derived classes');
        return [];
    }
    getCardTags() {
        console.warn('getCardTags must be implemented in derived classes');
        return [];
    }
    getTabs() {
        console.warn('getTabs must be implemented in derived classes');
        return [];
    }
    getDetailsActions() {
        console.warn('getDetailsActions must be implemented in derived classes');
        return [];
    }
}
ObjectUIServiceBase.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String }
];


/***/ })

}]);
//# sourceMappingURL=default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09-es2015.js.map