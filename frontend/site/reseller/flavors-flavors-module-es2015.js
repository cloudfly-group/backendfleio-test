(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["flavors-flavors-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/flavor-create/flavor-create.component.html":
/*!*************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/flavors/flavor-create/flavor-create.component.html ***!
  \*************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-lg']\"></app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/flavor-details/flavor-details.component.html":
/*!***************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/flavors/flavor-details/flavor-details.component.html ***!
  \***************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\"></app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/flavor-edit/flavor-edit.component.html":
/*!*********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/flavors/flavor-edit/flavor-edit.component.html ***!
  \*********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-lg']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/flavor-list/flavor-list.component.html":
/*!*********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/flavors/flavor-list/flavor-list.component.html ***!
  \*********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-objects-view [objectsListController]=\"objectListController\"></app-objects-view>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/tabs/flavor-details-overview/flavor-details-overview.component.html":
/*!**************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/flavors/tabs/flavor-details-overview/flavor-details-overview.component.html ***!
  \**************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxFlex=\"column\">\n  <p class=\"fl-detail\">ID: {{object.id}}</p>\n  <p class=\"fl-detail\">Name: {{object.name}}</p>\n  <p class=\"fl-detail\">Ram: {{object.memory_mb}} MB</p>\n  <p class=\"fl-detail\">Virtual CPUs: {{object.vcpus}} MB</p>\n  <p class=\"fl-detail\">Disk space: {{object.root_gb}} GB</p>\n  <p class=\"fl-detail\">Swap: {{object.swap}} GB</p>\n  <p class=\"fl-detail\">Ephemeral storage: {{object.ephemeral_gb}} GB</p>\n  <p class=\"fl-detail\">Disabled: {{object.disabled}}</p>\n  <p class=\"fl-detail\">Public: {{object.is_public}}</p>\n  <p class=\"fl-detail\">Region: {{object.region}}</p>\n  <p class=\"fl-detail\">Description: {{object.description}}</p>\n  <p class=\"fl-detail\">Group: {{object.flavor_group || 'n/a'}}</p>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/tabs/flavor-edit-form/flavor-edit-form.component.html":
/*!************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/flavors/tabs/flavor-edit-form/flavor-edit-form.component.html ***!
  \************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form [formGroup]=\"flavorForm\">\n  <app-form-errors #formErrors [formGroup]=\"flavorForm\"></app-form-errors>\n  <div fxLayout=\"column\">\n     <mat-checkbox *ngIf=\"object.id\" formControlName=\"preserve_id\" color=\"primary\">\n      Preserve existing flavor ID (not recommended for major changes)\n    </mat-checkbox>\n    <div fxLayout=\"row\" fxLayoutGap=\"10px\">\n      <mat-form-field fxFlex=\"auto\">\n        <input matInput placeholder=\"Flavor name\" type=\"text\" formControlName=\"name\" required>\n        <mat-error>{{backendErrors['name'] || 'Field is required' }}</mat-error>\n      </mat-form-field>\n      <mat-form-field fxFlex=\"auto\">\n        <mat-select formControlName=\"region\" placeholder=\"Region\" required>\n          <mat-option *ngFor=\"let region of createOptions.regions\"\n                      [value]=\"region.id\">\n            {{region.id}}\n          </mat-option>\n        </mat-select>\n      </mat-form-field>\n    </div>\n    <div fxLayout=\"row\" fxLayoutGap=\"10px\">\n      <mat-form-field fxFlex=\"auto\">\n        <input matInput placeholder=\"Ram in MB\" type=\"number\"\n               formControlName=\"memory_mb\" required>\n        <mat-error>{{backendErrors['memory_mb'] || 'This field is required!' }}</mat-error>\n      </mat-form-field>\n      <mat-form-field fxFlex=\"auto\">\n        <input matInput placeholder=\"Virtual CPUs\" type=\"number\"\n               formControlName=\"vcpus\" required>\n        <mat-error>{{backendErrors['vcpus'] || 'This field is required!' }}</mat-error>\n      </mat-form-field>\n      <mat-form-field fxFlex=\"auto\">\n        <input matInput placeholder=\"Disk size (GB)\" type=\"number\"\n               formControlName=\"root_gb\" required>\n        <mat-error>{{backendErrors['root_gb'] || 'This field is required!' }}</mat-error>\n      </mat-form-field>\n      <mat-form-field fxFlex=\"auto\">\n        <input matInput placeholder=\"Swap space (MB)\" type=\"number\"\n               formControlName=\"swap\" required>\n        <mat-error>{{backendErrors['swap'] || 'This field is required!' }}</mat-error>\n      </mat-form-field>\n      <mat-form-field fxFlex=\"auto\">\n        <input matInput placeholder=\"Ephemeral disk space (GB)\" type=\"number\"\n               formControlName=\"ephemeral_gb\" required>\n        <mat-error>{{backendErrors['ephemeral_gb'] || 'This field is required!' }}</mat-error>\n      </mat-form-field>\n    </div>\n    <div fxLayout=\"row\">\n      <mat-form-field fxFlex=\"auto\">\n        <mat-label>Description</mat-label>\n        <textarea matInput formControlName=\"description\" rows=\"10\"></textarea>\n      </mat-form-field>\n    </div>\n    <mat-checkbox formControlName=\"is_public\" color=\"primary\">\n      Is public\n    </mat-checkbox>\n    <mat-checkbox formControlName=\"show_in_fleio\" color=\"primary\">\n      Show in end user panel\n    </mat-checkbox>\n    <mat-checkbox formControlName=\"out_of_stock\" color=\"primary\">\n      Out of stock\n    </mat-checkbox>\n  </div>\n</form>\n"

/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavor-create/flavor-create.component.scss":
/*!***********************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavor-create/flavor-create.component.scss ***!
  \***********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ZsYXZvcnMvZmxhdm9yLWNyZWF0ZS9mbGF2b3ItY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavor-create/flavor-create.component.ts":
/*!*********************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavor-create/flavor-create.component.ts ***!
  \*********************************************************************************/
/*! exports provided: FlavorCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorCreateComponent", function() { return FlavorCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _flavor_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../flavor-list-ui.service */ "./src/app/reseller/cloud/flavors/flavor-list-ui.service.ts");





let FlavorCreateComponent = class FlavorCreateComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, flavorListUIService) {
        super(route, flavorListUIService, 'create', null);
    }
};
FlavorCreateComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _flavor_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["FlavorListUIService"] }
];
FlavorCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-flavor-create',
        template: __webpack_require__(/*! raw-loader!./flavor-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/flavor-create/flavor-create.component.html"),
        styles: [__webpack_require__(/*! ./flavor-create.component.scss */ "./src/app/reseller/cloud/flavors/flavor-create/flavor-create.component.scss")]
    })
], FlavorCreateComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavor-details/flavor-details.component.scss":
/*!*************************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavor-details/flavor-details.component.scss ***!
  \*************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ZsYXZvcnMvZmxhdm9yLWRldGFpbHMvZmxhdm9yLWRldGFpbHMuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavor-details/flavor-details.component.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavor-details/flavor-details.component.ts ***!
  \***********************************************************************************/
