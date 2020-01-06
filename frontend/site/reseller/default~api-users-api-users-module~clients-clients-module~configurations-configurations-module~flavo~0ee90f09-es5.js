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
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");


var BaseAction = /** @class */ (function () {
    function BaseAction(init) {
        this.refreshAfterExecute = true;
        this.redirectAfterExecute = false;
        Object.assign(this, init);
        if (this.noPermissions && !this.tooltip) {
            this.tooltip = 'You don\'t have permissions to perform this action';
        }
    }
    BaseAction.prototype.executeImpl = function () {
        console.warn('Base object action executeImpl method invoked, ' +
            'override this in your derived classes.');
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_0__["of"])({ message: 'Base object action execute method invoked.' }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_1__["delay"])(1000));
    };
    BaseAction.prototype.getActiveOptions = function (executionOptions) {
        var activeOptions = {
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
    };
    BaseAction.prototype.execute = function (notificationService, refreshService, options) {
        var _this = this;
        this.isRunning = true;
        this.notificationService = notificationService;
        var activeOptions = this.getActiveOptions(options);
        var dialogResult$ = Object(rxjs__WEBPACK_IMPORTED_MODULE_0__["of"])('yes');
        if (this.confirmOptions && this.confirmOptions.confirm && activeOptions.displayConfirmation) {
            dialogResult$ = notificationService.confirmDialog({
                title: this.confirmOptions.title,
                message: this.confirmOptions.message,
            });
        }
        dialogResult$.subscribe(function (dialogResult) {
            if (dialogResult === 'yes') {
                _this.executeImpl().subscribe(function (result) {
                    _this.isRunning = false;
                    if (activeOptions.displayMessages && result) {
                        notificationService.showMessage(result.message);
                    }
                    if (_this.refreshAfterExecute) {
                        refreshService.refresh();
                    }
                    if (_this.redirectAfterExecute) {
                        refreshService.redirect(_this.redirectUrl);
                    }
                });
            }
            else {
                _this.isRunning = false;
            }
        });
    };
    BaseAction.ctorParameters = function () { return [
        { type: undefined }
    ]; };
    return BaseAction;
}());



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
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _base_action__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base-action */ "./src/app/shared/ui/objects-view/actions/base-action.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");



var CallbackAction = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](CallbackAction, _super);
    function CallbackAction(init) {
        var _this = _super.call(this, init) || this;
        if (!_this.options) {
            _this.options = { displayConfirmation: false, displayMessages: false };
        }
        _this.refreshAfterExecute = init ? !!init.refreshAfterExecute : false;
        return _this;
    }
    CallbackAction.prototype.executeImpl = function () {
        if (this.callback) {
            return this.callback(this);
        }
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null);
    };
    CallbackAction.ctorParameters = function () { return [
        { type: undefined }
    ]; };
    return CallbackAction;
}(_base_action__WEBPACK_IMPORTED_MODULE_1__["BaseAction"]));



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
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _base_action__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base-action */ "./src/app/shared/ui/objects-view/actions/base-action.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");




var RouterLinkAction = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](RouterLinkAction, _super);
    function RouterLinkAction(init) {
        var _this = _super.call(this, init) || this;
        if (!_this.options) {
            _this.options = { displayConfirmation: false, displayMessages: false };
        }
        _this.refreshAfterExecute = false;
        return _this;
    }
    RouterLinkAction.prototype.executeImpl = function () {
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["from"])(this.router.navigateByUrl(this.routerUrl)).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(function (result) {
            return { message: 'Navigated successfully' };
        }));
    };
    RouterLinkAction.ctorParameters = function () { return [
        { type: undefined }
    ]; };
    return RouterLinkAction;
}(_base_action__WEBPACK_IMPORTED_MODULE_1__["BaseAction"]));



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
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _object_controller__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./object-controller */ "./src/app/shared/ui/objects-view/object-controller.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");




