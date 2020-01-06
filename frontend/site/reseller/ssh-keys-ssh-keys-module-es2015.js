(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["ssh-keys-ssh-keys-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/ssh-key-create/ssh-key-create.component.html":
/*!****************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/ssh-keys/ssh-key-create/ssh-key-create.component.html ***!
  \****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/ssh-key-details/ssh-key-details.component.html":
/*!******************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/ssh-keys/ssh-key-details/ssh-key-details.component.html ***!
  \******************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\"></app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/ssh-key-edit/ssh-key-edit.component.html":
/*!************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/ssh-keys/ssh-key-edit/ssh-key-edit.component.html ***!
  \************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/ssh-key-list/ssh-key-list.component.html":
/*!************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/ssh-keys/ssh-key-list/ssh-key-list.component.html ***!
  \************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-objects-view [objectsListController]=\"objectListController\"></app-objects-view>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-details-overview/ssh-key-details-overview.component.html":
/*!*****************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-details-overview/ssh-key-details-overview.component.html ***!
  \*****************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxLayout=\"column\">\n  <p class=\"fl-detail\">Created on: {{object.created_at}}</p>\n  <p class=\"fl-detail\">User: {{object.user.username}}</p>\n  <p class=\"fl-detail\">Fingerprint: {{object.fingerprint}}</p>\n  <p class=\"fl-detail wrap-text-content\">Public key:\n    <span class=\"fl-indent display-inline-block\">{{object.public_key}}</span>\n    <button mat-button color=\"primary\" (click)=\"clipboard.copyTextToClipboard(object.public_key)\">\n      Copy to clipboard\n    </button>\n  </p>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-edit-form/ssh-key-edit-form.component.html":
/*!***************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-edit-form/ssh-key-edit-form.component.html ***!
  \***************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form [formGroup]=\"sshKeyForm\">\n  <app-form-errors #formErrors [formGroup]=\"sshKeyForm\"></app-form-errors>\n  <div fxLayout=\"column\">\n    <mat-form-field>\n      <input matInput placeholder=\"Name\" type=\"text\" formControlName=\"name\" required>\n      <mat-error>{{backendErrors['name'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n    <mat-form-field>\n      <textarea matInput rows=\"10\" #publicKey\n                placeholder=\"Key content\" type=\"text\" formControlName=\"public_key\" required>\n      </textarea>\n      <mat-error>{{backendErrors['public_key'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n      <button *ngIf=\"generatedKey\" mat-button color=\"primary\"\n              (click)=\"clipboard.copyTextAreaToClipboard(publicKey)\">\n        Copy public key to clipboard\n      </button>\n    <ng-container *ngIf=\"generatedKey\">\n      <mat-form-field>\n        <p class=\"fl-detail\">Private key. You should save this key locally, it will not be saved on server.</p>\n        <textarea matInput rows=\"10\" #privateKey\n                  placeholder=\"Private key\" type=\"text\" formControlName=\"private_key\" readonly>\n        </textarea>\n      </mat-form-field>\n      <button mat-button color=\"primary\" (click)=\"clipboard.copyTextAreaToClipboard(privateKey)\">\n        Copy private key to clipboard\n      </button>\n    </ng-container>\n  </div>\n</form>\n"

/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-key-create/ssh-key-create.component.scss":
/*!**************************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-key-create/ssh-key-create.component.scss ***!
  \**************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3NzaC1rZXlzL3NzaC1rZXktY3JlYXRlL3NzaC1rZXktY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-key-create/ssh-key-create.component.ts":
/*!************************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-key-create/ssh-key-create.component.ts ***!
  \************************************************************************************/
/*! exports provided: SshKeyCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SshKeyCreateComponent", function() { return SshKeyCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ssh_key_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../ssh-key-list-ui.service */ "./src/app/reseller/cloud/ssh-keys/ssh-key-list-ui.service.ts");





let SshKeyCreateComponent = class SshKeyCreateComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, sshKeyListUIService) {
        super(route, sshKeyListUIService, 'create', null);
    }
};
SshKeyCreateComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _ssh_key_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["SshKeyListUIService"] }
];
SshKeyCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-ssh-key-create',
        template: __webpack_require__(/*! raw-loader!./ssh-key-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/ssh-key-create/ssh-key-create.component.html"),
        styles: [__webpack_require__(/*! ./ssh-key-create.component.scss */ "./src/app/reseller/cloud/ssh-keys/ssh-key-create/ssh-key-create.component.scss")]
    })
], SshKeyCreateComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-key-details/ssh-key-details.component.scss":
/*!****************************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-key-details/ssh-key-details.component.scss ***!
  \****************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3NzaC1rZXlzL3NzaC1rZXktZGV0YWlscy9zc2gta2V5LWRldGFpbHMuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-key-details/ssh-key-details.component.ts":
/*!**************************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-key-details/ssh-key-details.component.ts ***!
  \**************************************************************************************/