/*! exports provided: FlavorDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorDetailsComponent", function() { return FlavorDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _flavor_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../flavor-list-ui.service */ "./src/app/reseller/cloud/flavors/flavor-list-ui.service.ts");





let FlavorDetailsComponent = class FlavorDetailsComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, flavorListUIService) {
        super(route, flavorListUIService, 'details', 'flavor');
    }
};
FlavorDetailsComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _flavor_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["FlavorListUIService"] }
];
FlavorDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-flavor-details',
        template: __webpack_require__(/*! raw-loader!./flavor-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/flavor-details/flavor-details.component.html"),
        styles: [__webpack_require__(/*! ./flavor-details.component.scss */ "./src/app/reseller/cloud/flavors/flavor-details/flavor-details.component.scss")]
    })
], FlavorDetailsComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavor-edit/flavor-edit.component.scss":
/*!*******************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavor-edit/flavor-edit.component.scss ***!
  \*******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ZsYXZvcnMvZmxhdm9yLWVkaXQvZmxhdm9yLWVkaXQuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavor-edit/flavor-edit.component.ts":
/*!*****************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavor-edit/flavor-edit.component.ts ***!
  \*****************************************************************************/
/*! exports provided: FlavorEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorEditComponent", function() { return FlavorEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _flavor_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../flavor-list-ui.service */ "./src/app/reseller/cloud/flavors/flavor-list-ui.service.ts");





