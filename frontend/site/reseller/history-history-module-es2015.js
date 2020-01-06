(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["history-history-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/history/billing-history/billing-history.component.html":
/*!*******************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/history/billing-history/billing-history.component.html ***!
  \*******************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [detailsData]=\"detailsData\">\n\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/history/tabs/billing-history-overview/billing-history-overview.component.html":
/*!******************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/billing/history/tabs/billing-history-overview/billing-history-overview.component.html ***!
  \******************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxLayout=\"column\" *ngFor=\"let serviceUsage of usage | keyvalue\">\n  <div class=\"full-width\" fxFlex=\"100\">\n    <mat-expansion-panel class=\"full-width\">\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"half-width\">\n          {{serviceUsage.value.income.client_display}} - Service '{{serviceUsage.value.income.service_display}}'\n        </mat-panel-title>\n        <mat-panel-description>\n          {{serviceUsage.value.income.price}}&nbsp;{{serviceUsage.value.income.client_currency.code}}\n          <ng-container *ngIf=\"serviceUsage.value.cost\">\n            ({{serviceUsage.value.cost.price}}&nbsp;{{serviceUsage.value.cost.client_currency.code}})\n          </ng-container>\n        </mat-panel-description>\n      </mat-expansion-panel-header>\n      <app-fleio-service-dynamic-usage [dynamicUsage]=\"serviceUsage.value.income\"\n                                       [dynamicUsageCost]=\"serviceUsage.value.cost\">\n      </app-fleio-service-dynamic-usage>\n    </mat-expansion-panel>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/reseller/billing/history/billing-history/billing-history.component.scss":
/*!*****************************************************************************************!*\
  !*** ./src/app/reseller/billing/history/billing-history/billing-history.component.scss ***!
  \*****************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaGlzdG9yeS9iaWxsaW5nLWhpc3RvcnkvYmlsbGluZy1oaXN0b3J5LmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/billing/history/billing-history/billing-history.component.ts":
/*!***************************************************************************************!*\
  !*** ./src/app/reseller/billing/history/billing-history/billing-history.component.ts ***!
  \***************************************************************************************/
/*! exports provided: BillingHistoryComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BillingHistoryComponent", function() { return BillingHistoryComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _tabs_billing_history_overview_billing_history_overview_component__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../tabs/billing-history-overview/billing-history-overview.component */ "./src/app/reseller/billing/history/tabs/billing-history-overview/billing-history-overview.component.ts");



let BillingHistoryComponent = class BillingHistoryComponent {
    constructor() {
        this.detailsData = {
            header: {
                title: {
                    text: 'Billing history',
                }
            },
            tabs: [{
                    tabName: 'Overview',
                    component: _tabs_billing_history_overview_billing_history_overview_component__WEBPACK_IMPORTED_MODULE_2__["BillingHistoryOverviewComponent"],
                }],
        };
    }
    ngOnInit() {
    }
};
BillingHistoryComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-billing-history',
        template: __webpack_require__(/*! raw-loader!./billing-history.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/history/billing-history/billing-history.component.html"),
        styles: [__webpack_require__(/*! ./billing-history.component.scss */ "./src/app/reseller/billing/history/billing-history/billing-history.component.scss")]
    })
], BillingHistoryComponent);



/***/ }),

/***/ "./src/app/reseller/billing/history/history-routing.module.ts":
/*!********************************************************************!*\
  !*** ./src/app/reseller/billing/history/history-routing.module.ts ***!
  \********************************************************************/
/*! exports provided: HistoryRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HistoryRoutingModule", function() { return HistoryRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _billing_history_billing_history_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./billing-history/billing-history.component */ "./src/app/reseller/billing/history/billing-history/billing-history.component.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");





const routes = [
    {
        path: '',
        component: _billing_history_billing_history_component__WEBPACK_IMPORTED_MODULE_3__["BillingHistoryComponent"],
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__["AuthGuard"]],
        data: {
            config: {
                feature: 'billing.history'
            }
        }
    },
];
let HistoryRoutingModule = class HistoryRoutingModule {
};
HistoryRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], HistoryRoutingModule);



/***/ }),

