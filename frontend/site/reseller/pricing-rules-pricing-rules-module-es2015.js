(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["pricing-rules-pricing-rules-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-create/pricing-rule-create.component.html":
/*!****************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-create/pricing-rule-create.component.html ***!
  \****************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-edit/pricing-rule-edit.component.html":
/*!************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-edit/pricing-rule-edit.component.html ***!
  \************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-md']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/pricing-rules/tabs/pricing-rule-edit-form/pricing-rule-edit-form.component.html":
/*!***************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/cloud/pricing-rules/tabs/pricing-rule-edit-form/pricing-rule-edit-form.component.html ***!
  \***************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form [formGroup]=\"pricingRuleForm\">\n  <app-form-errors #formErrors [formGroup]=\"pricingRuleForm\"></app-form-errors>\n  <div fxLayout=\"row\">\n    <mat-form-field fxFlex=\"100\">\n      <mat-select formControlName=\"resource\" placeholder=\"Resource type\" required\n                  (selectionChange)=\"selectedResourceChanged()\">\n        <mat-option *ngFor=\"let resource of createOptions.resources\" [value]=\"resource.id\">{{resource.name}}\n        </mat-option>\n      </mat-select>\n      <mat-error>{{backendErrors['resource'] || 'This field is required!'}}</mat-error>\n    </mat-form-field>\n  </div>\n  <div fxLayout=\"row\">\n    <mat-form-field fxFlex=\"100\">\n      <mat-label>Name</mat-label>\n      <input matInput formControlName=\"display_name\" required type=\"text\">\n      <mat-error>{{backendErrors['display_name'] || 'This field is required!' }}</mat-error>\n    </mat-form-field>\n  </div>\n  <div fxLayout=\"row\" *ngIf=\"hasPricingAttribute()\">\n    <mat-form-field *ngIf=\"selectedResource && selectedResource.attribute_display\" fxFlex=\"33\">\n      <mat-select formControlName=\"attribute\"\n                  (selectionChange)=\"canSelectUnitForAttribute()\"\n                  placeholder=\"Attribute\" required>\n        <mat-option [value]=\"' '\">existence</mat-option>\n        <ng-container *ngFor=\"let attribute of attributes\">\n          <mat-option *ngIf=\"attribute.type === 'integer'\" [value]=\"attribute.name\">{{attribute.name}}</mat-option>\n        </ng-container>\n      </mat-select>\n      <mat-error>{{backendErrors['attribute'] || 'This field is required!'}}</mat-error>\n    </mat-form-field>\n    <mat-form-field *ngIf=\"selectedResource && selectedResource.attribute_display\" fxFlex=\"33\">\n      <mat-select formControlName=\"attribute_unit\"\n                  placeholder=\"Attribute unit\" required>\n        <ng-container *ngFor=\"let key of objectKeys(createOptions.attribute_units)\">\n          <mat-option [value]=\"key\">{{createOptions.attribute_units[key]}}</mat-option>\n        </ng-container>\n      </mat-select>\n      <mat-error>{{backendErrors['attribute_unit'] || 'This field is required!'}}</mat-error>\n    </mat-form-field>\n    <mat-form-field *ngIf=\"selectedResource && selectedResource.attribute_display\" fxFlex=\"33\">\n      <mat-select formControlName=\"time_unit\"\n                  placeholder=\"Time unit\" required>\n        <ng-container *ngFor=\"let key of objectKeys(createOptions.time_units)\">\n          <mat-option [value]=\"key\">{{createOptions.time_units[key]}}</mat-option>\n        </ng-container>\n      </mat-select>\n      <mat-error>{{backendErrors['time_unit'] || 'This field is required!'}}</mat-error>\n    </mat-form-field>\n  </div>\n\n  <div fxLayout=\"row\" *ngIf=\"selectedResource && selectedResource.metric_display\">\n    <mat-form-field fxFlex=\"100\">\n      <mat-select formControlName=\"attribute\"\n                  placeholder=\"Metric\" required>\n        <ng-container *ngFor=\"let metric of selectedResource.metrics\">\n          <mat-option [value]=\"metric.name\">{{metric.display_name}}</mat-option>\n        </ng-container>\n      </mat-select>\n      <mat-error>{{backendErrors['attribute'] || 'This field is required!'}}</mat-error>\n    </mat-form-field>\n  </div>\n  <div class=\"fl-margin-bottom\" fxLayout=\"row\"\n       *ngIf=\"selectedResource && selectedResource.metric_display && getMetricHelpText()\">\n    {{getMetricHelpText()}}\n  </div>\n  <div fxLayout=\"row\" *ngIf=\"selectedResource && selectedResource.metric_display\" class=\"fl-margin-bottom\">\n    <span class=\"pr-header\">Pricing:</span>\n    <mat-radio-group\n      aria-labelledby=\"rate_type\"\n      (change)=\"resetPrices()\"\n      [(ngModel)]=\"rateType\"\n      [ngModelOptions]=\"{standalone: true}\">\n      <mat-radio-button class=\"rate-type-radio-btns\" [color]=\"'primary'\" [value]=\"'flat'\">\n        Flat\n      </mat-radio-button>\n      <mat-radio-button class=\"rate-type-radio-btns\" [color]=\"'primary'\" [value]=\"'tiered'\">\n        Tiered\n      </mat-radio-button>\n    </mat-radio-group>\n  </div>\n  <div formGroupName=\"pricing\">\n    <div formArrayName=\"prices\" fxLayout=\"row\"\n      *ngFor=\"let item of pricingRuleForm.get('pricing').get('prices').controls; let i = index;\">\n        <div [formGroupName]=\"i\" [fxFlex]=\"rateType === 'flat' ? 25 : 100\">\n          <mat-form-field *ngIf=\"rateType !== 'flat'\" fxFlex=\"97\">\n            <mat-label>From</mat-label>\n            <input (change)=\"reCalculateTiers()\" matInput formControlName=\"f\" placeholder=\"From\" type=\"number\" required>\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <mat-form-field *ngIf=\"rateType !== 'flat'\" fxFlex=\"97\" fxFlexOffset=\"3\">\n            <mat-label>To</mat-label>\n            <input matInput formControlName=\"t\" placeholder=\"To\" type=\"text\">\n          </mat-form-field>\n          <mat-form-field fxFlex=\"100\" [fxFlexOffset]=\"rateType === 'flat' ? 0 : 3\">\n            <mat-label>Price ({{pricingPlan ? pricingPlan.currency : ''}})</mat-label>\n            <input matInput formControlName=\"p\" type=\"number\" required>\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <div *ngIf=\"rateType !== 'flat'\">\n            <button (click)=\"removeTier(i)\" class=\"fl-margin-top-medium\" fl-tooltip=\"Remove tier\" mat-icon-button>\n              <mat-icon>delete</mat-icon>\n            </button>\n          </div>\n        </div>\n    </div>\n    <mat-error class=\"fl-margin-bottom\">{{backendErrors['pricing']}}</mat-error>\n  </div>\n  <div *ngIf=\"rateType !== 'flat'\" class=\"fl-margin-bottom\">\n    <button mat-mini-fab class=\"add-item-button\" fl-tooltip=\"Add tier\" fl-tooltip-direction=\"right\" (click)=\"addTier()\">\n      <mat-icon>add</mat-icon>\n    </button>\n  </div>\n\n  <div *ngIf=\"selectedResource && (selectedResource.attribute_display || selectedResource.type === 'internal')\"\n       fxLayout=\"row\" class=\"fl-margin-bottom\">\n    <span class=\"pr-header\">Filters</span>\n  </div>\n\n  <ng-container *ngIf=\"selectedResource && (selectedResource.attribute_display || selectedResource.type === 'internal')\">\n    <div formArrayName=\"conditions\" fxLayout=\"row\"\n      *ngFor=\"let item of pricingRuleForm.get('conditions').controls; let i = index;\">\n        <div [formGroupName]=\"i\" fxFlex=\"100\">\n          <mat-form-field fxFlex=\"97\">\n            <mat-select formControlName=\"attribute\"\n                        (selectionChange)=\"filterAttributeChanged(i)\"\n                        placeholder=\"Attribute name\" required>\n              <mat-option *ngFor=\"let attribute of attributes\" [value]=\"attribute.name\">{{attribute.name}}</mat-option>\n            </mat-select>\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <mat-form-field fxFlex=\"97\" fxFlexOffset=\"3\">\n            <mat-select formControlName=\"operator\"\n                        placeholder=\"Operator\" required>\n              <mat-option\n                *ngFor=\"let key of objectKeys(getOperatorsForAttribute(pricingRuleForm.get('conditions').controls[i].value.attribute))\"\n                [value]=\"key\">\n                {{getOperatorsForAttribute(pricingRuleForm.get('conditions').controls[i].value.attribute)[key]}}\n              </mat-option>\n            </mat-select>\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <mat-form-field fxFlex=\"97\" fxFlexOffset=\"3\"\n                          *ngIf=\"getFilterValueInputType(\n                            pricingRuleForm.get('conditions').controls[i].value.attribute\n                          ) === 'choices'\">\n            <mat-select formControlName=\"value\"\n                        placeholder=\"Value\" required>\n              <mat-option\n                *ngFor=\"let item of getAttributeByAttributeName(\n                  pricingRuleForm.get('conditions').controls[i].value.attribute\n                ).choices\"\n                [value]=\"item\">\n                {{item}}\n              </mat-option>\n            </mat-select>\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <mat-form-field fxFlex=\"97\" fxFlexOffset=\"3\"\n                          *ngIf=\"getFilterValueInputType(\n                            pricingRuleForm.get('conditions').controls[i].value.attribute\n                          ) === 'textarea'\">\n            <textarea matInput formControlName=\"value\" placeholder=\"Value\"></textarea>\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <mat-form-field fxFlex=\"97\" fxFlexOffset=\"3\"\n                          *ngIf=\"getFilterValueInputType(\n                            pricingRuleForm.get('conditions').controls[i].value.attribute\n                          ) === 'number'\">\n            <input matInput formControlName=\"value\" placeholder=\"Value\" type=\"number\">\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <mat-form-field fxFlex=\"97\" fxFlexOffset=\"3\"\n                          *ngIf=\"getFilterValueInputType(\n                            pricingRuleForm.get('conditions').controls[i].value.attribute\n                          ) === 'datetime'\">\n            <input matInput [matDatepicker]=\"picker\" formControlName=\"value\" placeholder=\"Choose a date\">\n            <mat-datepicker-toggle matSuffix [for]=\"picker\"></mat-datepicker-toggle>\n            <mat-datepicker #picker></mat-datepicker>\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <mat-form-field fxFlex=\"97\" fxFlexOffset=\"3\"\n                          *ngIf=\"showAttributeUnitForFiltersModifiers(\n                            pricingRuleForm.get('conditions').controls[i].value.attribute\n                          )\">\n            <mat-select formControlName=\"attribute_unit\"\n                        placeholder=\"Attribute unit\" required>\n              <mat-option\n                *ngFor=\"let key of objectKeys(createOptions.attribute_units)\"\n                [value]=\"key\">\n                {{createOptions.attribute_units[key]}}\n              </mat-option>\n            </mat-select>\n            <mat-error>{{'This field is required!'}}</mat-error>\n          </mat-form-field>\n          <div>\n            <button (click)=\"removeFilter(i)\" class=\"fl-margin-top-medium\" fl-tooltip=\"Remove filter\" mat-icon-button>\n              <mat-icon>delete</mat-icon>\n            </button>\n          </div>\n        </div>\n    </div>\n  </ng-container>\n\n  <div fxLayout=\"row\"\n       *ngIf=\"selectedResource && (selectedResource.attribute_display || selectedResource.type === 'internal')\">\n    <button mat-mini-fab class=\"add-item-button\" fl-tooltip=\"Add filter\" fl-tooltip-direction=\"right\"\n            (click)=\"addFilter()\">\n      <mat-icon>add</mat-icon>\n    </button>\n  </div>\n\n  <!-- MODIFIERS -->\n  <div fxLayout=\"row\" class=\"fl-margin-top fl-margin-bottom\"\n  *ngIf=\"selectedResource && selectedResource.attribute_display\">\n    <span class=\"pr-header\">Price modifiers</span>\n  </div>\n\n  <ng-container *ngIf=\"selectedResource && selectedResource.attribute_display\">\n    <div formArrayName=\"modifiers\"\n      *ngFor=\"let item of pricingRuleForm.get('modifiers').controls; let i = index;\">\n        <div [formGroupName]=\"i\" fxFlex=\"100\">\n          <div fxLayout=\"row\">\n            <mat-form-field fxFlex=\"20\">\n              <input matInput formControlName=\"name\" placeholder=\"Name\" type=\"text\">\n              <mat-error>{{'This field is required!'}}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"15\" fxFlexOffset=\"3\">\n              <mat-select formControlName=\"attribute\"\n                          (selectionChange)=\"modifierAttributeChanged(i)\"\n                          placeholder=\"Attribute name\" required>\n                <mat-option *ngFor=\"let attribute of attributes\" [value]=\"attribute.name\">{{attribute.name}}</mat-option>\n              </mat-select>\n              <mat-error>{{'This field is required!'}}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"15\" fxFlexOffset=\"3\">\n              <mat-select formControlName=\"operator\"\n                          placeholder=\"Operator\" required>\n                <mat-option\n                  *ngFor=\"let key of objectKeys(getOperatorsForAttribute(pricingRuleForm.get('modifiers').controls[i].value.attribute))\"\n                  [value]=\"key\">\n                  {{getOperatorsForAttribute(pricingRuleForm.get('modifiers').controls[i].value.attribute)[key]}}\n                </mat-option>\n              </mat-select>\n              <mat-error>{{'This field is required!'}}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"15\" fxFlexOffset=\"3\"\n                            *ngIf=\"getFilterValueInputType(\n                              pricingRuleForm.get('modifiers').controls[i].value.attribute\n                            ) === 'choices'\">\n              <mat-select formControlName=\"value\"\n                          placeholder=\"Value\" required>\n                <mat-option\n                  *ngFor=\"let item of getAttributeByAttributeName(\n                    pricingRuleForm.get('modifiers').controls[i].value.attribute\n                  ).choices\"\n                  [value]=\"item\">\n                  {{item}}\n                </mat-option>\n              </mat-select>\n              <mat-error>{{'This field is required!'}}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"15\" fxFlexOffset=\"3\"\n                            *ngIf=\"getFilterValueInputType(\n                              pricingRuleForm.get('modifiers').controls[i].value.attribute\n                            ) === 'textarea'\">\n              <textarea matInput formControlName=\"value\" placeholder=\"Value\"></textarea>\n              <mat-error>{{'This field is required!'}}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"15\" fxFlexOffset=\"3\"\n                            *ngIf=\"getFilterValueInputType(\n                              pricingRuleForm.get('modifiers').controls[i].value.attribute\n                            ) === 'number'\">\n              <input matInput formControlName=\"value\" placeholder=\"Value\" type=\"number\">\n              <mat-error>{{'This field is required!'}}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"15\" fxFlexOffset=\"3\"\n                            *ngIf=\"getFilterValueInputType(\n                              pricingRuleForm.get('modifiers').controls[i].value.attribute\n                            ) === 'datetime'\">\n              <input matInput [matDatepicker]=\"picker\" formControlName=\"value\" placeholder=\"Choose a date\">\n              <mat-datepicker-toggle matSuffix [for]=\"picker\"></mat-datepicker-toggle>\n              <mat-datepicker #picker></mat-datepicker>\n              <mat-error>{{'This field is required!'}}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"15\" fxFlexOffset=\"3\"\n                            *ngIf=\"showAttributeUnitForFiltersModifiers(\n                              pricingRuleForm.get('modifiers').controls[i].value.attribute\n                            )\">\n              <mat-select formControlName=\"attribute_unit\"\n                          placeholder=\"Attribute unit\" required>\n                <mat-option\n                  *ngFor=\"let key of objectKeys(createOptions.attribute_units)\"\n                  [value]=\"key\">\n                  {{createOptions.attribute_units[key]}}\n                </mat-option>\n              </mat-select>\n              <mat-error>{{'This field is required!'}}</mat-error>\n            </mat-form-field>\n            <div>\n              <button (click)=\"removeModifier(i)\" class=\"fl-margin-top-medium\"\n                      fl-tooltip=\"Remove modifier\" mat-icon-button>\n                <mat-icon>delete</mat-icon>\n              </button>\n            </div>\n          </div>\n          <div fxLayout=\"row\">\n            <mat-checkbox [color]=\"'primary'\" fxFlex=\"20\" formControlName=\"price_is_percent\">\n              Price is percent\n            </mat-checkbox>\n          </div>\n          <div fxLayout=\"row\" class=\"fl-margin-top-small\">\n            <mat-form-field fxFlex=\"20\" *ngIf=\"pricingPlan\">\n              <input matInput formControlName=\"price\"\n                     placeholder=\"{{pricingRuleForm.get('modifiers').controls[i].value.price_is_percent ?\n                     'Percent (%)' : 'Price (' + pricingPlan.currency +')'}}\"\n                     type=\"number\">\n              <mat-error>{{'This field is required!'}}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"20\" fxFlexOffset=\"3\"\n                            *ngIf=\"!pricingRuleForm.get('modifiers').controls[i].value.price_is_percent\">\n              <mat-select formControlName=\"time_unit\"\n                          placeholder=\"Time unit\" required>\n                <mat-option\n                  *ngFor=\"let key of objectKeys(createOptions.time_units)\"\n                  [value]=\"key\">\n                  {{createOptions.time_units[key]}}\n                </mat-option>\n              </mat-select>\n              <mat-error>{{'This field is required!'}}</mat-error>\n            </mat-form-field>\n          </div>\n        </div>\n    </div>\n  </ng-container>\n\n  <div fxLayout=\"row\" *ngIf=\"selectedResource && selectedResource.attribute_display\" class=\"fl-margin-top\">\n    <button mat-mini-fab class=\"add-item-button\" fl-tooltip=\"Add price modifier\" fl-tooltip-direction=\"right\"\n            (click)=\"addModifier()\">\n      <mat-icon>add</mat-icon>\n    </button>\n  </div>\n\n\n</form>\n"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-create/pricing-rule-create.component.scss":
/*!**************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-create/pricing-rule-create.component.scss ***!
  \**************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL3ByaWNpbmctcnVsZXMvcHJpY2luZy1ydWxlLWNyZWF0ZS9wcmljaW5nLXJ1bGUtY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-create/pricing-rule-create.component.ts":
/*!************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-create/pricing-rule-create.component.ts ***!
  \************************************************************************************************************/
/*! exports provided: PricingRuleCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRuleCreateComponent", function() { return PricingRuleCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _pricing_rule_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../pricing-rule-list-ui.service */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-list-ui.service.ts");





let PricingRuleCreateComponent = class PricingRuleCreateComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, pricingRuleListUIService) {
        super(route, pricingRuleListUIService, 'create', null);
    }
};
PricingRuleCreateComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _pricing_rule_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["PricingRuleListUIService"] }
];
PricingRuleCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-pricing-rule-create',
        template: __webpack_require__(/*! raw-loader!./pricing-rule-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-create/pricing-rule-create.component.html"),
        styles: [__webpack_require__(/*! ./pricing-rule-create.component.scss */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-create/pricing-rule-create.component.scss")]
    })
], PricingRuleCreateComponent);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-edit/pricing-rule-edit.component.scss":
/*!**********************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-edit/pricing-rule-edit.component.scss ***!
  \**********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL3ByaWNpbmctcnVsZXMvcHJpY2luZy1ydWxlLWVkaXQvcHJpY2luZy1ydWxlLWVkaXQuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-edit/pricing-rule-edit.component.ts":
/*!********************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-edit/pricing-rule-edit.component.ts ***!
  \********************************************************************************************************/
