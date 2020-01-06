(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["volumes-volumes-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/dialogs/volume-extend/volume-extend.component.html":
/*!*********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/volumes/dialogs/volume-extend/volume-extend.component.html ***!
  \*********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<h1 mat-dialog-title>Extend volume {{data.volume.name}}</h1>\n<div mat-dialog-content>\n  <form [formGroup]=\"extendForm\">\n    <app-form-errors #formErrors [formGroup]=\"extendForm\"></app-form-errors>\n    <mat-form-field class=\"full-width\">\n      <input matInput placeholder=\"Size\" type=\"number\" formControlName=\"size\" required>\n      <mat-error>{{backendErrors['size'] || 'Field is required' }}</mat-error>\n    </mat-form-field>\n  </form>\n</div>\n<div mat-dialog-actions>\n  <button mat-button (click)=\"close()\">Cancel</button>\n  <button mat-button disabled=\"{{!extendForm.controls.size.dirty}}\" (click)=\"extendVolume()\"\n          [color]=\"'primary'\">\n    Extend\n  </button>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/dialogs/volume-rename/volume-rename.component.html":
/*!*********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/volumes/dialogs/volume-rename/volume-rename.component.html ***!
  \*********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<h1 mat-dialog-title>Rename volume {{data.volume.name}}</h1>\n<div mat-dialog-content>\n  <div [formGroup]=\"renameForm\">\n    <mat-form-field class=\"full-width\">\n      <input matInput placeholder=\"Name\" type=\"text\" formControlName=\"name\" required>\n    </mat-form-field>\n  </div>\n</div>\n<div mat-dialog-actions>\n  <button mat-button (click)=\"close()\">Cancel</button>\n  <button mat-button disabled=\"{{!renameForm.controls.name.dirty}}\" (click)=\"renameVolume()\"\n          [color]=\"'primary'\">\n    Rename\n  </button>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/tabs/volume-details-overview/volume-details-overview.component.html":
/*!**************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/volumes/tabs/volume-details-overview/volume-details-overview.component.html ***!
  \**************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxLayout=\"column\">\n  <p class=\"fl-detail\">ID: {{object.id}}</p>\n  <p class=\"fl-detail\">\n    Client:\n    <a class=\"active-link\"\n       [routerLink]=\"config.getPanelUrl('clients-users/clients/' + object.client.id)\">\n      {{object.client.name}}\n    </a>\n  </p>\n  <p class=\"fl-detail\">Size: {{object.size}} GB</p>\n  <p class=\"fl-detail\">Type: {{object.type || 'n/a'}}</p>\n  <p class=\"fl-detail\">Created at: {{object.created_at | date}}</p>\n  <p class=\"fl-detail\">Bootable: {{object.bootable}}</p>\n  <p *ngIf=\"this.object.related_instance_uuid\" class=\"fl-detail\">\n    This volume is attached to\n    <a class=\"active-link\"\n       routerLink=\"{{config.getPanelUrl('cloud/instances/') + this.object.related_instance_uuid}}\">\n      {{this.object.related_instance_uuid}}\n    </a>\n  </p>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/tabs/volume-edit-form/volume-edit-form.component.html":
/*!************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/volumes/tabs/volume-edit-form/volume-edit-form.component.html ***!
  \************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-fl-backdrop *ngIf=\"loading\" [verticalAlignMiddle]=\"true\"></app-fl-backdrop>\n<form [formGroup]=\"volumeForm\">\n  <app-form-errors #formErrors [formGroup]=\"volumeForm\"></app-form-errors>\n  <div fxLayout=\"row\" fxLayoutGap=\"10px\">\n    <div fxLayout=\"column\" [fxFlex]=\"!object.id ? 50 : 100\">\n      <mat-form-field>\n        <input matInput placeholder=\"Client\" type=\"text\" formControlName=\"client\" required\n               [matAutocomplete]=\"autocompleteClient\">\n        <mat-autocomplete #autocompleteClient=\"matAutocomplete\" [displayWith]=\"clientDisplay\">\n          <mat-option *ngFor=\"let client of filteredClients$ | async\" [value]=\"client\">\n            {{client.first_name}} {{client.last_name}}\n          </mat-option>\n        </mat-autocomplete>\n        <mat-error>{{backendErrors['name'] || 'This field is required!'}}</mat-error>\n      </mat-form-field>\n      <mat-form-field>\n        <mat-select formControlName=\"region\" placeholder=\"Region\" required>\n          <mat-option *ngFor=\"let region of createOptions.regions\"\n                      [value]=\"region.id\">\n            {{region.id}}\n          </mat-option>\n        </mat-select>\n      </mat-form-field>\n      <mat-form-field>\n        <input matInput placeholder=\"Name\" type=\"text\" formControlName=\"name\" required>\n        <mat-error>{{backendErrors['name'] || 'This field is required!' }}</mat-error>\n      </mat-form-field>\n      <mat-form-field class=\"full-width\">\n        <input matInput placeholder=\"Description\" type=\"text\" formControlName=\"description\">\n        <mat-error>{{backendErrors['description']}}</mat-error>\n      </mat-form-field>\n      <ng-container formGroupName=\"source\">\n        <mat-form-field>\n          <mat-select formControlName=\"source_type\" placeholder=\"Select source type\" required>\n            <mat-option *ngFor=\"let sourceType of sourceTypes\"\n                        [value]=\"sourceType.name\">\n              {{sourceType.description}}\n            </mat-option>\n          </mat-select>\n        </mat-form-field>\n        <mat-form-field *ngIf=\"volumeForm.value.source.source_type === 'image'\">\n          <input matInput placeholder=\"Image\" type=\"text\" formControlName=\"source\" required\n                 [matAutocomplete]=\"autocompleteImage\">\n          <mat-autocomplete #autocompleteImage=\"matAutocomplete\" [displayWith]=\"imageDisplay\">\n            <mat-option *ngFor=\"let image of filteredImages$ | async\" [value]=\"image\">\n              {{image.name}}\n            </mat-option>\n          </mat-autocomplete>\n        </mat-form-field>\n      </ng-container>\n      <mat-form-field fxFlex=\"auto\">\n        <input matInput placeholder=\"Size (GB)\" type=\"number\"\n               formControlName=\"size\" required>\n        <mat-error>{{backendErrors['size'] || 'This field is required!' }}</mat-error>\n      </mat-form-field>\n      <mat-form-field>\n        <mat-select formControlName=\"type\" placeholder=\"Volume type\" required>\n          <mat-option *ngFor=\"let volumeType of createOptions.types\"\n                      [value]=\"volumeType.name\">\n            {{volumeType.type_display}}\n          </mat-option>\n        </mat-select>\n      </mat-form-field>\n    </div>\n    <div *ngIf=\"!object.id\" fxLayout=\"column\" fxFlex=\"50\">\n      <p>\n        <strong>New OpenStack Volume</strong><br>\n        You can create a new Volume by first selecting a Client with an OpenStack project assigned <br>\n        then a Region where the volume will be created then setting <br>\n        the name and a description for it.<br>\n      </p>\n      <p>\n        <strong>Source Selection</strong><br>\n        You can create an empty volume or use an image or an existing volume as a source.<br>\n        Selecting a source will copy the data from that source to the new volume.<br>\n        In the case you select a bootable image, the volume will also be marked as bootable <br>\n        and you will be able to boot directly from that volume. <br>\n      </p>\n      <p>\n        <strong>Size</strong><br>\n        Enter the size of the new volume. This size must be equal of higher than the source size if <br>\n        any source is selected. For example, if an image has a minimum size of 3GB, the new volume size <br>\n        must be at least 3GB.\n      </p>\n      <p>\n        <strong>Type</strong><br>\n        A volume type can also be set while creating the volume. <br>\n        All volume types available in the selected region will be available to select from.<br>\n      </p>\n    </div>\n  </div>\n</form>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/volume-create/volume-create.component.html":
/*!*************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/volumes/volume-create/volume-create.component.html ***!
  \*************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/volume-details/volume-details.component.html":
/*!***************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/volumes/volume-details/volume-details.component.html ***!
  \***************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\"></app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/volume-edit/volume-edit.component.html":
/*!*********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/volumes/volume-edit/volume-edit.component.html ***!
  \*********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-sm']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/volume-list/volume-list.component.html":
/*!*********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/cloud/volumes/volume-list/volume-list.component.html ***!
  \*********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-objects-view [objectsListController]=\"objectListController\"></app-objects-view>\n"

/***/ }),

