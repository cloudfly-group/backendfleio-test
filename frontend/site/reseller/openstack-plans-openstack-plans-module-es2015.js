(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["openstack-plans-openstack-plans-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/dialogs/pricing-plan-delete/pricing-plan-delete.component.html":
/*!**************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/cloud/openstack-plans/dialogs/pricing-plan-delete/pricing-plan-delete.component.html ***!
  \**************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<h1 mat-dialog-title>Delete plan {{data.planToDelete.name}}</h1>\n<div mat-dialog-content>\n  <p>Select another plan to migrate services from {{data.planToDelete.name}}</p>\n  <div [formGroup]=\"deleteOptions\">\n    <mat-select formControlName=\"selectedPlan\" placeholder=\"Plan to migrate\">\n      <mat-option *ngFor=\"let alternativePlan of alternativePlans\" [value]=\"alternativePlan.id\">\n        {{alternativePlan.name}}\n      </mat-option>\n    </mat-select>\n  </div>\n</div>\n<div mat-dialog-actions>\n  <button mat-button (click)=\"close()\">Cancel</button>\n  <button mat-button disabled=\"{{!(this.selectedPlan.value > 0)}}\" (click)=\"delete()\"\n          [color]=\"'primary'\">\n    Delete\n  </button>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-create/openstack-plan-create.component.html":
/*!**********************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-create/openstack-plan-create.component.html ***!
  \**********************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-sm']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-details/openstack-plan-details.component.html":
/*!************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-details/openstack-plan-details.component.html ***!
  \************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\"></app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-edit/openstack-plan-edit.component.html":
/*!******************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-edit/openstack-plan-edit.component.html ***!
  \******************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-sm']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list/openstack-plan-list.component.html":
/*!******************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list/openstack-plan-list.component.html ***!
  \******************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-objects-view [objectsListController]=\"objectListController\"></app-objects-view>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-details-overview/pricing-plan-details-overview.component.html":
/*!*******************************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-details-overview/pricing-plan-details-overview.component.html ***!
  \*******************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxLayout=\"row\">\n  <a mat-button\n     class=\"create-new-rule-btn\"\n     color=\"primary\"\n     [routerLink]=\"[config.getPanelUrl('settings/pricing-rules/create'), object.id]\">\n      Create new pricing rule\n  </a>\n</div>\n\n<div fxLayout=\"row\" *ngIf=\"object.pricing_rules.length\">\n  <table mat-table [dataSource]=\"object.pricing_rules\" class=\"full-width\">\n    <ng-container matColumnDef=\"display_name\">\n      <th mat-header-cell *matHeaderCellDef>Name</th>\n      <td mat-cell *matCellDef=\"let element\">{{element.display_name}}</td>\n    </ng-container>\n    <ng-container matColumnDef=\"resource_name\">\n      <th mat-header-cell *matHeaderCellDef>Resource</th>\n      <td mat-cell *matCellDef=\"let element\">{{element.resource_name}}</td>\n    </ng-container>\n    <ng-container matColumnDef=\"price\">\n      <th mat-header-cell *matHeaderCellDef>Price</th>\n      <td mat-cell *matCellDef=\"let element\">\n        <ng-container *ngIf=\"element.tiered_price.length === 1\">{{element.price}}</ng-container>\n        <ng-container *ngIf=\"element.tiered_price.length > 1\">{{element.tiered_price[0].p}}</ng-container>\n        ({{object.currency}}) / {{element.pricing_attribute}} {{element.display_unit}}\n        <ng-container *ngIf=\"element.tiered_price.length > 1\">(Tiered)</ng-container>\n        <span *ngIf=\"element.modifiers_count === 1\"> + 1 modifier</span>\n        <span *ngIf=\"element.modifiers_count > 1\"> + {{element.modifiers_count}} modifiers</span>\n      </td>\n    </ng-container>\n    <ng-container matColumnDef=\"actions\">\n      <th mat-header-cell *matHeaderCellDef>Actions</th>\n      <td mat-cell *matCellDef=\"let element\">\n        <a mat-icon-button\n           fl-tooltip=\"Edit pricing rule\"\n           [routerLink]=\"config.getPanelUrl('settings/pricing-rules/' + element.id + '/edit')\">\n          <mat-icon>edit</mat-icon>\n        </a>\n        <a mat-icon-button\n           fl-tooltip=\"Delete pricing rule\"\n           (click)=\"deletePricingRule(element.id)\">\n          <mat-icon>delete</mat-icon>\n        </a>\n      </td>\n    </ng-container>\n    <tr mat-header-row *matHeaderRowDef=\"displayedColumns\"></tr>\n    <tr mat-row *matRowDef=\"let row; columns: displayedColumns;\"></tr>\n  </table>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-edit-form/pricing-plan-edit-form.component.html":
/*!*****************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-edit-form/pricing-plan-edit-form.component.html ***!
  \*****************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form [formGroup]=\"pricingPlanForm\">\n  <app-form-errors #formErrors [formGroup]=\"pricingPlanForm\"></app-form-errors>\n  <mat-form-field class=\"full-width\">\n    <input matInput placeholder=\"Name\" type=\"text\" formControlName=\"name\" required>\n    <mat-error>{{backendErrors['name'] || 'This field is required!' }}</mat-error>\n  </mat-form-field>\n  <mat-form-field class=\"full-width\">\n    <mat-select formControlName=\"currency\" placeholder=\"Currency\">\n      <mat-option *ngFor=\"let currency of createOptions.currencies\" [value]=\"currency.code\">{{currency.code}}\n      </mat-option>\n    </mat-select>\n    <mat-error>{{backendErrors['currency']}}</mat-error>\n  </mat-form-field>\n  <div class=\"half-width half-width-spacing checkbox-container\">\n    <mat-checkbox [color]=\"'primary'\" formControlName=\"is_default\">\n      Is default\n    </mat-checkbox>\n    <mat-error>{{backendErrors['is_default']}}</mat-error>\n  </div>\n  <mat-form-field class=\"full-width\" *ngIf=\"initialDefault && !isDefault.value\">\n    <mat-select formControlName=\"other_default\" placeholder=\"New default plan\">\n      <mat-option *ngFor=\"let otherPlan of createOptions.non_default_plans\" [value]=\"otherPlan.id\">{{otherPlan.name}}\n      </mat-option>\n    </mat-select>\n    <mat-error>{{backendErrors['other_default']}}</mat-error>\n  </mat-form-field>\n</form>\n"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/dialogs/pricing-plan-delete/pricing-plan-delete.component.scss":
/*!************************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/dialogs/pricing-plan-delete/pricing-plan-delete.component.scss ***!
  \************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL29wZW5zdGFjay1wbGFucy9kaWFsb2dzL3ByaWNpbmctcGxhbi1kZWxldGUvcHJpY2luZy1wbGFuLWRlbGV0ZS5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/dialogs/pricing-plan-delete/pricing-plan-delete.component.ts":
/*!**********************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/dialogs/pricing-plan-delete/pricing-plan-delete.component.ts ***!
  \**********************************************************************************************************************/
/*! exports provided: PricingPlanDeleteComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingPlanDeleteComponent", function() { return PricingPlanDeleteComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");
/* harmony import */ var _shared_fleio_api_cloud_pricing_plan_pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../../shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts");
/* harmony import */ var _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../../shared/ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");






let PricingPlanDeleteComponent = class PricingPlanDeleteComponent {
    constructor(dialogRef, data, pricingPlansApiService, notificationService) {
        this.dialogRef = dialogRef;
        this.data = data;
        this.pricingPlansApiService = pricingPlansApiService;
        this.notificationService = notificationService;
        this.alternativePlans = null;
        this.selectedPlan = new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormControl"]();
        this.deleteOptions = new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormGroup"]({
            selectedPlan: this.selectedPlan,
        });
    }
    ngOnInit() {
        this.pricingPlansApiService.getAlternativePlans(this.data.planToDelete.id).subscribe(alternativePlans => {
            this.alternativePlans = alternativePlans;
        });
    }
    close() {
        this.dialogRef.close(false);
    }
    delete() {
        if (this.selectedPlan.value > 0) {
            this.pricingPlansApiService.delete(this.data.planToDelete.id, { plan_to_migrate: this.selectedPlan.value }).subscribe(result => {
                if (result) {
                    this.dialogRef.close('Plan deleted successfully');
                }
                else {
                    this.dialogRef.close('Failed to delete plan');
                }
            });
        }
        else {
            this.notificationService.showMessage('You need to select an alternate pricing plan.');
        }
    }
};
PricingPlanDeleteComponent.ctorParameters = () => [
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"] },
    { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"],] }] },
    { type: _shared_fleio_api_cloud_pricing_plan_pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_3__["PricingPlansApiService"] },
    { type: _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_4__["NotificationService"] }
];
PricingPlanDeleteComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-pricing-plan-delete',
        template: __webpack_require__(/*! raw-loader!./pricing-plan-delete.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/dialogs/pricing-plan-delete/pricing-plan-delete.component.html"),
        styles: [__webpack_require__(/*! ./pricing-plan-delete.component.scss */ "./src/app/reseller/settings/cloud/openstack-plans/dialogs/pricing-plan-delete/pricing-plan-delete.component.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__param"](1, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"]))
], PricingPlanDeleteComponent);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-create/openstack-plan-create.component.scss":
/*!********************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-create/openstack-plan-create.component.scss ***!
  \********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL29wZW5zdGFjay1wbGFucy9vcGVuc3RhY2stcGxhbi1jcmVhdGUvb3BlbnN0YWNrLXBsYW4tY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-create/openstack-plan-create.component.ts":
/*!******************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-create/openstack-plan-create.component.ts ***!
  \******************************************************************************************************************/