/***/ "./src/app/reseller/billing/history/history.module.ts":
/*!************************************************************!*\
  !*** ./src/app/reseller/billing/history/history.module.ts ***!
  \************************************************************/
/*! exports provided: HistoryModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HistoryModule", function() { return HistoryModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _billing_history_billing_history_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./billing-history/billing-history.component */ "./src/app/reseller/billing/history/billing-history/billing-history.component.ts");
/* harmony import */ var _history_routing_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./history-routing.module */ "./src/app/reseller/billing/history/history-routing.module.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _tabs_billing_history_overview_billing_history_overview_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./tabs/billing-history-overview/billing-history-overview.component */ "./src/app/reseller/billing/history/tabs/billing-history-overview/billing-history-overview.component.ts");
/* harmony import */ var _angular_material_expansion__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/expansion */ "./node_modules/@angular/material/esm2015/expansion.js");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/table */ "./node_modules/@angular/material/esm2015/table.js");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/divider */ "./node_modules/@angular/material/esm2015/divider.js");
/* harmony import */ var _shared_fleio_data_controls_fleio_data_controls_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/fleio-data-controls/fleio-data-controls.module */ "./src/app/shared/fleio-data-controls/fleio-data-controls.module.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/slide-toggle */ "./node_modules/@angular/material/esm2015/slide-toggle.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");














let HistoryModule = class HistoryModule {
};
HistoryModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _billing_history_billing_history_component__WEBPACK_IMPORTED_MODULE_3__["BillingHistoryComponent"],
            _tabs_billing_history_overview_billing_history_overview_component__WEBPACK_IMPORTED_MODULE_6__["BillingHistoryOverviewComponent"],
        ],
        entryComponents: [
            _tabs_billing_history_overview_billing_history_overview_component__WEBPACK_IMPORTED_MODULE_6__["BillingHistoryOverviewComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _history_routing_module__WEBPACK_IMPORTED_MODULE_4__["HistoryRoutingModule"],
            _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_5__["ObjectsViewModule"],
            _angular_material_expansion__WEBPACK_IMPORTED_MODULE_7__["MatExpansionModule"],
            _angular_material_table__WEBPACK_IMPORTED_MODULE_8__["MatTableModule"],
            _angular_material_divider__WEBPACK_IMPORTED_MODULE_9__["MatDividerModule"],
            _shared_fleio_data_controls_fleio_data_controls_module__WEBPACK_IMPORTED_MODULE_10__["FleioDataControlsModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_11__["FlexLayoutModule"],
            _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_12__["MatSlideToggleModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_13__["ReactiveFormsModule"],
        ]
    })
], HistoryModule);



/***/ }),