let FlavorEditComponent = class FlavorEditComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, flavorListUIService) {
        super(route, flavorListUIService, 'edit', 'flavor');
    }
};
FlavorEditComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _flavor_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["FlavorListUIService"] }
];
FlavorEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-flavor-edit',
        template: __webpack_require__(/*! raw-loader!./flavor-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/flavor-edit/flavor-edit.component.html"),
        styles: [__webpack_require__(/*! ./flavor-edit.component.scss */ "./src/app/reseller/cloud/flavors/flavor-edit/flavor-edit.component.scss")]
    })
], FlavorEditComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavor-list-ui.service.ts":
/*!******************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavor-list-ui.service.ts ***!
  \******************************************************************/
/*! exports provided: FlavorListUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorListUIService", function() { return FlavorListUIService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_fleio_api_cloud_flavor_flavors_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/flavor/flavors-api.service */ "./src/app/shared/fleio-api/cloud/flavor/flavors-api.service.ts");
/* harmony import */ var _flavor_ui_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./flavor-ui.service */ "./src/app/reseller/cloud/flavors/flavor-ui.service.ts");








let FlavorListUIService = class FlavorListUIService {
    constructor(router, config, flavorsApiService) {
        this.router = router;
        this.config = config;
        this.flavorsApiService = flavorsApiService;
    }
    getObjectUIService(object, permissions, state) {
        return new _flavor_ui_service__WEBPACK_IMPORTED_MODULE_7__["FlavorUiService"](object, permissions, state, this.router, this.config, this.flavorsApiService);
    }
    getTableData(objectList) {
        const tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Name', enableSort: true, fieldName: 'name' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Labels', enableSort: false, fieldName: 'tags' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Region', enableSort: true, fieldName: 'region' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'vCPUs', enableSort: true, fieldName: 'vcpus' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Memory', enableSort: true, fieldName: 'memory_mb' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Root', enableSort: true, fieldName: 'root_gb' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Description', enableSort: false, fieldName: 'description' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Actions, displayName: 'Actions', enableSort: false, fieldName: '(actions)' },
                ],
                columnNames: ['name', 'tags', 'region', 'vcpus', 'memory_mb', 'root_gb', 'description', '(actions)'],
                statusColumn: 'name',
            },
            rows: [],
        };
        for (const flavor of objectList.objects) {
            const rowUIService = this.getObjectUIService(flavor, objectList.permissions, 'table-view');
            const row = {
                cells: {
                    name: { text: flavor.name },
                    tags: { tags: rowUIService.getCardTags() },
                    region: { text: flavor.region },
                    vcpus: { text: `${flavor.vcpus} vCPUs` },
                    memory_mb: { text: `${flavor.memory_mb} MB` },
                    root_gb: { text: `${flavor.root_gb} GB` },
                    description: { text: flavor.description },
                },
                icon: rowUIService.getIcon(),
                status: rowUIService.getStatus(),
                actions: rowUIService.getActions(),
                url: rowUIService.isGlobal() ? null : rowUIService.getDetailsLink(),
            };
            tableData.rows.push(row);
        }
        return tableData;
    }
    getActions(objectList) {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__["RouterLinkAction"]({
                name: 'Create new flavor',
                tooltip: 'Create new flavor',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('cloud/flavors/create')
            })
        ];
    }
};
FlavorListUIService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_cloud_flavor_flavors_api_service__WEBPACK_IMPORTED_MODULE_6__["FlavorsApiService"] }
];
FlavorListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], FlavorListUIService);



/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavor-list/flavor-list.component.scss":
/*!*******************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavor-list/flavor-list.component.scss ***!
  \*******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ZsYXZvcnMvZmxhdm9yLWxpc3QvZmxhdm9yLWxpc3QuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavor-list/flavor-list.component.ts":
/*!*****************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavor-list/flavor-list.component.ts ***!
  \*****************************************************************************/
/*! exports provided: FlavorListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorListComponent", function() { return FlavorListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _flavors_flavor_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../flavors/flavor-list-ui.service */ "./src/app/reseller/cloud/flavors/flavor-list-ui.service.ts");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");