/*! exports provided: OpenstackPlanCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OpenstackPlanCreateComponent", function() { return OpenstackPlanCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../openstack-plan-list-ui.service */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list-ui.service.ts");





let OpenstackPlanCreateComponent = class OpenstackPlanCreateComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, pricingPlanListUIService) {
        super(route, pricingPlanListUIService, 'create', null);
    }
};
OpenstackPlanCreateComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["PricingPlanListUIService"] }
];
OpenstackPlanCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-openstack-plan-create',
        template: __webpack_require__(/*! raw-loader!./openstack-plan-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-create/openstack-plan-create.component.html"),
        styles: [__webpack_require__(/*! ./openstack-plan-create.component.scss */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-create/openstack-plan-create.component.scss")]
    })
], OpenstackPlanCreateComponent);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-details/openstack-plan-details.component.scss":
/*!**********************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-details/openstack-plan-details.component.scss ***!
  \**********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL29wZW5zdGFjay1wbGFucy9vcGVuc3RhY2stcGxhbi1kZXRhaWxzL29wZW5zdGFjay1wbGFuLWRldGFpbHMuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-details/openstack-plan-details.component.ts":
/*!********************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-details/openstack-plan-details.component.ts ***!
  \********************************************************************************************************************/
/*! exports provided: OpenstackPlanDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OpenstackPlanDetailsComponent", function() { return OpenstackPlanDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../openstack-plan-list-ui.service */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list-ui.service.ts");





