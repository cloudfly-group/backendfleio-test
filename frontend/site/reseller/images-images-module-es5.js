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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../image-list-ui.service */ "./src/app/reseller/cloud/images/image-list-ui.service.ts");





var ImageCreateComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImageCreateComponent, _super);
    function ImageCreateComponent(route, imageListUIService) {
        return _super.call(this, route, imageListUIService, 'create', null) || this;
    }
    ImageCreateComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ImageListUIService"] }
    ]; };
    ImageCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-image-create',
            template: __webpack_require__(/*! raw-loader!./image-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-create/image-create.component.html"),
            styles: [__webpack_require__(/*! ./image-create.component.scss */ "./src/app/reseller/cloud/images/image-create/image-create.component.scss")]
        })
    ], ImageCreateComponent);
    return ImageCreateComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../image-list-ui.service */ "./src/app/reseller/cloud/images/image-list-ui.service.ts");





var ImageDetailsComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImageDetailsComponent, _super);
    function ImageDetailsComponent(route, imageListUIService) {
        return _super.call(this, route, imageListUIService, 'details', 'image') || this;
    }
    ImageDetailsComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ImageListUIService"] }
    ]; };
    ImageDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-image-details',
            template: __webpack_require__(/*! raw-loader!./image-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-details/image-details.component.html"),
            styles: [__webpack_require__(/*! ./image-details.component.scss */ "./src/app/reseller/cloud/images/image-details/image-details.component.scss")]
        })
    ], ImageDetailsComponent);
    return ImageDetailsComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../image-list-ui.service */ "./src/app/reseller/cloud/images/image-list-ui.service.ts");





var ImageEditComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImageEditComponent, _super);
    function ImageEditComponent(route, imageListUIService) {
        return _super.call(this, route, imageListUIService, 'edit', 'image') || this;
    }
    ImageEditComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _image_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ImageListUIService"] }
    ]; };
    ImageEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-image-edit',
            template: __webpack_require__(/*! raw-loader!./image-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-edit/image-edit.component.html"),
            styles: [__webpack_require__(/*! ./image-edit.component.scss */ "./src/app/reseller/cloud/images/image-edit/image-edit.component.scss")]
        })
    ], ImageEditComponent);
    return ImageEditComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/image/image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");
/* harmony import */ var _image_ui_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./image-ui.service */ "./src/app/reseller/cloud/images/image-ui.service.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");









var ImageListUIService = /** @class */ (function () {
    function ImageListUIService(router, config, imagesApiService) {
        this.router = router;
        this.config = config;
        this.imagesApiService = imagesApiService;
        this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_8__["DatePipe"](this.config.locale);
    }
    ImageListUIService.prototype.getObjectUIService = function (object, permissions, state) {
        return new _image_ui_service__WEBPACK_IMPORTED_MODULE_7__["ImageUiService"](object, permissions, state, this.router, this.config, this.imagesApiService);
    };
    ImageListUIService.prototype.getTableData = function (objectList) {
        var e_1, _a;
        var tableData = {
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
        try {
            for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](objectList.objects), _c = _b.next(); !_c.done; _c = _b.next()) {
                var image = _c.value;
                var rowUIService = this.getObjectUIService(image, objectList.permissions, 'table-view');
                var row = {
                    cells: {
                        name: { text: image.name || image.id },
                        status: { text: image.status ? image.status.toLocaleUpperCase() : 'n/a' },
                        is_protected: { text: image.protected ? 'protected' : '' },
                        region: { text: image.region },
                        created_at: { text: this.datePipe.transform(image.created_at) },
                        min_disk: { text: image.min_disk + " GB" },
                    },
                    icon: rowUIService.getIcon(),
                    status: rowUIService.getStatus(),
                    actions: rowUIService.getActions(),
                    url: rowUIService.getDetailsLink(),
                };
                tableData.rows.push(row);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return tableData;
    };
    ImageListUIService.prototype.getActions = function (objectList) {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__["RouterLinkAction"]({
                name: 'Create new image',
                tooltip: 'Create new image',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('cloud/images/create')
            })
        ];
    };
    ImageListUIService.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
        { type: _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_6__["ImagesApiService"] }
    ]; };
    ImageListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ImageListUIService);
    return ImageListUIService;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _image_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../image-list-ui.service */ "./src/app/reseller/cloud/images/image-list-ui.service.ts");






var ImageListComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImageListComponent, _super);
    function ImageListComponent(route, imageListUIService, refreshService) {
        var _this = _super.call(this, route, imageListUIService, refreshService, 'images') || this;
        _this.route = route;
        _this.imageListUIService = imageListUIService;
        _this.refreshService = refreshService;
        return _this;
    }
    ImageListComponent.prototype.ngOnInit = function () {
        _super.prototype.ngOnInit.call(this);
    };
    ImageListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _image_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["ImageListUIService"] },
        { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
    ]; };
    ImageListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-image-list',
            template: __webpack_require__(/*! raw-loader!./image-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/image-list/image-list.component.html"),
            styles: [__webpack_require__(/*! ./image-list.component.scss */ "./src/app/reseller/cloud/images/image-list/image-list.component.scss")]
        })
    ], ImageListComponent);
    return ImageListComponent;
}(_shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"]));



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
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/object-status */ "./src/app/shared/ui/objects-view/interfaces/object-status.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/image/image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");
/* harmony import */ var _tabs_image_details_overview_image_details_overview_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/image-details-overview/image-details-overview.component */ "./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.ts");
/* harmony import */ var _tabs_image_edit_form_image_edit_form_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./tabs/image-edit-form/image-edit-form.component */ "./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.ts");












var ImageUiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImageUiService, _super);
    function ImageUiService(image, permissions, state, router, config, imagesApiService) {
        var _this = _super.call(this, image, permissions, state) || this;
        _this.router = router;
        _this.config = config;
        _this.imagesApiService = imagesApiService;
        _this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_7__["DatePipe"](_this.config.locale);
        return _this;
    }
    ImageUiService.prototype.getIcon = function () {
        return {
            class: 'fl-icons',
            name: this.object.os_distro || 'otheros',
        };
    };
    ImageUiService.prototype.getStatus = function () {
        switch (this.object.status) {
            case 'deactivated':
                return {
                    type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined,
                    value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Deactivated,
                };
            case 'active':
            default:
                return {
                    type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined,
                    value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Active,
                };
        }
    };
    ImageUiService.prototype.getTitle = function () {
        var prefix = '';
        if (this.object.type === 'snapshot') {
            prefix = 'snapshot';
        }
        if (this.object.disk_format === 'iso') {
            prefix = 'ISO';
        }
        if (prefix.length > 0) {
            prefix = "[" + prefix + "] ";
        }
        switch (this.state) {
            case 'edit':
                return {
                    text: "Edit " + (this.object.name || this.object.id),
                    subText: this.object.status ? this.object.status.toLocaleUpperCase() : 'n/a',
                };
            case 'create':
                return {
                    text: "Create new image",
                };
            case 'details':
            default:
                return {
                    text: "" + prefix + (this.object.name || this.object.id),
                    subText: this.object.status ? this.object.status.toLocaleUpperCase() : 'n/a',
                };
        }
    };
    ImageUiService.prototype.getActions = function () {
        var actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            name: 'Edit',
            tooltip: 'Edit image',
            routerUrl: this.config.getPanelUrl("cloud/images/" + this.object.id + "/edit"),
            router: this.router,
        }));
        actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_6__["ApiCallAction"]({
            object: this.object,
            icon: { name: 'delete' },
            name: 'Delete',
            tooltip: 'Delete image',
            confirmOptions: {
                confirm: true,
                title: 'Delete image',
                message: "Are you sure you want to delete image " + this.object.name,
            },
            apiService: this.imagesApiService,
            callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_6__["CallType"].Delete,
        }));
        return actions;
    };
    ImageUiService.prototype.getDetailsActions = function () {
        var actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("cloud/images"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("cloud/images"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    };
    ImageUiService.prototype.getDetailsLink = function () {
        return this.config.getPanelUrl("cloud/images/" + this.object.id);
    };
    ImageUiService.prototype.getCardFields = function () {
        var fields = [
            {
                value: this.object.min_disk + " GB min. disk, " + this.object.region
            },
            {
                name: 'Created:',
                value: this.datePipe.transform(this.object.created_at),
            },
        ];
        return fields;
    };
    ImageUiService.prototype.getTabs = function () {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Overview',
                        component: _tabs_image_details_overview_image_details_overview_component__WEBPACK_IMPORTED_MODULE_10__["ImageDetailsOverviewComponent"],
                    },
                ];
            case 'create':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_image_edit_form_image_edit_form_component__WEBPACK_IMPORTED_MODULE_11__["ImageEditFormComponent"],
                    },
                ];
            case 'edit':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_image_edit_form_image_edit_form_component__WEBPACK_IMPORTED_MODULE_11__["ImageEditFormComponent"],
                    },
                ];
        }
    };
    ImageUiService.prototype.getCardTags = function () {
        var tags = [];
        if (this.object.protected) {
            tags.push('protected');
        }
        return tags;
    };
    ImageUiService.ctorParameters = function () { return [
        { type: undefined },
        { type: undefined },
        { type: String },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
        { type: _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_9__["ImagesApiService"] }
    ]; };
    return ImageUiService;
}(_shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_2__["ObjectUIServiceBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
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













var routes = [
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
                    objectList: function (data) {
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
                getBreadCrumbDetail: function () {
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
                getBreadCrumbDetail: function (data) {
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
                getBreadCrumbDetail: function (data) {
                    return data.image.name || data.image.id;
                },
            },
        }
    },
];
var ImagesRoutingModule = /** @class */ (function () {
    function ImagesRoutingModule() {
    }
    ImagesRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
        })
    ], ImagesRoutingModule);
    return ImagesRoutingModule;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _image_create_image_create_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./image-create/image-create.component */ "./src/app/reseller/cloud/images/image-create/image-create.component.ts");