/*! exports provided: PricingRuleEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRuleEditComponent", function() { return PricingRuleEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _pricing_rule_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../pricing-rule-list-ui.service */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-list-ui.service.ts");





let PricingRuleEditComponent = class PricingRuleEditComponent extends _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"] {
    constructor(route, pricingRuleListUIService) {
        super(route, pricingRuleListUIService, 'edit', 'pricingRule');
    }
};
PricingRuleEditComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _pricing_rule_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["PricingRuleListUIService"] }
];
PricingRuleEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-pricing-rule-edit',
        template: __webpack_require__(/*! raw-loader!./pricing-rule-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-edit/pricing-rule-edit.component.html"),
        styles: [__webpack_require__(/*! ./pricing-rule-edit.component.scss */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-edit/pricing-rule-edit.component.scss")]
    })
], PricingRuleEditComponent);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-list-ui.service.ts":
/*!***************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-list-ui.service.ts ***!
  \***************************************************************************************/
/*! exports provided: PricingRuleListUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRuleListUIService", function() { return PricingRuleListUIService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");
/* harmony import */ var _pricing_rule_ui_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./pricing-rule-ui.service */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-ui.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_pricing_rule_pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../../shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service */ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service.ts");









let PricingRuleListUIService = class PricingRuleListUIService {
    constructor(router, config, pricingRulesApiService, matDialog) {
        this.router = router;
        this.config = config;
        this.pricingRulesApiService = pricingRulesApiService;
        this.matDialog = matDialog;
    }
    getObjectUIService(object, permissions, state) {
        return new _pricing_rule_ui_service__WEBPACK_IMPORTED_MODULE_7__["PricingRuleUIService"](object, permissions, state, this.router, this.config, this.pricingRulesApiService, this.matDialog);
    }
    getTableData(objectList) {
        const tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Name', enableSort: true, fieldName: 'display_name' },
                ],
                columnNames: ['display_name'],
                statusColumn: 'display_name',
            },
            rows: [],
        };
        for (const object of objectList.objects) {
            const row = {
                cells: {
                    name: { text: object.display_name },
                },
            };
            const rowUIService = this.getObjectUIService(object, objectList.permissions, 'table-view');
            row.icon = rowUIService.getIcon();
            row.status = rowUIService.getStatus();
            tableData.rows.push(row);
        }
        return tableData;
    }
    getActions(objectList) {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__["RouterLinkAction"]({
                name: 'Create new pricing rule',
                tooltip: 'Create new pricing rule',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('settings/pricing-rules/create')
            })
        ];
    }
};
PricingRuleListUIService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
    { type: _shared_fleio_api_cloud_pricing_rule_pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_8__["PricingRulesApiService"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_6__["MatDialog"] }
];
PricingRuleListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root',
    })
], PricingRuleListUIService);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-ui.service.ts":
/*!**********************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-ui.service.ts ***!
  \**********************************************************************************/