let OpenstackPlanDetailsComponent = class OpenstackPlanDetailsComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, pricingPlanListUIService) {
        super(route, pricingPlanListUIService, 'details', 'pricingPlan');
    }
};
OpenstackPlanDetailsComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["PricingPlanListUIService"] }
];
OpenstackPlanDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-openstack-plan-details',
        template: __webpack_require__(/*! raw-loader!./openstack-plan-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-details/openstack-plan-details.component.html"),
        styles: [__webpack_require__(/*! ./openstack-plan-details.component.scss */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-details/openstack-plan-details.component.scss")]
    })
], OpenstackPlanDetailsComponent);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-edit/openstack-plan-edit.component.scss":
/*!****************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-edit/openstack-plan-edit.component.scss ***!
  \****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL29wZW5zdGFjay1wbGFucy9vcGVuc3RhY2stcGxhbi1lZGl0L29wZW5zdGFjay1wbGFuLWVkaXQuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-edit/openstack-plan-edit.component.ts":
/*!**************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-edit/openstack-plan-edit.component.ts ***!
  \**************************************************************************************************************/
/*! exports provided: OpenstackPlanEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OpenstackPlanEditComponent", function() { return OpenstackPlanEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../openstack-plan-list-ui.service */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list-ui.service.ts");





let OpenstackPlanEditComponent = class OpenstackPlanEditComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, pricingPlanListUIService) {
        super(route, pricingPlanListUIService, 'edit', 'pricingPlan');
    }
};
OpenstackPlanEditComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["PricingPlanListUIService"] }
];
OpenstackPlanEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-openstack-plan-edit',
        template: __webpack_require__(/*! raw-loader!./openstack-plan-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-edit/openstack-plan-edit.component.html"),
        styles: [__webpack_require__(/*! ./openstack-plan-edit.component.scss */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-edit/openstack-plan-edit.component.scss")]
    })
], OpenstackPlanEditComponent);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list-ui.service.ts":
/*!*******************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list-ui.service.ts ***!
  \*******************************************************************************************/
/*! exports provided: PricingPlanListUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingPlanListUIService", function() { return PricingPlanListUIService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_fleio_api_cloud_pricing_plan_pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts");
/* harmony import */ var _openstack_plan_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./openstack-plan-ui.service */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-ui.service.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");









