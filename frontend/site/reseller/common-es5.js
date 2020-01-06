(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["common"],{

/***/ "./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts":
/*!***************************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/invoices/invoices-api.service.ts ***!
  \***************************************************************************/
/*! exports provided: InvoicesApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "InvoicesApiService", function() { return InvoicesApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var InvoicesApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](InvoicesApiService, _super);
    // noinspection JSUnusedGlobalSymbols
    function InvoicesApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('billing/invoices')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    InvoicesApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    InvoicesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], InvoicesApiService);
    return InvoicesApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ }),

/***/ "./src/app/shared/fleio-api/billing/service-dynamic-usage/service-dynamic-usages-api.service.ts":
/*!******************************************************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/service-dynamic-usage/service-dynamic-usages-api.service.ts ***!
  \******************************************************************************************************/
/*! exports provided: ServiceDynamicUsagesApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServiceDynamicUsagesApiService", function() { return ServiceDynamicUsagesApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var ServiceDynamicUsagesApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ServiceDynamicUsagesApiService, _super);
    // noinspection JSUnusedGlobalSymbols
    function ServiceDynamicUsagesApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('openstack/billing/usage')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    ServiceDynamicUsagesApiService.prototype.getForClient = function (clientId) {
        return this.list({ client_id: clientId, }, 'client');
    };
    ServiceDynamicUsagesApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    ServiceDynamicUsagesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ServiceDynamicUsagesApiService);
    return ServiceDynamicUsagesApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ }),

/***/ "./src/app/shared/fleio-api/billing/services/service-api.service.ts":
/*!**************************************************************************!*\
  !*** ./src/app/shared/fleio-api/billing/services/service-api.service.ts ***!
  \**************************************************************************/
/*! exports provided: ServicesApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ServicesApiService", function() { return ServicesApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var ServicesApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ServicesApiService, _super);
    // noinspection JSUnusedGlobalSymbols
    function ServicesApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('billing/services')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    ServicesApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    ServicesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ServicesApiService);
    return ServicesApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts":
/*!*******************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/image/image-api.service.ts ***!
  \*******************************************************************/
/*! exports provided: ImagesApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImagesApiService", function() { return ImagesApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var ImagesApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImagesApiService, _super);
    // noinspection JSUnusedGlobalSymbols
    function ImagesApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('openstack/images')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    ImagesApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    ImagesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ImagesApiService);
    return ImagesApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plan.resolver.ts":
/*!******************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plan.resolver.ts ***!
  \******************************************************************************/
/*! exports provided: PricingPlanResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingPlanResolver", function() { return PricingPlanResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./pricing-plans-api.service */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts");





var PricingPlanResolver = /** @class */ (function () {
    function PricingPlanResolver(pricingPlansApiService) {
        this.pricingPlansApiService = pricingPlansApiService;
    }
    PricingPlanResolver.prototype.resolve = function (route, state) {
        return this.pricingPlansApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    PricingPlanResolver.ctorParameters = function () { return [
        { type: _pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_4__["PricingPlansApiService"] }
    ]; };
    PricingPlanResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], PricingPlanResolver);
    return PricingPlanResolver;
}());



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts":
/*!**********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts ***!
  \**********************************************************************************/
/*! exports provided: PricingPlansApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingPlansApiService", function() { return PricingPlansApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");






var PricingPlansApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](PricingPlansApiService, _super);
    // noinspection JSUnusedGlobalSymbols
    function PricingPlansApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('openstack/billing/plan')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    PricingPlansApiService.prototype.getAlternativePlans = function (currentPlanId) {
        return this.list().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(function (plans) {
            var e_1, _a;
            var alternativePlans = [];
            try {
                // TODO: do this query in backend
                for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](plans.objects), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var plan = _c.value;
                    if (plan.id !== currentPlanId) {
                        alternativePlans.push(plan);
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
            return alternativePlans;
        }));
    };
    PricingPlansApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] }
    ]; };
    PricingPlansApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], PricingPlansApiService);
    return PricingPlansApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service.ts":
/*!**********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service.ts ***!
  \**********************************************************************************/
/*! exports provided: PricingRulesApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRulesApiService", function() { return PricingRulesApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");





var PricingRulesApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](PricingRulesApiService, _super);
    // noinspection JSUnusedGlobalSymbols
    function PricingRulesApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('openstack/billing/pricerule')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    PricingRulesApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] }
    ]; };
    PricingRulesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], PricingRulesApiService);
    return PricingRulesApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts":
/*!**********************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts ***!
  \**********************************************************************/
/*! exports provided: VolumesApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumesApiService", function() { return VolumesApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var VolumesApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](VolumesApiService, _super);
    // noinspection JSUnusedGlobalSymbols
    function VolumesApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('openstack/volumes')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    VolumesApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    VolumesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], VolumesApiService);
    return VolumesApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ }),

/***/ "./src/app/shared/ui/objects-view/actions/api-call-action.ts":
/*!*******************************************************************!*\
  !*** ./src/app/shared/ui/objects-view/actions/api-call-action.ts ***!
  \*******************************************************************/
/*! exports provided: CallType, ApiCallAction */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CallType", function() { return CallType; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ApiCallAction", function() { return ApiCallAction; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _base_action__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./base-action */ "./src/app/shared/ui/objects-view/actions/base-action.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");




var CallType;
(function (CallType) {
    CallType[CallType["Post"] = 0] = "Post";
    CallType[CallType["Delete"] = 1] = "Delete";
})(CallType || (CallType = {}));
var ApiCallAction = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ApiCallAction, _super);
    function ApiCallAction(init) {
        var _this = _super.call(this, init) || this;
        if (!_this.callType) {
            _this.callType = CallType.Post;
        }
        return _this;
    }
    ApiCallAction.prototype.executeImpl = function () {
        var _this = this;
        switch (this.callType) {
            case CallType.Post:
                return this.apiService.objectPostAction(this.object.id, this.apiAction, this.apiParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(function (response) {
                    if (response.detail) {
                        return { message: response.detail };
                    }
                    else {
                        console.warn('Unable to extract message from backend response');
                        console.warn(response);
                        return null;
                    }
                }));
            case CallType.Delete:
                return this.apiService.delete(this.object.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(function (success) {
                    var message;
                    if (success) {
                        message = _this.successMessage || 'Object deleted successfully';
                    }
                    else {
                        message = _this.errorMessage || 'Failed to delete object';
                    }
                    return { message: message };
                }));
            default:
                console.warn('Unsupported call type in action');
                return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])({ message: 'Unsupported call type' });
        }
    };
    ApiCallAction.ctorParameters = function () { return [
        { type: undefined }
    ]; };
    return ApiCallAction;
}(_base_action__WEBPACK_IMPORTED_MODULE_1__["BaseAction"]));



