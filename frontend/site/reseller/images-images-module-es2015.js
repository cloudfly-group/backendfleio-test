(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["images-images-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-create/image-create.component.html":
/*!**********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/images/image-create/image-create.component.html ***!
  \**********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-lg']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-details/image-details.component.html":
/*!************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/images/image-details/image-details.component.html ***!
  \************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\"></app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-edit/image-edit.component.html":
/*!******************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/images/image-edit/image-edit.component.html ***!
  \******************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-lg']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-list/image-list.component.html":
/*!******************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/images/image-list/image-list.component.html ***!
  \******************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-objects-view [objectsListController]=\"objectListController\"></app-objects-view>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.html":
/*!***********************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.html ***!
  \***********************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxLayout=\"row\">\n  <div fxLayout=\"column\" fxFlex=\"50\">\n    <p class=\"fl-detail\">ID: {{object.id}}</p>\n    <p class=\"fl-detail\">Size: {{object.size / (1024 * 1024 * 1024)}} GB</p>\n    <p class=\"fl-detail\">Minimum memory: {{object.min_ram}} MB</p>\n    <p class=\"fl-detail\">Minimum disk size: {{object.min_disk}} GB</p>\n    <p class=\"fl-detail\">Created at: {{object.created_at | date}}</p>\n    <p class=\"fl-detail\">Updated at: {{object.updated_at | date}}</p>\n    <p class=\"fl-detail\">Architecture: {{object.architecture}}</p>\n    <p class=\"fl-detail\">Container format: {{object.container_format}}</p>\n    <p class=\"fl-detail\">Disk format: {{object.disk_format}}</p>\n    <p class=\"fl-detail\">OS distro: {{object.os_distro}}</p>\n    <p class=\"fl-detail\">Hypervisor type: {{object.hypervisor_type}}</p>\n    <p class=\"fl-detail\">OS version: {{object.os_version}}</p>\n    <p class=\"fl-detail\">Status: {{object.status}}</p>\n    <p class=\"fl-detail\">Visibility: {{object.visibility}}</p>\n  </div>\n  <div fxLayout=\"column\" fxFlex=\"50\" class=\"wrap-text-content\">\n    <p class=\"fl-detail\">Properties:</p>\n    <div fxLayout=\"row\" *ngFor=\"let property of object.properties | keyvalue\" class=\"property-row\">\n      <p fxFlex=\"50\" class=\"fl-detail\">{{property.key}}:</p>\n      <p fxFlex=\"50\" class=\"fl-detail\">{{property.value}}</p>\n    </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.html":
/*!*********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.html ***!
  \*********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form [formGroup]=\"imageForm\">\n  <app-form-errors #formErrors [formGroup]=\"imageForm\"></app-form-errors>\n  <div fxLayout=\"row\" fxLayoutGap=\"10px\">\n    <div fxLayout=\"column\" fxFlex=\"50\">\n      <mat-form-field *ngIf=\"!object.id\">\n        <mat-select formControlName=\"region\" placeholder=\"Region\">\n          <mat-option *ngFor=\"let region of createOptions.regions\"\n                      [value]=\"region.id\">\n            {{region.id}}\n          </mat-option>\n        </mat-select>\n      </mat-form-field>\n      <mat-form-field>\n        <input matInput placeholder=\"Image name\" type=\"text\" formControlName=\"name\" required>\n        <mat-error>{{backendErrors['name'] || 'Field is required' }}</mat-error>\n      </mat-form-field>\n      <div fxLayout=\"row\" fxLayoutGap=\"10px\">\n        <mat-form-field fxFlex=\"50\">\n          <input matInput placeholder=\"Minimum disk size (GB)\" type=\"number\"\n                 formControlName=\"min_disk\" required>\n          <mat-error>{{backendErrors['min_disk'] || 'This field is required!' }}</mat-error>\n        </mat-form-field>\n        <mat-form-field fxFlex=\"50\">\n          <input matInput placeholder=\"Minimum required RAM (MB)\" type=\"number\"\n                 formControlName=\"min_ram\" required>\n          <mat-error>{{backendErrors['min_ram'] || 'This field is required!' }}</mat-error>\n        </mat-form-field>\n      </div>\n      <mat-form-field>\n        <mat-select formControlName=\"disk_format\" placeholder=\"Disk format\">\n          <mat-option *ngFor=\"let diskFormat of createOptions.disk_formats\"\n                      [value]=\"diskFormat\">\n            {{diskFormat}}\n          </mat-option>\n        </mat-select>\n      </mat-form-field>\n      <div fxLayout=\"row\" fxLayoutGap=\"10px\">\n        <mat-form-field fxFlex=\"33\">\n          <mat-select formControlName=\"os_distro\" placeholder=\"OS distro\">\n            <mat-option *ngFor=\"let osDistro of createOptions.os_distros\"\n                        [value]=\"osDistro\">\n              {{osDistro}}\n            </mat-option>\n          </mat-select>\n        </mat-form-field>\n        <mat-form-field fxFlex=\"33\">\n          <input matInput placeholder=\"OS version\" type=\"text\" formControlName=\"os_version\">\n          <mat-error>{{backendErrors['os_version']}}</mat-error>\n        </mat-form-field>\n        <mat-form-field fxFlex=\"33\">\n          <input matInput placeholder=\"Architecture\" type=\"text\" formControlName=\"architecture\" required>\n          <mat-error>{{backendErrors['architecture'] || 'Field is required' }}</mat-error>\n        </mat-form-field>\n      </div>\n      <mat-form-field>\n        <mat-select formControlName=\"hypervisor_type\" placeholder=\"Hypervisor type\">\n          <mat-option [value]=\"''\" selected=\"true\">Any hypervisor</mat-option>\n          <mat-option *ngFor=\"let hypervisorType of createOptions.hypervisor_types\"\n                      [value]=\"hypervisorType\">\n            {{hypervisorType}}\n          </mat-option>\n        </mat-select>\n      </mat-form-field>\n      <mat-form-field>\n        <mat-select formControlName=\"visibility\" placeholder=\"Visibility\">\n          <mat-option *ngFor=\"let visibility of createOptions.visibilities\"\n                      [value]=\"visibility\">\n            {{visibility}}\n          </mat-option>\n        </mat-select>\n      </mat-form-field>\n      <mat-checkbox formControlName=\"protected\" color=\"primary\">\n        Protected\n      </mat-checkbox>\n      <div fxLayout=\"row\" fxLayoutAlign=\"center\" *ngIf=\"!object.id\">\n        <mat-form-field fxFlex=\"20\">\n          <mat-select formControlName=\"source\" placeholder=\"Source\">\n            <mat-option value=\"url\">URL</mat-option>\n            <mat-option value=\"file\">File</mat-option>\n          </mat-select>\n        </mat-form-field>\n        <mat-form-field fxFlex=\"auto\" *ngIf=\"imageForm.controls.source.value === 'url'\">\n          <input matInput placeholder=\"URL\" type=\"text\" formControlName=\"url\" required>\n          <mat-error>{{backendErrors['url'] || 'This field is required!' }}</mat-error>\n        </mat-form-field>\n        <mat-form-field fxFlex=\"auto\" *ngIf=\"imageForm.controls.source.value === 'file'\">\n          <input #fileInput type=\"file\" (change)=\"fileChanged($event)\" required>\n          <input matInput type=\"text\" formControlName=\"file\" required hidden>\n          <mat-error>{{backendErrors['file'] || 'This field is required!' }}</mat-error>\n        </mat-form-field>\n      </div>\n    </div>\n    <div fxLayout=\"column\" fxFlex=\"50\">\n      <p>\n        <strong>Image name</strong><br>\n        Set an image display name that will reflect what the image contains, like it's operating system\n        or snapshot of an instance.\n      </p>\n      <p>\n        <strong>Minimum disk size (GB)</strong><br>\n        This property will tell OpenStack Compute what the minimum required disk size is for this image.\n        <br>\n        This allows you to set a limit in order to avoid potential problems while creating an Instance with\n        a lower disk size than the installed software on that image.\n      </p>\n      <p>\n        <strong>Minimum required RAM (MB)</strong><br>\n        Like the minimum required disk size, this option allows you to set a limit for the minimum required\n        RAM an instance created from this image will required in order to run properly.\n      </p>\n      <p>\n        <strong>Visibility</strong><br>\n        An image can be set as <strong>private</strong>, making it only available to it's owner, or\n        <strong>public</strong>, making it available to everyone. You can also set an image visibility to\n        <strong>shared</strong> to allow only image members to access this image. The\n        <strong>community</strong>\n        visibility behaves similar to <strong>public</strong>\n      </p>\n      <p>\n        <strong>OS distro, OS version and Architecture</strong><br>\n        These special attributes allows Fleio to show the distro icon next to each instance created from\n        this image\n        and allows OpenStack to properly create an Instance especially for Windows or other non Linux\n        distributions.\n      </p>\n      <p>\n        <strong>Protected</strong><br>\n        Set this option in order to protect the image from accidental deletion\n      </p>\n    </div>\n  </div>\n  <mat-progress-bar *ngIf=\"uploading\" color=\"primary\" mode=\"determinate\" value=\"{{uploadProgress}}\">\n  </mat-progress-bar>\n</form>\n"

/***/ }),