let PricingPlanListUIService = class PricingPlanListUIService {
    constructor(router, config, pricingPlansApiService, matDialog) {
        this.router = router;
        this.config = config;
        this.pricingPlansApiService = pricingPlansApiService;
        this.matDialog = matDialog;
    }
    getObjectUIService(object, permissions, state) {
        return new _openstack_plan_ui_service__WEBPACK_IMPORTED_MODULE_4__["PricingPlanUIService"](object, permissions, state, this.router, this.config, this.pricingPlansApiService, this.matDialog);
    }
    getTableData(objectList) {
        const tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_6__["ColumnType"].Value, displayName: 'Name', enableSort: true, fieldName: 'name' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_6__["ColumnType"].Value, displayName: 'Currency', enableSort: true, fieldName: 'currency' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_6__["ColumnType"].Value, displayName: 'Is default', enableSort: false, fieldName: 'is_default' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_6__["ColumnType"].Actions, displayName: 'Actions', enableSort: false, fieldName: '(actions)' },
                ],
                columnNames: ['name', 'currency', 'is_default', '(actions)'],
            },
            rows: [],
        };
        for (const plan of objectList.objects) {
            const rowUIService = this.getObjectUIService(plan, objectList.permissions, 'table-view');
            const row = {
                cells: {
                    name: { text: plan.name },
                    currency: { text: plan.currency },
                    is_default: { text: plan.is_default.toString() },
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
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_7__["RouterLinkAction"]({
                name: 'Create new pricing plan',
                tooltip: 'Create new pricing plan',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('settings/openstack-plans/create')
            })
        ];
    }
};
PricingPlanListUIService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
    { type: _shared_fleio_api_cloud_pricing_plan_pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_3__["PricingPlansApiService"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_8__["MatDialog"] }
];
PricingPlanListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], PricingPlanListUIService);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list/openstack-plan-list.component.scss":
/*!****************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list/openstack-plan-list.component.scss ***!
  \****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL29wZW5zdGFjay1wbGFucy9vcGVuc3RhY2stcGxhbi1saXN0L29wZW5zdGFjay1wbGFuLWxpc3QuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list/openstack-plan-list.component.ts":
/*!**************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list/openstack-plan-list.component.ts ***!
  \**************************************************************************************************************/
/*! exports provided: OpenstackPlanListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OpenstackPlanListComponent", function() { return OpenstackPlanListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../openstack-plan-list-ui.service */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list-ui.service.ts");






let OpenstackPlanListComponent = class OpenstackPlanListComponent extends _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"] {
    constructor(route, pricingPlanListUIService, refreshService) {
        super(route, pricingPlanListUIService, refreshService, 'pricingPlans');
        this.route = route;
        this.pricingPlanListUIService = pricingPlanListUIService;
        this.refreshService = refreshService;
    }
    ngOnInit() {
        super.ngOnInit();
    }
};
OpenstackPlanListComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["PricingPlanListUIService"] },
    { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
];
OpenstackPlanListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-openstack-plan-list',
        template: __webpack_require__(/*! raw-loader!./openstack-plan-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list/openstack-plan-list.component.html"),
        styles: [__webpack_require__(/*! ./openstack-plan-list.component.scss */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list/openstack-plan-list.component.scss")]
    })
], OpenstackPlanListComponent);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-ui.service.ts":
/*!**************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-ui.service.ts ***!
  \**************************************************************************************/
/*! exports provided: PricingPlanUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingPlanUIService", function() { return PricingPlanUIService; });
/* harmony import */ var _shared_fleio_api_cloud_pricing_plan_pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _tabs_pricing_plan_details_overview_pricing_plan_details_overview_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tabs/pricing-plan-details-overview/pricing-plan-details-overview.component */ "./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-details-overview/pricing-plan-details-overview.component.ts");
/* harmony import */ var _tabs_pricing_plan_edit_form_pricing_plan_edit_form_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./tabs/pricing-plan-edit-form/pricing-plan-edit-form.component */ "./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-edit-form/pricing-plan-edit-form.component.ts");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _dialogs_pricing_plan_delete_pricing_plan_delete_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./dialogs/pricing-plan-delete/pricing-plan-delete.component */ "./src/app/reseller/settings/cloud/openstack-plans/dialogs/pricing-plan-delete/pricing-plan-delete.component.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");











class PricingPlanUIService extends _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__["ObjectUIServiceBase"] {
    constructor(pricingPlan, permissions, state, router, config, pricingPlansApiService, matDialog) {
        super(pricingPlan, permissions, state);
        this.matDialog = matDialog;
        this.router = router;
        this.config = config;
        this.pricingPlansApiService = pricingPlansApiService;
    }
    getIcon() {
        return null;
    }
    getStatus() {
        return null;
    }
    getTitle() {
        switch (this.state) {
            case 'details':
                return {
                    text: `Openstack plan ${this.object.name}`,
                };
            case 'edit':
                return {
                    text: `Edit ${this.object.name}`,
                };
            case 'create':
                return {
                    text: 'Create pricing plan',
                };
            default:
                return {
                    text: `${this.object.name}`,
                };
        }
    }
    getActions() {
        const actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_4__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            name: 'Edit',
            tooltip: 'Edit',
            routerUrl: this.config.getPanelUrl(`settings/openstack-plans/${this.object.id}/edit`),
            router: this.router,
        }));
        actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({
            object: this.object,
            icon: { name: 'delete' },
            tooltip: 'Delete',
            name: 'Delete',
            callback: action => {
                return this.matDialog.open(_dialogs_pricing_plan_delete_pricing_plan_delete_component__WEBPACK_IMPORTED_MODULE_9__["PricingPlanDeleteComponent"], {
                    data: { planToDelete: this.object }
                }).afterClosed().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_8__["map"])(result => {
                    if (result === false) {
                        return;
                    }
                    this.router.navigateByUrl(this.config.getPanelUrl('settings/openstack-plans')).catch();
                    return { message: result };
                }));
            }
        }));
        return actions;
    }
    getDetailsLink() {
        return this.config.getPanelUrl(`settings/openstack-plans/${this.object.id}`);
    }
    getCardFields() {
        const fields = [
            {
                name: 'Name',
                value: `${this.object.name}`
            },
            {
                name: 'Currency',
                value: `${this.object.currency}`
            },
        ];
        return fields;
    }
    getCardTags() {
        if (this.object.is_default) {
            return ['default'];
        }
        else {
            return [];
        }
    }
    getTabs() {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Overview',
                        component: _tabs_pricing_plan_details_overview_pricing_plan_details_overview_component__WEBPACK_IMPORTED_MODULE_5__["PricingPlanDetailsOverviewComponent"],
                    },
                ];
            case 'edit':
            case 'create':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_pricing_plan_edit_form_pricing_plan_edit_form_component__WEBPACK_IMPORTED_MODULE_6__["PricingPlanEditFormComponent"],
                    },
                ];
        }
    }
    getDetailsActions() {
        const actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_4__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`settings/openstack-plans`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_4__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`settings/openstack-plans`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    }
}
PricingPlanUIService.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_cloud_pricing_plan_pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_0__["PricingPlansApiService"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_10__["MatDialog"] }
];