let FlavorListComponent = class FlavorListComponent extends _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"] {
    constructor(route, flavorListUIService, refreshService) {
        super(route, flavorListUIService, refreshService, 'flavors');
        this.route = route;
        this.flavorListUIService = flavorListUIService;
        this.refreshService = refreshService;
    }
    ngOnInit() {
        super.ngOnInit();
    }
};
FlavorListComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _flavors_flavor_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["FlavorListUIService"] },
    { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_5__["RefreshService"] }
];
FlavorListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-flavor-list',
        template: __webpack_require__(/*! raw-loader!./flavor-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/flavor-list/flavor-list.component.html"),
        styles: [__webpack_require__(/*! ./flavor-list.component.scss */ "./src/app/reseller/cloud/flavors/flavor-list/flavor-list.component.scss")]
    })
], FlavorListComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavor-ui.service.ts":
/*!*************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavor-ui.service.ts ***!
  \*************************************************************/
/*! exports provided: FlavorUiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorUiService", function() { return FlavorUiService; });
/* harmony import */ var _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/object-status */ "./src/app/shared/ui/objects-view/interfaces/object-status.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_fleio_api_cloud_flavor_flavors_api_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/flavor/flavors-api.service */ "./src/app/shared/fleio-api/cloud/flavor/flavors-api.service.ts");
/* harmony import */ var _tabs_flavor_details_overview_flavor_details_overview_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/flavor-details-overview/flavor-details-overview.component */ "./src/app/reseller/cloud/flavors/tabs/flavor-details-overview/flavor-details-overview.component.ts");
/* harmony import */ var _tabs_flavor_edit_form_flavor_edit_form_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/flavor-edit-form/flavor-edit-form.component */ "./src/app/reseller/cloud/flavors/tabs/flavor-edit-form/flavor-edit-form.component.ts");











class FlavorUiService extends _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__["ObjectUIServiceBase"] {
    constructor(flavor, permissions, state, router, config, flavorsApiService) {
        super(flavor, permissions, state);
        this.router = router;
        this.config = config;
        this.flavorsApiService = flavorsApiService;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_6__["DatePipe"](this.config.locale);
    }
    isGlobal() {
        return !this.object.reseller_resources;
    }
    getIcon() {
        return null;
    }
    getStatus() {
        if (this.object.disabled) {
            return { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Disabled };
        }
        else {
            return { type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined, value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Enabled };
        }
    }
    getTitle() {
        switch (this.state) {
            case 'edit':
                return {
                    text: `Edit ${this.object.name}`,
                };
            case 'create':
                return {
                    text: `Create new flavor`,
                };
            case 'details':
            default:
                return {
                    text: `${this.object.name}`,
                    subText: `${this.object.disabled ? 'DISABLED' : 'ACTIVE'}, ${this.object.region}`,
                };
        }
    }
    getActions() {
        const actions = [];
        if (!this.isGlobal()) {
            actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                icon: { name: 'edit', class: 'fl-icons' },
                name: 'Edit',
                tooltip: 'Edit',
                routerUrl: this.config.getPanelUrl(`cloud/flavors/${this.object.id}/edit`),
                router: this.router,
            }));
            actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["ApiCallAction"]({
                object: this.object,
                icon: { name: 'delete' },
                name: 'Delete',
                tooltip: 'Delete',
                confirmOptions: {
                    confirm: true,
                    title: 'Delete flavor',
                    message: `Are you sure you want to delete flavor ${this.object.name}`,
                },
                apiService: this.flavorsApiService,
                callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["CallType"].Delete,
            }));
        }
        else {
            if (this.object.display_for_clients) {
                actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["ApiCallAction"]({
                    object: this.object,
                    icon: { name: 'visibility_off' },
                    name: 'Hide for clients',
                    tooltip: 'Hide for clients',
                    confirmOptions: {
                        confirm: true,
                        title: 'Hide flavor for clients',
                        message: `Are you sure you want hide flavor ${this.object.name} for clients`,
                    },
                    apiService: this.flavorsApiService,
                    callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["CallType"].Post,
                    apiAction: 'hide_for_clients'
                }));
            }
            else {
                actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["ApiCallAction"]({
                    object: this.object,
                    icon: { name: 'visibility' },
                    name: 'Display for clients',
                    tooltip: 'Display for clients',
                    confirmOptions: {
                        confirm: true,
                        title: 'Display flavor for clients',
                        message: `Are you sure you want display flavor ${this.object.name} for clients`,
                    },
                    apiService: this.flavorsApiService,
                    callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["CallType"].Post,
                    apiAction: 'display_for_clients'
                }));
            }
        }
        return actions;
    }
    getDetailsActions() {
        const actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`cloud/flavors`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`cloud/flavors`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({
                    name: 'Save',
                    refreshAfterExecute: false,
                }));
                break;
            default:
                break;
        }
        return actions;
    }
    getDetailsLink() {
        return this.config.getPanelUrl(`cloud/flavors/${this.object.id}`);
    }
    getCardFields() {
        const fields = [
            {
                value: `${this.object.vcpus} vCPUs`
            },
            {
                value: `${this.object.memory_mb} MB RAM, ${this.object.root_gb} GB disk`
            },
            {
                name: 'Group',
                value: this.object.flavor_group || 'n/a'
            },
        ];
        return fields;
    }
    getTabs() {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Overview',
                        component: _tabs_flavor_details_overview_flavor_details_overview_component__WEBPACK_IMPORTED_MODULE_9__["FlavorDetailsOverviewComponent"],
                    },
                ];
            case 'create':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_flavor_edit_form_flavor_edit_form_component__WEBPACK_IMPORTED_MODULE_10__["FlavorEditFormComponent"],
                    },
                ];
            case 'edit':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_flavor_edit_form_flavor_edit_form_component__WEBPACK_IMPORTED_MODULE_10__["FlavorEditFormComponent"],
                    },
                ];
        }
    }
    getCardTags() {
        const tags = [];
        if (this.isGlobal()) {
            tags.push('global');
            if (this.object.display_for_clients) {
                tags.push('visible');
            }
            else {
                tags.push('hidden');
            }
        }
        else {
            if (this.object.show_in_fleio && this.object.is_public) {
                tags.push('visible');
            }
            else {
                tags.push('hidden');
            }
        }
        return tags;
    }
}
FlavorUiService.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] },
    { type: _shared_fleio_api_cloud_flavor_flavors_api_service__WEBPACK_IMPORTED_MODULE_8__["FlavorsApiService"] }
];