/*! exports provided: SshKeyDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SshKeyDetailsComponent", function() { return SshKeyDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ssh_key_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../ssh-key-list-ui.service */ "./src/app/reseller/cloud/ssh-keys/ssh-key-list-ui.service.ts");





let SshKeyDetailsComponent = class SshKeyDetailsComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, sshKeyListUIService) {
        super(route, sshKeyListUIService, 'details', 'sshKey');
    }
};
SshKeyDetailsComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _ssh_key_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["SshKeyListUIService"] }
];
SshKeyDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-ssh-key-details',
        template: __webpack_require__(/*! raw-loader!./ssh-key-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/ssh-key-details/ssh-key-details.component.html"),
        styles: [__webpack_require__(/*! ./ssh-key-details.component.scss */ "./src/app/reseller/cloud/ssh-keys/ssh-key-details/ssh-key-details.component.scss")]
    })
], SshKeyDetailsComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-key-edit/ssh-key-edit.component.scss":
/*!**********************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-key-edit/ssh-key-edit.component.scss ***!
  \**********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3NzaC1rZXlzL3NzaC1rZXktZWRpdC9zc2gta2V5LWVkaXQuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-key-edit/ssh-key-edit.component.ts":
/*!********************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-key-edit/ssh-key-edit.component.ts ***!
  \********************************************************************************/
/*! exports provided: SshKeyEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SshKeyEditComponent", function() { return SshKeyEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ssh_key_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../ssh-key-list-ui.service */ "./src/app/reseller/cloud/ssh-keys/ssh-key-list-ui.service.ts");





let SshKeyEditComponent = class SshKeyEditComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, sshKeyListUIService) {
        super(route, sshKeyListUIService, 'edit', 'sshKey');
    }
};
SshKeyEditComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _ssh_key_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["SshKeyListUIService"] }
];
SshKeyEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-ssh-key-edit',
        template: __webpack_require__(/*! raw-loader!./ssh-key-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/ssh-key-edit/ssh-key-edit.component.html"),
        styles: [__webpack_require__(/*! ./ssh-key-edit.component.scss */ "./src/app/reseller/cloud/ssh-keys/ssh-key-edit/ssh-key-edit.component.scss")]
    })
], SshKeyEditComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-key-list-ui.service.ts":
/*!********************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-key-list-ui.service.ts ***!
  \********************************************************************/
/*! exports provided: SshKeyListUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SshKeyListUIService", function() { return SshKeyListUIService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_fleio_api_public_key_public_key_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/public-key/public-key-api.service */ "./src/app/shared/fleio-api/public-key/public-key-api.service.ts");
/* harmony import */ var _ssh_key_ui_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./ssh-key-ui.service */ "./src/app/reseller/cloud/ssh-keys/ssh-key-ui.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");









