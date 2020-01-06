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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");



const routes = [
    {
        path: 'instances',
        loadChildren: () => Promise.all(/*! import() | instances-instances-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("default~clients-clients-module~history-history-module~instances-instances-module"), __webpack_require__.e("common"), __webpack_require__.e("instances-instances-module")]).then(__webpack_require__.bind(null, /*! ./instances/instances.module */ "./src/app/reseller/cloud/instances/instances.module.ts")).then(mod => mod.InstancesModule),
    },
    // {
    //   path: 'flavor-groups',
    //   loadChildren: () => import('./flavor-groups/flavor-groups.module').then(mod => mod.FlavorGroupsModule),
    // },
    {
        path: 'flavors',
        loadChildren: () => Promise.all(/*! import() | flavors-flavors-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("flavors-flavors-module")]).then(__webpack_require__.bind(null, /*! ./flavors/flavors.module */ "./src/app/reseller/cloud/flavors/flavors.module.ts")).then(mod => mod.FlavorsModule),
    },
    {
        path: 'ssh-keys',
        loadChildren: () => Promise.all(/*! import() | ssh-keys-ssh-keys-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("ssh-keys-ssh-keys-module")]).then(__webpack_require__.bind(null, /*! ./ssh-keys/ssh-keys.module */ "./src/app/reseller/cloud/ssh-keys/ssh-keys.module.ts")).then(mod => mod.SshKeysModule),
    },
    {
        path: 'volumes',
        loadChildren: () => Promise.all(/*! import() | volumes-volumes-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("volumes-volumes-module")]).then(__webpack_require__.bind(null, /*! ./volumes/volumes.module */ "./src/app/reseller/cloud/volumes/volumes.module.ts")).then(mod => mod.VolumesModule),
    },
    {
        path: 'images',
        loadChildren: () => Promise.all(/*! import() | images-images-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("images-images-module")]).then(__webpack_require__.bind(null, /*! ./images/images.module */ "./src/app/reseller/cloud/images/images.module.ts")).then(mod => mod.ImagesModule),
    },
    {
        path: 'api-users',
        loadChildren: () => Promise.all(/*! import() | api-users-api-users-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("api-users-api-users-module")]).then(__webpack_require__.bind(null, /*! ./api-users/api-users.module */ "./src/app/reseller/cloud/api-users/api-users.module.ts")).then(mod => mod.ApiUsersModule),
    },
];
let CloudRoutingModule = class CloudRoutingModule {
};
CloudRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], CloudRoutingModule);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _cloud_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./cloud-routing.module */ "./src/app/reseller/cloud/cloud-routing.module.ts");




let CloudModule = class CloudModule {
};
CloudModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _cloud_routing_module__WEBPACK_IMPORTED_MODULE_3__["CloudRoutingModule"],
        ]
    })
], CloudModule);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");



const routes = [
    {
        path: 'openstack-plans',
        loadChildren: () => Promise.all(/*! import() | openstack-plans-openstack-plans-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("openstack-plans-openstack-plans-module")]).then(__webpack_require__.bind(null, /*! ./openstack-plans/openstack-plans.module */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plans.module.ts")).then(mod => mod.OpenstackPlansModule),
    },
    {
        path: 'pricing-rules',
        loadChildren: () => Promise.all(/*! import() | pricing-rules-pricing-rules-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~flavo~0ee90f09"), __webpack_require__.e("common"), __webpack_require__.e("pricing-rules-pricing-rules-module")]).then(__webpack_require__.bind(null, /*! ./pricing-rules/pricing-rules.module */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rules.module.ts")).then(mod => mod.PricingRulesModule),
    },
];
let CloudRoutingModule = class CloudRoutingModule {
};
CloudRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], CloudRoutingModule);



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _cloud_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./cloud-routing.module */ "./src/app/reseller/settings/cloud/cloud-routing.module.ts");




let CloudModule = class CloudModule {
};
CloudModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _cloud_routing_module__WEBPACK_IMPORTED_MODULE_3__["CloudRoutingModule"],
        ]
    })
], CloudModule);



/***/ })

}]);
//# sourceMappingURL=cloud-cloud-module-es2015.js.map