/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavors-routing.module.ts":
/*!******************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavors-routing.module.ts ***!
  \******************************************************************/
/*! exports provided: FlavorsRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorsRoutingModule", function() { return FlavorsRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _flavor_list_flavor_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./flavor-list/flavor-list.component */ "./src/app/reseller/cloud/flavors/flavor-list/flavor-list.component.ts");
/* harmony import */ var _flavor_create_flavor_create_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./flavor-create/flavor-create.component */ "./src/app/reseller/cloud/flavors/flavor-create/flavor-create.component.ts");
/* harmony import */ var _flavor_details_flavor_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./flavor-details/flavor-details.component */ "./src/app/reseller/cloud/flavors/flavor-details/flavor-details.component.ts");
/* harmony import */ var _flavor_edit_flavor_edit_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./flavor-edit/flavor-edit.component */ "./src/app/reseller/cloud/flavors/flavor-edit/flavor-edit.component.ts");
/* harmony import */ var _shared_fleio_api_cloud_flavor_flavor_list_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/flavor/flavor-list.resolver */ "./src/app/shared/fleio-api/cloud/flavor/flavor-list.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_flavor_flavor_resolver__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/flavor/flavor.resolver */ "./src/app/shared/fleio-api/cloud/flavor/flavor.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_flavor_flavor_permissions_resolver__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/flavor/flavor-permissions.resolver */ "./src/app/shared/fleio-api/cloud/flavor/flavor-permissions.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_flavor_flavor_create_options_resolver__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/flavor/flavor-create-options.resolver */ "./src/app/shared/fleio-api/cloud/flavor/flavor-create-options.resolver.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/ui-api/interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");