let SshKeyListUIService = class SshKeyListUIService {
    constructor(router, config, publicKeysApiService) {
        this.router = router;
        this.config = config;
        this.publicKeysApiService = publicKeysApiService;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_8__["DatePipe"](this.config.locale);
    }
    getObjectUIService(object, permissions, state) {
        return new _ssh_key_ui_service__WEBPACK_IMPORTED_MODULE_7__["SshKeyUiService"](object, permissions, state, this.router, this.config, this.publicKeysApiService);
    }
    getTableData(objectList) {
        const tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Name', enableSort: true, fieldName: 'name' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Fingerprint', enableSort: false, fieldName: 'fingerprint' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Created at', enableSort: true, fieldName: 'created_at' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Actions, displayName: 'Actions', enableSort: false, fieldName: '(actions)' },
                ],
                columnNames: ['name', 'fingerprint', 'created_at', '(actions)'],
                statusColumn: 'name',
            },
            rows: [],
        };
        for (const publicKey of objectList.objects) {
            const rowUIService = this.getObjectUIService(publicKey, objectList.permissions, 'table-view');
            const row = {
                cells: {
                    name: { text: publicKey.name },
                    fingerprint: { text: publicKey.fingerprint },
                    created_at: { text: this.datePipe.transform(publicKey.created_at) },
                },
                icon: rowUIService.getIcon(),
                status: rowUIService.getStatus(),
                actions: rowUIService.getActions(),
                url: rowUIService.getDetailsLink(),
            };
            tableData.rows.push(row);
        }
        return tableData;
    }
    getActions(objectList) {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__["RouterLinkAction"]({
                name: 'Create new ssh key',
                tooltip: 'Create new ssh key',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('cloud/ssh-keys/create')
            })
        ];
    }
};
SshKeyListUIService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_public_key_public_key_api_service__WEBPACK_IMPORTED_MODULE_6__["PublicKeysApiService"] }
];
SshKeyListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], SshKeyListUIService);



/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-key-list/ssh-key-list.component.scss":
/*!**********************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-key-list/ssh-key-list.component.scss ***!
  \**********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3NzaC1rZXlzL3NzaC1rZXktbGlzdC9zc2gta2V5LWxpc3QuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-key-list/ssh-key-list.component.ts":
/*!********************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-key-list/ssh-key-list.component.ts ***!
  \********************************************************************************/
/*! exports provided: SshKeyListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SshKeyListComponent", function() { return SshKeyListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _ssh_key_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../ssh-key-list-ui.service */ "./src/app/reseller/cloud/ssh-keys/ssh-key-list-ui.service.ts");






let SshKeyListComponent = class SshKeyListComponent extends _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"] {
    constructor(route, sshKeyListUIService, refreshService) {
        super(route, sshKeyListUIService, refreshService, 'sshKeys');
        this.route = route;
        this.sshKeyListUIService = sshKeyListUIService;
        this.refreshService = refreshService;
    }
    ngOnInit() {
        super.ngOnInit();
    }
};
SshKeyListComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _ssh_key_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["SshKeyListUIService"] },
    { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
];
SshKeyListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-ssh-key-list',
        template: __webpack_require__(/*! raw-loader!./ssh-key-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/ssh-key-list/ssh-key-list.component.html"),
        styles: [__webpack_require__(/*! ./ssh-key-list.component.scss */ "./src/app/reseller/cloud/ssh-keys/ssh-key-list/ssh-key-list.component.scss")]
    })
], SshKeyListComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-key-ui.service.ts":
/*!***************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-key-ui.service.ts ***!
  \***************************************************************/
/*! exports provided: SshKeyUiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SshKeyUiService", function() { return SshKeyUiService; });
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_fleio_api_public_key_public_key_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/public-key/public-key-api.service */ "./src/app/shared/fleio-api/public-key/public-key-api.service.ts");
/* harmony import */ var _tabs_ssh_key_details_overview_ssh_key_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/ssh-key-details-overview/ssh-key-details-overview.component */ "./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-details-overview/ssh-key-details-overview.component.ts");
/* harmony import */ var _tabs_ssh_key_edit_form_ssh_key_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/ssh-key-edit-form/ssh-key-edit-form.component */ "./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-edit-form/ssh-key-edit-form.component.ts");