/*! exports provided: PricingRuleUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRuleUIService", function() { return PricingRuleUIService; });
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");
/* harmony import */ var _tabs_pricing_rule_edit_form_pricing_rule_edit_form_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./tabs/pricing-rule-edit-form/pricing-rule-edit-form.component */ "./src/app/reseller/settings/cloud/pricing-rules/tabs/pricing-rule-edit-form/pricing-rule-edit-form.component.ts");
/* harmony import */ var _shared_fleio_api_cloud_pricing_rule_pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service */ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service.ts");








class PricingRuleUIService extends _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_0__["ObjectUIServiceBase"] {
    constructor(pricingRule, permissions, state, router, config, pricingRulesApiService, matDialog) {
        super(pricingRule, permissions, state);
        this.matDialog = matDialog;
        this.router = router;
        this.config = config;
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
                    text: `Pricing rule ${this.object.display_name}`,
                };
            case 'edit':
                return {
                    text: `Edit ${this.object.display_name}`,
                };
            case 'create':
                return {
                    text: 'Create pricing rule',
                };
            default:
                return {
                    text: `${this.object.display_name}`,
                };
        }
    }
    getActions() {
        const actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            name: 'Edit',
            routerUrl: this.config.getPanelUrl(`settings/pricing-rules/${this.object.id}/edit`),
            router: this.router,
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
                value: `${this.object.display_name}`
            },
        ];
        return fields;
    }
    getCardTags() {
        return [];
    }
    getTabs() {
        switch (this.state) {
            case 'details':
            case 'edit':
            case 'create':
                return [
                    {
                        tabName: 'Edit',
                        component: _tabs_pricing_rule_edit_form_pricing_rule_edit_form_component__WEBPACK_IMPORTED_MODULE_6__["PricingRuleEditFormComponent"],
                    },
                ];
        }
    }
    getDetailsActions() {
        const actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`settings/openstack-plans`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_4__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_3__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl(`settings/openstack-plans`),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_4__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    }
}
PricingRuleUIService.ctorParameters = () => [
    { type: undefined },
    { type: undefined },
    { type: String },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_1__["Router"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] },
    { type: _shared_fleio_api_cloud_pricing_rule_pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_7__["PricingRulesApiService"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_5__["MatDialog"] }
];