/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plans-routing.module.ts":
/*!*******************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plans-routing.module.ts ***!
  \*******************************************************************************************/
/*! exports provided: OpenstackPlansRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OpenstackPlansRoutingModule", function() { return OpenstackPlansRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _openstack_plan_list_openstack_plan_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./openstack-plan-list/openstack-plan-list.component */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list/openstack-plan-list.component.ts");
/* harmony import */ var _openstack_plan_details_openstack_plan_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./openstack-plan-details/openstack-plan-details.component */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-details/openstack-plan-details.component.ts");
/* harmony import */ var _openstack_plan_edit_openstack_plan_edit_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./openstack-plan-edit/openstack-plan-edit.component */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-edit/openstack-plan-edit.component.ts");
/* harmony import */ var _openstack_plan_create_openstack_plan_create_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./openstack-plan-create/openstack-plan-create.component */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-create/openstack-plan-create.component.ts");
/* harmony import */ var _shared_fleio_api_cloud_pricing_plan_pricing_plan_list_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../shared/fleio-api/cloud/pricing-plan/pricing-plan-list.resolver */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plan-list.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_pricing_plan_pricing_plan_resolver__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../../shared/fleio-api/cloud/pricing-plan/pricing-plan.resolver */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plan.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_pricing_plan_pricing_plan_create_options_resolver__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../../shared/fleio-api/cloud/pricing-plan/pricing-plan-create-options.resolver */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plan-create-options.resolver.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../../shared/ui-api/interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");












const routes = [
    {
        path: '',
        component: _openstack_plan_list_openstack_plan_list_component__WEBPACK_IMPORTED_MODULE_3__["OpenstackPlanListComponent"],
        resolve: {
            pricingPlans: _shared_fleio_api_cloud_pricing_plan_pricing_plan_list_resolver__WEBPACK_IMPORTED_MODULE_7__["PricingPlanListResolver"],
            createOptions: _shared_fleio_api_cloud_pricing_plan_pricing_plan_create_options_resolver__WEBPACK_IMPORTED_MODULE_9__["PricingPlanCreateOptionsResolver"],
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_11__["AuthGuard"]],
        data: {
            config: {
                feature: 'openstack.plans',
                search: {
                    show: true,
                    placeholder: 'Search plans ...',
                },
                ordering: {
                    default: {
                        field: 'name',
                        display: 'Name',
                        direction: _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_10__["OrderingDirection"].Descending
                    },
                    options: [
                        {
                            field: 'name',
                            display: 'Name'
                        },
                        {
                            field: 'currency',
                            display: 'Currency'
                        },
                    ],
                },
                subheader: {
                    objectName: 'openstack plan',
                    objectNamePlural: 'openstack plans',
                    objectList(data) {
                        return data.pricingPlans;
                    }
                },
                getBreadCrumbDetail: () => {
                    return 'Openstack plans';
                },
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: 'create',
        component: _openstack_plan_create_openstack_plan_create_component__WEBPACK_IMPORTED_MODULE_6__["OpenstackPlanCreateComponent"],
        resolve: {
            createOptions: _shared_fleio_api_cloud_pricing_plan_pricing_plan_create_options_resolver__WEBPACK_IMPORTED_MODULE_9__["PricingPlanCreateOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: () => {
                    return 'Create new pricing plan';
                },
            },
        },
    },
    {
        path: ':id',
        component: _openstack_plan_details_openstack_plan_details_component__WEBPACK_IMPORTED_MODULE_4__["OpenstackPlanDetailsComponent"],
        resolve: {
            pricingPlan: _shared_fleio_api_cloud_pricing_plan_pricing_plan_resolver__WEBPACK_IMPORTED_MODULE_8__["PricingPlanResolver"]
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return `Pricing plan ${data.pricingPlan.name}`;
                },
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: ':id/edit',
        component: _openstack_plan_edit_openstack_plan_edit_component__WEBPACK_IMPORTED_MODULE_5__["OpenstackPlanEditComponent"],
        resolve: {
            pricingPlan: _shared_fleio_api_cloud_pricing_plan_pricing_plan_resolver__WEBPACK_IMPORTED_MODULE_8__["PricingPlanResolver"],
            createOptions: _shared_fleio_api_cloud_pricing_plan_pricing_plan_create_options_resolver__WEBPACK_IMPORTED_MODULE_9__["PricingPlanCreateOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return `Edit pricing plan ${data.pricingPlan.name}`;
                },
            },
        },
    },
];
let OpenstackPlansRoutingModule = class OpenstackPlansRoutingModule {
};
OpenstackPlansRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], OpenstackPlansRoutingModule);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plans.module.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/openstack-plans.module.ts ***!
  \***********************************************************************************/