/***/ "./src/app/reseller/cloud/images/image-create/image-create.component.scss":
/*!********************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/image-create/image-create.component.scss ***!
  \********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ltYWdlcy9pbWFnZS1jcmVhdGUvaW1hZ2UtY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/cloud/images/image-create/image-create.component.ts":
/*!******************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/image-create/image-create.component.ts ***!
  \******************************************************************************/
/*! exports provided: ImageCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageCreateComponent", function() { return ImageCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../image-list-ui.service */ "./src/app/reseller/cloud/images/image-list-ui.service.ts");





let ImageCreateComponent = class ImageCreateComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, imageListUIService) {
        super(route, imageListUIService, 'create', null);
    }
};
ImageCreateComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ImageListUIService"] }
];
ImageCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-image-create',
        template: __webpack_require__(/*! raw-loader!./image-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-create/image-create.component.html"),
        styles: [__webpack_require__(/*! ./image-create.component.scss */ "./src/app/reseller/cloud/images/image-create/image-create.component.scss")]
    })
], ImageCreateComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/images/image-details/image-details.component.scss":
/*!**********************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/image-details/image-details.component.scss ***!
  \**********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ltYWdlcy9pbWFnZS1kZXRhaWxzL2ltYWdlLWRldGFpbHMuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/images/image-details/image-details.component.ts":
/*!********************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/image-details/image-details.component.ts ***!
  \********************************************************************************/