const routes = [
    {
        path: '',
        component: _flavor_list_flavor_list_component__WEBPACK_IMPORTED_MODULE_3__["FlavorListComponent"],
        resolve: {
            flavors: _shared_fleio_api_cloud_flavor_flavor_list_resolver__WEBPACK_IMPORTED_MODULE_7__["FlavorListResolver"],
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_12__["AuthGuard"]],
        data: {
            config: {
                feature: 'openstack.flavors',
                search: {
                    show: true,
                    placeholder: 'Search flavors ...',
                },
                subheader: {
                    objectNamePlural: 'flavors',
                    objectName: 'flavor',
                    objectList(data) {
                        return data.flavors;
                    }
                },
                ordering: {
                    default: {
                        field: 'memory_mb',
                        display: 'Memory MB',
                        direction: _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__["OrderingDirection"].Ascending,
                    },
                    options: [
                        {
                            field: 'name',
                            display: 'Name',
                        },
                        {
                            field: 'region',
                            display: 'Region',
                        },
                        {
                            field: 'vcpus',
                            display: 'vCPUs',
                        },
                        {
                            field: 'memory_mb',
                            display: 'Memory MB',
                        },
                        {
                            field: 'root_gb',
                            display: 'Root',
                        },
                    ]
                }
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: 'create',
        component: _flavor_create_flavor_create_component__WEBPACK_IMPORTED_MODULE_4__["FlavorCreateComponent"],
        resolve: {
            createOptions: _shared_fleio_api_cloud_flavor_flavor_create_options_resolver__WEBPACK_IMPORTED_MODULE_10__["FlavorCreateOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: () => {
                    return 'Create flavor';
                },
            },
        }
    },
    {
        path: ':id',
        component: _flavor_details_flavor_details_component__WEBPACK_IMPORTED_MODULE_5__["FlavorDetailsComponent"],
        resolve: {
            flavor: _shared_fleio_api_cloud_flavor_flavor_resolver__WEBPACK_IMPORTED_MODULE_8__["FlavorResolver"],
            permissions: _shared_fleio_api_cloud_flavor_flavor_permissions_resolver__WEBPACK_IMPORTED_MODULE_9__["FlavorPermissionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.flavor.name;
                },
            },
        }
    },
    {
        path: ':id/edit',
        component: _flavor_edit_flavor_edit_component__WEBPACK_IMPORTED_MODULE_6__["FlavorEditComponent"],
        resolve: {
            flavor: _shared_fleio_api_cloud_flavor_flavor_resolver__WEBPACK_IMPORTED_MODULE_8__["FlavorResolver"],
            createOptions: _shared_fleio_api_cloud_flavor_flavor_create_options_resolver__WEBPACK_IMPORTED_MODULE_10__["FlavorCreateOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.flavor.name;
                },
            },
        }
    },
];
let FlavorsRoutingModule = class FlavorsRoutingModule {
};
FlavorsRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], FlavorsRoutingModule);



/***/ }),

/***/ "./src/app/reseller/cloud/flavors/flavors.module.ts":
/*!**********************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/flavors.module.ts ***!
  \**********************************************************/
/*! exports provided: FlavorsModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorsModule", function() { return FlavorsModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _flavor_create_flavor_create_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./flavor-create/flavor-create.component */ "./src/app/reseller/cloud/flavors/flavor-create/flavor-create.component.ts");
/* harmony import */ var _flavor_details_flavor_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./flavor-details/flavor-details.component */ "./src/app/reseller/cloud/flavors/flavor-details/flavor-details.component.ts");
/* harmony import */ var _flavor_edit_flavor_edit_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./flavor-edit/flavor-edit.component */ "./src/app/reseller/cloud/flavors/flavor-edit/flavor-edit.component.ts");
/* harmony import */ var _flavor_list_flavor_list_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./flavor-list/flavor-list.component */ "./src/app/reseller/cloud/flavors/flavor-list/flavor-list.component.ts");
/* harmony import */ var _flavors_routing_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./flavors-routing.module */ "./src/app/reseller/cloud/flavors/flavors-routing.module.ts");
/* harmony import */ var _tabs_flavor_details_overview_flavor_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/flavor-details-overview/flavor-details-overview.component */ "./src/app/reseller/cloud/flavors/tabs/flavor-details-overview/flavor-details-overview.component.ts");
/* harmony import */ var _tabs_flavor_edit_form_flavor_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/flavor-edit-form/flavor-edit-form.component */ "./src/app/reseller/cloud/flavors/tabs/flavor-edit-form/flavor-edit-form.component.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm2015/select.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm2015/checkbox.js");


















