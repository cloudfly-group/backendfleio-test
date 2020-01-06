(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["cloud-cloud-module"],{

/***/ "./src/app/reseller/cloud/cloud-routing.module.ts":
/*!********************************************************!*\
  !*** ./src/app/reseller/cloud/cloud-routing.module.ts ***!
  \********************************************************/
/*! exports provided: CloudRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CloudRoutingModule", function() { return CloudRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");



var routes = [
    {
        path: 'instances',
        loadChildren: function () { return Promise.all(/*! import() | instances-instances-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("default~clients-clients-module~history-history-module~instances-instances-module"), __webpack_require__.e("common"), __webpack_require__.e("instances-instances-module")]).then(__webpack_require__.bind(null, /*! ./instances/instances.module */ "./src/app/reseller/cloud/instances/instances.module.ts")).then(function (mod) { return mod.InstancesModule; }); },
    },
    // {
    //   path: 'flavor-groups',
    //   loadChildren: () => import('./flavor-groups/flavor-groups.module').then(mod => mod.FlavorGroupsModule),
    // },
    {
        path: 'flavors',
        loadChildren: function () { return Promise.all(/*! import() | flavors-flavors-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("flavors-flavors-module")]).then(__webpack_require__.bind(null, /*! ./flavors/flavors.module */ "./src/app/reseller/cloud/flavors/flavors.module.ts")).then(function (mod) { return mod.FlavorsModule; }); },
    },
    {
        path: 'ssh-keys',
        loadChildren: function () { return Promise.all(/*! import() | ssh-keys-ssh-keys-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("ssh-keys-ssh-keys-module")]).then(__webpack_require__.bind(null, /*! ./ssh-keys/ssh-keys.module */ "./src/app/reseller/cloud/ssh-keys/ssh-keys.module.ts")).then(function (mod) { return mod.SshKeysModule; }); },
    },
    {
        path: 'volumes',
        loadChildren: function () { return Promise.all(/*! import() | volumes-volumes-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("volumes-volumes-module")]).then(__webpack_require__.bind(null, /*! ./volumes/volumes.module */ "./src/app/reseller/cloud/volumes/volumes.module.ts")).then(function (mod) { return mod.VolumesModule; }); },
    },
    {
        path: 'images',
        loadChildren: function () { return Promise.all(/*! import() | images-images-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("images-images-module")]).then(__webpack_require__.bind(null, /*! ./images/images.module */ "./src/app/reseller/cloud/images/images.module.ts")).then(function (mod) { return mod.ImagesModule; }); },
    },
    {
        path: 'api-users',
        loadChildren: function () { return Promise.all(/*! import() | api-users-api-users-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("api-users-api-users-module")]).then(__webpack_require__.bind(null, /*! ./api-users/api-users.module */ "./src/app/reseller/cloud/api-users/api-users.module.ts")).then(function (mod) { return mod.ApiUsersModule; }); },
    },
];
var CloudRoutingModule = /** @class */ (function () {
    function CloudRoutingModule() {
    }
    CloudRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
        })
    ], CloudRoutingModule);
    return CloudRoutingModule;
}());



/***/ }),

/***/ "./src/app/reseller/cloud/cloud.module.ts":
/*!************************************************!*\
  !*** ./src/app/reseller/cloud/cloud.module.ts ***!
  \************************************************/
/*! exports provided: CloudModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CloudModule", function() { return CloudModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _cloud_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./cloud-routing.module */ "./src/app/reseller/cloud/cloud-routing.module.ts");




var CloudModule = /** @class */ (function () {
    function CloudModule() {
    }
    CloudModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            declarations: [],
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _cloud_routing_module__WEBPACK_IMPORTED_MODULE_3__["CloudRoutingModule"],
            ]
        })
    ], CloudModule);
    return CloudModule;
}());



/***/ }),

/***/ "./src/app/reseller/settings/cloud/cloud-routing.module.ts":
/*!*****************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/cloud-routing.module.ts ***!
  \*****************************************************************/
/*! exports provided: CloudRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CloudRoutingModule", function() { return CloudRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");



var routes = [
    {
        path: 'openstack-plans',
        loadChildren: function () { return Promise.all(/*! import() | openstack-plans-openstack-plans-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("openstack-plans-openstack-plans-module")]).then(__webpack_require__.bind(null, /*! ./openstack-plans/openstack-plans.module */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plans.module.ts")).then(function (mod) { return mod.OpenstackPlansModule; }); },
    },
    {
        path: 'pricing-rules',
        loadChildren: function () { return Promise.all(/*! import() | pricing-rules-pricing-rules-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("pricing-rules-pricing-rules-module")]).then(__webpack_require__.bind(null, /*! ./pricing-rules/pricing-rules.module */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rules.module.ts")).then(function (mod) { return mod.PricingRulesModule; }); },
    },
];
var CloudRoutingModule = /** @class */ (function () {
    function CloudRoutingModule() {
    }
    CloudRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
        })
    ], CloudRoutingModule);
    return CloudRoutingModule;
}());



/***/ }),

/***/ "./src/app/reseller/settings/cloud/cloud.module.ts":
/*!*********************************************************!*\
  !*** ./src/app/reseller/settings/cloud/cloud.module.ts ***!
  \*********************************************************/
/*! exports provided: CloudModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CloudModule", function() { return CloudModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _cloud_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./cloud-routing.module */ "./src/app/reseller/settings/cloud/cloud-routing.module.ts");




var CloudModule = /** @class */ (function () {
    function CloudModule() {
    }
    CloudModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            declarations: [],
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _cloud_routing_module__WEBPACK_IMPORTED_MODULE_3__["CloudRoutingModule"],
            ]
        })
    ], CloudModule);
    return CloudModule;
}());



/***/ })

}]);
//# sourceMappingURL=cloud-cloud-module-es5.js.map