class SshKeyUiService extends _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_0__["ObjectUIServiceBase"] {
    constructor(publicKey, permissions, state, router, config, publicKeysApiService) {
        super(publicKey, permissions, state);
        this.router = router;
        this.config = config;
        this.publicKeysApiService = publicKeysApiService;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_5__["DatePipe"](this.config.locale);
    }
    getIcon() {
        return null;
    }
    getStatus() {
        return null;
    }
    getTitle() {
        switch (this.state) {
            case 'edit':
                return {
                    text: `Edit ${this.object.name}`,
                };
            case 'create':
                return {
                    text: `Create new ssh key`,
                };
            case 'details':
                return {
                    text: `${this.object.name}`,
                    subText: `Created at: ${this.datePipe.transform(this.object.created_at)}`,
                };
            default:
                return {
                    text: `${this.object.name}`,
                };
        }
    }
    getActions() {
        const actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_1__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            name: 'Edit',
            tooltip: 'Edit',
            routerUrl: this.config.getPanelUrl(`cloud/ssh-keys/${this.object.id}/edit`),
            router: this.router,
        }));
        actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_4__["ApiCallAction"]({
            object: this.object,
            icon: { name: 'delete' },
            name: 'Delete',
            tooltip: 'Delete',
            confirmOptions: {
                confirm: true,
                title: 'Delete ssh key',
                message: `Are you sure you want to delete ssh key ${this.object.name}`,
            },
            apiService: this.publicKeysApiService,
            callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_4__["CallType"].Delete,
        }));
        return actions;
    }
    getDetailsActions() {
        const actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_1__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`cloud/ssh-keys`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_6__["CallbackAction"]({ name: 'Generate new key' }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_6__["CallbackAction"]({ name: 'Save' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_1__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`cloud/ssh-keys`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_6__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    }
    getDetailsLink() {
        return this.config.getPanelUrl(`cloud/ssh-keys/${this.object.id}`);
    }
    getCardFields() {
        const fields = [
            {
                name: 'Created on',
                value: this.datePipe.transform(this.object.created_at)
            },
            {
                name: 'Fingerprint',
                value: this.object.fingerprint
            },
            {
                name: 'Owner',
                value: this.object.user.username,
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
                        component: _tabs_ssh_key_details_overview_ssh_key_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["SshKeyDetailsOverviewComponent"],
                    },
                ];
            case 'create':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_ssh_key_edit_form_ssh_key_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["SshKeyEditFormComponent"],
                    },
                ];
            case 'edit':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_ssh_key_edit_form_ssh_key_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["SshKeyEditFormComponent"],
                    },
                ];
        }
    }
    getCardTags() {
        return [];
    }
}
SshKeyUiService.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_public_key_public_key_api_service__WEBPACK_IMPORTED_MODULE_7__["PublicKeysApiService"] }
];


/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-keys-routing.module.ts":
/*!********************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-keys-routing.module.ts ***!
  \********************************************************************/
/*! exports provided: SshKeysRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SshKeysRoutingModule", function() { return SshKeysRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ssh_key_list_ssh_key_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./ssh-key-list/ssh-key-list.component */ "./src/app/reseller/cloud/ssh-keys/ssh-key-list/ssh-key-list.component.ts");
/* harmony import */ var _ssh_key_create_ssh_key_create_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./ssh-key-create/ssh-key-create.component */ "./src/app/reseller/cloud/ssh-keys/ssh-key-create/ssh-key-create.component.ts");
/* harmony import */ var _ssh_key_details_ssh_key_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./ssh-key-details/ssh-key-details.component */ "./src/app/reseller/cloud/ssh-keys/ssh-key-details/ssh-key-details.component.ts");
/* harmony import */ var _ssh_key_edit_ssh_key_edit_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./ssh-key-edit/ssh-key-edit.component */ "./src/app/reseller/cloud/ssh-keys/ssh-key-edit/ssh-key-edit.component.ts");
/* harmony import */ var _shared_fleio_api_public_key_public_key_list_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/public-key/public-key-list.resolver */ "./src/app/shared/fleio-api/public-key/public-key-list.resolver.ts");
/* harmony import */ var _shared_fleio_api_public_key_public_key_resolver__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/public-key/public-key.resolver */ "./src/app/shared/fleio-api/public-key/public-key.resolver.ts");
/* harmony import */ var _shared_fleio_api_public_key_public_key_permissions_resolver__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/fleio-api/public-key/public-key-permissions.resolver */ "./src/app/shared/fleio-api/public-key/public-key-permissions.resolver.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/ui-api/interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");