/*! exports provided: OpenstackPlansModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OpenstackPlansModule", function() { return OpenstackPlansModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _openstack_plans_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./openstack-plans-routing.module */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plans-routing.module.ts");
/* harmony import */ var _openstack_plan_list_openstack_plan_list_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./openstack-plan-list/openstack-plan-list.component */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list/openstack-plan-list.component.ts");
/* harmony import */ var _openstack_plan_details_openstack_plan_details_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./openstack-plan-details/openstack-plan-details.component */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-details/openstack-plan-details.component.ts");
/* harmony import */ var _openstack_plan_create_openstack_plan_create_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./openstack-plan-create/openstack-plan-create.component */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-create/openstack-plan-create.component.ts");
/* harmony import */ var _openstack_plan_edit_openstack_plan_edit_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./openstack-plan-edit/openstack-plan-edit.component */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-edit/openstack-plan-edit.component.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _tabs_pricing_plan_details_overview_pricing_plan_details_overview_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/pricing-plan-details-overview/pricing-plan-details-overview.component */ "./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-details-overview/pricing-plan-details-overview.component.ts");
/* harmony import */ var _tabs_pricing_plan_edit_form_pricing_plan_edit_form_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/pricing-plan-edit-form/pricing-plan-edit-form.component */ "./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-edit-form/pricing-plan-edit-form.component.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm2015/select.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm2015/checkbox.js");
/* harmony import */ var _dialogs_pricing_plan_delete_pricing_plan_delete_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./dialogs/pricing-plan-delete/pricing-plan-delete.component */ "./src/app/reseller/settings/cloud/openstack-plans/dialogs/pricing-plan-delete/pricing-plan-delete.component.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm2015/button.js");
/* harmony import */ var _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./openstack-plan-list-ui.service */ "./src/app/reseller/settings/cloud/openstack-plans/openstack-plan-list-ui.service.ts");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @angular/material/table */ "./node_modules/@angular/material/esm2015/table.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! @angular/material/icon */ "./node_modules/@angular/material/esm2015/icon.js");
























