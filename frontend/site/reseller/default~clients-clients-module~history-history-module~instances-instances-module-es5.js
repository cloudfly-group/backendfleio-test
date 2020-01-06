(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["default~clients-clients-module~history-history-module~instances-instances-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/fleio-data-controls/flavors-as-cards/flavors-as-cards.component.html":
/*!***********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/fleio-data-controls/flavors-as-cards/flavors-as-cards.component.html ***!
  \***********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<!-- Display when there are flavors inside a flavor group -->\n<mat-tab-group *ngIf=\"groupsList.length > 1\" [animationDuration]=\"0\">\n  <mat-tab *ngFor=\"let group of groupsList\"\n          label=\"{{group.name}}\">\n    <div class=\"fl-content-flavors-boxes\">\n      <div fxLayout=\"row\" class=\"cards-wrap\">\n        <div *ngFor=\"let flavor of groups[group.name]\"\n             (click)=\"flavorClick(flavor);\"\n             class=\"fl-flavor-card-container\"\n             [class.fl-selected-checkmark]=\"selectedFlavor && selectedFlavor.id === flavor.id\"\n             [class.out_of_stock_flavor_card]=\"flavor.out_of_stock === true\">\n          <mat-icon class=\"fl-icons fl-flavor-selected-checkmark mat-primary\">check</mat-icon>\n          <mat-icon *ngIf=\"flavorIncompatibility === true\"\n                   class=\"fl-flavor-selected-checkmark fl-flavor-selected-checkmark-warning mat-primary\">\n            warning\n          </mat-icon>\n          <div class=\"flavor-card\"\n               [class.fl-selected]=\"selectedFlavor && selectedFlavor.id === flavor.id\"\n               [class.fl-selected-warning]=\"flavorIncompatibility === true\">\n            <div class=\"fl-ellipsis-text\">\n              <span title=\"{{flavor.name}}\" class=\"flavor-title\">\n                {{flavor.name}}\n              </span>\n            </div>\n            <mat-divider></mat-divider>\n            <div>\n              <span class=\"flavor-out-of-stock-txt\" *ngIf=\"flavor.out_of_stock\" translate>Flavor is out of stock</span>\n              <div class=\"flavor-card-info-row\"\n                   *ngFor=\"let description of flavor.description.split('\\n')\">\n                <span>{{description}}</span>\n              </div>\n            </div>\n          </div>\n        </div>\n      </div>\n    </div>\n  </mat-tab>\n</mat-tab-group>\n<!-- Display when there are no flavors inside a flavor group -->\n<div class=\"cards-wrap\" fxLayout=\"row\" *ngIf=\"groupsList.length === 1\">\n  <div *ngFor=\"let flavor of groups[groupsList[0].name]\"\n       (click)=\"flavorClick(flavor);\"\n       class=\"fl-flavor-card-container\"\n       [class.fl-selected-checkmark]=\"selectedFlavor && selectedFlavor.id === flavor.id\"\n       [class.out_of_stock_flavor_card]=\"flavor.out_of_stock === true\">\n    <mat-icon class=\"fl-icons fl-flavor-selected-checkmark mat-primary\">check</mat-icon>\n    <mat-icon *ngIf=\"flavorIncompatibility === true\"\n             class=\"fl-flavor-selected-checkmark fl-flavor-selected-checkmark-warning mat-primary\">\n      warning\n    </mat-icon>\n    <div class=\"flavor-card\"\n         [class.fl-selected]=\"selectedFlavor && selectedFlavor.id === flavor.id\"\n         [class.fl-selected-warning]=\"flavorIncompatibility === true\">\n      <div class=\"fl-ellipsis-text\">\n        <span title=\"{{flavor.name}}\" class=\"flavor-title\">\n          {{flavor.name}}\n        </span>\n      </div>\n      <mat-divider></mat-divider>\n      <div>\n        <span class=\"flavor-out-of-stock-txt\" *ngIf=\"flavor.out_of_stock\">Flavor is out of stock</span>\n        <div class=\"flavor-card-info-row\"\n             *ngFor=\"let description of flavor.description.split('\\n')\">\n          <span>{{description}}</span>\n        </div>\n      </div>\n    </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/fleio-data-controls/images-as-cards/images-as-cards.component.html":
/*!*********************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/fleio-data-controls/images-as-cards/images-as-cards.component.html ***!
  \*********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"images-wrap\" fxLayout=\"row\">\n  <div *ngFor=\"let image of images\"\n       (click)=\"selectedImage = image\"\n       class=\"fl-image-card-container\"\n       [class.fl-selected-checkmark]=\"selectedImage && selectedImage.id === image.id\">\n    <mat-icon class=\"fl-icons fl-image-selected-checkmark mat-primary\">check</mat-icon>\n    <div class=\"image-card\"\n         [class.fl-selected]=\"selectedImage && selectedImage.id === image.id\">\n      <div class=\"fl-ellipsis-text\">\n        <span title=\"{{image.name}}\" class=\"image-title\">\n          <app-icon [icon]=\"{name: image.os_distro || 'otheros', class: 'fl-icons'}\"></app-icon>\n        </span>\n      </div>\n      <mat-divider></mat-divider>\n      <div>\n        <div class=\"image-card-info-row\">\n          {{image.name}}\n        </div>\n      </div>\n    </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/fleio-data-controls/service-dynamic-usage/fleio-service-dynamic-usage.component.html":
/*!***************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/fleio-data-controls/service-dynamic-usage/fleio-service-dynamic-usage.component.html ***!
  \***************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div *ngIf=\"dynamicUsage\" class=\"full-width\" fxLayout=\"row\" fxLayout.xs=\"column\">\n  <div fxFlex=\"100\" fxLayout=\"column\">\n    <ng-container *ngIf=\"dynamicUsage.usage\">\n      <div *ngFor=\"let usage_details of dynamicUsage.usage.usage_details\">\n        <mat-expansion-panel>\n          <mat-expansion-panel-header>\n            <mat-panel-title class=\"half-width\">\n              {{usage_details.resource_name | uppercase}}\n            </mat-panel-title>\n            <mat-panel-description>\n              {{usage_details.price}} {{dynamicUsage.usage.currency.code}}\n              <ng-container *ngIf=\"getCostUsageDetails(usage_details)\">\n                ({{getCostUsageDetails(usage_details).price}} {{dynamicUsageCost.usage.currency.code}})\n              </ng-container>\n            </mat-panel-description>\n          </mat-expansion-panel-header>\n          <div class=\"full-width\" *ngIf=\"usage_details.usage.length\">\n            <table [dataSource]=\"usage_details.usage\" class=\"full-width\" mat-table multiTemplateDataRows>\n              <ng-container matColumnDef=\"name\">\n                <th *matHeaderCellDef mat-header-cell>Name</th>\n                <td *matCellDef=\"let usage\" class=\"fl-detail\" mat-cell>{{usage.display_name}}</td>\n              </ng-container>\n\n              <ng-container matColumnDef=\"region\">\n                <th *matHeaderCellDef mat-header-cell>Region</th>\n                <td *matCellDef=\"let usage\" class=\"fl-detail\" mat-cell>{{usage.region}}</td>\n              </ng-container>\n\n              <ng-container matColumnDef=\"price\">\n                <th *matHeaderCellDef mat-header-cell><p class=\"price-cell\">Price</p></th>\n                <td *matCellDef=\"let usage\" class=\"fl-detail\" mat-cell>\n                  <p class=\"fl-detail price-cell\">\n                    {{usage.price}} {{dynamicUsage.usage.currency.code}}\n                    <ng-container *ngIf=\"getCostUsage(usage_details, usage)\">\n                      ({{getCostUsage(usage_details, usage).price}} {{dynamicUsageCost.usage.currency.code}})\n                    </ng-container>\n                  </p>\n                </td>\n              </ng-container>\n\n              <ng-container matColumnDef=\"expandedDetail\">\n                <td *matCellDef=\"let usage\" [colSpan]=\"detailColumns.length\" mat-cell>\n                  <div [@detailExpand]=\"usage == expandedElement ? 'expanded' : 'collapsed'\"\n                       class=\"element-detail\">\n                    <div fxLayout=\"column\">\n                      <p class=\"fl-detail\">Usage history:</p>\n                      <div *ngFor=\"let history of usage.history\">\n                        <p class=\"fl-detail\">\n                          {{history.name}} - {{history.price_details.units}} {{history.price_details.unit_display}}\n                          ({{history.price}} {{dynamicUsage.usage.currency.code}})\n                        </p>\n                        <div *ngFor=\"let modifier of history.modifiers\" class=\"indent\">\n                          <p class=\"fl-detail\">\n                            {{modifier.name}} - {{modifier.price_details.units}}&nbsp;\n                            {{modifier.price_details.unit_display}}\n                            ({{modifier.price}} {{dynamicUsage.usage.currency.code}})\n                          </p>\n                        </div>\n                      </div>\n                      <ng-container *ngIf=\"getCostUsage(usage_details, usage)\">\n                        <p class=\"fl-detail\">Cost history:</p>\n                        <div *ngFor=\"let history of getCostUsage(usage_details, usage).history\">\n                          <p class=\"fl-detail\">\n                            {{history.name}} - {{history.price_details.units}} {{history.price_details.unit_display}}\n                            ({{history.price}} {{dynamicUsage.usage.currency.code}})\n                          </p>\n                          <div *ngFor=\"let modifier of history.modifiers\" class=\"indent\">\n                            <p class=\"fl-detail\">\n                              {{modifier.name}} - {{modifier.price_details.units}}&nbsp;\n                              {{modifier.price_details.unit_display}}\n                              ({{modifier.price}} {{dynamicUsage.usage.currency.code}})\n                            </p>\n                          </div>\n                        </div>\n                      </ng-container>\n                    </div>\n                  </div>\n                </td>\n              </ng-container>\n\n              <tr *matHeaderRowDef=\"detailColumns\" mat-header-row></tr>\n              <tr mat-row (click)=\"expandedElement = expandedElement === usage ? null : usage\"\n                  *matRowDef=\"let usage; columns: detailColumns;\" class=\"example-element-row\">\n              </tr>\n              <tr *matRowDef=\"let row; columns: ['expandedDetail']\" class=\"details-row\" mat-row></tr>\n            </table>\n          </div>\n          <div class=\"full-width\" *ngIf=\"!usage_details.usage.length\">\n            <p class=\"fl-detail\">n/a</p>\n          </div>\n        </mat-expansion-panel>\n        <p class=\"fl-detail total fl-margin-top-small\">\n          Total {{usage_details.resource_name}} cost: {{usage_details.price}} {{dynamicUsage.usage.currency.code}}\n          <ng-container *ngIf=\"getCostUsageDetails(usage_details); else noCostTotal\">\n            ({{getCostUsageDetails(usage_details).price}} {{dynamicUsageCost.usage.currency.code}})\n          </ng-container>\n          <ng-template #noCostTotal>\n            (n/a)\n          </ng-template>\n        </p>\n      </div>\n    </ng-container>\n    <div *ngIf=\"dynamicUsage\" class=\"full-width\">\n      <p class=\"total fl-margin-top-small\">\n        Total cost: {{dynamicUsage.price}} {{dynamicUsage.client_currency.code}}\n      </p>\n    </div>\n  </div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/shared/fleio-data-controls/flavors-as-cards/flavors-as-cards.component.scss":
/*!*********************************************************************************************!*\
  !*** ./src/app/shared/fleio-data-controls/flavors-as-cards/flavors-as-cards.component.scss ***!
  \*********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "/* flavor cards */\n.flavor-card {\n  min-width: 190px;\n  max-width: 190px;\n  width: 100%;\n  margin: 3px 5px;\n  padding: 15px 10px;\n  border: 1px solid #ebebeb;\n  position: relative;\n  overflow: hidden;\n  cursor: pointer;\n}\n.cards-wrap {\n  flex-wrap: wrap;\n}\n.flavor-card.flavor-card-incompatible {\n  color: #ebebeb !important;\n}\n.flavor-card md-divider {\n  margin-top: 2px;\n  margin-bottom: 5px;\n}\n.flavor-card .flavor-title {\n  font-size: 16px;\n  font-weight: bold;\n  padding: 0;\n}\n.flavor-card .flavor-subtitle {\n  font-size: 16px;\n}\n.flavor-card .flavor-card-info-row {\n  padding: 2px 0;\n}\n.fl-selected {\n  border-color: #37953c;\n  color: #37953c;\n}\n.flavor-card.fl-selected {\n  border-width: 3px;\n  min-width: 190px;\n  padding: 13px 8px;\n}\n.fl-flavor-selected-checkmark {\n  position: absolute;\n  top: -5px;\n  left: -4px;\n  z-index: 1;\n  background: #fff;\n  visibility: hidden;\n  border-radius: 100%;\n}\n.fl-selected-checkmark .fl-flavor-selected-checkmark {\n  visibility: visible;\n}\n.fl-content-flavors-boxes {\n  padding: 15px 3px 10px;\n}\n.fl-flavor-card-container {\n  position: relative;\n  display: -webkit-box;\n  display: flex;\n}\n.flavor-card.fl-selected.fl-selected-warning {\n  color: #ccc;\n  border-color: #ccc;\n}\n.flavor-card.fl-selected.fl-selected-warning mat-divider {\n  background-color: #ccc;\n}\n.fl-flavor-selected-checkmark-warning {\n  color: #ccc !important;\n}\nmat-divider {\n  position: relative !important;\n  margin-top: 5px;\n  margin-bottom: 5px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC9mbGVpby1kYXRhLWNvbnRyb2xzL2ZsYXZvcnMtYXMtY2FyZHMvZmxhdm9ycy1hcy1jYXJkcy5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvc2hhcmVkL2ZsZWlvLWRhdGEtY29udHJvbHMvZmxhdm9ycy1hcy1jYXJkcy9mbGF2b3JzLWFzLWNhcmRzLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBLGlCQUFBO0FBQ0E7RUFDRSxnQkFBQTtFQUNBLGdCQUFBO0VBQ0EsV0FBQTtFQUNBLGVBQUE7RUFDQSxrQkFBQTtFQUNBLHlCQUFBO0VBQ0Esa0JBQUE7RUFDQSxnQkFBQTtFQUNBLGVBQUE7QUNDRjtBRENBO0VBQ0UsZUFBQTtBQ0VGO0FEQUE7RUFDRSx5QkFBQTtBQ0dGO0FEREE7RUFDRSxlQUFBO0VBQ0Esa0JBQUE7QUNJRjtBREZBO0VBQ0UsZUFBQTtFQUNBLGlCQUFBO0VBQ0EsVUFBQTtBQ0tGO0FESEE7RUFDRSxlQUFBO0FDTUY7QURKQTtFQUNFLGNBQUE7QUNPRjtBRExBO0VBQ0UscUJBQUE7RUFDQSxjQUFBO0FDUUY7QUROQTtFQUNFLGlCQUFBO0VBQ0EsZ0JBQUE7RUFDQSxpQkFBQTtBQ1NGO0FEUEE7RUFDRSxrQkFBQTtFQUNBLFNBQUE7RUFDQSxVQUFBO0VBQ0EsVUFBQTtFQUNBLGdCQUFBO0VBQ0Esa0JBQUE7RUFDQSxtQkFBQTtBQ1VGO0FEUkE7RUFDRSxtQkFBQTtBQ1dGO0FEVEE7RUFDRSxzQkFBQTtBQ1lGO0FEVkE7RUFDRSxrQkFBQTtFQUNBLG9CQUFBO0VBQUEsYUFBQTtBQ2FGO0FEWEE7RUFDRSxXQUFBO0VBQ0Esa0JBQUE7QUNjRjtBRFpBO0VBQ0Usc0JBQUE7QUNlRjtBRGJBO0VBQ0Usc0JBQUE7QUNnQkY7QURkQTtFQUNFLDZCQUFBO0VBQ0EsZUFBQTtFQUNBLGtCQUFBO0FDaUJGIiwiZmlsZSI6InNyYy9hcHAvc2hhcmVkL2ZsZWlvLWRhdGEtY29udHJvbHMvZmxhdm9ycy1hcy1jYXJkcy9mbGF2b3JzLWFzLWNhcmRzLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLyogZmxhdm9yIGNhcmRzICovXG4uZmxhdm9yLWNhcmQge1xuICBtaW4td2lkdGg6IDE5MHB4O1xuICBtYXgtd2lkdGg6IDE5MHB4O1xuICB3aWR0aDogMTAwJTtcbiAgbWFyZ2luOiAzcHggNXB4O1xuICBwYWRkaW5nOiAxNXB4IDEwcHg7XG4gIGJvcmRlcjogMXB4IHNvbGlkICNlYmViZWI7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgb3ZlcmZsb3c6IGhpZGRlbjtcbiAgY3Vyc29yOiBwb2ludGVyO1xufVxuLmNhcmRzLXdyYXAge1xuICBmbGV4LXdyYXA6IHdyYXA7XG59XG4uZmxhdm9yLWNhcmQuZmxhdm9yLWNhcmQtaW5jb21wYXRpYmxlIHtcbiAgY29sb3I6ICNlYmViZWIgIWltcG9ydGFudDtcbn1cbi5mbGF2b3ItY2FyZCBtZC1kaXZpZGVyIHtcbiAgbWFyZ2luLXRvcDogMnB4O1xuICBtYXJnaW4tYm90dG9tOiA1cHg7XG59XG4uZmxhdm9yLWNhcmQgLmZsYXZvci10aXRsZSB7XG4gIGZvbnQtc2l6ZTogMTZweDtcbiAgZm9udC13ZWlnaHQ6IGJvbGQ7XG4gIHBhZGRpbmc6IDA7XG59XG4uZmxhdm9yLWNhcmQgLmZsYXZvci1zdWJ0aXRsZSB7XG4gIGZvbnQtc2l6ZTogMTZweDtcbn1cbi5mbGF2b3ItY2FyZCAuZmxhdm9yLWNhcmQtaW5mby1yb3cge1xuICBwYWRkaW5nOiAycHggMDtcbn1cbi5mbC1zZWxlY3RlZCB7XG4gIGJvcmRlci1jb2xvcjogcmdiKDU1LCAxNDksIDYwKTtcbiAgY29sb3I6IHJnYig1NSwgMTQ5LCA2MCk7XG59XG4uZmxhdm9yLWNhcmQuZmwtc2VsZWN0ZWQge1xuICBib3JkZXItd2lkdGg6IDNweDtcbiAgbWluLXdpZHRoOiAxOTBweDtcbiAgcGFkZGluZzogMTNweCA4cHg7XG59XG4uZmwtZmxhdm9yLXNlbGVjdGVkLWNoZWNrbWFyayB7XG4gIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgdG9wOiAtNXB4O1xuICBsZWZ0OiAtNHB4O1xuICB6LWluZGV4OiAxO1xuICBiYWNrZ3JvdW5kOiAjZmZmO1xuICB2aXNpYmlsaXR5OiBoaWRkZW47XG4gIGJvcmRlci1yYWRpdXM6IDEwMCU7XG59XG4uZmwtc2VsZWN0ZWQtY2hlY2ttYXJrIC5mbC1mbGF2b3Itc2VsZWN0ZWQtY2hlY2ttYXJrIHtcbiAgdmlzaWJpbGl0eTogdmlzaWJsZTtcbn1cbi5mbC1jb250ZW50LWZsYXZvcnMtYm94ZXMge1xuICBwYWRkaW5nOiAxNXB4IDNweCAxMHB4O1xufVxuLmZsLWZsYXZvci1jYXJkLWNvbnRhaW5lciB7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgZGlzcGxheTogZmxleDtcbn1cbi5mbGF2b3ItY2FyZC5mbC1zZWxlY3RlZC5mbC1zZWxlY3RlZC13YXJuaW5nIHtcbiAgY29sb3I6ICNjY2M7XG4gIGJvcmRlci1jb2xvcjogI2NjYztcbn1cbi5mbGF2b3ItY2FyZC5mbC1zZWxlY3RlZC5mbC1zZWxlY3RlZC13YXJuaW5nIG1hdC1kaXZpZGVyIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogI2NjYztcbn1cbi5mbC1mbGF2b3Itc2VsZWN0ZWQtY2hlY2ttYXJrLXdhcm5pbmcge1xuICBjb2xvcjogI2NjYyAhaW1wb3J0YW50O1xufVxubWF0LWRpdmlkZXIge1xuICBwb3NpdGlvbjogcmVsYXRpdmUgIWltcG9ydGFudDtcbiAgbWFyZ2luLXRvcDogNXB4O1xuICBtYXJnaW4tYm90dG9tOiA1cHg7XG59XG4iLCIvKiBmbGF2b3IgY2FyZHMgKi9cbi5mbGF2b3ItY2FyZCB7XG4gIG1pbi13aWR0aDogMTkwcHg7XG4gIG1heC13aWR0aDogMTkwcHg7XG4gIHdpZHRoOiAxMDAlO1xuICBtYXJnaW46IDNweCA1cHg7XG4gIHBhZGRpbmc6IDE1cHggMTBweDtcbiAgYm9yZGVyOiAxcHggc29saWQgI2ViZWJlYjtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xuICBvdmVyZmxvdzogaGlkZGVuO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbi5jYXJkcy13cmFwIHtcbiAgZmxleC13cmFwOiB3cmFwO1xufVxuXG4uZmxhdm9yLWNhcmQuZmxhdm9yLWNhcmQtaW5jb21wYXRpYmxlIHtcbiAgY29sb3I6ICNlYmViZWIgIWltcG9ydGFudDtcbn1cblxuLmZsYXZvci1jYXJkIG1kLWRpdmlkZXIge1xuICBtYXJnaW4tdG9wOiAycHg7XG4gIG1hcmdpbi1ib3R0b206IDVweDtcbn1cblxuLmZsYXZvci1jYXJkIC5mbGF2b3ItdGl0bGUge1xuICBmb250LXNpemU6IDE2cHg7XG4gIGZvbnQtd2VpZ2h0OiBib2xkO1xuICBwYWRkaW5nOiAwO1xufVxuXG4uZmxhdm9yLWNhcmQgLmZsYXZvci1zdWJ0aXRsZSB7XG4gIGZvbnQtc2l6ZTogMTZweDtcbn1cblxuLmZsYXZvci1jYXJkIC5mbGF2b3ItY2FyZC1pbmZvLXJvdyB7XG4gIHBhZGRpbmc6IDJweCAwO1xufVxuXG4uZmwtc2VsZWN0ZWQge1xuICBib3JkZXItY29sb3I6ICMzNzk1M2M7XG4gIGNvbG9yOiAjMzc5NTNjO1xufVxuXG4uZmxhdm9yLWNhcmQuZmwtc2VsZWN0ZWQge1xuICBib3JkZXItd2lkdGg6IDNweDtcbiAgbWluLXdpZHRoOiAxOTBweDtcbiAgcGFkZGluZzogMTNweCA4cHg7XG59XG5cbi5mbC1mbGF2b3Itc2VsZWN0ZWQtY2hlY2ttYXJrIHtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICB0b3A6IC01cHg7XG4gIGxlZnQ6IC00cHg7XG4gIHotaW5kZXg6IDE7XG4gIGJhY2tncm91bmQ6ICNmZmY7XG4gIHZpc2liaWxpdHk6IGhpZGRlbjtcbiAgYm9yZGVyLXJhZGl1czogMTAwJTtcbn1cblxuLmZsLXNlbGVjdGVkLWNoZWNrbWFyayAuZmwtZmxhdm9yLXNlbGVjdGVkLWNoZWNrbWFyayB7XG4gIHZpc2liaWxpdHk6IHZpc2libGU7XG59XG5cbi5mbC1jb250ZW50LWZsYXZvcnMtYm94ZXMge1xuICBwYWRkaW5nOiAxNXB4IDNweCAxMHB4O1xufVxuXG4uZmwtZmxhdm9yLWNhcmQtY29udGFpbmVyIHtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xuICBkaXNwbGF5OiBmbGV4O1xufVxuXG4uZmxhdm9yLWNhcmQuZmwtc2VsZWN0ZWQuZmwtc2VsZWN0ZWQtd2FybmluZyB7XG4gIGNvbG9yOiAjY2NjO1xuICBib3JkZXItY29sb3I6ICNjY2M7XG59XG5cbi5mbGF2b3ItY2FyZC5mbC1zZWxlY3RlZC5mbC1zZWxlY3RlZC13YXJuaW5nIG1hdC1kaXZpZGVyIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogI2NjYztcbn1cblxuLmZsLWZsYXZvci1zZWxlY3RlZC1jaGVja21hcmstd2FybmluZyB7XG4gIGNvbG9yOiAjY2NjICFpbXBvcnRhbnQ7XG59XG5cbm1hdC1kaXZpZGVyIHtcbiAgcG9zaXRpb246IHJlbGF0aXZlICFpbXBvcnRhbnQ7XG4gIG1hcmdpbi10b3A6IDVweDtcbiAgbWFyZ2luLWJvdHRvbTogNXB4O1xufSJdfQ== */"

/***/ }),

/***/ "./src/app/shared/fleio-data-controls/flavors-as-cards/flavors-as-cards.component.ts":
/*!*******************************************************************************************!*\
  !*** ./src/app/shared/fleio-data-controls/flavors-as-cards/flavors-as-cards.component.ts ***!
  \*******************************************************************************************/
/*! exports provided: FlavorsAsCardsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlavorsAsCardsComponent", function() { return FlavorsAsCardsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");


var FlavorsAsCardsComponent = /** @class */ (function () {
    function FlavorsAsCardsComponent() {
        this.flavorIncompatibility = false;
    }
    FlavorsAsCardsComponent.prototype.updateFlavorsAndGroups = function () {
        var e_1, _a;
        this.groupsList = [];
        this.groups = {};
        var flavorGroup;
        try {
            for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](this.flavors), _c = _b.next(); !_c.done; _c = _b.next()) {
                var flavor = _c.value;
                flavorGroup = flavor.flavor_group;
                if (flavorGroup !== null) {
                    if (typeof this.groups[flavorGroup.name] !== 'undefined') {
                        this.groups[flavorGroup.name].push(flavor);
                    }
                    else {
                        this.groupsList.push({
                            name: flavorGroup.name,
                            priority: flavorGroup.priority
                        });
                        this.groups[flavorGroup.name] = [flavor];
                    }
                }
                else {
                    if (!this.groups.hasOwnProperty('standard')) {
                        this.groups.standard = [];
                        this.groupsList.unshift({ name: 'standard', priority: 0 });
                    }
                    this.groups.standard.push(flavor);
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        this.groupsList = this.groupsList.sort(function (g1, g2) { return g1.priority - g2.priority; });
    };
    FlavorsAsCardsComponent.prototype.flavorClick = function (flavor) {
        this.selectedFlavor = flavor;
    };
    FlavorsAsCardsComponent.prototype.ngOnInit = function () {
        this.selectedFlavor = null;
        this.updateFlavorsAndGroups();
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
    ], FlavorsAsCardsComponent.prototype, "flavors", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
    ], FlavorsAsCardsComponent.prototype, "flavorIncompatibility", void 0);
    FlavorsAsCardsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-flavors-as-cards',
            template: __webpack_require__(/*! raw-loader!./flavors-as-cards.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/fleio-data-controls/flavors-as-cards/flavors-as-cards.component.html"),
            styles: [__webpack_require__(/*! ./flavors-as-cards.component.scss */ "./src/app/shared/fleio-data-controls/flavors-as-cards/flavors-as-cards.component.scss")]
        })
    ], FlavorsAsCardsComponent);
    return FlavorsAsCardsComponent;
}());