/***/ "./src/app/reseller/cloud/volumes/dialogs/volume-extend/volume-extend.component.scss":
/*!*******************************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/dialogs/volume-extend/volume-extend.component.scss ***!
  \*******************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3ZvbHVtZXMvZGlhbG9ncy92b2x1bWUtZXh0ZW5kL3ZvbHVtZS1leHRlbmQuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/volumes/dialogs/volume-extend/volume-extend.component.ts":
/*!*****************************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/dialogs/volume-extend/volume-extend.component.ts ***!
  \*****************************************************************************************/
/*! exports provided: VolumeExtendComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeExtendComponent", function() { return VolumeExtendComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");
/* harmony import */ var _shared_fleio_api_cloud_volume_volumes_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/volume/volumes-api.service */ "./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts");





var VolumeExtendComponent = /** @class */ (function () {
    function VolumeExtendComponent(dialogRef, data, volumesApiService, formBuilder) {
        this.dialogRef = dialogRef;
        this.data = data;
        this.volumesApiService = volumesApiService;
        this.formBuilder = formBuilder;
        this.backendErrors = {};
        this.extendForm = this.formBuilder.group({
            size: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
        });
    }
    VolumeExtendComponent.prototype.ngOnInit = function () {
        this.extendForm.controls.size.setValue(this.data.volume.size);
    };
    VolumeExtendComponent.prototype.close = function () {
        this.dialogRef.close(false);
    };
    VolumeExtendComponent.prototype.extendVolume = function () {
        var _this = this;
        this.volumesApiService.objectPostAction(this.data.volume.id, 'extend', this.extendForm.value).subscribe(function (result) {
            if (result) {
                _this.dialogRef.close('Volume extended');
            }
            else {
                _this.dialogRef.close('');
            }
        }, function (error) {
            _this.backendErrors = error.error;
            _this.formErrors.setBackendErrors(error.error);
        });
    };
    VolumeExtendComponent.ctorParameters = function () { return [
        { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__["MatDialogRef"] },
        { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__["MAT_DIALOG_DATA"],] }] },
        { type: _shared_fleio_api_cloud_volume_volumes_api_service__WEBPACK_IMPORTED_MODULE_4__["VolumesApiService"] },
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"] }
    ]; };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('formErrors', { static: false })
    ], VolumeExtendComponent.prototype, "formErrors", void 0);
    VolumeExtendComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-volume-extend',
            template: __webpack_require__(/*! raw-loader!./volume-extend.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/dialogs/volume-extend/volume-extend.component.html"),
            styles: [__webpack_require__(/*! ./volume-extend.component.scss */ "./src/app/reseller/cloud/volumes/dialogs/volume-extend/volume-extend.component.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__param"](1, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(_angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__["MAT_DIALOG_DATA"]))
    ], VolumeExtendComponent);
    return VolumeExtendComponent;
}());



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/dialogs/volume-rename/volume-rename.component.scss":
/*!*******************************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/dialogs/volume-rename/volume-rename.component.scss ***!
  \*******************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3ZvbHVtZXMvZGlhbG9ncy92b2x1bWUtcmVuYW1lL3ZvbHVtZS1yZW5hbWUuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/volumes/dialogs/volume-rename/volume-rename.component.ts":
/*!*****************************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/dialogs/volume-rename/volume-rename.component.ts ***!
  \*****************************************************************************************/
/*! exports provided: VolumeRenameComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeRenameComponent", function() { return VolumeRenameComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");
/* harmony import */ var _shared_fleio_api_cloud_volume_volumes_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/volume/volumes-api.service */ "./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts");