var DetailsBase = /** @class */ (function () {
    function DetailsBase(route, objectListUIService, state, objectName, additionalObjectNames) {
        if (additionalObjectNames === void 0) { additionalObjectNames = null; }
        this.route = route;
        this.objectListUIService = objectListUIService;
        this.state = state;
        this.objectName = objectName;
        this.additionalObjectNames = additionalObjectNames;
    }
    Object.defineProperty(DetailsBase.prototype, "object", {
        get: function () {
            return this.objectController.object;
        },
        enumerable: true,
        configurable: true
    });
    DetailsBase.prototype.ngOnInit = function () {
        var _this = this;
        this.objectController = new _object_controller__WEBPACK_IMPORTED_MODULE_1__["ObjectController"](this.route.data.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["map"])(function (data) {
            var e_1, _a;
            var object;
            var additionalObjects;
            if (_this.objectName) {
                object = data[_this.objectName];
                if (!object) {
                    console.error("No object named " + _this.objectName + " found in router data");
                }
                if (_this.additionalObjectNames) {
                    additionalObjects = {};
                    try {
                        for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](_this.additionalObjectNames), _c = _b.next(); !_c.done; _c = _b.next()) {
                            var additionalObjectName = _c.value;
                            var additionalObject = data[additionalObjectName];
                            if (!additionalObject) {
                                console.error("No additional object named " + additionalObjectName + " found in router data");
                                console.error(data);
                            }
                            else {
                                additionalObjects[additionalObjectName] = data[additionalObjectName];
                            }
                        }
                    }
                    catch (e_1_1) { e_1 = { error: e_1_1 }; }
                    finally {
                        try {
                            if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                        }
                        finally { if (e_1) throw e_1.error; }
                    }
                }
            }
            else {
                object = {};
            }
            return {
                object: object,
                additionalObjects: additionalObjects,
                permissions: data.permissions,
            };
        })), this.objectListUIService, this.state);
    };
    DetailsBase.prototype.ngOnDestroy = function () {
        if (this.objectController) {
            this.objectController.unsubscribe();
            this.objectController = null;
        }
    };
    DetailsBase.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: undefined },
        { type: String },
        { type: String },
        { type: undefined }
    ]; };
    return DetailsBase;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _ui_api_helpers_refresh_timer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../ui-api/helpers/refresh-timer */ "./src/app/shared/ui-api/helpers/refresh-timer.ts");



var DetailsComponentBase = /** @class */ (function () {
    function DetailsComponentBase() {
        this.tabActive = false;
    }
    DetailsComponentBase.prototype.ngOnDestroy = function () {
        if (this.refreshTimer) {
            this.refreshTimer.stop();
            delete this.refreshTimer;
        }
    };
    Object.defineProperty(DetailsComponentBase.prototype, "object", {
        get: function () {
            return this.objectController.object;
        },
        enumerable: true,
        configurable: true
    });
    DetailsComponentBase.prototype.initTabEvents = function () {
        var _this = this;
        this.objectController.currentTabIndex$.subscribe(function (tabIndex) {
            if (tabIndex === _this.componentTabIndex) {
                if (!_this.tabActive) {
                    _this.tabActive = true;
                    _this.tabActivated();
                }
            }
            else {
                if (_this.tabActive) {
                    _this.tabActive = false;
                    _this.tabDeactivated();
                }
            }
        });
    };
    DetailsComponentBase.prototype.setupRefreshTimer = function (interval) {
        var _this = this;
        this.initTabEvents();
        this.refreshTimer = new _ui_api_helpers_refresh_timer__WEBPACK_IMPORTED_MODULE_2__["RefreshTimer"](interval, function () {
            _this.refreshData();
        }, false);
    };
    DetailsComponentBase.prototype.boostRefreshTimer = function (boostIntervals) {
        if (boostIntervals === void 0) { boostIntervals = _ui_api_helpers_refresh_timer__WEBPACK_IMPORTED_MODULE_2__["DEFAULT_BOOST_INTERVALS"]; }
        if (!this.refreshTimer) {
            console.error('refresh timer is not initialized');
            return;
        }
        this.refreshTimer.boost(boostIntervals);
    };
    DetailsComponentBase.prototype.tabActivated = function () {
        if (this.refreshTimer) {
            this.refreshData();
            this.refreshTimer.start();
        }
    };
    DetailsComponentBase.prototype.tabDeactivated = function () {
        if (this.refreshTimer) {
            this.refreshTimer.stop();
        }
    };
    DetailsComponentBase.prototype.refreshData = function () {
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
    ], DetailsComponentBase.prototype, "objectController", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
    ], DetailsComponentBase.prototype, "componentTabIndex", void 0);
    return DetailsComponentBase;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");





var DetailsFormBase = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](DetailsFormBase, _super);
    function DetailsFormBase() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.backendErrors = {};
        return _this;
    }
    DetailsFormBase.prototype.validate = function () {
        if (!this.formErrors) {
            console.error('You should declare form errors in your form');
        }
        else {
            if (!this.formGroup) {
                this.formGroup = this.formErrors.formGroup;
            }
        }
    };
    DetailsFormBase.prototype.setErrors = function (backendErrors) {
        this.validate();
        this.backendErrors = backendErrors;
        this.formErrors.setBackendErrors(backendErrors);
    };
    DetailsFormBase.prototype.createOrUpdate = function (api, value, raise) {
        var _this = this;
        if (raise === void 0) { raise = false; }
        this.validate();
        if (this.formGroup.invalid) {
            Object.keys(this.formGroup.controls).map(function (name) {
                var control = _this.formGroup.controls[name];
                if (control.invalid) {
                    control.markAsTouched();
                }
            });
            return rxjs__WEBPACK_IMPORTED_MODULE_4__["EMPTY"];
        }
        var request;
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
        return request.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function (error) {
            if (error.error) {
                _this.setErrors(error.error);
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
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["ViewChild"])('formErrors', { static: false })
    ], DetailsFormBase.prototype, "formErrors", void 0);
    return DetailsFormBase;
}(_details_component_base__WEBPACK_IMPORTED_MODULE_1__["DetailsComponentBase"]));



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
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _actions_callback_action__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");



