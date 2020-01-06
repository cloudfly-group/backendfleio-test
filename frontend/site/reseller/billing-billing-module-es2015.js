(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["billing-billing-module"],{

/***/ "./src/app/reseller/billing/billing-routing.module.ts":
/*!************************************************************!*\
  !*** ./src/app/reseller/billing/billing-routing.module.ts ***!
  \************************************************************/
/*! exports provided: BillingRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BillingRoutingModule", function() { return BillingRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");



const routes = [
    {
        path: 'invoices',
        loadChildren: () => Promise.all(/*! import() | invoices-invoices-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("invoices-invoices-module")]).then(__webpack_require__.bind(null, /*! ./invoices/invoices.module */ "./src/app/reseller/billing/invoices/invoices.module.ts")).then(mod => mod.InvoicesModule),
    },
    {
        path: 'services',
        loadChildren: () => Promise.all(/*! import() | services-services-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("services-services-module")]).then(__webpack_require__.bind(null, /*! ./services/services.module */ "./src/app/reseller/billing/services/services.module.ts")).then(mod => mod.ServicesModule),
    },
    // {
    //   path: 'orders',
    //   loadChildren: () => import('./orders/orders.module').then(mod => mod.OrdersModule),
    // },
    // {
    //   path: 'products',
    //   loadChildren: () => import('./products/products.module').then(mod => mod.ProductsModule),
    // },
    // {
    //   path: 'config-options',
    //   loadChildren: () => import('./config-options/config-options.module').then(mod => mod.ConfigOptionsModule),
    // },
    {
        path: 'history',
        loadChildren: () => Promise.all(/*! import() | history-history-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~clients-clients-module~history-history-module~instances-instances-module"), __webpack_require__.e("common"), __webpack_require__.e("history-history-module")]).then(__webpack_require__.bind(null, /*! ./history/history.module */ "./src/app/reseller/billing/history/history.module.ts")).then(mod => mod.HistoryModule),
    },
];
let BillingRoutingModule = class BillingRoutingModule {
};
BillingRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], BillingRoutingModule);



/***/ }),

/***/ "./src/app/reseller/billing/billing.module.ts":
/*!****************************************************!*\
  !*** ./src/app/reseller/billing/billing.module.ts ***!
  \****************************************************/
/*! exports provided: BillingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BillingModule", function() { return BillingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _billing_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./billing-routing.module */ "./src/app/reseller/billing/billing-routing.module.ts");




let BillingModule = class BillingModule {
};
BillingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _billing_routing_module__WEBPACK_IMPORTED_MODULE_3__["BillingRoutingModule"],
        ]
    })
], BillingModule);



/***/ })

}]);
//# sourceMappingURL=billing-billing-module-es2015.js.map