var VolumeRenameComponent = /** @class */ (function () {
    function VolumeRenameComponent(dialogRef, data, volumesApiService, formBuilder) {
        this.dialogRef = dialogRef;
        this.data = data;
        this.volumesApiService = volumesApiService;
        this.formBuilder = formBuilder;
        this.renameForm = this.formBuilder.group({
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
        });
    }
    VolumeRenameComponent.prototype.ngOnInit = function () {
        this.renameForm.controls.name.setValue(this.data.volume.name);
    };
    VolumeRenameComponent.prototype.close = function () {
        this.dialogRef.close(false);
    };
    VolumeRenameComponent.prototype.renameVolume = function () {
        var _this = this;
        this.volumesApiService.objectPostAction(this.data.volume.id, 'rename', this.renameForm.value).subscribe(function (result) {
            if (result) {
                _this.dialogRef.close('Volume renamed');
            }
            else {
                _this.dialogRef.close('');
            }
        });
    };
    VolumeRenameComponent.ctorParameters = function () { return [
        { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__["MatDialogRef"] },
        { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__["MAT_DIALOG_DATA"],] }] },
        { type: _shared_fleio_api_cloud_volume_volumes_api_service__WEBPACK_IMPORTED_MODULE_4__["VolumesApiService"] },
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"] }
    ]; };
    VolumeRenameComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-volume-rename',
            template: __webpack_require__(/*! raw-loader!./volume-rename.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/dialogs/volume-rename/volume-rename.component.html"),
            styles: [__webpack_require__(/*! ./volume-rename.component.scss */ "./src/app/reseller/cloud/volumes/dialogs/volume-rename/volume-rename.component.scss")]
        }),
        tslib__WEBPACK_IMPORTED_MODULE_0__["__param"](1, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(_angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__["MAT_DIALOG_DATA"]))
    ], VolumeRenameComponent);
    return VolumeRenameComponent;
}());



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/tabs/volume-details-overview/volume-details-overview.component.scss":
/*!************************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/tabs/volume-details-overview/volume-details-overview.component.scss ***!
  \************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3ZvbHVtZXMvdGFicy92b2x1bWUtZGV0YWlscy1vdmVydmlldy92b2x1bWUtZGV0YWlscy1vdmVydmlldy5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/cloud/volumes/tabs/volume-details-overview/volume-details-overview.component.ts":
/*!**********************************************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/tabs/volume-details-overview/volume-details-overview.component.ts ***!
  \**********************************************************************************************************/
/*! exports provided: VolumeDetailsOverviewComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeDetailsOverviewComponent", function() { return VolumeDetailsOverviewComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");




var VolumeDetailsOverviewComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](VolumeDetailsOverviewComponent, _super);
    function VolumeDetailsOverviewComponent(config) {
        var _this = _super.call(this) || this;
        _this.config = config;
        return _this;
    }
    VolumeDetailsOverviewComponent.prototype.ngOnInit = function () {
    };
    VolumeDetailsOverviewComponent.ctorParameters = function () { return [
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] }
    ]; };
    VolumeDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-volume-details-overview',
            template: __webpack_require__(/*! raw-loader!./volume-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/tabs/volume-details-overview/volume-details-overview.component.html"),
            styles: [__webpack_require__(/*! ./volume-details-overview.component.scss */ "./src/app/reseller/cloud/volumes/tabs/volume-details-overview/volume-details-overview.component.scss")]
        })
    ], VolumeDetailsOverviewComponent);
    return VolumeDetailsOverviewComponent;
}(_shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"]));



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/tabs/volume-edit-form/volume-edit-form.component.scss":
/*!**********************************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/tabs/volume-edit-form/volume-edit-form.component.scss ***!
  \**********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3ZvbHVtZXMvdGFicy92b2x1bWUtZWRpdC1mb3JtL3ZvbHVtZS1lZGl0LWZvcm0uY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/volumes/tabs/volume-edit-form/volume-edit-form.component.ts":
/*!********************************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/tabs/volume-edit-form/volume-edit-form.component.ts ***!
  \********************************************************************************************/
/*! exports provided: VolumeEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeEditFormComponent", function() { return VolumeEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _shared_fleio_api_cloud_volume_volumes_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/volume/volumes-api.service */ "./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _shared_fleio_api_client_user_client_clients_api_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../../../shared/fleio-api/client-user/client/clients-api.service */ "./src/app/shared/fleio-api/client-user/client/clients-api.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../../../shared/fleio-api/cloud/image/image-api.service */ "./src/app/shared/fleio-api/cloud/image/image-api.service.ts");











var VolumeEditFormComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](VolumeEditFormComponent, _super);
    function VolumeEditFormComponent(formBuilder, volumesApi, clientsApi, router, config, activatedRoute, imagesApi) {
        var _this = _super.call(this) || this;
        _this.formBuilder = formBuilder;
        _this.volumesApi = volumesApi;
        _this.clientsApi = clientsApi;
        _this.router = router;
        _this.config = config;
        _this.activatedRoute = activatedRoute;
        _this.imagesApi = imagesApi;
        _this.volumeForm = _this.formBuilder.group({
            client: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            region: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            description: [''],
            source: _this.formBuilder.group({
                source: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
                source_type: ['new', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            }),
            size: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            type: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
        });
        _this.loading = false;
        _this.client = _this.volumeForm.controls.client;
        _this.region = _this.volumeForm.controls.region;
        _this.image = _this.volumeForm.controls.source.controls.source;
        _this.source_type = _this.volumeForm.controls.source.controls.source_type;
        return _this;
    }
    VolumeEditFormComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.createOptions = this.activatedRoute.snapshot.data.createOptions;
        this.objectController.actionCallback = function () { return _this.saveVolume(); };
        this.volumeForm.patchValue(this.object);
        this.image.disable();
        if (!this.object.id) {
            // creating new volume
            this.volumeForm.controls.region.setValue(this.createOptions.selected_region);
        }
        else {
            this.volumeForm.disable();
        }
        this.filteredClients$ = this.client.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["startWith"])(''), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["map"])(function (value) {
            return typeof value === 'string' ? value : value.id;
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["mergeMap"])(function (value) {
            return _this.clientsApi.list({
                search: value,
                openstack_project: true,
            }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["map"])(function (clientsList) { return clientsList.objects; }));
        }));
        this.filteredImages$ = this.image.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["startWith"])(''), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["map"])(function (image) {
            return typeof image === 'string' ? image : image.id;
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["mergeMap"])(function (value) {
            return _this.imagesApi.list({
                search: value,
                region: _this.volumeForm.controls.region.value,
            }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["map"])(function (imagesList) { return imagesList.objects; }));
        }));
        this.region.valueChanges.subscribe(function (region) {
            _this.volumesApi.createOptions({ region: region }).subscribe(function (createOptions) {
                _this.createOptions = createOptions;
                _this.refreshSourceTypes();
            });
        });
        this.source_type.valueChanges.subscribe(function (sourceType) {
            if (sourceType === 'image') {
                _this.image.enable();
            }
            else {
                _this.image.disable();
            }
        });
        this.refreshSourceTypes();
    };
    VolumeEditFormComponent.prototype.refreshSourceTypes = function () {
        this.sourceTypes = [{ name: 'new', description: 'Create a new empty volume' }];
        if (this.createOptions.sources) {
            if (this.createOptions.sources.image && this.createOptions.sources.image.length) {
                this.sourceTypes.push({ name: 'image', description: 'Use image as a source' });
            }
            if (this.createOptions.sources.volume && this.createOptions.sources.volume.length) {
                this.sourceTypes.push({ name: 'volume', description: 'Use an existing volume' });
            }
        }
    };
    VolumeEditFormComponent.prototype.clientDisplay = function (client) {
        if (client) {
            return client.name ? client.name : client.first_name + " " + client.last_name;
        }
        else {
            return undefined;
        }
    };
    VolumeEditFormComponent.prototype.imageDisplay = function (image) {
        if (image) {
            return image.name;
        }
        else {
            return undefined;
        }
    };
    VolumeEditFormComponent.prototype.saveVolume = function () {
        var _this = this;
        var value = this.volumeForm.value;
        if (typeof (value.client) === 'object') {
            value.client = value.client.id;
        }
        if (typeof (value.source.source) === 'object') {
            value.source.source = value.source.source.id;
        }
        this.loading = true;
        this.createOrUpdate(this.volumesApi, value).subscribe(function () {
            _this.loading = false;
            _this.router.navigateByUrl(_this.config.getPrevUrl('cloud/volumes')).catch(function () {
                _this.loading = false;
            });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_6__["of"])(null);
    };
    VolumeEditFormComponent.ctorParameters = function () { return [
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
        { type: _shared_fleio_api_cloud_volume_volumes_api_service__WEBPACK_IMPORTED_MODULE_7__["VolumesApiService"] },
        { type: _shared_fleio_api_client_user_client_clients_api_service__WEBPACK_IMPORTED_MODULE_9__["ClientsApiService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
        { type: _shared_fleio_api_cloud_image_image_api_service__WEBPACK_IMPORTED_MODULE_10__["ImagesApiService"] }
    ]; };
    VolumeEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-volume-edit-form',
            template: __webpack_require__(/*! raw-loader!./volume-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/tabs/volume-edit-form/volume-edit-form.component.html"),
            styles: [__webpack_require__(/*! ./volume-edit-form.component.scss */ "./src/app/reseller/cloud/volumes/tabs/volume-edit-form/volume-edit-form.component.scss")]
        })
    ], VolumeEditFormComponent);
    return VolumeEditFormComponent;
}(_shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"]));



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-create/volume-create.component.scss":
/*!***********************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-create/volume-create.component.scss ***!
  \***********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3ZvbHVtZXMvdm9sdW1lLWNyZWF0ZS92b2x1bWUtY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-create/volume-create.component.ts":
/*!*********************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-create/volume-create.component.ts ***!
  \*********************************************************************************/
/*! exports provided: VolumeCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeCreateComponent", function() { return VolumeCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../volume-list-ui.service */ "./src/app/reseller/cloud/volumes/volume-list-ui.service.ts");





var VolumeCreateComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](VolumeCreateComponent, _super);
    function VolumeCreateComponent(route, volumeListUIService) {
        return _super.call(this, route, volumeListUIService, 'create', null) || this;
    }
    VolumeCreateComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["VolumeListUIService"] }
    ]; };
    VolumeCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-volume-create',
            template: __webpack_require__(/*! raw-loader!./volume-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/volume-create/volume-create.component.html"),
            styles: [__webpack_require__(/*! ./volume-create.component.scss */ "./src/app/reseller/cloud/volumes/volume-create/volume-create.component.scss")]
        })
    ], VolumeCreateComponent);
    return VolumeCreateComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-details/volume-details.component.scss":
/*!*************************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-details/volume-details.component.scss ***!
  \*************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3ZvbHVtZXMvdm9sdW1lLWRldGFpbHMvdm9sdW1lLWRldGFpbHMuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-details/volume-details.component.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-details/volume-details.component.ts ***!
  \***********************************************************************************/
/*! exports provided: VolumeDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeDetailsComponent", function() { return VolumeDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../volume-list-ui.service */ "./src/app/reseller/cloud/volumes/volume-list-ui.service.ts");





var VolumeDetailsComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](VolumeDetailsComponent, _super);
    function VolumeDetailsComponent(route, volumeListUIService) {
        return _super.call(this, route, volumeListUIService, 'details', 'volume') || this;
    }
    VolumeDetailsComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["VolumeListUIService"] }
    ]; };
    VolumeDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-volume-details',
            template: __webpack_require__(/*! raw-loader!./volume-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/volume-details/volume-details.component.html"),
            styles: [__webpack_require__(/*! ./volume-details.component.scss */ "./src/app/reseller/cloud/volumes/volume-details/volume-details.component.scss")]
        })
    ], VolumeDetailsComponent);
    return VolumeDetailsComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-edit/volume-edit.component.scss":