/***/ }),

/***/ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rules-routing.module.ts":
/*!***************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/pricing-rules/pricing-rules-routing.module.ts ***!
  \***************************************************************************************/
/*! exports provided: PricingRulesRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRulesRoutingModule", function() { return PricingRulesRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _pricing_rule_create_pricing_rule_create_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./pricing-rule-create/pricing-rule-create.component */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-create/pricing-rule-create.component.ts");
/* harmony import */ var _shared_fleio_api_cloud_pricing_rule_pricing_rule_create_options_resolver__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/fleio-api/cloud/pricing-rule/pricing-rule-create-options.resolver */ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rule-create-options.resolver.ts");
/* harmony import */ var _shared_fleio_api_cloud_pricing_plan_pricing_plan_resolver__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../shared/fleio-api/cloud/pricing-plan/pricing-plan.resolver */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plan.resolver.ts");
/* harmony import */ var _pricing_rule_edit_pricing_rule_edit_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./pricing-rule-edit/pricing-rule-edit.component */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-edit/pricing-rule-edit.component.ts");
/* harmony import */ var _shared_fleio_api_cloud_pricing_rule_pricing_rule_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../shared/fleio-api/cloud/pricing-rule/pricing-rule.resolver */ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rule.resolver.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");









const routes = [
    {
        path: 'create/:id',
        component: _pricing_rule_create_pricing_rule_create_component__WEBPACK_IMPORTED_MODULE_3__["PricingRuleCreateComponent"],
        resolve: {
            pricingPlan: _shared_fleio_api_cloud_pricing_plan_pricing_plan_resolver__WEBPACK_IMPORTED_MODULE_5__["PricingPlanResolver"],
            createOptions: _shared_fleio_api_cloud_pricing_rule_pricing_rule_create_options_resolver__WEBPACK_IMPORTED_MODULE_4__["PricingRuleCreateOptionsResolver"],
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_8__["AuthGuard"]],
        data: {
            config: {
                feature: 'openstack.plans',
                getBreadCrumbDetail: () => {
                    return 'Create new pricing rule';
                },
            },
        },
    },
    {
        path: ':id/edit',
        component: _pricing_rule_edit_pricing_rule_edit_component__WEBPACK_IMPORTED_MODULE_6__["PricingRuleEditComponent"],
        resolve: {
            pricingRule: _shared_fleio_api_cloud_pricing_rule_pricing_rule_resolver__WEBPACK_IMPORTED_MODULE_7__["PricingRuleResolver"],
            createOptions: _shared_fleio_api_cloud_pricing_rule_pricing_rule_create_options_resolver__WEBPACK_IMPORTED_MODULE_4__["PricingRuleCreateOptionsResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: (data) => {
                    return `Edit pricing rule ${data.pricingRule.display_name}`;
                },
            },
        },
    },
];
let PricingRulesRoutingModule = class PricingRulesRoutingModule {
};
PricingRulesRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
    })
], PricingRulesRoutingModule);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rules.module.ts":
/*!*******************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/pricing-rules/pricing-rules.module.ts ***!
  \*******************************************************************************/