const routes = [
    {
        path: '',
        component: _ssh_key_list_ssh_key_list_component__WEBPACK_IMPORTED_MODULE_3__["SshKeyListComponent"],
        resolve: {
            sshKeys: _shared_fleio_api_public_key_public_key_list_resolver__WEBPACK_IMPORTED_MODULE_7__["PublicKeyListResolver"],
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_10__["AuthGuard"]],
        data: {
            config: {
                feature: 'openstack.sshkeys',
                search: {
                    show: true,
                    placeholder: 'Search ssh keys ...',
                },
                subheader: {
                    objectList(data) {
                        return data.sshKey;
                    },
                    objectName: 'ssh key',
                    objectNamePlural: 'ssh keys',
                },
                ordering: {
                    default: {
                        field: 'created_at',
                        display: 'Created at',
                        direction: _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__["OrderingDirection"].Descending
                    },
                    options: [
                        {
                            display: 'Name',
                            field: 'name',
                        },
                        {
                            display: 'Date created',
                            field: 'created_at',
                        }
                    ]
                }
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: 'create',
        component: _ssh_key_create_ssh_key_create_component__WEBPACK_IMPORTED_MODULE_4__["SshKeyCreateComponent"],
        resolve: {},
        data: {
            config: {
                getBreadCrumbDetail: () => {
                    return 'Create ssh key';
                },
            },
        }
    },
    {
        path: ':id',
        component: _ssh_key_details_ssh_key_details_component__WEBPACK_IMPORTED_MODULE_5__["SshKeyDetailsComponent"],
        resolve: {
            sshKey: _shared_fleio_api_public_key_public_key_resolver__WEBPACK_IMPORTED_MODULE_8__["PublicKeyResolver"],
            permissions: _shared_fleio_api_public_key_public_key_permissions_resolver__WEBPACK_IMPORTED_MODULE_9__["PublicKeyPermissionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.sshKey.name;
                },
            },
        }
    },
    {
        path: ':id/edit',
        component: _ssh_key_edit_ssh_key_edit_component__WEBPACK_IMPORTED_MODULE_6__["SshKeyEditComponent"],
        resolve: {
            sshKey: _shared_fleio_api_public_key_public_key_resolver__WEBPACK_IMPORTED_MODULE_8__["PublicKeyResolver"],
            permissions: _shared_fleio_api_public_key_public_key_permissions_resolver__WEBPACK_IMPORTED_MODULE_9__["PublicKeyPermissionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.sshKey.name;
                },
            },
        }
    },
];
let SshKeysRoutingModule = class SshKeysRoutingModule {
};
SshKeysRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], SshKeysRoutingModule);



/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/ssh-keys.module.ts":
/*!************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/ssh-keys.module.ts ***!
  \************************************************************/