let OpenstackPlansModule = class OpenstackPlansModule {
};
OpenstackPlansModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _openstack_plan_list_openstack_plan_list_component__WEBPACK_IMPORTED_MODULE_4__["OpenstackPlanListComponent"],
            _openstack_plan_details_openstack_plan_details_component__WEBPACK_IMPORTED_MODULE_5__["OpenstackPlanDetailsComponent"],
            _openstack_plan_create_openstack_plan_create_component__WEBPACK_IMPORTED_MODULE_6__["OpenstackPlanCreateComponent"],
            _openstack_plan_edit_openstack_plan_edit_component__WEBPACK_IMPORTED_MODULE_7__["OpenstackPlanEditComponent"],
            _tabs_pricing_plan_details_overview_pricing_plan_details_overview_component__WEBPACK_IMPORTED_MODULE_9__["PricingPlanDetailsOverviewComponent"],
            _tabs_pricing_plan_edit_form_pricing_plan_edit_form_component__WEBPACK_IMPORTED_MODULE_10__["PricingPlanEditFormComponent"],
            _dialogs_pricing_plan_delete_pricing_plan_delete_component__WEBPACK_IMPORTED_MODULE_17__["PricingPlanDeleteComponent"],
        ],
        entryComponents: [
            _tabs_pricing_plan_details_overview_pricing_plan_details_overview_component__WEBPACK_IMPORTED_MODULE_9__["PricingPlanDetailsOverviewComponent"],
            _tabs_pricing_plan_edit_form_pricing_plan_edit_form_component__WEBPACK_IMPORTED_MODULE_10__["PricingPlanEditFormComponent"],
            _dialogs_pricing_plan_delete_pricing_plan_delete_component__WEBPACK_IMPORTED_MODULE_17__["PricingPlanDeleteComponent"],
        ],
        exports: [
            _dialogs_pricing_plan_delete_pricing_plan_delete_component__WEBPACK_IMPORTED_MODULE_17__["PricingPlanDeleteComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _openstack_plans_routing_module__WEBPACK_IMPORTED_MODULE_3__["OpenstackPlansRoutingModule"],
            _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_8__["ObjectsViewModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_11__["ReactiveFormsModule"],
            _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_12__["ErrorHandlingModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_13__["MatFormFieldModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_14__["MatSelectModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_15__["MatInputModule"],
            _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_16__["MatCheckboxModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_18__["MatDialogModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_19__["MatButtonModule"],
            _angular_material_table__WEBPACK_IMPORTED_MODULE_21__["MatTableModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_22__["FlexModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_23__["MatIconModule"],
        ],
        providers: [
            {
                provide: _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_20__["PricingPlanListUIService"],
                useClass: _openstack_plan_list_ui_service__WEBPACK_IMPORTED_MODULE_20__["PricingPlanListUIService"],
                multi: false,
            },
        ]
    })
], OpenstackPlansModule);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-details-overview/pricing-plan-details-overview.component.scss":
/*!*****************************************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-details-overview/pricing-plan-details-overview.component.scss ***!
  \*****************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".create-new-rule-btn {\n  margin-bottom: 10px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL29wZW5zdGFjay1wbGFucy90YWJzL3ByaWNpbmctcGxhbi1kZXRhaWxzLW92ZXJ2aWV3L3ByaWNpbmctcGxhbi1kZXRhaWxzLW92ZXJ2aWV3LmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9yZXNlbGxlci9zZXR0aW5ncy9jbG91ZC9vcGVuc3RhY2stcGxhbnMvdGFicy9wcmljaW5nLXBsYW4tZGV0YWlscy1vdmVydmlldy9wcmljaW5nLXBsYW4tZGV0YWlscy1vdmVydmlldy5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLG1CQUFBO0FDQ0YiLCJmaWxlIjoic3JjL2FwcC9yZXNlbGxlci9zZXR0aW5ncy9jbG91ZC9vcGVuc3RhY2stcGxhbnMvdGFicy9wcmljaW5nLXBsYW4tZGV0YWlscy1vdmVydmlldy9wcmljaW5nLXBsYW4tZGV0YWlscy1vdmVydmlldy5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5jcmVhdGUtbmV3LXJ1bGUtYnRuIHtcbiAgbWFyZ2luLWJvdHRvbTogMTBweDtcbn1cbiIsIi5jcmVhdGUtbmV3LXJ1bGUtYnRuIHtcbiAgbWFyZ2luLWJvdHRvbTogMTBweDtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-details-overview/pricing-plan-details-overview.component.ts":
/*!***************************************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-details-overview/pricing-plan-details-overview.component.ts ***!
  \***************************************************************************************************************************************/
/*! exports provided: PricingPlanDetailsOverviewComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingPlanDetailsOverviewComponent", function() { return PricingPlanDetailsOverviewComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../../shared/ui/objects-view/details-component-base */ "./src/app/shared/ui/objects-view/details-component-base.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../../shared/ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_pricing_rule_pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../../shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service */ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");








let PricingPlanDetailsOverviewComponent = class PricingPlanDetailsOverviewComponent extends _shared_ui_objects_view_details_component_base__WEBPACK_IMPORTED_MODULE_2__["DetailsComponentBase"] {
    constructor(config, notificationService, pricingRulesApiService, router, route) {
        super();
        this.config = config;
        this.notificationService = notificationService;
        this.pricingRulesApiService = pricingRulesApiService;
        this.router = router;
        this.route = route;
        this.displayedColumns = ['display_name', 'resource_name', 'price', 'actions'];
    }
    deletePricingRule(id) {
        let dialogResult$;
        dialogResult$ = this.notificationService.confirmDialog({
            title: 'Delete pricing rule?',
            message: 'Deleting the princing rule will apply to all calculated costs',
        });
        dialogResult$.subscribe(dialogResult => {
            if (dialogResult === 'yes') {
                this.pricingRulesApiService.delete(id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["map"])(success => {
                    if (success) {
                        this.notificationService.showMessage('Successfully deleted price rule.');
                        const queryParams = {};
                        Object.assign(queryParams, this.route.snapshot.queryParams);
                        this.router.navigate([], {
                            relativeTo: this.route,
                            queryParams
                        }).catch(() => {
                            // TODO: handle navigation error
                        });
                    }
                    else {
                        this.notificationService.showMessage('Could not delete price rule.');
                    }
                })).subscribe();
            }
        });
    }
    ngOnInit() {
    }
};
PricingPlanDetailsOverviewComponent.ctorParameters = () => [
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_ui_api_notification_service__WEBPACK_IMPORTED_MODULE_4__["NotificationService"] },
    { type: _shared_fleio_api_cloud_pricing_rule_pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_5__["PricingRulesApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["Router"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["ActivatedRoute"] }
];
PricingPlanDetailsOverviewComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-pricing-plan-details-overview',
        template: __webpack_require__(/*! raw-loader!./pricing-plan-details-overview.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-details-overview/pricing-plan-details-overview.component.html"),
        styles: [__webpack_require__(/*! ./pricing-plan-details-overview.component.scss */ "./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-details-overview/pricing-plan-details-overview.component.scss")]
    })
], PricingPlanDetailsOverviewComponent);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-edit-form/pricing-plan-edit-form.component.scss":
/*!***************************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-edit-form/pricing-plan-edit-form.component.scss ***!
  \***************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL29wZW5zdGFjay1wbGFucy90YWJzL3ByaWNpbmctcGxhbi1lZGl0LWZvcm0vcHJpY2luZy1wbGFuLWVkaXQtZm9ybS5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-edit-form/pricing-plan-edit-form.component.ts":
/*!*************************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-edit-form/pricing-plan-edit-form.component.ts ***!
  \*************************************************************************************************************************/