/*! exports provided: PricingRulesModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRulesModule", function() { return PricingRulesModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _pricing_rule_create_pricing_rule_create_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./pricing-rule-create/pricing-rule-create.component */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-create/pricing-rule-create.component.ts");
/* harmony import */ var _tabs_pricing_rule_edit_form_pricing_rule_edit_form_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tabs/pricing-rule-edit-form/pricing-rule-edit-form.component */ "./src/app/reseller/settings/cloud/pricing-rules/tabs/pricing-rule-edit-form/pricing-rule-edit-form.component.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _pricing_rules_routing_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./pricing-rules-routing.module */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rules-routing.module.ts");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm2015/select.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _angular_material_radio__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/radio */ "./node_modules/@angular/material/esm2015/radio.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm2015/button.js");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/material/icon */ "./node_modules/@angular/material/esm2015/icon.js");
/* harmony import */ var _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/material/datepicker */ "./node_modules/@angular/material/esm2015/datepicker.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm2015/checkbox.js");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/divider */ "./node_modules/@angular/material/esm2015/divider.js");
/* harmony import */ var _pricing_rule_edit_pricing_rule_edit_component__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./pricing-rule-edit/pricing-rule-edit.component */ "./src/app/reseller/settings/cloud/pricing-rules/pricing-rule-edit/pricing-rule-edit.component.ts");




