/*! exports provided: SshKeysModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SshKeysModule", function() { return SshKeysModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _ssh_key_create_ssh_key_create_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./ssh-key-create/ssh-key-create.component */ "./src/app/reseller/cloud/ssh-keys/ssh-key-create/ssh-key-create.component.ts");
/* harmony import */ var _ssh_key_details_ssh_key_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./ssh-key-details/ssh-key-details.component */ "./src/app/reseller/cloud/ssh-keys/ssh-key-details/ssh-key-details.component.ts");
/* harmony import */ var _ssh_key_edit_ssh_key_edit_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./ssh-key-edit/ssh-key-edit.component */ "./src/app/reseller/cloud/ssh-keys/ssh-key-edit/ssh-key-edit.component.ts");
/* harmony import */ var _ssh_key_list_ssh_key_list_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./ssh-key-list/ssh-key-list.component */ "./src/app/reseller/cloud/ssh-keys/ssh-key-list/ssh-key-list.component.ts");
/* harmony import */ var _ssh_keys_routing_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./ssh-keys-routing.module */ "./src/app/reseller/cloud/ssh-keys/ssh-keys-routing.module.ts");
/* harmony import */ var _tabs_ssh_key_details_overview_ssh_key_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/ssh-key-details-overview/ssh-key-details-overview.component */ "./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-details-overview/ssh-key-details-overview.component.ts");
/* harmony import */ var _tabs_ssh_key_edit_form_ssh_key_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/ssh-key-edit-form/ssh-key-edit-form.component */ "./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-edit-form/ssh-key-edit-form.component.ts");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm2015/button.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");

















let SshKeysModule = class SshKeysModule {
};
SshKeysModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _ssh_key_create_ssh_key_create_component__WEBPACK_IMPORTED_MODULE_3__["SshKeyCreateComponent"],
            _ssh_key_details_ssh_key_details_component__WEBPACK_IMPORTED_MODULE_4__["SshKeyDetailsComponent"],
            _ssh_key_edit_ssh_key_edit_component__WEBPACK_IMPORTED_MODULE_5__["SshKeyEditComponent"],
            _ssh_key_list_ssh_key_list_component__WEBPACK_IMPORTED_MODULE_6__["SshKeyListComponent"],
            _tabs_ssh_key_details_overview_ssh_key_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["SshKeyDetailsOverviewComponent"],
            _tabs_ssh_key_edit_form_ssh_key_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["SshKeyEditFormComponent"]
        ],
        entryComponents: [
            _tabs_ssh_key_details_overview_ssh_key_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["SshKeyDetailsOverviewComponent"],
            _tabs_ssh_key_edit_form_ssh_key_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["SshKeyEditFormComponent"]
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _ssh_keys_routing_module__WEBPACK_IMPORTED_MODULE_7__["SshKeysRoutingModule"],
            _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_10__["ErrorHandlingModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_11__["ReactiveFormsModule"],
            _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_12__["ObjectsViewModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_13__["MatButtonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_14__["FlexModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_15__["MatFormFieldModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_16__["MatInputModule"],
        ]
    })
], SshKeysModule);



/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-details-overview/ssh-key-details-overview.component.scss":
/*!***************************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-details-overview/ssh-key-details-overview.component.scss ***!
  \***************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3NzaC1rZXlzL3RhYnMvc3NoLWtleS1kZXRhaWxzLW92ZXJ2aWV3L3NzaC1rZXktZGV0YWlscy1vdmVydmlldy5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-details-overview/ssh-key-details-overview.component.ts":
/*!*************************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-details-overview/ssh-key-details-overview.component.ts ***!
  \*************************************************************************************************************/
/*! exports provided: SshKeyDetailsOverviewComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SshKeyDetailsOverviewComponent", function() { return SshKeyDetailsOverviewComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");
/* harmony import */ var _shared_ui_api_clipboard_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/ui-api/clipboard.service */ "./src/app/shared/ui-api/clipboard.service.ts");