/*! exports provided: ImageDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageDetailsComponent", function() { return ImageDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../image-list-ui.service */ "./src/app/reseller/cloud/images/image-list-ui.service.ts");





let ImageDetailsComponent = class ImageDetailsComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, imageListUIService) {
        super(route, imageListUIService, 'details', 'image');
    }
};
ImageDetailsComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ImageListUIService"] }
];
ImageDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-image-details',
        template: __webpack_require__(/*! raw-loader!./image-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-details/image-details.component.html"),
        styles: [__webpack_require__(/*! ./image-details.component.scss */ "./src/app/reseller/cloud/images/image-details/image-details.component.scss")]
    })
], ImageDetailsComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/images/image-edit/image-edit.component.scss":
/*!****************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/image-edit/image-edit.component.scss ***!
  \****************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ltYWdlcy9pbWFnZS1lZGl0L2ltYWdlLWVkaXQuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/images/image-edit/image-edit.component.ts":
/*!**************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/image-edit/image-edit.component.ts ***!
  \**************************************************************************/
/*! exports provided: ImageEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageEditComponent", function() { return ImageEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../image-list-ui.service */ "./src/app/reseller/cloud/images/image-list-ui.service.ts");





let ImageEditComponent = class ImageEditComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, imageListUIService) {
        super(route, imageListUIService, 'edit', 'image');
    }
};
ImageEditComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ImageListUIService"] }
];
ImageEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-image-edit',
        template: __webpack_require__(/*! raw-loader!./image-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-edit/image-edit.component.html"),
        styles: [__webpack_require__(/*! ./image-edit.component.scss */ "./src/app/reseller/cloud/images/image-edit/image-edit.component.scss")]
    })
], ImageEditComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/images/image-list-ui.service.ts":
/*!****************************************************************!*\
  !*** ./src/app/reseller/cloud/images/image-list-ui.service.ts ***!
  \****************************************************************/
/*! exports provided: ImageListUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageListUIService", function() { return ImageListUIService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/image/image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");
/* harmony import */ var _image_ui_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./image-ui.service */ "./src/app/reseller/cloud/images/image-ui.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");