var ObjectController = /** @class */ (function () {
    function ObjectController(objectData, objectListUIService, state) {
        var _this = this;
        this.currentTabIndex = new rxjs__WEBPACK_IMPORTED_MODULE_1__["BehaviorSubject"](0);
        this.currentTabIndex$ = this.currentTabIndex.asObservable();
        this.actionCallback = null;
        this.state = state;
        this.dataSubscription = objectData.subscribe(function (data) {
            _this.object = data.object;
            _this.additionalObjects = data.additionalObjects;
            _this.permissions = data.permissions;
            _this.objectUIService = objectListUIService.getObjectUIService(_this.object, _this.permissions, state);
        });
    }
    ObjectController.prototype.unsubscribe = function () {
        if (this.dataSubscription) {
            this.dataSubscription.unsubscribe();
            this.dataSubscription = null;
        }
    };
    ObjectController.prototype.setActionCallback = function (actions) {
        var _this = this;
        var e_1, _a;
        try {
            for (var actions_1 = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](actions), actions_1_1 = actions_1.next(); !actions_1_1.done; actions_1_1 = actions_1.next()) {
                var action = actions_1_1.value;
                if (action instanceof _actions_callback_action__WEBPACK_IMPORTED_MODULE_2__["CallbackAction"] && !action.callback) {
                    action.callback = function (callbackAction) {
                        if (_this.actionCallback) {
                            return _this.actionCallback(callbackAction);
                        }
                        return Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["of"])(null);
                    };
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (actions_1_1 && !actions_1_1.done && (_a = actions_1.return)) _a.call(actions_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return actions;
    };
    ObjectController.prototype.getObjectActions = function () {
        if (['card-view', 'list-view', 'details'].indexOf(this.state) === -1) {
            return [];
        }
        return this.objectUIService.getActions();
    };
    ObjectController.prototype.getSummaryCardData = function () {
        var detailsLink = this.objectUIService.getDetailsLink();
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
    };
    ObjectController.prototype.getDetailsCardData = function () {
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
    };
    ObjectController.ctorParameters = function () { return [
        { type: rxjs__WEBPACK_IMPORTED_MODULE_1__["Observable"] },
        { type: undefined },
        { type: String }
    ]; };
    return ObjectController;
}());



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
var ObjectUIServiceBase = /** @class */ (function () {
    function ObjectUIServiceBase(object, permissions, state) {
        this.state = state;
        this.setData(object, permissions);
    }
    ObjectUIServiceBase.prototype.setData = function (object, permissions) {
        this.object = object;
        this.permissions = permissions;
    };
    ObjectUIServiceBase.prototype.getIcon = function () {
        console.warn('getIcon must be implemented in derived classes');
        return null;
    };
    ObjectUIServiceBase.prototype.getStatus = function () {
        console.warn('getStatus must be implemented in derived classes');
        return null;
    };
    ObjectUIServiceBase.prototype.getTitle = function () {
        console.warn('getTitle must be implemented in derived classes');
        return null;
    };
    ObjectUIServiceBase.prototype.getActions = function () {
        console.warn('getActions must be implemented in derived classes');
        return [];
    };
    ObjectUIServiceBase.prototype.getDetailsLink = function () {
        console.warn('getDetailsLink must be implemented in derived classes');
        return null;
    };
    ObjectUIServiceBase.prototype.getCardFields = function () {
        console.warn('getCardFields must be implemented in derived classes');
        return [];
    };
    ObjectUIServiceBase.prototype.getCardTags = function () {
        console.warn('getCardTags must be implemented in derived classes');
        return [];
    };
    ObjectUIServiceBase.prototype.getTabs = function () {
        console.warn('getTabs must be implemented in derived classes');
        return [];
    };
    ObjectUIServiceBase.prototype.getDetailsActions = function () {
        console.warn('getDetailsActions must be implemented in derived classes');
        return [];
    };
    ObjectUIServiceBase.ctorParameters = function () { return [
        { type: undefined },
        { type: undefined },
        { type: String }
    ]; };
    return ObjectUIServiceBase;
}());



/***/ })

}]);
//# sourceMappingURL=default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09-es5.js.map