let SshKeyDetailsOverviewComponent = class SshKeyDetailsOverviewComponent extends _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"] {
    constructor(clipboard) {
        super();
        this.clipboard = clipboard;
    }
    ngOnInit() {
    }
};
SshKeyDetailsOverviewComponent.ctorParameters = () => [
    { type: _shared_ui_api_clipboard_service__WEBPACK_IMPORTED_MODULE_3__["ClipboardService"] }
];
SshKeyDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-ssh-key-details-overview',
        template: __webpack_require__(/*! raw-loader!./ssh-key-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-details-overview/ssh-key-details-overview.component.html"),
        styles: [__webpack_require__(/*! ./ssh-key-details-overview.component.scss */ "./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-details-overview/ssh-key-details-overview.component.scss")]
    })
], SshKeyDetailsOverviewComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-edit-form/ssh-key-edit-form.component.scss":
/*!*************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-edit-form/ssh-key-edit-form.component.scss ***!
  \*************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3NzaC1rZXlzL3RhYnMvc3NoLWtleS1lZGl0LWZvcm0vc3NoLWtleS1lZGl0LWZvcm0uY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-edit-form/ssh-key-edit-form.component.ts":
/*!***********************************************************************************************!*\
  !*** ./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-edit-form/ssh-key-edit-form.component.ts ***!
  \***********************************************************************************************/
/*! exports provided: SshKeyEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SshKeyEditFormComponent", function() { return SshKeyEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _shared_fleio_api_public_key_public_key_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../shared/fleio-api/public-key/public-key-api.service */ "./src/app/shared/fleio-api/public-key/public-key-api.service.ts");
/* harmony import */ var _shared_ui_api_clipboard_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../../../shared/ui-api/clipboard.service */ "./src/app/shared/ui-api/clipboard.service.ts");









let SshKeyEditFormComponent = class SshKeyEditFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"] {
    constructor(formBuilder, publicKeysApiService, router, config, clipboard) {
        super();
        this.formBuilder = formBuilder;
        this.publicKeysApiService = publicKeysApiService;
        this.router = router;
        this.config = config;
        this.clipboard = clipboard;
        this.sshKeyForm = this.formBuilder.group({
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            public_key: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            private_key: [''],
        });
    }
    ngOnInit() {
        this.objectController.actionCallback = (action) => this.keyActions(action);
        this.sshKeyForm.patchValue(this.object);
        if (!this.object.id) {
        }
    }
    keyActions(action) {
        if (action.name === 'Generate new key') {
            this.publicKeysApiService.getAction('get_generated_key_pair').subscribe(key => {
                this.generatedKey = key;
                this.sshKeyForm.patchValue(key);
            });
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_6__["of"])(null);
        }
        const value = this.sshKeyForm.value;
        this.createOrUpdate(this.publicKeysApiService, value).subscribe(() => {
            this.router.navigateByUrl(this.config.getPrevUrl('cloud/ssh-keys')).catch(() => {
            });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_6__["of"])(null);
    }
};
SshKeyEditFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
    { type: _shared_fleio_api_public_key_public_key_api_service__WEBPACK_IMPORTED_MODULE_7__["PublicKeysApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
    { type: _shared_ui_api_clipboard_service__WEBPACK_IMPORTED_MODULE_8__["ClipboardService"] }
];
SshKeyEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-ssh-key-edit-form',
        template: __webpack_require__(/*! raw-loader!./ssh-key-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-edit-form/ssh-key-edit-form.component.html"),
        styles: [__webpack_require__(/*! ./ssh-key-edit-form.component.scss */ "./src/app/reseller/cloud/ssh-keys/tabs/ssh-key-edit-form/ssh-key-edit-form.component.scss")]
    })
], SshKeyEditFormComponent);



/***/ }),

/***/ "./src/app/shared/fleio-api/public-key/public-key-api.service.ts":
/*!***********************************************************************!*\
  !*** ./src/app/shared/fleio-api/public-key/public-key-api.service.ts ***!
  \***********************************************************************/
/*! exports provided: PublicKeysApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PublicKeysApiService", function() { return PublicKeysApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../config/config.service */ "./src/app/shared/config/config.service.ts");





let PublicKeysApiService = class PublicKeysApiService extends _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"] {
    // noinspection JSUnusedGlobalSymbols
    constructor(httpClient, config) {
        super(config.getPanelApiUrl('pkm'));
        this.httpClient = httpClient;
        this.config = config;
    }
};
PublicKeysApiService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] }
];
PublicKeysApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PublicKeysApiService);