let PricingRulesModule = class PricingRulesModule {
};
PricingRulesModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _pricing_rule_create_pricing_rule_create_component__WEBPACK_IMPORTED_MODULE_3__["PricingRuleCreateComponent"],
            _tabs_pricing_rule_edit_form_pricing_rule_edit_form_component__WEBPACK_IMPORTED_MODULE_4__["PricingRuleEditFormComponent"],
            _pricing_rule_edit_pricing_rule_edit_component__WEBPACK_IMPORTED_MODULE_19__["PricingRuleEditComponent"]
        ],
        entryComponents: [
            _tabs_pricing_rule_edit_form_pricing_rule_edit_form_component__WEBPACK_IMPORTED_MODULE_4__["PricingRuleEditFormComponent"]
        ],
        exports: [],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _pricing_rules_routing_module__WEBPACK_IMPORTED_MODULE_10__["PricingRulesRoutingModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatFormFieldModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_6__["MatInputModule"],
            _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_7__["ErrorHandlingModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_8__["ReactiveFormsModule"],
            _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_9__["ObjectsViewModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_11__["MatSelectModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_12__["FlexModule"],
            _angular_material_radio__WEBPACK_IMPORTED_MODULE_13__["MatRadioModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_8__["FormsModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_14__["MatButtonModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_15__["MatIconModule"],
            _angular_material_datepicker__WEBPACK_IMPORTED_MODULE_16__["MatDatepickerModule"],
            _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_17__["MatCheckboxModule"],
            _angular_material_divider__WEBPACK_IMPORTED_MODULE_18__["MatDividerModule"],
        ],
        providers: []
    })
], PricingRulesModule);



/***/ }),

/***/ "./src/app/reseller/settings/cloud/pricing-rules/tabs/pricing-rule-edit-form/pricing-rule-edit-form.component.scss":
/*!*************************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/pricing-rules/tabs/pricing-rule-edit-form/pricing-rule-edit-form.component.scss ***!
  \*************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".rate-type-radio-btns {\n  margin-left: 20px;\n}\n\n.pr-header {\n  font-size: 19px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL3ByaWNpbmctcnVsZXMvdGFicy9wcmljaW5nLXJ1bGUtZWRpdC1mb3JtL3ByaWNpbmctcnVsZS1lZGl0LWZvcm0uY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2Nsb3VkL3ByaWNpbmctcnVsZXMvdGFicy9wcmljaW5nLXJ1bGUtZWRpdC1mb3JtL3ByaWNpbmctcnVsZS1lZGl0LWZvcm0uY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxpQkFBQTtBQ0NGOztBREVBO0VBQ0UsZUFBQTtBQ0NGIiwiZmlsZSI6InNyYy9hcHAvcmVzZWxsZXIvc2V0dGluZ3MvY2xvdWQvcHJpY2luZy1ydWxlcy90YWJzL3ByaWNpbmctcnVsZS1lZGl0LWZvcm0vcHJpY2luZy1ydWxlLWVkaXQtZm9ybS5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbIi5yYXRlLXR5cGUtcmFkaW8tYnRucyB7XG4gIG1hcmdpbi1sZWZ0OiAyMHB4O1xufVxuXG4ucHItaGVhZGVyIHtcbiAgZm9udC1zaXplOiAxOXB4O1xufVxuIiwiLnJhdGUtdHlwZS1yYWRpby1idG5zIHtcbiAgbWFyZ2luLWxlZnQ6IDIwcHg7XG59XG5cbi5wci1oZWFkZXIge1xuICBmb250LXNpemU6IDE5cHg7XG59Il19 */"

/***/ }),

/***/ "./src/app/reseller/settings/cloud/pricing-rules/tabs/pricing-rule-edit-form/pricing-rule-edit-form.component.ts":
/*!***********************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/cloud/pricing-rules/tabs/pricing-rule-edit-form/pricing-rule-edit-form.component.ts ***!
  \***********************************************************************************************************************/
/*! exports provided: PricingRuleEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRuleEditFormComponent", function() { return PricingRuleEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _shared_fleio_api_cloud_pricing_rule_pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../../shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service */ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service.ts");
/* harmony import */ var _shared_fleio_api_cloud_pricing_plan_pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../../../../shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service */ "./src/app/shared/fleio-api/cloud/pricing-plan/pricing-plans-api.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");










