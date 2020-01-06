(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["clients-users-clients-users-module"],{

/***/ "./src/app/reseller/clients-users/clients-users-routing.module.ts":
/*!************************************************************************!*\
  !*** ./src/app/reseller/clients-users/clients-users-routing.module.ts ***!
  \************************************************************************/
/*! exports provided: ClientsUsersRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ClientsUsersRoutingModule", function() { return ClientsUsersRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");



const routes = [
    {
        path: 'clients',
        loadChildren: () => Promise.all(/*! import() | clients-clients-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("default~clients-clients-module~history-history-module~instances-instances-module"), __webpack_require__.e("common"), __webpack_require__.e("clients-clients-module")]).then(__webpack_require__.bind(null, /*! ./clients/clients.module */ "./src/app/reseller/clients-users/clients/clients.module.ts")).then(mod => mod.ClientsModule),
    },
    // {
    //   path: 'client-groups',
    //   loadChildren: () => import('./client-groups/client-groups.module').then(mod => mod.ClientGroupsModule),
    // },
    {
        path: 'users',
        loadChildren: () => Promise.all(/*! import() | users-users-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("users-users-module")]).then(__webpack_require__.bind(null, /*! ./users/users.module */ "./src/app/reseller/clients-users/users/users.module.ts")).then(mod => mod.UsersModule),
    },
];
let ClientsUsersRoutingModule = class ClientsUsersRoutingModule {
};
ClientsUsersRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], ClientsUsersRoutingModule);



/***/ }),

/***/ "./src/app/reseller/clients-users/clients-users.module.ts":
/*!****************************************************************!*\
  !*** ./src/app/reseller/clients-users/clients-users.module.ts ***!
  \****************************************************************/
/*! exports provided: ClientsUsersModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ClientsUsersModule", function() { return ClientsUsersModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _clients_users_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./clients-users-routing.module */ "./src/app/reseller/clients-users/clients-users-routing.module.ts");




let ClientsUsersModule = class ClientsUsersModule {
};
ClientsUsersModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _clients_users_routing_module__WEBPACK_IMPORTED_MODULE_3__["ClientsUsersRoutingModule"]
        ]
    })
], ClientsUsersModule);



/***/ })

}]);
//# sourceMappingURL=clients-users-clients-users-module-es2015.js.map