/*! exports provided: PricingPlanEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingPlanEditFormComponent", function() { return PricingPlanEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _shared_fleio_api_cloud_pricing_plan_pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../../shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");








let PricingPlanEditFormComponent = class PricingPlanEditFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_4__["DetailsFormBase"] {
    constructor(formBuilder, activatedRoute, config, pricingPlansApi, router) {
        super();
        this.formBuilder = formBuilder;
        this.activatedRoute = activatedRoute;
        this.config = config;
        this.pricingPlansApi = pricingPlansApi;
        this.router = router;
        this.pricingPlanForm = this.formBuilder.group({
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            currency: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            is_default: [false],
            other_default: [''],
        });
        this.initialDefault = false;
        this.isDefault = this.pricingPlanForm.controls.is_default;
    }
    ngOnInit() {
        this.createOptions = this.activatedRoute.snapshot.data.createOptions;
        this.objectController.actionCallback = () => this.savePlan();
        this.pricingPlanForm.patchValue(this.object);
        if (this.object) {
            this.initialDefault = !!this.object.is_default;
        }
    }
    ngAfterViewInit() {
    }
    savePlan() {
        const value = this.pricingPlanForm.value;
        this.createOrUpdate(this.pricingPlansApi, value).subscribe(() => {
            this.router.navigateByUrl(this.config.getPrevUrl('settings/openstack-plans')).catch(() => { });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_5__["of"])(null);
    }
};
PricingPlanEditFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_7__["ConfigService"] },
    { type: _shared_fleio_api_cloud_pricing_plan_pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_6__["PricingPlansApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] }
];
PricingPlanEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-pricing-plan-edit-form',
        template: __webpack_require__(/*! raw-loader!./pricing-plan-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-edit-form/pricing-plan-edit-form.component.html"),
        styles: [__webpack_require__(/*! ./pricing-plan-edit-form.component.scss */ "./src/app/reseller/settings/cloud/openstack-plans/tabs/pricing-plan-edit-form/pricing-plan-edit-form.component.scss")]
    })
], PricingPlanEditFormComponent);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plan-create-options.resolver.ts":
/*!*********************************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plan-create-options.resolver.ts ***!
  \*********************************************************************************************/
/*! exports provided: PricingPlanCreateOptionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingPlanCreateOptionsResolver", function() { return PricingPlanCreateOptionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./pricing-plans-api.service */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts");





let PricingPlanCreateOptionsResolver = class PricingPlanCreateOptionsResolver {
    constructor(pricingPlansApiService) {
        this.pricingPlansApiService = pricingPlansApiService;
    }
    resolve(route, state) {
        return this.pricingPlansApiService.createOptions()
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
PricingPlanCreateOptionsResolver.ctorParameters = () => [
    { type: _pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_4__["PricingPlansApiService"] }
];
PricingPlanCreateOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PricingPlanCreateOptionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plan-list.resolver.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plan-list.resolver.ts ***!
  \***********************************************************************************/
/*! exports provided: PricingPlanListResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingPlanListResolver", function() { return PricingPlanListResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./pricing-plans-api.service */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts");





let PricingPlanListResolver = class PricingPlanListResolver {
    constructor(pricingPlansApiService) {
        this.pricingPlansApiService = pricingPlansApiService;
    }
    resolve(route, state) {
        return this.pricingPlansApiService.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
PricingPlanListResolver.ctorParameters = () => [
    { type: _pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_4__["PricingPlansApiService"] }
];
PricingPlanListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PricingPlanListResolver);



/***/ })

}]);
//# sourceMappingURL=openstack-plans-openstack-plans-module-es2015.js.map