let FlavorsModule = class FlavorsModule {
};
FlavorsModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _flavor_create_flavor_create_component__WEBPACK_IMPORTED_MODULE_3__["FlavorCreateComponent"],
            _flavor_details_flavor_details_component__WEBPACK_IMPORTED_MODULE_4__["FlavorDetailsComponent"],
            _flavor_edit_flavor_edit_component__WEBPACK_IMPORTED_MODULE_5__["FlavorEditComponent"],
            _flavor_list_flavor_list_component__WEBPACK_IMPORTED_MODULE_6__["FlavorListComponent"],
            _tabs_flavor_details_overview_flavor_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["FlavorDetailsOverviewComponent"],
            _tabs_flavor_edit_form_flavor_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["FlavorEditFormComponent"],
        ],
        entryComponents: [
            _tabs_flavor_details_overview_flavor_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["FlavorDetailsOverviewComponent"],
            _tabs_flavor_edit_form_flavor_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["FlavorEditFormComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _flavors_routing_module__WEBPACK_IMPORTED_MODULE_7__["FlavorsRoutingModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_10__["ReactiveFormsModule"],
            _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__["ErrorHandlingModule"],
            _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_12__["ObjectsViewModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_13__["FlexModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_14__["MatFormFieldModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_15__["MatInputModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_16__["MatSelectModule"],
            _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_17__["MatCheckboxModule"],
        ]
    })
], FlavorsModule);



/***/ }),

/***/ "./src/app/reseller/cloud/flavors/tabs/flavor-details-overview/flavor-details-overview.component.scss":
/*!************************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/tabs/flavor-details-overview/flavor-details-overview.component.scss ***!
  \************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ZsYXZvcnMvdGFicy9mbGF2b3ItZGV0YWlscy1vdmVydmlldy9mbGF2b3ItZGV0YWlscy1vdmVydmlldy5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/cloud/flavors/tabs/flavor-details-overview/flavor-details-overview.component.ts":
/*!**********************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/tabs/flavor-details-overview/flavor-details-overview.component.ts ***!
  \**********************************************************************************************************/
/*! exports provided: FlavorDetailsOverviewComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorDetailsOverviewComponent", function() { return FlavorDetailsOverviewComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");



let FlavorDetailsOverviewComponent = class FlavorDetailsOverviewComponent extends _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"] {
    constructor() {
        super();
    }
    ngOnInit() {
    }
};
FlavorDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-flavor-details-overview',
        template: __webpack_require__(/*! raw-loader!./flavor-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/tabs/flavor-details-overview/flavor-details-overview.component.html"),
        styles: [__webpack_require__(/*! ./flavor-details-overview.component.scss */ "./src/app/reseller/cloud/flavors/tabs/flavor-details-overview/flavor-details-overview.component.scss")]
    })
], FlavorDetailsOverviewComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/flavors/tabs/flavor-edit-form/flavor-edit-form.component.scss":
/*!**********************************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/tabs/flavor-edit-form/flavor-edit-form.component.scss ***!
  \**********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ZsYXZvcnMvdGFicy9mbGF2b3ItZWRpdC1mb3JtL2ZsYXZvci1lZGl0LWZvcm0uY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/flavors/tabs/flavor-edit-form/flavor-edit-form.component.ts":
/*!********************************************************************************************!*\
  !*** ./src/app/reseller/cloud/flavors/tabs/flavor-edit-form/flavor-edit-form.component.ts ***!
  \********************************************************************************************/
/*! exports provided: FlavorEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorEditFormComponent", function() { return FlavorEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_fleio_api_cloud_flavor_flavors_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/flavor/flavors-api.service */ "./src/app/shared/fleio-api/cloud/flavor/flavors-api.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");








let FlavorEditFormComponent = class FlavorEditFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"] {
    constructor(formBuilder, flavorsApi, router, config, activatedRoute) {
        super();
        this.formBuilder = formBuilder;
        this.flavorsApi = flavorsApi;
        this.router = router;
        this.config = config;
        this.activatedRoute = activatedRoute;
        this.flavorForm = this.formBuilder.group({
            preserve_id: [true],
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            region: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            memory_mb: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            vcpus: [1, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            root_gb: [1, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            swap: [0, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            ephemeral_gb: [0, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            description: [''],
            is_public: [true],
            show_in_fleio: [true],
            out_of_stock: [false],
        });
    }
    ngOnInit() {
        this.createOptions = this.activatedRoute.snapshot.data.createOptions;
        this.objectController.actionCallback = () => this.saveFlavor();
        this.flavorForm.patchValue(this.object);
        if (!this.object.id) {
            // creating new flavor
            this.flavorForm.controls.region.setValue(this.createOptions.selected_region);
        }
    }
    saveFlavor() {
        const value = this.flavorForm.value;
        this.createOrUpdate(this.flavorsApi, value).subscribe(() => {
            this.router.navigateByUrl(this.config.getPrevUrl('cloud/flavors')).catch(() => {
            });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_7__["of"])(null);
    }
};
FlavorEditFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
    { type: _shared_fleio_api_cloud_flavor_flavors_api_service__WEBPACK_IMPORTED_MODULE_4__["FlavorsApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_6__["ConfigService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["ActivatedRoute"] }
];
FlavorEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-flavor-edit-form',
        template: __webpack_require__(/*! raw-loader!./flavor-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/flavors/tabs/flavor-edit-form/flavor-edit-form.component.html"),
        styles: [__webpack_require__(/*! ./flavor-edit-form.component.scss */ "./src/app/reseller/cloud/flavors/tabs/flavor-edit-form/flavor-edit-form.component.scss")]
    })
], FlavorEditFormComponent);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/flavor/flavor-create-options.resolver.ts":
/*!*********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/flavor/flavor-create-options.resolver.ts ***!
  \*********************************************************************************/