/***/ }),

/***/ "./src/app/shared/fleio-data-controls/fleio-data-controls.module.ts":
/*!**************************************************************************!*\
  !*** ./src/app/shared/fleio-data-controls/fleio-data-controls.module.ts ***!
  \**************************************************************************/
/*! exports provided: FleioDataControlsModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FleioDataControlsModule", function() { return FleioDataControlsModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/autocomplete */ "./node_modules/@angular/material/esm5/autocomplete.es5.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _service_dynamic_usage_fleio_service_dynamic_usage_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./service-dynamic-usage/fleio-service-dynamic-usage.component */ "./src/app/shared/fleio-data-controls/service-dynamic-usage/fleio-service-dynamic-usage.component.ts");
/* harmony import */ var _angular_material_divider__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/divider */ "./node_modules/@angular/material/esm5/divider.es5.js");
/* harmony import */ var _angular_material_expansion__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/expansion */ "./node_modules/@angular/material/esm5/expansion.es5.js");
/* harmony import */ var _angular_material_table__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/table */ "./node_modules/@angular/material/esm5/table.es5.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var _flavors_as_cards_flavors_as_cards_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./flavors-as-cards/flavors-as-cards.component */ "./src/app/shared/fleio-data-controls/flavors-as-cards/flavors-as-cards.component.ts");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/icon */ "./node_modules/@angular/material/esm5/icon.es5.js");
/* harmony import */ var _images_as_cards_images_as_cards_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./images-as-cards/images-as-cards.component */ "./src/app/shared/fleio-data-controls/images-as-cards/images-as-cards.component.ts");
/* harmony import */ var _ui_ui_module__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../ui/ui.module */ "./src/app/shared/ui/ui.module.ts");
/* harmony import */ var _angular_material_tabs__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/tabs */ "./node_modules/@angular/material/esm5/tabs.es5.js");