/* harmony import */ var _image_details_image_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-details/image-details.component */ "./src/app/reseller/cloud/images/image-details/image-details.component.ts");
/* harmony import */ var _image_edit_image_edit_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./image-edit/image-edit.component */ "./src/app/reseller/cloud/images/image-edit/image-edit.component.ts");
/* harmony import */ var _image_list_image_list_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./image-list/image-list.component */ "./src/app/reseller/cloud/images/image-list/image-list.component.ts");
/* harmony import */ var _images_routing_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./images-routing.module */ "./src/app/reseller/cloud/images/images-routing.module.ts");
/* harmony import */ var _tabs_image_details_overview_image_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/image-details-overview/image-details-overview.component */ "./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.ts");
/* harmony import */ var _tabs_image_edit_form_image_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/image-edit-form/image-edit-form.component */ "./src/app/reseller/cloud/images/tabs/image-edit-form/image-edit-form.component.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm5/form-field.es5.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm5/input.es5.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm5/select.es5.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm5/checkbox.es5.js");
/* harmony import */ var _angular_material_progress_bar__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/progress-bar */ "./node_modules/@angular/material/esm5/progress-bar.es5.js");



















var ImagesModule = /** @class */ (function () {
    function ImagesModule() {
    }
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
    return ImagesModule;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");



var ImageDetailsOverviewComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImageDetailsOverviewComponent, _super);
    function ImageDetailsOverviewComponent() {
        return _super.call(this) || this;
    }
    ImageDetailsOverviewComponent.prototype.ngOnInit = function () {
    };
    ImageDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-image-details-overview',
            template: __webpack_require__(/*! raw-loader!./image-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.html"),
            styles: [__webpack_require__(/*! ./image-details-overview.component.scss */ "./src/app/reseller/cloud/images/tabs/image-details-overview/image-details-overview.component.scss")]
        })
    ], ImageDetailsOverviewComponent);
    return ImageDetailsOverviewComponent;
}(_shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/image/image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");









var ImageEditFormComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ImageEditFormComponent, _super);
    function ImageEditFormComponent(formBuilder, imagesApi, router, config, activatedRoute) {
        var _this = _super.call(this) || this;
        _this.formBuilder = formBuilder;
        _this.imagesApi = imagesApi;
        _this.router = router;
        _this.config = config;
        _this.activatedRoute = activatedRoute;
        _this.imageForm = _this.formBuilder.group({
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
        _this.uploading = false;
        _this.uploadProgress = 7;
        return _this;
    }
    ImageEditFormComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.createOptions = this.activatedRoute.snapshot.data.createOptions;
        this.objectController.actionCallback = function () { return _this.saveImage(); };
        this.imageForm.patchValue(this.object);
        if (!this.object.id) {
            // creating new flavor
            this.imageForm.controls.region.setValue(this.createOptions.selected_region);
            this.imageForm.controls.file.disable();
            this.imageForm.controls.source.valueChanges.subscribe(function (newValue) {
                if (newValue === 'url') {
                    _this.imageForm.controls.file.disable();
                    _this.imageForm.controls.url.enable();
                }
                else {
                    _this.imageForm.controls.file.enable();
                    _this.imageForm.controls.url.disable();
                }
            });
        }
        else {
            this.imageForm.controls.source.disable();
            this.imageForm.controls.url.disable();
            this.imageForm.controls.file.disable();
        }
    };
    ImageEditFormComponent.prototype.fileChanged = function ($event) {
        var files = $event.target.files;
        this.imageFile = files.length > 0 ? files[0] : null;
        this.imageForm.controls.file.setValue(this.imageFile.name);
    };
    ImageEditFormComponent.prototype.saveImage = function () {
        var _this = this;
        var imageData = this.imageForm.value;
        var formData;
        if (imageData.source === 'file' && this.imageFile) {
            imageData.file = this.imageFile;
            formData = new FormData();
            Object.keys(imageData).map(function (fieldName) {
                formData.append(fieldName, imageData[fieldName]);
            });
            formData.append('file', this.imageFile, this.imageFile.name);
        }
        var response = this.createOrUpdate(this.imagesApi, formData ? formData : imageData);
        if (response !== rxjs__WEBPACK_IMPORTED_MODULE_4__["EMPTY"]) {
            this.uploading = !!formData;
            response.subscribe(function (data) {
                var requestCompleted = false;
                if (formData) {
                    var event_1 = data;
                    if (event_1.type === _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpEventType"].UploadProgress) {
                        _this.uploadProgress = event_1.loaded / event_1.total * 100;
                    }
                    if (event_1.type === _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpEventType"].Response) {
                        requestCompleted = true;
                    }
                }
                else {
                    requestCompleted = true;
                }
                if (requestCompleted) {
                    _this.uploading = false;
                    _this.router.navigateByUrl(_this.config.getPrevUrl('cloud/images')).catch(function () {
                    });
                }
            });
        }
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["of"])(null);
    };
    ImageEditFormComponent.ctorParameters = function () { return [
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
        { type: _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_5__["ImagesApiService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_7__["ConfigService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_6__["ActivatedRoute"] }
    ]; };
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
    return ImageEditFormComponent;
}(_shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"]));



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _image_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");





var ImageCreateOptionsResolver = /** @class */ (function () {
    function ImageCreateOptionsResolver(imagesApiService) {
        this.imagesApiService = imagesApiService;
    }
    ImageCreateOptionsResolver.prototype.resolve = function (route, state) {
        return this.imagesApiService.createOptions()
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    ImageCreateOptionsResolver.ctorParameters = function () { return [
        { type: _image_api_service__WEBPACK_IMPORTED_MODULE_4__["ImagesApiService"] }
    ]; };
    ImageCreateOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ImageCreateOptionsResolver);
    return ImageCreateOptionsResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _image_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");





var ImageListResolver = /** @class */ (function () {
    function ImageListResolver(imagesApiService) {
        this.imagesApiService = imagesApiService;
    }
    ImageListResolver.prototype.resolve = function (route, state) {
        return this.imagesApiService.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    ImageListResolver.ctorParameters = function () { return [
        { type: _image_api_service__WEBPACK_IMPORTED_MODULE_4__["ImagesApiService"] }
    ]; };
    ImageListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ImageListResolver);
    return ImageListResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _image_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");





var ImagePermissionsResolver = /** @class */ (function () {
    function ImagePermissionsResolver(imagesApi) {
        this.imagesApi = imagesApi;
    }
    ImagePermissionsResolver.prototype.resolve = function (route, state) {
        return this.imagesApi.permissions().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    ImagePermissionsResolver.ctorParameters = function () { return [
        { type: _image_api_service__WEBPACK_IMPORTED_MODULE_4__["ImagesApiService"] }
    ]; };
    ImagePermissionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ImagePermissionsResolver);
    return ImagePermissionsResolver;
}());



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
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _image_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");





var ImageResolver = /** @class */ (function () {
    function ImageResolver(imagesApiService) {
        this.imagesApiService = imagesApiService;
    }
    ImageResolver.prototype.resolve = function (route, state) {
        return this.imagesApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    ImageResolver.ctorParameters = function () { return [
        { type: _image_api_service__WEBPACK_IMPORTED_MODULE_4__["ImagesApiService"] }
    ]; };
    ImageResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ImageResolver);
    return ImageResolver;
}());



/***/ })

}]);
//# sourceMappingURL=images-images-module-es5.js.map