/***/ }),

/***/ "./src/app/shared/ui/objects-view/list-base.ts":
/*!*****************************************************!*\
  !*** ./src/app/shared/ui/objects-view/list-base.ts ***!
  \*****************************************************/
/*! exports provided: ListBase */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ListBase", function() { return ListBase; });
/* harmony import */ var _object_list_controller__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./object-list-controller */ "./src/app/shared/ui/objects-view/object-list-controller.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");




var ListBase = /** @class */ (function () {
    function ListBase(route, objectListUIService, refreshService, listName, refreshInterval) {
        if (refreshInterval === void 0) { refreshInterval = 10000; }
        this.baseRoute = route;
        this.objectListUIService = objectListUIService;
        this.baseRefreshService = refreshService;
        this.listName = listName;
        this.refreshInterval = refreshInterval;
    }
    ListBase.prototype.ngOnInit = function () {
        var _this = this;
        this.objectListController = new _object_list_controller__WEBPACK_IMPORTED_MODULE_0__["ObjectListController"](this.baseRoute.data.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["map"])(function (routeData) {
            if (!routeData[_this.listName]) {
                console.error("Route data has no member named '" + _this.listName + "'");
            }
            return routeData[_this.listName];
        })), this.objectListUIService);
        this.baseRefreshService.startRefreshTimer(this.refreshInterval);
    };
    ListBase.prototype.ngOnDestroy = function () {
        if (this.objectListController) {
            this.objectListController.unsubscribe();
            this.objectListController = null;
        }
        this.baseRefreshService.stopRefreshTimer();
    };
    ListBase.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_1__["ActivatedRoute"] },
        { type: undefined },
        { type: _ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_3__["RefreshService"] },
        { type: String },
        { type: Number }
    ]; };
    return ListBase;
}());



/***/ }),

/***/ "./src/app/shared/ui/objects-view/object-list-controller.ts":
/*!******************************************************************!*\
  !*** ./src/app/shared/ui/objects-view/object-list-controller.ts ***!
  \******************************************************************/
/*! exports provided: ObjectListController */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ObjectListController", function() { return ObjectListController; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _object_controller__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./object-controller */ "./src/app/shared/ui/objects-view/object-controller.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");



var ObjectListController = /** @class */ (function () {
    function ObjectListController(objectsList$, objectListUIService) {
        var _this = this;
        this.tableDataBS = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"](null);
        this.cardViewDataBS = new rxjs__WEBPACK_IMPORTED_MODULE_2__["BehaviorSubject"]([]);
        this.cardViewData$ = this.cardViewDataBS.asObservable();
        this.tableData$ = this.tableDataBS.asObservable();
        this.objectListUIService = objectListUIService;
        this.objectListSubscription = objectsList$.subscribe(function (objectsList) {
            if (objectsList) {
                _this.objectList = objectsList;
                _this.permissions = objectsList.permissions;
                _this.tableDataBS.next(_this.objectListUIService.getTableData(objectsList));
                _this.cardViewDataBS.next(_this.getCardViewData());
            }
        });
    }
    ObjectListController.prototype.getCardViewData = function () {
        var e_1, _a;
        var cardViewData = [];
        try {
            for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](this.objects), _c = _b.next(); !_c.done; _c = _b.next()) {
                var object = _c.value;
                cardViewData.push(this.controller(object, 'card-view').getSummaryCardData());
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return cardViewData;
    };
    ObjectListController.prototype.unsubscribe = function () {
        this.objectListSubscription.unsubscribe();
    };
    Object.defineProperty(ObjectListController.prototype, "objects", {
        get: function () {
            if (this.objectList) {
                return this.objectList.objects;
            }
            else {
                return [];
            }
        },
        enumerable: true,
        configurable: true
    });
    ObjectListController.prototype.controller = function (object, state) {
        return new _object_controller__WEBPACK_IMPORTED_MODULE_1__["ObjectController"](Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])({ object: object, permissions: this.permissions }), this.objectListUIService, state);
    };
    ObjectListController.prototype.actions = function () {
        return this.objectListUIService.getActions(this.objectList);
    };
    ObjectListController.ctorParameters = function () { return [
        { type: rxjs__WEBPACK_IMPORTED_MODULE_2__["Observable"] },
        { type: undefined }
    ]; };
    return ObjectListController;
}());



/***/ })

}]);
//# sourceMappingURL=common-es5.js.map