/***/ "./src/app/reseller/billing/history/tabs/billing-history-overview/billing-history-overview.component.scss":
/*!****************************************************************************************************************!*\
  !*** ./src/app/reseller/billing/history/tabs/billing-history-overview/billing-history-overview.component.scss ***!
  \****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".total {\n  float: right;\n}\n\n.details-row {\n  height: 0;\n}\n\n.element-detail {\n  overflow: hidden;\n  display: -webkit-box;\n  display: flex;\n}\n\n.price-cell {\n  float: right;\n  width: 25%;\n}\n\n.indent {\n  margin-left: 20px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaGlzdG9yeS90YWJzL2JpbGxpbmctaGlzdG9yeS1vdmVydmlldy9iaWxsaW5nLWhpc3Rvcnktb3ZlcnZpZXcuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3Jlc2VsbGVyL2JpbGxpbmcvaGlzdG9yeS90YWJzL2JpbGxpbmctaGlzdG9yeS1vdmVydmlldy9iaWxsaW5nLWhpc3Rvcnktb3ZlcnZpZXcuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxZQUFBO0FDQ0Y7O0FERUE7RUFDRSxTQUFBO0FDQ0Y7O0FERUE7RUFDRSxnQkFBQTtFQUNBLG9CQUFBO0VBQUEsYUFBQTtBQ0NGOztBREVBO0VBQ0UsWUFBQTtFQUNBLFVBQUE7QUNDRjs7QURFQTtFQUNFLGlCQUFBO0FDQ0YiLCJmaWxlIjoic3JjL2FwcC9yZXNlbGxlci9iaWxsaW5nL2hpc3RvcnkvdGFicy9iaWxsaW5nLWhpc3Rvcnktb3ZlcnZpZXcvYmlsbGluZy1oaXN0b3J5LW92ZXJ2aWV3LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLnRvdGFsIHtcbiAgZmxvYXQ6IHJpZ2h0O1xufVxuXG4uZGV0YWlscy1yb3cge1xuICBoZWlnaHQ6IDA7XG59XG5cbi5lbGVtZW50LWRldGFpbCB7XG4gIG92ZXJmbG93OiBoaWRkZW47XG4gIGRpc3BsYXk6IGZsZXg7XG59XG5cbi5wcmljZS1jZWxsIHtcbiAgZmxvYXQ6IHJpZ2h0O1xuICB3aWR0aDogMjUlO1xufVxuXG4uaW5kZW50IHtcbiAgbWFyZ2luLWxlZnQ6IDIwcHg7XG59XG4iLCIudG90YWwge1xuICBmbG9hdDogcmlnaHQ7XG59XG5cbi5kZXRhaWxzLXJvdyB7XG4gIGhlaWdodDogMDtcbn1cblxuLmVsZW1lbnQtZGV0YWlsIHtcbiAgb3ZlcmZsb3c6IGhpZGRlbjtcbiAgZGlzcGxheTogZmxleDtcbn1cblxuLnByaWNlLWNlbGwge1xuICBmbG9hdDogcmlnaHQ7XG4gIHdpZHRoOiAyNSU7XG59XG5cbi5pbmRlbnQge1xuICBtYXJnaW4tbGVmdDogMjBweDtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/reseller/billing/history/tabs/billing-history-overview/billing-history-overview.component.ts":
/*!**************************************************************************************************************!*\
  !*** ./src/app/reseller/billing/history/tabs/billing-history-overview/billing-history-overview.component.ts ***!
  \**************************************************************************************************************/
/*! exports provided: BillingHistoryOverviewComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BillingHistoryOverviewComponent", function() { return BillingHistoryOverviewComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");
/* harmony import */ var _shared_fleio_api_billing_service_dynamic_usage_service_dynamic_usages_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/fleio-api/billing/service-dynamic-usage/service-dynamic-usages-api.service */ "./src/app/shared/fleio-api/billing/service-dynamic-usage/service-dynamic-usages-api.service.ts");




let BillingHistoryOverviewComponent = class BillingHistoryOverviewComponent extends _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"] {
    constructor(serviceDynamicUsagesApiService) {
        super();
        this.serviceDynamicUsagesApiService = serviceDynamicUsagesApiService;
        this.serviceDynamicUsageList = null;
        this.usage = {};
    }
    ngOnInit() {
        this.serviceDynamicUsagesApiService.list().subscribe((list) => {
            this.serviceDynamicUsageList = list;
            for (const serviceDynamicUsage of list.objects) {
                if (serviceDynamicUsage.service) {
                    if (!this.usage[serviceDynamicUsage.service]) {
                        this.usage[serviceDynamicUsage.service] = {};
                    }
                    this.usage[serviceDynamicUsage.service].income = serviceDynamicUsage;
                }
                else {
                    if (!this.usage[serviceDynamicUsage.reseller_service]) {
                        this.usage[serviceDynamicUsage.reseller_service] = {};
                    }
                    this.usage[serviceDynamicUsage.reseller_service].cost = serviceDynamicUsage;
                }
            }
        });
    }
};
BillingHistoryOverviewComponent.ctorParameters = () => [
    { type: _shared_fleio_api_billing_service_dynamic_usage_service_dynamic_usages_api_service__WEBPACK_IMPORTED_MODULE_3__["ServiceDynamicUsagesApiService"] }
];
BillingHistoryOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-billing-history-overview',
        template: __webpack_require__(/*! raw-loader!./billing-history-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/billing/history/tabs/billing-history-overview/billing-history-overview.component.html"),
        styles: [__webpack_require__(/*! ./billing-history-overview.component.scss */ "./src/app/reseller/billing/history/tabs/billing-history-overview/billing-history-overview.component.scss")]
    })
], BillingHistoryOverviewComponent);



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


/***/ })

}]);
//# sourceMappingURL=history-history-module-es2015.js.map