var FleioDataControlsModule = /** @class */ (function () {
    function FleioDataControlsModule() {
    }
    FleioDataControlsModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            declarations: [
                _service_dynamic_usage_fleio_service_dynamic_usage_component__WEBPACK_IMPORTED_MODULE_5__["FleioServiceDynamicUsageComponent"],
                _flavors_as_cards_flavors_as_cards_component__WEBPACK_IMPORTED_MODULE_10__["FlavorsAsCardsComponent"],
                _images_as_cards_images_as_cards_component__WEBPACK_IMPORTED_MODULE_12__["ImagesAsCardsComponent"],
            ],
            exports: [
                _service_dynamic_usage_fleio_service_dynamic_usage_component__WEBPACK_IMPORTED_MODULE_5__["FleioServiceDynamicUsageComponent"],
                _flavors_as_cards_flavors_as_cards_component__WEBPACK_IMPORTED_MODULE_10__["FlavorsAsCardsComponent"],
                _images_as_cards_images_as_cards_component__WEBPACK_IMPORTED_MODULE_12__["ImagesAsCardsComponent"]
            ],
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _angular_material_autocomplete__WEBPACK_IMPORTED_MODULE_3__["MatAutocompleteModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
                _angular_material_divider__WEBPACK_IMPORTED_MODULE_6__["MatDividerModule"],
                _angular_material_expansion__WEBPACK_IMPORTED_MODULE_7__["MatExpansionModule"],
                _angular_material_table__WEBPACK_IMPORTED_MODULE_8__["MatTableModule"],
                _angular_flex_layout__WEBPACK_IMPORTED_MODULE_9__["FlexLayoutModule"],
                _angular_material_icon__WEBPACK_IMPORTED_MODULE_11__["MatIconModule"],
                _ui_ui_module__WEBPACK_IMPORTED_MODULE_13__["UiModule"],
                _angular_material_tabs__WEBPACK_IMPORTED_MODULE_14__["MatTabsModule"]
            ]
        })
    ], FleioDataControlsModule);
    return FleioDataControlsModule;
}());