/*!*******************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-edit/volume-edit.component.scss ***!
  \*******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3ZvbHVtZXMvdm9sdW1lLWVkaXQvdm9sdW1lLWVkaXQuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-edit/volume-edit.component.ts":
/*!*****************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-edit/volume-edit.component.ts ***!
  \*****************************************************************************/
/*! exports provided: VolumeEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeEditComponent", function() { return VolumeEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../volume-list-ui.service */ "./src/app/reseller/cloud/volumes/volume-list-ui.service.ts");





var VolumeEditComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](VolumeEditComponent, _super);
    function VolumeEditComponent(route, volumeListUIService) {
        return _super.call(this, route, volumeListUIService, 'edit', 'volume') || this;
    }
    VolumeEditComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["VolumeListUIService"] }
    ]; };
    VolumeEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-volume-edit',
            template: __webpack_require__(/*! raw-loader!./volume-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/volume-edit/volume-edit.component.html"),
            styles: [__webpack_require__(/*! ./volume-edit.component.scss */ "./src/app/reseller/cloud/volumes/volume-edit/volume-edit.component.scss")]
        })
    ], VolumeEditComponent);
    return VolumeEditComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-list-ui.service.ts":
/*!******************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-list-ui.service.ts ***!
  \******************************************************************/
/*! exports provided: VolumeListUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeListUIService", function() { return VolumeListUIService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_fleio_api_cloud_volume_volumes_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/volume/volumes-api.service */ "./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts");
/* harmony import */ var _volume_ui_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./volume-ui.service */ "./src/app/reseller/cloud/volumes/volume-ui.service.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");









var VolumeListUIService = /** @class */ (function () {
    function VolumeListUIService(router, config, volumesApiService, matDialog) {
        this.router = router;
        this.config = config;
        this.volumesApiService = volumesApiService;
        this.matDialog = matDialog;
    }
    VolumeListUIService.prototype.getObjectUIService = function (object, permissions, state) {
        return new _volume_ui_service__WEBPACK_IMPORTED_MODULE_7__["VolumeUiService"](object, permissions, state, this.router, this.config, this.volumesApiService, this.matDialog);
    };
    VolumeListUIService.prototype.getTableData = function (objectList) {
        var e_1, _a;
        var tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Name', enableSort: true, fieldName: 'name' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Region', enableSort: false, fieldName: 'region' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Size', enableSort: false, fieldName: 'size' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Client', enableSort: false, fieldName: 'client' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Actions, displayName: 'Actions', enableSort: false, fieldName: '(actions)' },
                ],
                columnNames: ['name', 'region', 'size', 'client', '(actions)'],
                statusColumn: 'name',
            },
            rows: [],
        };
        try {
            for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](objectList.objects), _c = _b.next(); !_c.done; _c = _b.next()) {
                var volume = _c.value;
                var rowUIService = this.getObjectUIService(volume, objectList.permissions, 'table-view');
                var row = {
                    cells: {
                        name: { text: volume.name },
                        region: { text: volume.region || '' },
                        size: { text: volume.size ? (volume.size + ' GB') : '' },
                        client: {
                            text: volume.client ? volume.client.name : '',
                            url: volume.client ? this.config.getPanelUrl("clients-users/clients/" + volume.client.id) : null,
                        },
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
    VolumeListUIService.prototype.getActions = function (objectList) {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__["RouterLinkAction"]({
                name: 'Create new volume',
                tooltip: 'Create new volume',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('cloud/volumes/create')
            })
        ];
    };
    VolumeListUIService.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
        { type: _shared_fleio_api_cloud_volume_volumes_api_service__WEBPACK_IMPORTED_MODULE_6__["VolumesApiService"] },
        { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialog"] }
    ]; };
    VolumeListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], VolumeListUIService);
    return VolumeListUIService;
}());



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-list/volume-list.component.scss":
/*!*******************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-list/volume-list.component.scss ***!
  \*******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL2Nsb3VkL3ZvbHVtZXMvdm9sdW1lLWxpc3Qvdm9sdW1lLWxpc3QuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-list/volume-list.component.ts":
/*!*****************************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-list/volume-list.component.ts ***!
  \*****************************************************************************/
/*! exports provided: VolumeListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeListComponent", function() { return VolumeListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../volume-list-ui.service */ "./src/app/reseller/cloud/volumes/volume-list-ui.service.ts");






var VolumeListComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](VolumeListComponent, _super);
    function VolumeListComponent(route, volumeListUIService, refreshService) {
        var _this = _super.call(this, route, volumeListUIService, refreshService, 'volumes') || this;
        _this.route = route;
        _this.volumeListUIService = volumeListUIService;
        _this.refreshService = refreshService;
        return _this;
    }
    VolumeListComponent.prototype.ngOnInit = function () {
        _super.prototype.ngOnInit.call(this);
    };
    VolumeListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["VolumeListUIService"] },
        { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
    ]; };
    VolumeListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-volume-list',
            template: __webpack_require__(/*! raw-loader!./volume-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/cloud/volumes/volume-list/volume-list.component.html"),
            styles: [__webpack_require__(/*! ./volume-list.component.scss */ "./src/app/reseller/cloud/volumes/volume-list/volume-list.component.scss")]
        })
    ], VolumeListComponent);
    return VolumeListComponent;
}(_shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"]));



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-routing.module.ts":
/*!*****************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-routing.module.ts ***!
  \*****************************************************************/
/*! exports provided: VolumesRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumesRoutingModule", function() { return VolumesRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _volume_list_volume_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./volume-list/volume-list.component */ "./src/app/reseller/cloud/volumes/volume-list/volume-list.component.ts");
/* harmony import */ var _volume_create_volume_create_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./volume-create/volume-create.component */ "./src/app/reseller/cloud/volumes/volume-create/volume-create.component.ts");
/* harmony import */ var _volume_details_volume_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./volume-details/volume-details.component */ "./src/app/reseller/cloud/volumes/volume-details/volume-details.component.ts");
/* harmony import */ var _shared_fleio_api_cloud_volume_volume_resolver__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/volume/volume.resolver */ "./src/app/shared/fleio-api/cloud/volume/volume.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_volume_volume_permissions_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/volume/volume-permissions.resolver */ "./src/app/shared/fleio-api/cloud/volume/volume-permissions.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_volume_volume_list_resolver__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/volume/volume-list.resolver */ "./src/app/shared/fleio-api/cloud/volume/volume-list.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_volume_volume_create_options_resolver__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/volume/volume-create-options.resolver */ "./src/app/shared/fleio-api/cloud/volume/volume-create-options.resolver.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/ui-api/interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");