let ImageListUIService = class ImageListUIService {
    constructor(router, config, imagesApiService) {
        this.router = router;
        this.config = config;
        this.imagesApiService = imagesApiService;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_8__["DatePipe"](this.config.locale);
    }
    getObjectUIService(object, permissions, state) {
        return new _image_ui_service__WEBPACK_IMPORTED_MODULE_7__["ImageUiService"](object, permissions, state, this.router, this.config, this.imagesApiService);
    }
    getTableData(objectList) {
        const tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Image, displayName: 'Image', enableSort: false, fieldName: '(image)' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Name', enableSort: true, fieldName: 'name' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Status', enableSort: true, fieldName: 'status' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Is protected', enableSort: false, fieldName: 'is_protected' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Region', enableSort: false, fieldName: 'region' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Created at', enableSort: true, fieldName: 'created_at' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Min disk', enableSort: false, fieldName: 'min_disk' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Actions, displayName: 'Actions', enableSort: false, fieldName: '(actions)' },
                ],
                columnNames: [
                    '(image)', 'name', 'status', 'is_protected', 'region', 'created_at', 'min_disk', '(actions)'
                ],
                statusColumn: '(image)',
            },
            rows: [],
        };
        for (const image of objectList.objects) {
            const rowUIService = this.getObjectUIService(image, objectList.permissions, 'table-view');
            const row = {
                cells: {
                    name: { text: image.name || image.id },
                    status: { text: image.status ? image.status.toLocaleUpperCase() : 'n/a' },
                    is_protected: { text: image.protected ? 'protected' : '' },
                    region: { text: image.region },
                    created_at: { text: this.datePipe.transform(image.created_at) },
                    min_disk: { text: `${image.min_disk} GB` },
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
                name: 'Create new image',
                tooltip: 'Create new image',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('cloud/images/create')
            })
        ];
    }
};
ImageListUIService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_6__["ImagesApiService"] }
];
ImageListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ImageListUIService);



/***/ }),

/***/ "./src/app/reseller/cloud/images/image-list/image-list.component.scss":
/*!****************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/image-list/image-list.component.scss ***!
  \****************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ltYWdlcy9pbWFnZS1saXN0L2ltYWdlLWxpc3QuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/images/image-list/image-list.component.ts":
/*!**************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/image-list/image-list.component.ts ***!
  \**************************************************************************/
/*! exports provided: ImageListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageListComponent", function() { return ImageListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _image_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../image-list-ui.service */ "./src/app/reseller/cloud/images/image-list-ui.service.ts");






let ImageListComponent = class ImageListComponent extends _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"] {
    constructor(route, imageListUIService, refreshService) {
        super(route, imageListUIService, refreshService, 'images');
        this.route = route;
        this.imageListUIService = imageListUIService;
        this.refreshService = refreshService;
    }
    ngOnInit() {
        super.ngOnInit();
    }
};
ImageListComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _image_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["ImageListUIService"] },
    { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
];
ImageListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-image-list',
        template: __webpack_require__(/*! raw-loader!./image-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-list/image-list.component.html"),
        styles: [__webpack_require__(/*! ./image-list.component.scss */ "./src/app/reseller/cloud/images/image-list/image-list.component.scss")]
    })
], ImageListComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/images/image-ui.service.ts":
/*!***********************************************************!*\
  !*** ./src/app/reseller/cloud/images/image-ui.service.ts ***!
  \***********************************************************/
/*! exports provided: ImageUiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageUiService", function() { return ImageUiService; });
/* harmony import */ var _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/object-status */ "./src/app/shared/ui/objects-view/interfaces/object-status.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/image/image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");
/* harmony import */ var _tabs_image_details_overview_image_details_overview_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/image-details-overview/image-details-overview.component */ "./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.ts");
/* harmony import */ var _tabs_image_edit_form_image_edit_form_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/image-edit-form/image-edit-form.component */ "./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.ts");