/***/ }),

/***/ "./src/app/shared/fleio-data-controls/images-as-cards/images-as-cards.component.scss":
/*!*******************************************************************************************!*\
  !*** ./src/app/shared/fleio-data-controls/images-as-cards/images-as-cards.component.scss ***!
  \*******************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "/* image cards */\n.image-card {\n  min-width: 190px;\n  max-width: 190px;\n  width: 100%;\n  margin: 3px 5px;\n  padding: 15px 10px;\n  border: 1px solid #ebebeb;\n  position: relative;\n  overflow: hidden;\n  cursor: pointer;\n}\n.images-wrap {\n  flex-wrap: wrap;\n}\n.image-card md-divider {\n  margin-top: 2px;\n  margin-bottom: 5px;\n}\n.image-card .image-title {\n  font-size: 16px;\n  font-weight: bold;\n  padding: 0;\n}\n.image-card .image-subtitle {\n  font-size: 16px;\n}\n.image-card .image-card-info-row {\n  padding: 2px 0;\n}\n.fl-selected {\n  border-color: #37953c;\n  color: #37953c;\n}\n.image-card.fl-selected {\n  border-width: 3px;\n  min-width: 190px;\n  padding: 13px 8px;\n}\n.fl-image-selected-checkmark {\n  position: absolute;\n  top: -5px;\n  left: -4px;\n  z-index: 1;\n  background: #fff;\n  visibility: hidden;\n  border-radius: 100%;\n}\n.fl-selected-checkmark .fl-image-selected-checkmark {\n  visibility: visible;\n}\n.fl-content-images-boxes {\n  padding: 15px 3px 10px;\n}\n.fl-image-card-container {\n  position: relative;\n  display: -webkit-box;\n  display: flex;\n}\nmat-divider {\n  position: relative !important;\n  margin-top: 5px;\n  margin-bottom: 5px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC9mbGVpby1kYXRhLWNvbnRyb2xzL2ltYWdlcy1hcy1jYXJkcy9pbWFnZXMtYXMtY2FyZHMuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3NoYXJlZC9mbGVpby1kYXRhLWNvbnRyb2xzL2ltYWdlcy1hcy1jYXJkcy9pbWFnZXMtYXMtY2FyZHMuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUEsZ0JBQUE7QUFDQTtFQUNFLGdCQUFBO0VBQ0EsZ0JBQUE7RUFDQSxXQUFBO0VBQ0EsZUFBQTtFQUNBLGtCQUFBO0VBQ0EseUJBQUE7RUFDQSxrQkFBQTtFQUNBLGdCQUFBO0VBQ0EsZUFBQTtBQ0NGO0FEQ0E7RUFDRSxlQUFBO0FDRUY7QURBQTtFQUNFLGVBQUE7RUFDQSxrQkFBQTtBQ0dGO0FEREE7RUFDRSxlQUFBO0VBQ0EsaUJBQUE7RUFDQSxVQUFBO0FDSUY7QURGQTtFQUNFLGVBQUE7QUNLRjtBREhBO0VBQ0UsY0FBQTtBQ01GO0FESkE7RUFDRSxxQkFBQTtFQUNBLGNBQUE7QUNPRjtBRExBO0VBQ0UsaUJBQUE7RUFDQSxnQkFBQTtFQUNBLGlCQUFBO0FDUUY7QUROQTtFQUNFLGtCQUFBO0VBQ0EsU0FBQTtFQUNBLFVBQUE7RUFDQSxVQUFBO0VBQ0EsZ0JBQUE7RUFDQSxrQkFBQTtFQUNBLG1CQUFBO0FDU0Y7QURQQTtFQUNFLG1CQUFBO0FDVUY7QURSQTtFQUNFLHNCQUFBO0FDV0Y7QURUQTtFQUNFLGtCQUFBO0VBQ0Esb0JBQUE7RUFBQSxhQUFBO0FDWUY7QURWQTtFQUNFLDZCQUFBO0VBQ0EsZUFBQTtFQUNBLGtCQUFBO0FDYUYiLCJmaWxlIjoic3JjL2FwcC9zaGFyZWQvZmxlaW8tZGF0YS1jb250cm9scy9pbWFnZXMtYXMtY2FyZHMvaW1hZ2VzLWFzLWNhcmRzLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLyogaW1hZ2UgY2FyZHMgKi9cbi5pbWFnZS1jYXJkIHtcbiAgbWluLXdpZHRoOiAxOTBweDtcbiAgbWF4LXdpZHRoOiAxOTBweDtcbiAgd2lkdGg6IDEwMCU7XG4gIG1hcmdpbjogM3B4IDVweDtcbiAgcGFkZGluZzogMTVweCAxMHB4O1xuICBib3JkZXI6IDFweCBzb2xpZCAjZWJlYmViO1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIG92ZXJmbG93OiBoaWRkZW47XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cbi5pbWFnZXMtd3JhcCB7XG4gIGZsZXgtd3JhcDogd3JhcDtcbn1cbi5pbWFnZS1jYXJkIG1kLWRpdmlkZXIge1xuICBtYXJnaW4tdG9wOiAycHg7XG4gIG1hcmdpbi1ib3R0b206IDVweDtcbn1cbi5pbWFnZS1jYXJkIC5pbWFnZS10aXRsZSB7XG4gIGZvbnQtc2l6ZTogMTZweDtcbiAgZm9udC13ZWlnaHQ6IGJvbGQ7XG4gIHBhZGRpbmc6IDA7XG59XG4uaW1hZ2UtY2FyZCAuaW1hZ2Utc3VidGl0bGUge1xuICBmb250LXNpemU6IDE2cHg7XG59XG4uaW1hZ2UtY2FyZCAuaW1hZ2UtY2FyZC1pbmZvLXJvdyB7XG4gIHBhZGRpbmc6IDJweCAwO1xufVxuLmZsLXNlbGVjdGVkIHtcbiAgYm9yZGVyLWNvbG9yOiByZ2IoNTUsIDE0OSwgNjApO1xuICBjb2xvcjogcmdiKDU1LCAxNDksIDYwKTtcbn1cbi5pbWFnZS1jYXJkLmZsLXNlbGVjdGVkIHtcbiAgYm9yZGVyLXdpZHRoOiAzcHg7XG4gIG1pbi13aWR0aDogMTkwcHg7XG4gIHBhZGRpbmc6IDEzcHggOHB4O1xufVxuLmZsLWltYWdlLXNlbGVjdGVkLWNoZWNrbWFyayB7XG4gIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgdG9wOiAtNXB4O1xuICBsZWZ0OiAtNHB4O1xuICB6LWluZGV4OiAxO1xuICBiYWNrZ3JvdW5kOiAjZmZmO1xuICB2aXNpYmlsaXR5OiBoaWRkZW47XG4gIGJvcmRlci1yYWRpdXM6IDEwMCU7XG59XG4uZmwtc2VsZWN0ZWQtY2hlY2ttYXJrIC5mbC1pbWFnZS1zZWxlY3RlZC1jaGVja21hcmsge1xuICB2aXNpYmlsaXR5OiB2aXNpYmxlO1xufVxuLmZsLWNvbnRlbnQtaW1hZ2VzLWJveGVzIHtcbiAgcGFkZGluZzogMTVweCAzcHggMTBweDtcbn1cbi5mbC1pbWFnZS1jYXJkLWNvbnRhaW5lciB7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgZGlzcGxheTogZmxleDtcbn1cbm1hdC1kaXZpZGVyIHtcbiAgcG9zaXRpb246IHJlbGF0aXZlICFpbXBvcnRhbnQ7XG4gIG1hcmdpbi10b3A6IDVweDtcbiAgbWFyZ2luLWJvdHRvbTogNXB4O1xufVxuIiwiLyogaW1hZ2UgY2FyZHMgKi9cbi5pbWFnZS1jYXJkIHtcbiAgbWluLXdpZHRoOiAxOTBweDtcbiAgbWF4LXdpZHRoOiAxOTBweDtcbiAgd2lkdGg6IDEwMCU7XG4gIG1hcmdpbjogM3B4IDVweDtcbiAgcGFkZGluZzogMTVweCAxMHB4O1xuICBib3JkZXI6IDFweCBzb2xpZCAjZWJlYmViO1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIG92ZXJmbG93OiBoaWRkZW47XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuLmltYWdlcy13cmFwIHtcbiAgZmxleC13cmFwOiB3cmFwO1xufVxuXG4uaW1hZ2UtY2FyZCBtZC1kaXZpZGVyIHtcbiAgbWFyZ2luLXRvcDogMnB4O1xuICBtYXJnaW4tYm90dG9tOiA1cHg7XG59XG5cbi5pbWFnZS1jYXJkIC5pbWFnZS10aXRsZSB7XG4gIGZvbnQtc2l6ZTogMTZweDtcbiAgZm9udC13ZWlnaHQ6IGJvbGQ7XG4gIHBhZGRpbmc6IDA7XG59XG5cbi5pbWFnZS1jYXJkIC5pbWFnZS1zdWJ0aXRsZSB7XG4gIGZvbnQtc2l6ZTogMTZweDtcbn1cblxuLmltYWdlLWNhcmQgLmltYWdlLWNhcmQtaW5mby1yb3cge1xuICBwYWRkaW5nOiAycHggMDtcbn1cblxuLmZsLXNlbGVjdGVkIHtcbiAgYm9yZGVyLWNvbG9yOiAjMzc5NTNjO1xuICBjb2xvcjogIzM3OTUzYztcbn1cblxuLmltYWdlLWNhcmQuZmwtc2VsZWN0ZWQge1xuICBib3JkZXItd2lkdGg6IDNweDtcbiAgbWluLXdpZHRoOiAxOTBweDtcbiAgcGFkZGluZzogMTNweCA4cHg7XG59XG5cbi5mbC1pbWFnZS1zZWxlY3RlZC1jaGVja21hcmsge1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIHRvcDogLTVweDtcbiAgbGVmdDogLTRweDtcbiAgei1pbmRleDogMTtcbiAgYmFja2dyb3VuZDogI2ZmZjtcbiAgdmlzaWJpbGl0eTogaGlkZGVuO1xuICBib3JkZXItcmFkaXVzOiAxMDAlO1xufVxuXG4uZmwtc2VsZWN0ZWQtY2hlY2ttYXJrIC5mbC1pbWFnZS1zZWxlY3RlZC1jaGVja21hcmsge1xuICB2aXNpYmlsaXR5OiB2aXNpYmxlO1xufVxuXG4uZmwtY29udGVudC1pbWFnZXMtYm94ZXMge1xuICBwYWRkaW5nOiAxNXB4IDNweCAxMHB4O1xufVxuXG4uZmwtaW1hZ2UtY2FyZC1jb250YWluZXIge1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIGRpc3BsYXk6IGZsZXg7XG59XG5cbm1hdC1kaXZpZGVyIHtcbiAgcG9zaXRpb246IHJlbGF0aXZlICFpbXBvcnRhbnQ7XG4gIG1hcmdpbi10b3A6IDVweDtcbiAgbWFyZ2luLWJvdHRvbTogNXB4O1xufSJdfQ== */"

/***/ }),