var routes = [
    {
        path: '',
        component: _volume_list_volume_list_component__WEBPACK_IMPORTED_MODULE_3__["VolumeListComponent"],
        resolve: {
            volumes: _shared_fleio_api_cloud_volume_volume_list_resolver__WEBPACK_IMPORTED_MODULE_8__["VolumeListResolver"],
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_11__["AuthGuard"]],
        data: {
            config: {
                feature: 'openstack.volumes',
                search: {
                    show: true,
                    placeholder: 'Search volumes ...',
                },
                subheader: {
                    objectNamePlural: 'volumes',
                    objectName: 'volume',
                    objectList: function (data) {
                        return data.volumes;
                    }
                },
                ordering: {
                    default: {
                        display: 'Date created',
                        field: 'created_at',
                        direction: _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_10__["OrderingDirection"].Descending,
                    },
                    options: [
                        { display: 'Name', field: 'name' },
                        { display: 'Status', field: 'status' },
                        { display: 'Size', field: 'size' },
                        { display: 'Date created', field: 'created_at' },
                    ]
                }
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: 'create',
        component: _volume_create_volume_create_component__WEBPACK_IMPORTED_MODULE_4__["VolumeCreateComponent"],
        resolve: {
            createOptions: _shared_fleio_api_cloud_volume_volume_create_options_resolver__WEBPACK_IMPORTED_MODULE_9__["VolumeCreateOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: function () {
                    return 'Create volume';
                },
            },
        }
    },
    {
        path: ':id',
        component: _volume_details_volume_details_component__WEBPACK_IMPORTED_MODULE_5__["VolumeDetailsComponent"],
        resolve: {
            volume: _shared_fleio_api_cloud_volume_volume_resolver__WEBPACK_IMPORTED_MODULE_6__["VolumeResolver"],
            permissions: _shared_fleio_api_cloud_volume_volume_permissions_resolver__WEBPACK_IMPORTED_MODULE_7__["VolumePermissionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: function (data) {
                    return data.volume.name;
                },
            },
        },
        runGuardsAndResolvers: 'always',
    },
];
var VolumesRoutingModule = /** @class */ (function () {
    function VolumesRoutingModule() {
    }
    VolumesRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
        })
    ], VolumesRoutingModule);
    return VolumesRoutingModule;
}());



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volume-ui.service.ts":
/*!*************************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volume-ui.service.ts ***!
  \*************************************************************/
/*! exports provided: VolumeUiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeUiService", function() { return VolumeUiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/object-status */ "./src/app/shared/ui/objects-view/interfaces/object-status.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_fleio_api_cloud_volume_volumes_api_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../shared/fleio-api/cloud/volume/volumes-api.service */ "./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts");
/* harmony import */ var _tabs_volume_details_overview_volume_details_overview_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/volume-details-overview/volume-details-overview.component */ "./src/app/reseller/cloud/volumes/tabs/volume-details-overview/volume-details-overview.component.ts");
/* harmony import */ var _tabs_volume_edit_form_volume_edit_form_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./tabs/volume-edit-form/volume-edit-form.component */ "./src/app/reseller/cloud/volumes/tabs/volume-edit-form/volume-edit-form.component.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");
/* harmony import */ var _dialogs_volume_rename_volume_rename_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./dialogs/volume-rename/volume-rename.component */ "./src/app/reseller/cloud/volumes/dialogs/volume-rename/volume-rename.component.ts");
/* harmony import */ var _dialogs_volume_extend_volume_extend_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./dialogs/volume-extend/volume-extend.component */ "./src/app/reseller/cloud/volumes/dialogs/volume-extend/volume-extend.component.ts");
















var VolumeUiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](VolumeUiService, _super);
    function VolumeUiService(volume, permissions, state, router, config, volumesApiService, matDialog) {
        var _this = _super.call(this, volume, permissions, state) || this;
        _this.matDialog = matDialog;
        _this.router = router;
        _this.config = config;
        _this.volumesApiService = volumesApiService;
        _this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_7__["DatePipe"](_this.config.locale);
        return _this;
    }
    VolumeUiService.prototype.getIcon = function () {
        return null;
    };
    VolumeUiService.prototype.getStatus = function () {
        switch (this.object.status) {
            case 'error':
                return {
                    value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Error,
                    type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined,
                };
            case 'deleting':
                return {
                    value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Error,
                    type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Changing,
                };
            case 'in-use':
                return {
                    value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Warning,
                    type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined,
                };
            case 'extending':
            case 'attaching':
                return {
                    value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Warning,
                    type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Changing,
                };
            case 'available':
            default:
                return {
                    value: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusValue"].Enabled,
                    type: _shared_ui_objects_view_interfaces_object_status__WEBPACK_IMPORTED_MODULE_1__["StatusType"].Defined,
                };
        }
    };
    VolumeUiService.prototype.getTitle = function () {
        switch (this.state) {
            case 'edit':
                return {
                    text: "Edit volume " + (this.object.name || this.object.id),
                };
            case 'create':
                return {
                    text: "Create new volume",
                };
            default:
                return {
                    text: "" + (this.object.name || this.object.id),
                    subText: this.object.status.toLocaleUpperCase(),
                };
        }
    };
    VolumeUiService.prototype.getActions = function () {
        var _this = this;
        var actions = [];
        actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({
            object: this.object,
            icon: { name: 'edit' },
            tooltip: 'Rename volume',
            name: 'Rename',
            callback: function () {
                return _this.matDialog.open(_dialogs_volume_rename_volume_rename_component__WEBPACK_IMPORTED_MODULE_14__["VolumeRenameComponent"], {
                    data: { volume: _this.object }
                }).afterClosed().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_12__["map"])(function (result) {
                    if (result === false) {
                        return;
                    }
                    _this.router.navigateByUrl(_this.config.getPanelUrl('cloud/volumes')).catch();
                    return { message: result };
                }));
            }
        }));
        actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({
            object: this.object,
            icon: { name: 'resize', class: 'fl-icons' },
            tooltip: 'Extend volume',
            name: 'Extend',
            callback: function () {
                return _this.matDialog.open(_dialogs_volume_extend_volume_extend_component__WEBPACK_IMPORTED_MODULE_15__["VolumeExtendComponent"], {
                    data: { volume: _this.object }
                }).afterClosed().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_12__["map"])(function (result) {
                    if (result === false) {
                        return;
                    }
                    _this.router.navigateByUrl(_this.config.getPanelUrl('cloud/volumes')).catch();
                    return { message: result };
                }));
            }
        }));
        actions.push(new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_6__["ApiCallAction"]({
            object: this.object,
            icon: { name: 'delete' },
            name: 'Delete',
            tooltip: 'Delete',
            confirmOptions: {
                confirm: true,
                title: 'Delete volume',
                message: "Are you sure you want to delete volume " + this.object.name,
            },
            apiService: this.volumesApiService,
            callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_6__["CallType"].Delete,
        }));
        return actions;
    };
    VolumeUiService.prototype.getDetailsActions = function () {
        var actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("cloud/volumes"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("cloud/volumes"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_8__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    };
    VolumeUiService.prototype.getDetailsLink = function () {
        return this.config.getPanelUrl("cloud/volumes/" + this.object.id);
    };
    VolumeUiService.prototype.getCardFields = function () {
        var fields = [
            {
                value: this.object.size + " GB, " + this.object.region
            },
            {
                name: 'Client',
                value: this.object.client.name,
            },
            {
                value: this.object.type,
            }
        ];
        return fields;
    };
    VolumeUiService.prototype.getTabs = function () {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Overview',
                        component: _tabs_volume_details_overview_volume_details_overview_component__WEBPACK_IMPORTED_MODULE_10__["VolumeDetailsOverviewComponent"],
                    },
                ];
            case 'create':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_volume_edit_form_volume_edit_form_component__WEBPACK_IMPORTED_MODULE_11__["VolumeEditFormComponent"],
                    },
                ];
            case 'edit':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_volume_edit_form_volume_edit_form_component__WEBPACK_IMPORTED_MODULE_11__["VolumeEditFormComponent"],
                    },
                ];
        }
    };
    VolumeUiService.prototype.getCardTags = function () {
        var tags = [];
        return tags;
    };
    VolumeUiService.ctorParameters = function () { return [
        { type: undefined },
        { type: undefined },
        { type: String },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
        { type: _shared_fleio_api_cloud_volume_volumes_api_service__WEBPACK_IMPORTED_MODULE_9__["VolumesApiService"] },
        { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_13__["MatDialog"] }
    ]; };
    return VolumeUiService;
}(_shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_2__["ObjectUIServiceBase"]));



/***/ }),

/***/ "./src/app/reseller/cloud/volumes/volumes.module.ts":
/*!**********************************************************!*\
  !*** ./src/app/reseller/cloud/volumes/volumes.module.ts ***!
  \**********************************************************/
/*! exports provided: VolumesModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumesModule", function() { return VolumesModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _volume_create_volume_create_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./volume-create/volume-create.component */ "./src/app/reseller/cloud/volumes/volume-create/volume-create.component.ts");
/* harmony import */ var _volume_details_volume_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./volume-details/volume-details.component */ "./src/app/reseller/cloud/volumes/volume-details/volume-details.component.ts");
/* harmony import */ var _volume_edit_volume_edit_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./volume-edit/volume-edit.component */ "./src/app/reseller/cloud/volumes/volume-edit/volume-edit.component.ts");
/* harmony import */ var _volume_list_volume_list_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./volume-list/volume-list.component */ "./src/app/reseller/cloud/volumes/volume-list/volume-list.component.ts");
/* harmony import */ var _volume_routing_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./volume-routing.module */ "./src/app/reseller/cloud/volumes/volume-routing.module.ts");
/* harmony import */ var _tabs_volume_details_overview_volume_details_overview_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs/volume-details-overview/volume-details-overview.component */ "./src/app/reseller/cloud/volumes/tabs/volume-details-overview/volume-details-overview.component.ts");
/* harmony import */ var _tabs_volume_edit_form_volume_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/volume-edit-form/volume-edit-form.component */ "./src/app/reseller/cloud/volumes/tabs/volume-edit-form/volume-edit-form.component.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm5/form-field.es5.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm5/input.es5.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm5/select.es5.js");
/* harmony import */ var _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/material/autocomplete */ "./node_modules/@angular/material/esm5/autocomplete.es5.js");
/* harmony import */ var _dialogs_volume_rename_volume_rename_component__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./dialogs/volume-rename/volume-rename.component */ "./src/app/reseller/cloud/volumes/dialogs/volume-rename/volume-rename.component.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm5/dialog.es5.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm5/button.es5.js");
/* harmony import */ var _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./volume-list-ui.service */ "./src/app/reseller/cloud/volumes/volume-list-ui.service.ts");
/* harmony import */ var _dialogs_volume_extend_volume_extend_component__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./dialogs/volume-extend/volume-extend.component */ "./src/app/reseller/cloud/volumes/dialogs/volume-extend/volume-extend.component.ts");
/* harmony import */ var _shared_ui_ui_module__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ../../../shared/ui/ui.module */ "./src/app/shared/ui/ui.module.ts");
