/***/ }),

/***/ "./src/app/shared/fleio-api/public-key/public-key-list.resolver.ts":
/*!*************************************************************************!*\
  !*** ./src/app/shared/fleio-api/public-key/public-key-list.resolver.ts ***!
  \*************************************************************************/
/*! exports provided: PublicKeyListResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PublicKeyListResolver", function() { return PublicKeyListResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _public_key_api_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./public-key-api.service */ "./src/app/shared/fleio-api/public-key/public-key-api.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");





let PublicKeyListResolver = class PublicKeyListResolver {
    constructor(publicKeysApiService) {
        this.publicKeysApiService = publicKeysApiService;
    }
    resolve(route, state) {
        return this.publicKeysApiService.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_3__["of"])(null)));
    }
};
PublicKeyListResolver.ctorParameters = () => [
    { type: _public_key_api_service__WEBPACK_IMPORTED_MODULE_2__["PublicKeysApiService"] }
];
PublicKeyListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PublicKeyListResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/public-key/public-key-permissions.resolver.ts":
/*!********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/public-key/public-key-permissions.resolver.ts ***!
  \********************************************************************************/
/*! exports provided: PublicKeyPermissionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PublicKeyPermissionsResolver", function() { return PublicKeyPermissionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _public_key_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./public-key-api.service */ "./src/app/shared/fleio-api/public-key/public-key-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");





let PublicKeyPermissionsResolver = class PublicKeyPermissionsResolver {
    constructor(publicKeysApiService) {
        this.publicKeysApiService = publicKeysApiService;
    }
    resolve(route, state) {
        return this.publicKeysApiService.permissions().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
PublicKeyPermissionsResolver.ctorParameters = () => [
    { type: _public_key_api_service__WEBPACK_IMPORTED_MODULE_3__["PublicKeysApiService"] }
];
PublicKeyPermissionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PublicKeyPermissionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/public-key/public-key.resolver.ts":
/*!********************************************************************!*\
  !*** ./src/app/shared/fleio-api/public-key/public-key.resolver.ts ***!
  \********************************************************************/
/*! exports provided: PublicKeyResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PublicKeyResolver", function() { return PublicKeyResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _public_key_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./public-key-api.service */ "./src/app/shared/fleio-api/public-key/public-key-api.service.ts");





let PublicKeyResolver = class PublicKeyResolver {
    constructor(publicKeysApiService) {
        this.publicKeysApiService = publicKeysApiService;
    }
    resolve(route, state) {
        return this.publicKeysApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
PublicKeyResolver.ctorParameters = () => [
    { type: _public_key_api_service__WEBPACK_IMPORTED_MODULE_4__["PublicKeysApiService"] }
];
PublicKeyResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PublicKeyResolver);



/***/ }),

/***/ "./src/app/shared/ui-api/clipboard.service.ts":
/*!****************************************************!*\
  !*** ./src/app/shared/ui-api/clipboard.service.ts ***!
  \****************************************************/
/*! exports provided: ClipboardService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ClipboardService", function() { return ClipboardService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let ClipboardService = class ClipboardService {
    constructor() {
    }
    copyTextToClipboard(text) {
        const tempTextArea = document.createElement('textarea');
        tempTextArea.style.position = 'fixed';
        tempTextArea.style.left = '0';
        tempTextArea.style.top = '0';
        tempTextArea.style.opacity = '0';
        tempTextArea.value = text;
        document.body.appendChild(tempTextArea);
        tempTextArea.focus();
        tempTextArea.select();
        document.execCommand('copy');
        document.body.removeChild(tempTextArea);
    }
    copyTextAreaToClipboard(textArea) {
        textArea.focus();
        textArea.select();
        document.execCommand('copy');
        textArea.setSelectionRange(0, 0);
        document.body.removeChild(textArea);
    }
};
ClipboardService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ClipboardService);



/***/ })

}]);
//# sourceMappingURL=ssh-keys-ssh-keys-module-es2015.js.map