/*! exports provided: FlavorCreateOptionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorCreateOptionsResolver", function() { return FlavorCreateOptionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _flavors_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./flavors-api.service */ "./src/app/shared/fleio-api/cloud/flavor/flavors-api.service.ts");





let FlavorCreateOptionsResolver = class FlavorCreateOptionsResolver {
    constructor(flavorsApiService) {
        this.flavorsApiService = flavorsApiService;
    }
    resolve(route, state) {
        return this.flavorsApiService.createOptions()
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
FlavorCreateOptionsResolver.ctorParameters = () => [
    { type: _flavors_api_service__WEBPACK_IMPORTED_MODULE_4__["FlavorsApiService"] }
];
FlavorCreateOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], FlavorCreateOptionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/flavor/flavor-list.resolver.ts":
/*!***********************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/flavor/flavor-list.resolver.ts ***!
  \***********************************************************************/
/*! exports provided: FlavorListResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorListResolver", function() { return FlavorListResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _flavors_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./flavors-api.service */ "./src/app/shared/fleio-api/cloud/flavor/flavors-api.service.ts");





let FlavorListResolver = class FlavorListResolver {
    constructor(flavorsApiService) {
        this.flavorsApiService = flavorsApiService;
    }
    resolve(route, state) {
        return this.flavorsApiService.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
FlavorListResolver.ctorParameters = () => [
    { type: _flavors_api_service__WEBPACK_IMPORTED_MODULE_4__["FlavorsApiService"] }
];
FlavorListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], FlavorListResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/flavor/flavor-permissions.resolver.ts":
/*!******************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/flavor/flavor-permissions.resolver.ts ***!
  \******************************************************************************/
/*! exports provided: FlavorPermissionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorPermissionsResolver", function() { return FlavorPermissionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _flavors_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./flavors-api.service */ "./src/app/shared/fleio-api/cloud/flavor/flavors-api.service.ts");





let FlavorPermissionsResolver = class FlavorPermissionsResolver {
    constructor(flavorsApi) {
        this.flavorsApi = flavorsApi;
    }
    resolve(route, state) {
        return this.flavorsApi.permissions().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
FlavorPermissionsResolver.ctorParameters = () => [
    { type: _flavors_api_service__WEBPACK_IMPORTED_MODULE_4__["FlavorsApiService"] }
];
FlavorPermissionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], FlavorPermissionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/flavor/flavor.resolver.ts":
/*!******************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/flavor/flavor.resolver.ts ***!
  \******************************************************************/
/*! exports provided: FlavorResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorResolver", function() { return FlavorResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _flavors_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./flavors-api.service */ "./src/app/shared/fleio-api/cloud/flavor/flavors-api.service.ts");





let FlavorResolver = class FlavorResolver {
    constructor(flavorsApiService) {
        this.flavorsApiService = flavorsApiService;
    }
    resolve(route, state) {
        return this.flavorsApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
FlavorResolver.ctorParameters = () => [
    { type: _flavors_api_service__WEBPACK_IMPORTED_MODULE_4__["FlavorsApiService"] }
];
FlavorResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], FlavorResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/flavor/flavors-api.service.ts":
/*!**********************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/flavor/flavors-api.service.ts ***!
  \**********************************************************************/
/*! exports provided: FlavorsApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorsApiService", function() { return FlavorsApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");





let FlavorsApiService = class FlavorsApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('openstack/flavors'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
FlavorsApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
FlavorsApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], FlavorsApiService);



/***/ })

}]);
//# sourceMappingURL=flavors-flavors-module-es2015.js.map