var VolumesModule = /** @class */ (function () {
    function VolumesModule() {
    }
    VolumesModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            declarations: [
                _volume_create_volume_create_component__WEBPACK_IMPORTED_MODULE_3__["VolumeCreateComponent"],
                _volume_details_volume_details_component__WEBPACK_IMPORTED_MODULE_4__["VolumeDetailsComponent"],
                _volume_edit_volume_edit_component__WEBPACK_IMPORTED_MODULE_5__["VolumeEditComponent"],
                _volume_list_volume_list_component__WEBPACK_IMPORTED_MODULE_6__["VolumeListComponent"],
                _tabs_volume_details_overview_volume_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["VolumeDetailsOverviewComponent"],
                _tabs_volume_edit_form_volume_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["VolumeEditFormComponent"],
                _dialogs_volume_rename_volume_rename_component__WEBPACK_IMPORTED_MODULE_18__["VolumeRenameComponent"],
                _dialogs_volume_extend_volume_extend_component__WEBPACK_IMPORTED_MODULE_22__["VolumeExtendComponent"],
            ],
            entryComponents: [
                _tabs_volume_details_overview_volume_details_overview_component__WEBPACK_IMPORTED_MODULE_8__["VolumeDetailsOverviewComponent"],
                _tabs_volume_edit_form_volume_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["VolumeEditFormComponent"],
                _dialogs_volume_rename_volume_rename_component__WEBPACK_IMPORTED_MODULE_18__["VolumeRenameComponent"],
                _dialogs_volume_extend_volume_extend_component__WEBPACK_IMPORTED_MODULE_22__["VolumeExtendComponent"],
            ],
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _volume_routing_module__WEBPACK_IMPORTED_MODULE_7__["VolumesRoutingModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_10__["ReactiveFormsModule"],
                _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_11__["ErrorHandlingModule"],
                _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_12__["ObjectsViewModule"],
                _angular_flex_layout__WEBPACK_IMPORTED_MODULE_13__["FlexModule"],
                _angular_material_form_field__WEBPACK_IMPORTED_MODULE_14__["MatFormFieldModule"],
                _angular_material_input__WEBPACK_IMPORTED_MODULE_15__["MatInputModule"],
                _angular_material_select__WEBPACK_IMPORTED_MODULE_16__["MatSelectModule"],
                _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_17__["MatAutocompleteModule"],
                _angular_material_dialog__WEBPACK_IMPORTED_MODULE_19__["MatDialogModule"],
                _angular_material_button__WEBPACK_IMPORTED_MODULE_20__["MatButtonModule"],
                _shared_ui_ui_module__WEBPACK_IMPORTED_MODULE_23__["UiModule"],
            ],
            providers: [
                {
                    provide: _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_21__["VolumeListUIService"],
                    useClass: _volume_list_ui_service__WEBPACK_IMPORTED_MODULE_21__["VolumeListUIService"],
                    multi: false,
                },
            ]
        })
    ], VolumesModule);
    return VolumesModule;
}());



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/volume/volume-create-options.resolver.ts":
/*!*********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/volume/volume-create-options.resolver.ts ***!
  \*********************************************************************************/
/*! exports provided: VolumeCreateOptionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeCreateOptionsResolver", function() { return VolumeCreateOptionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _volumes_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./volumes-api.service */ "./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts");





var VolumeCreateOptionsResolver = /** @class */ (function () {
    function VolumeCreateOptionsResolver(volumesApiService) {
        this.volumesApiService = volumesApiService;
    }
    VolumeCreateOptionsResolver.prototype.resolve = function (route, state) {
        return this.volumesApiService.createOptions()
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    VolumeCreateOptionsResolver.ctorParameters = function () { return [
        { type: _volumes_api_service__WEBPACK_IMPORTED_MODULE_4__["VolumesApiService"] }
    ]; };
    VolumeCreateOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], VolumeCreateOptionsResolver);
    return VolumeCreateOptionsResolver;
}());



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/volume/volume-list.resolver.ts":
/*!***********************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/volume/volume-list.resolver.ts ***!
  \***********************************************************************/
/*! exports provided: VolumeListResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeListResolver", function() { return VolumeListResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _volumes_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./volumes-api.service */ "./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts");





var VolumeListResolver = /** @class */ (function () {
    function VolumeListResolver(volumesApiService) {
        this.volumesApiService = volumesApiService;
    }
    VolumeListResolver.prototype.resolve = function (route, state) {
        return this.volumesApiService.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    VolumeListResolver.ctorParameters = function () { return [
        { type: _volumes_api_service__WEBPACK_IMPORTED_MODULE_4__["VolumesApiService"] }
    ]; };
    VolumeListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], VolumeListResolver);
    return VolumeListResolver;
}());



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/volume/volume-permissions.resolver.ts":
/*!******************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/volume/volume-permissions.resolver.ts ***!
  \******************************************************************************/
/*! exports provided: VolumePermissionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumePermissionsResolver", function() { return VolumePermissionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _volumes_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./volumes-api.service */ "./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts");





var VolumePermissionsResolver = /** @class */ (function () {
    function VolumePermissionsResolver(volumesApi) {
        this.volumesApi = volumesApi;
    }
    VolumePermissionsResolver.prototype.resolve = function (route, state) {
        return this.volumesApi.permissions().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    VolumePermissionsResolver.ctorParameters = function () { return [
        { type: _volumes_api_service__WEBPACK_IMPORTED_MODULE_4__["VolumesApiService"] }
    ]; };
    VolumePermissionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], VolumePermissionsResolver);
    return VolumePermissionsResolver;
}());



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/volume/volume.resolver.ts":
/*!******************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/volume/volume.resolver.ts ***!
  \******************************************************************/
/*! exports provided: VolumeResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VolumeResolver", function() { return VolumeResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _volumes_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./volumes-api.service */ "./src/app/shared/fleio-api/cloud/volume/volumes-api.service.ts");





var VolumeResolver = /** @class */ (function () {
    function VolumeResolver(volumesApiService) {
        this.volumesApiService = volumesApiService;
    }
    VolumeResolver.prototype.resolve = function (route, state) {
        return this.volumesApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    VolumeResolver.ctorParameters = function () { return [
        { type: _volumes_api_service__WEBPACK_IMPORTED_MODULE_4__["VolumesApiService"] }
    ]; };
    VolumeResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], VolumeResolver);
    return VolumeResolver;
}());



/***/ })

}]);
//# sourceMappingURL=volumes-volumes-module-es5.js.map