class ImageUiService extends _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__["ObjectUIServiceBase"] {
    constructor(image, permissions, state, router, config, imagesApiService) {
        super(image, permissions, state);
        this.router = router;
        this.config = config;
        this.imagesApiService = imagesApiService;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_6__["DatePipe"](this.config.locale);
    }
    getIcon() {
        return {
            class: 'fl-icons',
            name: this.object.os_distro || 'otheros',
        };
    }
    getStatus() {
        switch (this.object.status) {
            case 'deactivated':
                return {
                    type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined,
                    value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Deactivated,
                };
            case 'active':
            default:
                return {
                    type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusType"].Defined,
                    value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_0__["StatusValue"].Active,
                };
        }
    }
    getTitle() {
        let prefix = '';
        if (this.object.type === 'snapshot') {
            prefix = 'snapshot';
        }
        if (this.object.disk_format === 'iso') {
            prefix = 'ISO';
        }
        if (prefix.length > 0) {
            prefix = `[${prefix}] `;
        }
        switch (this.state) {
            case 'edit':
                return {
                    text: `Edit ${this.object.name || this.object.id}`,
                    subText: this.object.status ? this.object.status.toLocaleUpperCase() : 'n/a',
                };
            case 'create':
                return {
                    text: `Create new image`,
                };
            case 'details':
            default:
                return {
                    text: `${prefix}${this.object.name || this.object.id}`,
                    subText: this.object.status ? this.object.status.toLocaleUpperCase() : 'n/a',
                };
        }
    }
    getActions() {
        const actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            name: 'Edit',
            tooltip: 'Edit image',
            routerUrl: this.config.getPanelUrl(`cloud/images/${this.object.id}/edit`),
            router: this.router,
        }));
        actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["ApiCallAction"]({
            object: this.object,
            icon: { name: 'delete' },
            name: 'Delete',
            tooltip: 'Delete image',
            confirmOptions: {
                confirm: true,
                title: 'Delete image',
                message: `Are you sure you want to delete image ${this.object.name}`,
            },
            apiService: this.imagesApiService,
            callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["CallType"].Delete,
        }));
        return actions;
    }
    getDetailsActions() {
        const actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`cloud/images`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`cloud/images`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    }
    getDetailsLink() {
        return this.config.getPanelUrl(`cloud/images/${this.object.id}`);
    }
    getCardFields() {
        const fields = [
            {
                value: `${this.object.min_disk} GB min. disk, ${this.object.region}`
            },
            {
                name: 'Created:',
                value: this.datePipe.transform(this.object.created_at),
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
                        component: _tabs_image_details_overview_image_details_overview_component__WEBPACK_IMPORTED_MODULE_9__["ImageDetailsOverviewComponent"],
                    },
                ];
            case 'create':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_image_edit_form_image_edit_form_component__WEBPACK_IMPORTED_MODULE_10__["ImageEditFormComponent"],
                    },
                ];
            case 'edit':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_image_edit_form_image_edit_form_component__WEBPACK_IMPORTED_MODULE_10__["ImageEditFormComponent"],
                    },
                ];
        }
    }
    getCardTags() {
        const tags = [];
        if (this.object.protected) {
            tags.push('protected');
        }
        return tags;
    }
}
ImageUiService.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] },
    { type: _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_8__["ImagesApiService"] }
];


/***/ }),

/***/ "./src/app/reseller/cloud/images/images-routing.module.ts":
/*!****************************************************************!*\
  !*** ./src/app/reseller/cloud/images/images-routing.module.ts ***!
  \****************************************************************/
/*! exports provided: ImagesRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImagesRoutingModule", function() { return ImagesRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _image_create_image_create_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./image-create/image-create.component */ "./src/app/reseller/cloud/images/image-create/image-create.component.ts");
/* harmony import */ var _image_edit_image_edit_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-edit/image-edit.component */ "./src/app/reseller/cloud/images/image-edit/image-edit.component.ts");
/* harmony import */ var _image_details_image_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./image-details/image-details.component */ "./src/app/reseller/cloud/images/image-details/image-details.component.ts");
/* harmony import */ var _image_list_image_list_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./image-list/image-list.component */ "./src/app/reseller/cloud/images/image-list/image-list.component.ts");
/* harmony import */ var _shared_fleio_api_cloud_image_image_list_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/image/image-list.resolver */ "./src/app/shared/fleio-api/cloud/image/image-list.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_image_image_resolver__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/image/image.resolver */ "./src/app/shared/fleio-api/cloud/image/image.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_image_image_permissions_resolver__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/image/image-permissions.resolver */ "./src/app/shared/fleio-api/cloud/image/image-permissions.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_image_image_create_options_resolver__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/image/image-create-options.resolver */ "./src/app/shared/fleio-api/cloud/image/image-create-options.resolver.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/ui-api/interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");