/***/ "./src/app/shared/fleio-data-controls/images-as-cards/images-as-cards.component.ts":
/*!*****************************************************************************************!*\
  !*** ./src/app/shared/fleio-data-controls/images-as-cards/images-as-cards.component.ts ***!
  \*****************************************************************************************/
/*! exports provided: ImagesAsCardsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ImagesAsCardsComponent", function() { return ImagesAsCardsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");


var ImagesAsCardsComponent = /** @class */ (function () {
    function ImagesAsCardsComponent() {
    }
    ImagesAsCardsComponent.prototype.ngOnInit = function () {
        this.selectedImage = null;
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
    ], ImagesAsCardsComponent.prototype, "images", void 0);
    ImagesAsCardsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-images-as-cards',
            template: __webpack_require__(/*! raw-loader!./images-as-cards.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/fleio-data-controls/images-as-cards/images-as-cards.component.html"),
            styles: [__webpack_require__(/*! ./images-as-cards.component.scss */ "./src/app/shared/fleio-data-controls/images-as-cards/images-as-cards.component.scss")]
        })
    ], ImagesAsCardsComponent);
    return ImagesAsCardsComponent;
}());



/***/ }),

/***/ "./src/app/shared/fleio-data-controls/service-dynamic-usage/fleio-service-dynamic-usage.component.scss":
/*!*************************************************************************************************************!*\
  !*** ./src/app/shared/fleio-data-controls/service-dynamic-usage/fleio-service-dynamic-usage.component.scss ***!
  \*************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".total {\n  float: right;\n}\n\n.details-row {\n  height: 0;\n}\n\n.element-detail {\n  overflow: hidden;\n  display: -webkit-box;\n  display: flex;\n}\n\n.price-cell {\n  float: right;\n  width: 25%;\n}\n\n.indent {\n  margin-left: 20px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC9mbGVpby1kYXRhLWNvbnRyb2xzL3NlcnZpY2UtZHluYW1pYy11c2FnZS9mbGVpby1zZXJ2aWNlLWR5bmFtaWMtdXNhZ2UuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3NoYXJlZC9mbGVpby1kYXRhLWNvbnRyb2xzL3NlcnZpY2UtZHluYW1pYy11c2FnZS9mbGVpby1zZXJ2aWNlLWR5bmFtaWMtdXNhZ2UuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxZQUFBO0FDQ0Y7O0FERUE7RUFDRSxTQUFBO0FDQ0Y7O0FERUE7RUFDRSxnQkFBQTtFQUNBLG9CQUFBO0VBQUEsYUFBQTtBQ0NGOztBREVBO0VBQ0UsWUFBQTtFQUNBLFVBQUE7QUNDRjs7QURFQTtFQUNFLGlCQUFBO0FDQ0YiLCJmaWxlIjoic3JjL2FwcC9zaGFyZWQvZmxlaW8tZGF0YS1jb250cm9scy9zZXJ2aWNlLWR5bmFtaWMtdXNhZ2UvZmxlaW8tc2VydmljZS1keW5hbWljLXVzYWdlLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLnRvdGFsIHtcbiAgZmxvYXQ6IHJpZ2h0O1xufVxuXG4uZGV0YWlscy1yb3cge1xuICBoZWlnaHQ6IDA7XG59XG5cbi5lbGVtZW50LWRldGFpbCB7XG4gIG92ZXJmbG93OiBoaWRkZW47XG4gIGRpc3BsYXk6IGZsZXg7XG59XG5cbi5wcmljZS1jZWxsIHtcbiAgZmxvYXQ6IHJpZ2h0O1xuICB3aWR0aDogMjUlO1xufVxuXG4uaW5kZW50IHtcbiAgbWFyZ2luLWxlZnQ6IDIwcHg7XG59XG4iLCIudG90YWwge1xuICBmbG9hdDogcmlnaHQ7XG59XG5cbi5kZXRhaWxzLXJvdyB7XG4gIGhlaWdodDogMDtcbn1cblxuLmVsZW1lbnQtZGV0YWlsIHtcbiAgb3ZlcmZsb3c6IGhpZGRlbjtcbiAgZGlzcGxheTogZmxleDtcbn1cblxuLnByaWNlLWNlbGwge1xuICBmbG9hdDogcmlnaHQ7XG4gIHdpZHRoOiAyNSU7XG59XG5cbi5pbmRlbnQge1xuICBtYXJnaW4tbGVmdDogMjBweDtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/shared/fleio-data-controls/service-dynamic-usage/fleio-service-dynamic-usage.component.ts":
/*!***********************************************************************************************************!*\
  !*** ./src/app/shared/fleio-data-controls/service-dynamic-usage/fleio-service-dynamic-usage.component.ts ***!
  \***********************************************************************************************************/
/*! exports provided: FleioServiceDynamicUsageComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FleioServiceDynamicUsageComponent", function() { return FleioServiceDynamicUsageComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/animations */ "./node_modules/@angular/animations/fesm5/animations.js");



var FleioServiceDynamicUsageComponent = /** @class */ (function () {
    function FleioServiceDynamicUsageComponent() {
        this.detailColumns = ['name', 'region', 'price'];
    }
    FleioServiceDynamicUsageComponent.prototype.ngOnInit = function () {
    };
    FleioServiceDynamicUsageComponent.prototype.getCostUsageDetails = function (usageDetails) {
        var e_1, _a;
        if (this.dynamicUsageCost && this.dynamicUsageCost.usage && this.dynamicUsageCost.usage.usage_details) {
            try {
                for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](this.dynamicUsageCost.usage.usage_details), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var costUsageDetails = _c.value;
                    if (costUsageDetails.resource_name === usageDetails.resource_name &&
                        costUsageDetails.resource_type === usageDetails.resource_type) {
                        return costUsageDetails;
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_1) throw e_1.error; }
            }
        }
        return null;
    };
    FleioServiceDynamicUsageComponent.prototype.getCostUsage = function (usageDetails, usage) {
        var e_2, _a;
        var costUsageDetails = this.getCostUsageDetails(usageDetails);
        if (costUsageDetails) {
            try {
                for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](costUsageDetails.usage), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var costUsage = _c.value;
                    if (costUsage.resource_id === usage.resource_id) {
                        return costUsage;
                    }
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_2) throw e_2.error; }
            }
        }
        return null;
    };
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
    ], FleioServiceDynamicUsageComponent.prototype, "dynamicUsage", void 0);
    tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
    ], FleioServiceDynamicUsageComponent.prototype, "dynamicUsageCost", void 0);
    FleioServiceDynamicUsageComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-fleio-service-dynamic-usage',
            template: __webpack_require__(/*! raw-loader!./fleio-service-dynamic-usage.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/fleio-data-controls/service-dynamic-usage/fleio-service-dynamic-usage.component.html"),
            animations: [
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_2__["trigger"])('detailExpand', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_2__["state"])('collapsed', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_2__["style"])({ height: '0px', minHeight: '0' })),
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_2__["state"])('expanded', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_2__["style"])({ height: '*' })),
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_2__["transition"])('expanded <=> collapsed', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_2__["animate"])('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
                ]),
            ],
            styles: [__webpack_require__(/*! ./fleio-service-dynamic-usage.component.scss */ "./src/app/shared/fleio-data-controls/service-dynamic-usage/fleio-service-dynamic-usage.component.scss")]
        })
    ], FleioServiceDynamicUsageComponent);
    return FleioServiceDynamicUsageComponent;
}());



/***/ })

}]);
//# sourceMappingURL=default~clients-clients-module~history-history-module~instances-instances-module-es5.js.map