let PricingRuleEditFormComponent = class PricingRuleEditFormComponent extends _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"] {
    constructor(formBuilder, activatedRoute, config, pricingRulesApiService, router, pricingPlanApi) {
        super();
        this.formBuilder = formBuilder;
        this.activatedRoute = activatedRoute;
        this.config = config;
        this.pricingRulesApiService = pricingRulesApiService;
        this.router = router;
        this.pricingPlanApi = pricingPlanApi;
        this.pricingRuleForm = this.formBuilder.group({
            display_name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            resource: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            attribute: [''],
            attribute_unit: [{ value: '', disabled: true }],
            time_unit: [''],
            pricing: this.formBuilder.group({
                prices: this.formBuilder.array([this.formBuilder.group({
                        f: 0,
                        p: [0, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
                        t: [{ value: '∞', disabled: true }]
                    })]),
            }),
            conditions: this.formBuilder.array([]),
            modifiers: this.formBuilder.array([])
        });
        this.attributes = [];
        this.selectedResource = null;
        this.objectKeys = Object.keys;
        this.rateType = 'flat';
    }
    createTier() {
        return this.formBuilder.group({
            f: 0,
            p: 0,
            t: [{ value: '∞', disabled: true }]
        });
    }
    createFilter() {
        return this.formBuilder.group({
            attribute: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            operator: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            value: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            attribute_unit: [null, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
        });
    }
    createModifier() {
        return this.formBuilder.group({
            attribute: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            operator: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            value: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            price: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            price_is_percent: [false, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            time_unit: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            attribute_unit: [null, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
        });
    }
    ngOnInit() {
        this.createOptions = this.activatedRoute.snapshot.data.createOptions;
        this.pricingPlan = this.activatedRoute.snapshot.data.pricingPlan;
        this.objectController.actionCallback = () => this.savePriceRule();
        // parse some fields in the json sent to backend, backend should be modified to accept params like they
        // are built in this form
        if (this.objectKeys(this.object).length) {
            this.pricingRuleForm.controls.resource.disable();
            const oldAttribute = this.object.pricing.attribute;
            const oldAttributeUnit = this.object.pricing.attribute_unit;
            const oldTimeUnit = this.object.pricing.time_unit;
            delete this.object.pricing.attribute;
            delete this.object.pricing.attribute_unit;
            delete this.object.pricing.time_unit;
            this.object.attribute = oldAttribute;
            this.object.attribute_unit = oldAttributeUnit;
            this.object.time_unit = oldTimeUnit;
            this.pricingRuleForm.patchValue(this.object);
            if (this.object && this.object.attribute === '') {
                this.pricingRuleForm.controls.attribute.setValue(' ');
            }
            const formModifiers = this.pricingRuleForm.get('modifiers');
            for (const modifier of this.object.modifiers) {
                formModifiers.push(this.formBuilder.group(modifier));
            }
            const formFilters = this.pricingRuleForm.get('conditions');
            for (const filter of this.object.conditions) {
                formFilters.push(this.formBuilder.group(filter));
            }
            const formPrices = this.pricingRuleForm.get('pricing').get('prices');
            formPrices.removeAt(0); // remove the initialization of prices from create page
            if (this.object.pricing.prices.length > 1) {
                this.rateType = 'tiered';
            }
            for (const price of this.object.pricing.prices) {
                formPrices.push(this.formBuilder.group(price));
            }
            if (this.rateType === 'tiered') {
                this.reCalculateTiers();
            }
            for (const resource of this.createOptions.resources) {
                if (resource.id === this.object.resource) {
                    this.selectedResource = resource;
                    this.attributes = this.selectedResource.attributes;
                    this.canSelectUnitForAttribute();
                }
            }
            this.pricingPlanApi.get(this.object.plan).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_9__["map"])(response => {
                this.pricingPlan = response;
            })).subscribe();
        }
    }
    ngAfterViewInit() {
    }
    savePriceRule() {
        const value = this.pricingRuleForm.getRawValue();
        // parse some fields in the json sent to backend, backend should be modified to accept params like they
        // are built in this form
        const attribute = value.attribute;
        const attributeUnit = value.attribute_unit || null;
        const timeUnit = value.time_unit;
        delete value.attribute;
        delete value.attribute_unit;
        delete value.time_unit;
        value.pricing.attribute = attribute;
        value.pricing.attribute_unit = attributeUnit;
        value.pricing.time_unit = timeUnit;
        value.plan = this.pricingPlan.id;
        this.createOrUpdate(this.pricingRulesApiService, value).subscribe(() => {
            this.router.navigateByUrl(this.config.getPanelUrl('settings/openstack-plans') + '/' + this.pricingPlan.id).catch(() => { });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_6__["of"])(null);
    }
    resetPrices() {
        const prices = this.pricingRuleForm.get('pricing').get('prices');
        while (prices.length) {
            prices.removeAt(0);
        }
        prices.push(this.createTier());
    }
    selectedResourceChanged() {
        this.selectedResource = this.createOptions.resources.find(x => x.id === this.pricingRuleForm.controls.resource.value);
        this.attributes = this.selectedResource.attributes;
        this.rateType = 'flat';
        this.resetPrices();
    }
    filterAttributeChanged(index) {
        // reset the operator and value after attribute changed in filter
        const filters = this.pricingRuleForm.get('conditions');
        const selectedFilter = filters.at(index);
        const oldAttribute = selectedFilter.value.attribute;
        filters.removeAt(index);
        filters.insert(index, this.formBuilder.group({
            attribute: [oldAttribute, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            operator: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            value: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            attribute_unit: [null],
        }));
    }
    modifierAttributeChanged(index) {
        // reset the operator and value after attribute changed in modifier
        const modifiers = this.pricingRuleForm.get('modifiers');
        const selectedFilter = modifiers.at(index);
        const oldAttribute = selectedFilter.value.attribute;
        const oldName = selectedFilter.value.name;
        const oldPrice = selectedFilter.value.price;
        const oldPriceAsPercent = selectedFilter.value.price_is_percent;
        const oldTimeUnit = selectedFilter.value.time_unit;
        modifiers.removeAt(index);
        modifiers.insert(index, this.formBuilder.group({
            attribute: [oldAttribute, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            name: [oldName, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            operator: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            value: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            attribute_unit: [null],
            price: [oldPrice, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            price_is_percent: [oldPriceAsPercent, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            time_unit: [oldTimeUnit, _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
        }));
    }
    hasPricingAttribute() {
        if (this.selectedResource && this.selectedResource.type === 'service') {
            for (const attribute of this.selectedResource.attributes) {
                if (attribute.type === 'integer') {
                    return true;
                }
            }
            return false;
        }
        return false;
    }
    canSelectUnitForAttribute() {
        if (this.selectedResource) {
            for (const attribute of this.selectedResource.attributes) {
                if (attribute.value_size && attribute.name === this.pricingRuleForm.controls.attribute.value) {
                    if (['k', 'm', 'g', 't', 'b', 'p', 'e'].indexOf(attribute.value_size)) {
                        return this.pricingRuleForm.controls.attribute_unit.enable();
                    }
                }
            }
            this.pricingRuleForm.controls.attribute_unit.setValue('');
            return this.pricingRuleForm.controls.attribute_unit.disable();
        }
        this.pricingRuleForm.controls.attribute_unit.setValue('');
        return this.pricingRuleForm.controls.attribute_unit.disable();
    }
    getMetricHelpText() {
        if (this.selectedResource) {
            for (const metric of this.selectedResource.metrics) {
                if (metric.name === this.pricingRuleForm.controls.attribute.value) {
                    return metric.help_text;
                }
            }
            return null;
        }
        return null;
    }
    addTier() {
        const prices = this.pricingRuleForm.get('pricing').get('prices');
        prices.push(this.createTier());
        this.reCalculateTiers();
    }
    addFilter() {
        const filters = this.pricingRuleForm.get('conditions');
        return filters.push(this.createFilter());
    }
    addModifier() {
        const modifiers = this.pricingRuleForm.get('modifiers');
        return modifiers.push(this.createModifier());
    }
    removeTier(index) {
        const prices = this.pricingRuleForm.get('pricing').get('prices');
        prices.removeAt(index);
        this.reCalculateTiers();
    }
    removeFilter(index) {
        const filters = this.pricingRuleForm.get('conditions');
        return filters.removeAt(index);
    }
    removeModifier(index) {
        const modifiers = this.pricingRuleForm.get('modifiers');
        return modifiers.removeAt(index);
    }
    reCalculateTiers() {
        // if a from field changed, re-calculate all tiers to be consecutive and have only one infinite
        const prices = this.pricingRuleForm.get('pricing').get('prices');
        // tslint:disable-next-line:prefer-for-of
        for (let tierToManipulateIndex = 0; tierToManipulateIndex < prices.length; tierToManipulateIndex++) {
            const oldFrom = prices.at(tierToManipulateIndex).value.f;
            const oldPrice = prices.at(tierToManipulateIndex).value.p;
            // tslint:disable-next-line:prefer-for-of
            const tierChanged = prices.at(tierToManipulateIndex).value;
            let nextMaxValue = 0;
            let toField = null;
            for (let tierToCompareWithIndex = 0; tierToCompareWithIndex < prices.length; tierToCompareWithIndex++) {
                if (prices.at(tierToCompareWithIndex).value.f > tierChanged.f &&
                    (nextMaxValue > prices.at(tierToCompareWithIndex).value.f || nextMaxValue === 0)) {
                    nextMaxValue = prices.at(tierToCompareWithIndex).value.f;
                }
            }
            if (nextMaxValue === 0) {
                toField = '∞';
            }
            else {
                toField = nextMaxValue;
            }
            prices.removeAt(tierToManipulateIndex);
            prices.insert(tierToManipulateIndex, this.formBuilder.group({
                f: oldFrom,
                p: oldPrice,
                t: [{ value: toField, disabled: true }]
            }));
        }
    }
    getAttributeByAttributeName(attributeName) {
        for (const attribute of this.selectedResource.attributes) {
            if (attribute.name === attributeName) {
                return attribute;
            }
        }
        return null;
    }
    getFilterValueInputType(attributeName) {
        const attribute = this.getAttributeByAttributeName(attributeName);
        if (attribute) {
            if (attribute.type === 'string' && !attribute.choices) {
                return 'textarea';
            }
            else if (attribute.type === 'integer' && !attribute.choices) {
                return 'number';
            }
            else if (attribute.type === 'datetime' && !attribute.choices) {
                return 'datetime';
            }
            else if (attribute.choices) {
                return 'choices';
            }
            return null;
        }
        return null;
    }
    showAttributeUnitForFiltersModifiers(attributeName) {
        const attribute = this.getAttributeByAttributeName(attributeName);
        if (attribute) {
            return (!attribute.choices && attribute.type === 'integer' &&
                ['k', 'm', 'g', 't', 'b', 'p', 'e'].indexOf(attribute.value_size) > -1);
        }
        return false;
    }
    getOperatorsForAttribute(selectedAttributeName) {
        const attribute = this.getAttributeByAttributeName(selectedAttributeName);
        if (attribute) {
            if (attribute.choices) {
                return { eq: 'Equal' };
            }
            else if (attribute.type === 'string') {
                return this.createOptions.string_operators;
            }
            else if (attribute.type === 'integer' || attribute.type === 'datetime') {
                return this.createOptions.number_operators;
            }
            else {
                return {};
            }
        }
        return {};
    }
};
PricingRuleEditFormComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] },
    { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
    { type: _shared_fleio_api_cloud_pricing_rule_pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_7__["PricingRulesApiService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _shared_fleio_api_cloud_pricing_plan_pricing_plans_api_service__WEBPACK_IMPORTED_MODULE_8__["PricingPlansApiService"] }
];
PricingRuleEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-pricing-rule-edit-form',
        template: __webpack_require__(/*! raw-loader!./pricing-rule-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/cloud/pricing-rules/tabs/pricing-rule-edit-form/pricing-rule-edit-form.component.html"),
        styles: [__webpack_require__(/*! ./pricing-rule-edit-form.component.scss */ "./src/app/reseller/settings/cloud/pricing-rules/tabs/pricing-rule-edit-form/pricing-rule-edit-form.component.scss")]
    })
], PricingRuleEditFormComponent);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rule-create-options.resolver.ts":
/*!*********************************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rule-create-options.resolver.ts ***!
  \*********************************************************************************************/
/*! exports provided: PricingRuleCreateOptionsResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRuleCreateOptionsResolver", function() { return PricingRuleCreateOptionsResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./pricing-rules-api.service */ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service.ts");





let PricingRuleCreateOptionsResolver = class PricingRuleCreateOptionsResolver {
    constructor(pricingRulesApiService) {
        this.pricingRulesApiService = pricingRulesApiService;
    }
    resolve(route, state) {
        return this.pricingRulesApiService.createOptions()
            .pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
PricingRuleCreateOptionsResolver.ctorParameters = () => [
    { type: _pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_4__["PricingRulesApiService"] }
];
PricingRuleCreateOptionsResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PricingRuleCreateOptionsResolver);



/***/ }),

/***/ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rule.resolver.ts":
/*!******************************************************************************!*\
  !*** ./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rule.resolver.ts ***!
  \******************************************************************************/
/*! exports provided: PricingRuleResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PricingRuleResolver", function() { return PricingRuleResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./pricing-rules-api.service */ "./src/app/shared/fleio-api/cloud/pricing-rule/pricing-rules-api.service.ts");





let PricingRuleResolver = class PricingRuleResolver {
    constructor(pricingRulesApiService) {
        this.pricingRulesApiService = pricingRulesApiService;
    }
    resolve(route, state) {
        return this.pricingRulesApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(() => Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null)));
    }
};
PricingRuleResolver.ctorParameters = () => [
    { type: _pricing_rules_api_service__WEBPACK_IMPORTED_MODULE_4__["PricingRulesApiService"] }
];
PricingRuleResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], PricingRuleResolver);



/***/ })

}]);
//# sourceMappingURL=pricing-rules-pricing-rules-module-es2015.js.map