const routes = [
    {
        path: '',
        component: _image_list_image_list_component__WEBPACK_IMPORTED_MODULE_6__["ImageListComponent"],
        resolve: {
            images: _shared_fleio_api_cloud_image_image_list_resolver__WEBPACK_IMPORTED_MODULE_7__["ImageListResolver"],
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_12__["AuthGuard"]],
        data: {
            config: {
                feature: 'openstack.images',
                search: {
                    show: true,
                    placeholder: 'Search images ...',
                },
                subheader: {
                    objectList(data) {
                        return data.images;
                    },
                    objectName: 'image',
                    objectNamePlural: 'images'
                },
                ordering: {
                    default: {
                        display: 'Created at',
                        field: 'created_at',
                        direction: _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__["OrderingDirection"].Descending,
                    },
                    options: [
                        { display: 'Name', field: 'name' },
                        { display: 'Status', field: 'status' },
                        { display: 'Type', field: 'type' },
                        { display: 'Created at', field: 'created_at' },
                    ]
                }
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: 'create',
        component: _image_create_image_create_component__WEBPACK_IMPORTED_MODULE_3__["ImageCreateComponent"],
        resolve: {
            createOptions: _shared_fleio_api_cloud_image_image_create_options_resolver__WEBPACK_IMPORTED_MODULE_10__["ImageCreateOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: () => {
                    return 'Create image';
                },
            },
        }
    },
    {
        path: ':id',
        component: _image_details_image_details_component__WEBPACK_IMPORTED_MODULE_5__["ImageDetailsComponent"],
        resolve: {
            image: _shared_fleio_api_cloud_image_image_resolver__WEBPACK_IMPORTED_MODULE_8__["ImageResolver"],
            permissions: _shared_fleio_api_cloud_image_image_permissions_resolver__WEBPACK_IMPORTED_MODULE_9__["ImagePermissionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.image.name || data.image.id;
                },
            },
        }
    },
    {
        path: ':id/edit',
        component: _image_edit_image_edit_component__WEBPACK_IMPORTED_MODULE_4__["ImageEditComponent"],
        resolve: {
            image: _shared_fleio_api_cloud_image_image_resolver__WEBPACK_IMPORTED_MODULE_8__["ImageResolver"],
            createOptions: _shared_fleio_api_cloud_image_image_create_options_resolver__WEBPACK_IMPORTED_MODULE_10__["ImageCreateOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return data.image.name || data.image.id;
                },
            },
        }
    },
];
let ImagesRoutingModule = class ImagesRoutingModule {
};
ImagesRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], ImagesRoutingModule);



/***/ }),

/***/ "./src/app/reseller/cloud/images/images.module.ts":
/*!********************************************************!*\
  !*** ./src/app/reseller/cloud/images/images.module.ts ***!
  \********************************************************/
/*! exports provided: ImagesModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImagesModule", function() { return ImagesModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _image_create_image_create_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./image-create/image-create.component */ "./src/app/reseller/cloud/images/image-create/image-create.component.ts");
/* harmony import */ var _image_details_image_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-details/image-details.component */ "./src/app/reseller/cloud/images/image-details/image-details.component.ts");
/* harmony import */ var _image_edit_image_edit_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./image-edit/image-edit.component */ "./src/app/reseller/cloud/images/image-edit/image-edit.component.ts");
/* harmony import */ var _image_list_image_list_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./image-list/image-list.component */ "./src/app/reseller/cloud/images/image-list/image-list.component.ts");
/* harmony import */ var _images_routing_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./images-routing.module */ "./src/app/reseller/cloud/images/images-routing.module.ts");
/* harmony import */ var _tabs_image_details_overview_image_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/image-details-overview/image-details-overview.component */ "./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.ts");
/* harmony import */ var _tabs_image_edit_form_image_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/image-edit-form/image-edit-form.component */ "./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm2015/select.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm2015/checkbox.js");
/* harmony import */ var _angular_material_progress_bar__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/progress-bar */ "./node_modules/@angular/material/esm2015/progress-bar.js");



















let ImagesModule = class ImagesModule {
};
ImagesModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _image_create_image_create_component__WEBPACK_IMPORTED_MODULE_3__["ImageCreateComponent"],
            _image_details_image_details_component__WEBPACK_IMPORTED_MODULE_4__["ImageDetailsComponent"],
            _image_edit_image_edit_component__WEBPACK_IMPORTED_MODULE_5__["ImageEditComponent"],
            _image_list_image_list_component__WEBPACK_IMPORTED_MODULE_6__["ImageListComponent"],
            _tabs_image_details_overview_image_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["ImageDetailsOverviewComponent"],
            _tabs_image_edit_form_image_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["ImageEditFormComponent"],
        ],
        entryComponents: [
            _tabs_image_details_overview_image_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["ImageDetailsOverviewComponent"],
            _tabs_image_edit_form_image_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["ImageEditFormComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _images_routing_module__WEBPACK_IMPORTED_MODULE_7__["ImagesRoutingModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_10__["ReactiveFormsModule"],
            _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__["ErrorHandlingModule"],
            _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_12__["ObjectsViewModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_13__["FlexLayoutModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_14__["MatFormFieldModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_15__["MatInputModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_16__["MatSelectModule"],
            _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_17__["MatCheckboxModule"],
            _angular_material_progress_bar__WEBPACK_IMPORTED_MODULE_18__["MatProgressBarModule"],
        ]
    })
], ImagesModule);



