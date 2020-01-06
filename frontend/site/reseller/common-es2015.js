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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let InvoicesApiService = class InvoicesApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('billing/invoices'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
InvoicesApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
InvoicesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], InvoicesApiService);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let ServiceDynamicUsagesApiService = class ServiceDynamicUsagesApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('openstack/billing/usage'));
        this.httpClient = httpClient;
        this.config = config;
    }
    getForClient(clientId) {
        return this.list({ client_id: clientId, }, 'client');
    }
};
ServiceDynamicUsagesApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
ServiceDynamicUsagesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ServiceDynamicUsagesApiService);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let ServicesApiService = class ServicesApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('billing/services'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
ServicesApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
ServicesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ServicesApiService);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let ImagesApiService = class ImagesApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('openstack/images'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
ImagesApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
ImagesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ImagesApiService);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./pricing-plans-api.service */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts");





let PricingPlanResolver = class PricingPlanResolver {
    constructor(pricingPlansApiService) {
        this.pricingPlansApiService = pricingPlansApiService;
    }
    resolve(route, state) {
        return this.pricingPlansApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
PricingPlanResolver.ctorParameters = () => [
    { type: _pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_4__["PricingPlansApiService"] }
];
PricingPlanResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PricingPlanResolver);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");






let PricingPlansApiService = class PricingPlansApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('openstack/billing/plan'));
        this.httpClient = httpClient;
        this.config = config;
    }
    getAlternativePlans(currentPlanId) {
        return this.list().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(plans => {
            const alternativePlans = [];
            // TODO: do this query in backend
            for (const plan of plans.objects) {
                if (plan.id !== currentPlanId) {
                    alternativePlans.push(plan);
                }
            }
            return alternativePlans;
        }));
    }
};
PricingPlansApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] }
];
PricingPlansApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PricingPlansApiService);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");





let PricingRulesApiService = class PricingRulesApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('openstack/billing/pricerule'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
PricingRulesApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] }
];
PricingRulesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PricingRulesApiService);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let VolumesApiService = class VolumesApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('openstack/volumes'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
VolumesApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
VolumesApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], VolumesApiService);



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
/* harmony import */ var _base_action__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base-action */ "./src/app/shared/ui/objects-view/actions/base-action.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");



var CallType;
(function (CallType) {
    CallType[CallType["Post"] = 0] = "Post";
    CallType[CallType["Delete"] = 1] = "Delete";
})(CallType || (CallType = {}));
class ApiCallAction extends _base_action__WEBPACK_IMPORTED_MODULE_0__["BaseAction"] {
    constructor(init) {
        super(init);
        if (!this.callType) {
            this.callType = CallType.Post;
        }
    }
    executeImpl() {
        switch (this.callType) {
            case CallType.Post:
                return this.apiService.objectPostAction(this.object.id, this.apiAction, this.apiParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["map"])(response => {
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
                return this.apiService.delete(this.object.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["map"])(success => {
                    let message;
                    if (success) {
                        message = this.successMessage || 'Object deleted successfully';
                    }
                    else {
                        message = this.errorMessage || 'Failed to delete object';
                    }
                    return { message };
                }));
            default:
                console.warn('Unsupported call type in action');
                return Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["of"])({ message: 'Unsupported call type' });
        }
    }
}
ApiCallAction.ctorParameters = () => [
    { type: undefined }
];


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
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");




class ListBase {
    constructor(route, objectListUIService, refreshService, listName, refreshInterval = 10000) {
        this.baseRoute = route;
        this.objectListUIService = objectListUIService;
        this.baseRefreshService = refreshService;
        this.listName = listName;
        this.refreshInterval = refreshInterval;
    }
    ngOnInit() {
        this.objectListController = new _object_list_controller__WEBPACK_IMPORTED_MODULE_0__["ObjectListController"](this.baseRoute.data.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["map"])(routeData => {
            if (!routeData[this.listName]) {
                console.error(`Route data has no member named '${this.listName}'`);
            }
            return routeData[this.listName];
        })), this.objectListUIService);
        this.baseRefreshService.startRefreshTimer(this.refreshInterval);
    }
    ngOnDestroy() {
        if (this.objectListController) {
            this.objectListController.unsubscribe();
            this.objectListController = null;
        }
        this.baseRefreshService.stopRefreshTimer();
    }
}
ListBase.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_1__["ActivatedRoute"] },
    { type: undefined },
    { type: _ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_3__["RefreshService"] },
    { type: String },
    { type: Number }
];


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
/* harmony import */ var _object_controller__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./object-controller */ "./src/app/shared/ui/objects-view/object-controller.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");


class ObjectListController {
    constructor(objectsList$, objectListUIService) {
        this.tableDataBS = new rxjs__WEBPACK_IMPORTED_MODULE_1__["BehaviorSubject"](null);
        this.cardViewDataBS = new rxjs__WEBPACK_IMPORTED_MODULE_1__["BehaviorSubject"]([]);
        this.cardViewData$ = this.cardViewDataBS.asObservable();
        this.tableData$ = this.tableDataBS.asObservable();
        this.objectListUIService = objectListUIService;
        this.objectListSubscription = objectsList$.subscribe(objectsList => {
            if (objectsList) {
                this.objectList = objectsList;
                this.permissions = objectsList.permissions;
                this.tableDataBS.next(this.objectListUIService.getTableData(objectsList));
                this.cardViewDataBS.next(this.getCardViewData());
            }
        });
    }
    getCardViewData() {
        const cardViewData = [];
        for (const object of this.objects) {
            cardViewData.push(this.controller(object, 'card-view').getSummaryCardData());
        }
        return cardViewData;
    }
    unsubscribe() {
        this.objectListSubscription.unsubscribe();
    }
    get objects() {
        if (this.objectList) {
            return this.objectList.objects;
        }
        else {
            return [];
        }
    }
    controller(object, state) {
        return new _object_controller__WEBPACK_IMPORTED_MODULE_0__["ObjectController"](Object(rxjs__WEBPACK_IMPORTED_MODULE_1__["of"])({ object, permissions: this.permissions }), this.objectListUIService, state);
    }
    actions() {
        return this.objectListUIService.getActions(this.objectList);
    }
}
ObjectListController.ctorParameters = () => [
    { type: rxjs__WEBPACK_IMPORTED_MODULE_1__["Observable"] },
    { type: undefined }
];


/***/ })

}]);
//# sourceMappingURL=common-es2015.js.map