/***/ }),

/***/ "./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.scss":
/*!*********************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.scss ***!
  \*********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".property-row {\n  padding: 0 5px;\n}\n\n.property-row:hover {\n  background: rgba(0, 0, 0, 0.05);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ltYWdlcy90YWJzL2ltYWdlLWRldGFpbHMtb3ZlcnZpZXcvaW1hZ2UtZGV0YWlscy1vdmVydmlldy5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvcmVzZWxsZXIvY2xvdWQvaW1hZ2VzL3RhYnMvaW1hZ2UtZGV0YWlscy1vdmVydmlldy9pbWFnZS1kZXRhaWxzLW92ZXJ2aWV3LmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsY0FBQTtBQ0NGOztBREVBO0VBQ0UsK0JBQUE7QUNDRiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ltYWdlcy90YWJzL2ltYWdlLWRldGFpbHMtb3ZlcnZpZXcvaW1hZ2UtZGV0YWlscy1vdmVydmlldy5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5wcm9wZXJ0eS1yb3cge1xuICBwYWRkaW5nOiAwIDVweDtcbn1cblxuLnByb3BlcnR5LXJvdzpob3ZlciB7XG4gIGJhY2tncm91bmQ6IHJnYmEoMCwgMCwgMCwgLjA1KTtcbn1cbiIsIi5wcm9wZXJ0eS1yb3cge1xuICBwYWRkaW5nOiAwIDVweDtcbn1cblxuLnByb3BlcnR5LXJvdzpob3ZlciB7XG4gIGJhY2tncm91bmQ6IHJnYmEoMCwgMCwgMCwgMC4wNSk7XG59Il19 */"

/***/ }),

/***/ "./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.ts":
/*!*******************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.ts ***!
  \*******************************************************************************************************/
/*! exports provided: ImageDetailsOverviewComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageDetailsOverviewComponent", function() { return ImageDetailsOverviewComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");



let ImageDetailsOverviewComponent = class ImageDetailsOverviewComponent extends _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"] {
    constructor() {
        super();
    }
    ngOnInit() {
    }
};
ImageDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-image-details-overview',
        template: __webpack_require__(/*! raw-loader!./image-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.html"),
        styles: [__webpack_require__(/*! ./image-details-overview.component.scss */ "./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.scss")]
    })
], ImageDetailsOverviewComponent);



/***/ }),

/***/ "./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.scss":
/*!*******************************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.scss ***!
  \*******************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL2ltYWdlcy90YWJzL2ltYWdlLWVkaXQtZm9ybS9pbWFnZS1lZGl0LWZvcm0uY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.ts":
/*!*****************************************************************************************!*\
  !*** ./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.ts ***!
  \*****************************************************************************************/
/*! exports provided: ImageEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageEditFormComponent", function() { return ImageEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/image/image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");









let ImageEditFormComponent = class ImageEditFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"] {
    constructor(formBuilder, imagesApi, router, config, activatedRoute) {
        super();
        this.formBuilder = formBuilder;
        this.imagesApi = imagesApi;
        this.router = router;
        this.config = config;
        this.activatedRoute = activatedRoute;
        this.imageForm = this.formBuilder.group({
            region: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            min_disk: [0, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            min_ram: [0, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            disk_format: ['qcow2', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            os_distro: [''],
            os_version: [''],
            architecture: ['x86_64', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            hypervisor_type: [''],
            visibility: ['private', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            protected: [false],
            source: ['url', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            url: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            file: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
        });
        this.uploading = false;
        this.uploadProgress = 7;
    }
    ngOnInit() {
        this.createOptions = this.activatedRoute.snapshot.data.createOptions;
        this.objectController.actionCallback = () => this.saveImage();
        this.imageForm.patchValue(this.object);
        if (!this.object.id) {
            // creating new flavor
            this.imageForm.controls.region.setValue(this.createOptions.selected_region);
            this.imageForm.controls.file.disable();
            this.imageForm.controls.source.valueChanges.subscribe((newValue) => {
                if (newValue === 'url') {
                    this.imageForm.controls.file.disable();
                    this.imageForm.controls.url.enable();
                }
                else {
                    this.imageForm.controls.file.enable();
                    this.imageForm.controls.url.disable();
                }
            });
        }
        else {
            this.imageForm.controls.source.disable();
            this.imageForm.controls.url.disable();
            this.imageForm.controls.file.disable();
        }
    }
    fileChanged($event) {
        const files = $event.target.files;
        this.imageFile = files.length > 0 ? files[0] : null;
        this.imageForm.controls.file.setValue(this.imageFile.name);
    }
    saveImage() {
        const imageData = this.imageForm.value;
        let formData;
        if (imageData.source === 'file' && this.imageFile) {
            imageData.file = this.imageFile;
            formData = new FormData();
            Object.keys(imageData).map(fieldName => {
                formData.append(fieldName, imageData[fieldName]);
            });
            formData.append('file', this.imageFile, this.imageFile.name);
        }
        const response = this.createOrUpdate(this.imagesApi, formData ? formData : imageData);
        if (response !== rxjs__WEBPACK_IMPORTED_MODULE_4__["EMPTY"]) {
            this.uploading = !!formData;
            response.subscribe((data) => {
                let requestCompleted = false;
                if (formData) {
                    const event = data;
                    if (event.type === _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpEventType"].UploadProgress) {
                        this.uploadProgress = event.loaded / event.total * 100;
                    }
                    if (event.type === _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpEventType"].Response) {
                        requestCompleted = true;
                    }
                }
                else {
                    requestCompleted = true;
                }
                if (requestCompleted) {
                    this.uploading = false;
                    this.router.navigateByUrl(this.config.getPrevUrl('cloud/images')).catch(() => {
                    });
                }
            });
        }
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["of"])(null);
    }
};
ImageEditFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
    { type: _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_5__["ImagesApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_7__["ConfigService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["ActivatedRoute"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('fileInput', { static: false })
], ImageEditFormComponent.prototype, "fileInput", void 0);
ImageEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-image-edit-form',
        template: __webpack_require__(/*! raw-loader!./image-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.html"),
        styles: [__webpack_require__(/*! ./image-edit-form.component.scss */ "./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.scss")]
    })
], ImageEditFormComponent);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/image/image-create-options.resolver.ts":
/*!*******************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/image/image-create-options.resolver.ts ***!
  \*******************************************************************************/
/*! exports provided: ImageCreateOptionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageCreateOptionsResolver", function() { return ImageCreateOptionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _image_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");





let ImageCreateOptionsResolver = class ImageCreateOptionsResolver {
    constructor(imagesApiService) {
        this.imagesApiService = imagesApiService;
    }
    resolve(route, state) {
        return this.imagesApiService.createOptions()
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
ImageCreateOptionsResolver.ctorParameters = () => [
    { type: _image_api_service__WEBPACK_IMPORTED_MODULE_4__["ImagesApiService"] }
];
ImageCreateOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ImageCreateOptionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/image/image-list.resolver.ts":
/*!*********************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/image/image-list.resolver.ts ***!
  \*********************************************************************/
/*! exports provided: ImageListResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageListResolver", function() { return ImageListResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _image_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");





let ImageListResolver = class ImageListResolver {
    constructor(imagesApiService) {
        this.imagesApiService = imagesApiService;
    }
    resolve(route, state) {
        return this.imagesApiService.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
ImageListResolver.ctorParameters = () => [
    { type: _image_api_service__WEBPACK_IMPORTED_MODULE_4__["ImagesApiService"] }
];
ImageListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ImageListResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/image/image-permissions.resolver.ts":
/*!****************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/image/image-permissions.resolver.ts ***!
  \****************************************************************************/
/*! exports provided: ImagePermissionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImagePermissionsResolver", function() { return ImagePermissionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _image_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");





let ImagePermissionsResolver = class ImagePermissionsResolver {
    constructor(imagesApi) {
        this.imagesApi = imagesApi;
    }
    resolve(route, state) {
        return this.imagesApi.permissions().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
ImagePermissionsResolver.ctorParameters = () => [
    { type: _image_api_service__WEBPACK_IMPORTED_MODULE_4__["ImagesApiService"] }
];
ImagePermissionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ImagePermissionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/image/image.resolver.ts":
/*!****************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/image/image.resolver.ts ***!
  \****************************************************************/
/*! exports provided: ImageResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImageResolver", function() { return ImageResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _image_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");





let ImageResolver = class ImageResolver {
    constructor(imagesApiService) {
        this.imagesApiService = imagesApiService;
    }
    resolve(route, state) {
        return this.imagesApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
ImageResolver.ctorParameters = () => [
    { type: _image_api_service__WEBPACK_IMPORTED_MODULE_4__["ImagesApiService"] }
];
ImageResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], ImageResolver);



/***/ })

}]);
//# sourceMappingURL=images-images-module-es2015.js.map