(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["main"],{

/***/ "./$$_lazy_route_resource lazy recursive":
/*!******************************************************!*\
  !*** ./$$_lazy_route_resource lazy namespace object ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncaught exception popping up in devtools
	return Promise.resolve().then(function() {
		var e = new Error("Cannot find module '" + req + "'");
		e.code = 'MODULE_NOT_FOUND';
		throw e;
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "./$$_lazy_route_resource lazy recursive";

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/app.component.html":
/*!**************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/app.component.html ***!
  \**************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<router-outlet></router-outlet>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/reseller/reseller.component.html":
/*!*************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/reseller/reseller.component.html ***!
  \*************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-panel-layout></app-panel-layout>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/auth/login/login.component.html":
/*!**********************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/auth/login/login.component.html ***!
  \**********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div align=\"center\">\n  <form [formGroup]=\"loginForm\" (ngSubmit)=\"login()\">\n    <div>\n      <mat-card class=\"login-card\">\n        <div>\n          <app-logo [dark]=\"true\" [withLink]=\"false\" [customStyle]=\"{\n            width: '140px',\n            height: '70px',\n            marginBottom: '20px'\n          }\"></app-logo>\n        </div>\n        <mat-card-title align=\"left\">\n          <span class=\"card-title\">Login</span>\n        </mat-card-title>\n        <mat-card-content>\n          <app-form-errors #formErrors [formGroup]=\"loginForm\"></app-form-errors>\n          <mat-form-field>\n            <input matInput placeholder=\"Username or email address\" type=\"text\" formControlName=\"username\" name=\"username\" required>\n            <mat-error>This field is required!</mat-error>\n          </mat-form-field>\n            <p>{{loginForm.errors}}</p>\n          <mat-form-field>\n            <input matInput placeholder=\"Password\" type=\"password\" formControlName=\"password\" name=\"password\" required>\n            <mat-error>This field is required!</mat-error>\n          </mat-form-field>\n          <mat-slide-toggle [color]=\"'primary'\" formControlName=\"rememberMe\">Remember me</mat-slide-toggle>\n        </mat-card-content>\n        <mat-card-actions>\n          <div>\n            <button mat-raised-button [color]=\"'primary'\" type=\"submit\" class=\"login-button\">Sign in</button>\n          </div>\n          <div>\n            <button mat-flat-button>Forgot password</button>\n          </div>\n        </mat-card-actions>\n      </mat-card>\n    </div>\n  </form>\n  <a class=\"powered-by-link\" href=\"http://fleio.com\" target=\"_blank\" *ngIf=\"!auth.userData.is_white_label\">\n    Powered by Fleio\n  </a>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/error-handling/form-errors/form-errors.component.html":
/*!********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/error-handling/form-errors/form-errors.component.html ***!
  \********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div *ngIf=\"visible\" fxLayout=\"row\" class=\"content\">\n  <div fxFlex=\"\" class=\"messages\">\n    <div fxLayout=\"column\">\n        <mat-error *ngFor=\"let message of errorMessages\">{{ message }}</mat-error>\n    </div>\n  </div>\n  <div fxFlex=\"none\" class=\"button\">\n    <button mat-raised-button (click)=\"hide()\">Hide</button>\n  </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/error-handling/page-not-found/page-not-found.component.html":
/*!**************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/error-handling/page-not-found/page-not-found.component.html ***!
  \**************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<h1>404: Not found :(</h1>\n<div>Page does not exist</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/fleio-data-controls/phone-input/phone-input.component.html":
/*!*************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/fleio-data-controls/phone-input/phone-input.component.html ***!
  \*************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div fxLayout=\"row\">\n   <mat-form-field fxFlex=\"20\">\n    <mat-select [(ngModel)]=\"flag\" (ngModelChange)=\"changePhoneCountry()\">\n      <mat-option *ngFor=\"let countryCode of countryCodeKeys\" [value]=\"countryCode\">\n        <span class=\"flag-icon flag-icon-{{countryCodes[countryCode][0].toLowerCase()}}\"></span>  {{countryCodes[countryCode][0]}}\n      </mat-option>\n    </mat-select>\n   </mat-form-field>\n  <mat-form-field fxFlexOffset=\"2\" fxFlex=\"78\" [class.mat-form-field-invalid]=\"!!error\">\n    <mat-label>Phone number</mat-label>\n    <input name=\"phone\"\n           matInput\n           id=\"phoneNr\"\n           (ngModelChange)=\"updateFlagOnPhoneChange($event)\"\n           type=\"text\"\n           [(ngModel)]=\"phoneNumber\">\n    <span class=\"mat-error fl-error\" *ngIf=\"error\">{{error}}</span>\n  </mat-form-field>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui-api/yes-no-dialog/yes-no-dialog.component.html":
/*!****************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui-api/yes-no-dialog/yes-no-dialog.component.html ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<h1 mat-dialog-title>{{data.title}}</h1>\n<div mat-dialog-content>\n  <p>{{data.message}}</p>\n  <p *ngIf=\"data.importantMessage\" class=\"fl-important-text\">{{data.importantMessage}}</p>\n</div>\n<div mat-dialog-actions>\n  <button mat-button (click)=\"close()\">No</button>\n  <button mat-button [mat-dialog-close]=\"'yes'\" [color]=\"'primary'\" cdkFocusInitial>Yes</button>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/common/icon/icon.component.html":
/*!*************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/common/icon/icon.component.html ***!
  \*************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<mat-icon [ngClass]=\"icon.class\">{{icon.name}}</mat-icon>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/fl-backdrop/fl-backdrop.component.html":
/*!********************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/fl-backdrop/fl-backdrop.component.html ***!
  \********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"fl-backdrop\"></div>\n<mat-progress-spinner class=\"fl-backdrop-progress\" [mode]=\"'indeterminate'\" [diameter]=\"spinnerDiameter\"\n                      [class.align-circle-middle]=\"verticalAlignMiddle\">\n</mat-progress-spinner>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/gravatar/gravatar.component.html":
/*!**************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/gravatar/gravatar.component.html ***!
  \**************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<img [ngStyle]=\"customStyle\" src=\"{{url}}\">\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/logo/logo.component.html":
/*!******************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/logo/logo.component.html ***!
  \******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<a *ngIf=\"withLink;else withoutLink\" [routerLink]=\"config.getPanelHomeUrl()\">\n  <img [ngStyle]=\"customStyle\" src=\"{{logoPath}}\">\n</a>\n<ng-template #withoutLink><img [ngStyle]=\"customStyle\" src=\"{{logoPath}}\"></ng-template>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/menu/menu-item-container/menu-item-container.component.html":
/*!*****************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/menu/menu-item-container/menu-item-container.component.html ***!
  \*****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<button mat-button class=\"menu-item-container\" (click)=\"toggle()\">\n  {{menuItemContainer.display}}\n  <mat-icon [@openCloseDropdown]=\"getExpanded() ? 'open' : 'closed'\">keyboard_arrow_right</mat-icon>\n</button>\n<div [@openCloseItems]=\"getExpanded() ? 'open' : 'closed'\" class=\"overflow-hidden\">\n  <ng-container *ngFor=\"let item of menuItemContainer.items\">\n    <app-menu-item [menuItem]=\"item\" [isAlone]=\"false\" *ngIf=\"item\"></app-menu-item>\n  </ng-container>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/menu/menu-item/menu-item.component.html":
/*!*********************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/menu/menu-item/menu-item.component.html ***!
  \*********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<a mat-button class=\"menu-link\"\n   [routerLink]=\"[menuItem.route]\"\n   [queryParams]=\"menuItem.queryParams\"\n   routerLinkActive=\"active-link\"\n   [routerLinkActiveOptions]=\"activeOptions\">\n  <mat-icon [ngClass]=\"menuItem.iconClass\">{{menuItem.icon}}</mat-icon>{{menuItem.routeDisplay}}\n</a>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/menu/side-nav-menu/side-nav-menu.component.html":
/*!*****************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/menu/side-nav-menu/side-nav-menu.component.html ***!
  \*****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div *ngFor=\"let item of menu.items\">\n  <app-menu-item *ngIf=\"item.type==='menuItem'\" [menuItem]=\"item\"></app-menu-item>\n  <app-menu-item-container *ngIf=\"item.type==='menuItemContainer' && canShowMenuItemContainer(item)\"\n                           [menuItemContainer]=\"item\"></app-menu-item-container>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/panel-layout/panel-layout.component.html":
/*!**********************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/panel-layout/panel-layout.component.html ***!
  \**********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"app-container app-theme-spring\">\n  <mat-toolbar [@openCloseTopBar]=\"showTopBar ? 'open' : 'closed'\" class=\"topbar-container\" color=\"primary\">\n    <mat-progress-bar mode=\"indeterminate\" color=\"accent\" *ngIf=\"loading\" class=\"loader\"></mat-progress-bar>\n    <button mat-icon-button (click)=\"showSidebar = !showSidebar\" class=\"switch-sidebar-button\">\n      <mat-icon>menu</mat-icon>\n    </button>\n    <app-top-bar class=\"full-width\"></app-top-bar>\n  </mat-toolbar>\n  <div class=\"content-container\" fxLayout=\"row\" [class.content-container-full]=\"!showSidebar\">\n    <div [@openCloseSidebar]=\"showSidebar ? 'open' : 'closed'\" class=\"sidenav-container\">\n      <app-side-nav-menu></app-side-nav-menu>\n      <span class=\"powered-text\">\n        <a href=\"http://fleio.com\" target=\"_blank\" *ngIf=\"!auth.userData.is_white_label\">\n          Powered by Fleio v. {{version}}\n        </a>\n      </span>\n    </div>\n    <div class=\"main-content-container\">\n      <div (click)=\"showSidebar = !showSidebar\" *ngIf=\"showSidebar\" class=\"main-content-container-overlay\"></div>\n      <router-outlet></router-outlet>\n    </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/top-bar/breadcrumbs/breadcrumbs.component.html":
/*!****************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/top-bar/breadcrumbs/breadcrumbs.component.html ***!
  \****************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"br\">\n  <span *ngFor=\"let breadCrumb of breadCrumbs; let x = index\"\n        [fxHide.lt-lg]=\"(x < 2 && breadCrumbs.length > 2) || (x === 0 && breadCrumbs.length > 1)\">\n    <a *ngIf=\"breadCrumb.url;else withoutUrl\" [routerLink]=\"breadCrumb.url\"\n       [queryParams]=\"breadCrumb.queryParams\">\n      {{breadCrumb.display}}\n    </a>\n    <ng-template #withoutUrl>{{breadCrumb.display}}</ng-template>\n    <mat-icon class=\"fl-icons vertical-align-middle breadcrumb-icon\" *ngIf=\"x !== breadCrumbs.length - 1\">\n      arrow_right\n    </mat-icon>\n  </span>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/top-bar/hello-user-button/hello-user-button.component.html":
/*!****************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/top-bar/hello-user-button/hello-user-button.component.html ***!
  \****************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<span *ngIf=\"authService.userData.user\">\n  <div matRipple [matRippleDisabled]=\"true\" [matMenuTriggerFor]=\"menu\" class=\"hello-user-button\">\n    Hello, {{authService.userData.user.first_name || authService.userData.user.username}}\n    <app-gravatar [email]=\"authService.userData.user.email\" [customStyle]=\"{\n      width: '24px',\n      borderRadius: '100%',\n      marginLeft: '15px',\n      verticalAlign: 'middle'\n    }\"></app-gravatar>\n  </div>\n  <mat-menu #menu=\"matMenu\" xPosition=\"before\" yPosition=\"below\">\n    <div (click) = \"$event.stopPropagation()\" class=\"hello-user-first-menu-item\">\n      <app-gravatar [email]=\"authService.userData.user.email\" [customStyle]=\"{\n        width: '50px',\n        marginRight: '15px',\n        verticalAlign: 'middle'\n      }\"></app-gravatar>\n      <div class=\"display-inline-block\">\n        <div>{{authService.userData.user.first_name}} {{authService.userData.user.last_name}}</div>\n        <div>{{authService.userData.user.email}}</div>\n      </div>\n    </div>\n<!--    <button mat-menu-item>Notifications</button>-->\n    <a mat-menu-item [routerLink]=\"[config.getPanelUrl('user-profile/profile/edit')]\">My profile</a>\n    <button mat-menu-item (click)=\"logout()\">Log out</button>\n  </mat-menu>\n</span>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/top-bar/search-box/search-box.component.html":
/*!**************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/top-bar/search-box/search-box.component.html ***!
  \**************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"search-container\" fxHide.lt-md>\n  <input placeholder=\"{{searchConfig.placeholder || 'Search ...' }}\" [formControl]=\"searchText\">\n  <button (click)=\"clearSearch()\" *ngIf=\"searchText.value\" class=\"close-search-button\" mat-icon-button>\n    <mat-icon>close</mat-icon>\n  </button>\n</div>\n<div class=\"search-container-mobile\" fxHide.gt-sm>\n  <input *ngIf=\"showMobileInput\" placeholder=\"{{searchConfig.placeholder || 'Search ...' }}\" [formControl]=\"searchText\">\n  <mat-icon *ngIf=\"showMobileInput\" (click)=\"showMobileInput = !showMobileInput\"\n            class=\"search-container-mobile-close\">\n    close\n  </mat-icon>\n  <mat-icon (click)=\"showMobileInput = !showMobileInput\" class=\"fl-icons\">search</mat-icon>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/top-bar/stop-impersonating-button/stop-impersonating-button.component.html":
/*!********************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/top-bar/stop-impersonating-button/stop-impersonating-button.component.html ***!
  \********************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<button mat-icon-button fl-tooltip=\"Close impersonating\" fl-tooltip-direction=\"left\" (click)=\"closeImpersonation()\">\n  <mat-icon class=\"fl-icon-off\">face</mat-icon>\n</button>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/shared/ui/top-bar/top-bar.component.html":
/*!************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/shared/ui/top-bar/top-bar.component.html ***!
  \************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"full-width topbar-items-container\">\n  <div fxHide.lt-lg>\n    <app-logo [dark]=\"false\" [customStyle]=\"{\n      width: '96px',\n      marginRight: '16px'\n    }\"></app-logo>\n  </div>\n  <div class=\"breadcrumbs-container\">\n    <app-breadcrumbs></app-breadcrumbs>\n  </div>\n  <div *ngIf=\"searchConfig.show\">\n    <app-search-box [searchConfig]=\"searchConfig\"  #searchBox></app-search-box>\n  </div>\n  <div fxLayout=\"row\" fxLayoutAlign=\"center center\" class=\"buttons-container\">\n    <app-hello-user-button></app-hello-user-button>\n    <app-stop-impersonating-button *ngIf=\"auth.isImpersonating()\"></app-stop-impersonating-button>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/app-routing.module.ts":
/*!***************************************!*\
  !*** ./src/app/app-routing.module.ts ***!
  \***************************************/
/*! exports provided: AppRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppRoutingModule", function() { return AppRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_error_handling_page_not_found_page_not_found_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./shared/error-handling/page-not-found/page-not-found.component */ "./src/app/shared/error-handling/page-not-found/page-not-found.component.ts");
/* harmony import */ var _reseller_reseller_reseller_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./reseller/reseller/reseller.component */ "./src/app/reseller/reseller/reseller.component.ts");





const routes = [
    {
        path: '',
        loadChildren: () => Promise.resolve(/*! import() */).then(__webpack_require__.bind(null, /*! ./reseller/reseller.module */ "./src/app/reseller/reseller.module.ts")).then(mod => mod.ResellerModule),
        component: _reseller_reseller_reseller_component__WEBPACK_IMPORTED_MODULE_4__["ResellerComponent"],
        data: {
            configurationName: 'reseller',
        }
    },
    {
        path: '**',
        component: _shared_error_handling_page_not_found_page_not_found_component__WEBPACK_IMPORTED_MODULE_3__["PageNotFoundComponent"]
    }
];
let AppRoutingModule = class AppRoutingModule {
};
AppRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forRoot(routes, { onSameUrlNavigation: 'reload' })],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
    })
], AppRoutingModule);



/***/ }),

/***/ "./src/app/app.component.scss":
/*!************************************!*\
  !*** ./src/app/app.component.scss ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL2FwcC5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/app.component.ts":
/*!**********************************!*\
  !*** ./src/app/app.component.ts ***!
  \**********************************/
/*! exports provided: AppComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppComponent", function() { return AppComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let AppComponent = class AppComponent {
};
AppComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-root',
        template: __webpack_require__(/*! raw-loader!./app.component.html */ "./node_modules/raw-loader/index.js!./src/app/app.component.html"),
        styles: [__webpack_require__(/*! ./app.component.scss */ "./src/app/app.component.scss")]
    })
], AppComponent);



/***/ }),

/***/ "./src/app/app.module.ts":
/*!*******************************!*\
  !*** ./src/app/app.module.ts ***!
  \*******************************/
/*! exports provided: initializeApp, AppModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "initializeApp", function() { return initializeApp; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppModule", function() { return AppModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm2015/platform-browser.js");
/* harmony import */ var _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/platform-browser/animations */ "./node_modules/@angular/platform-browser/fesm2015/animations.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _app_routing_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./app-routing.module */ "./src/app/app-routing.module.ts");
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./app.component */ "./src/app/app.component.ts");
/* harmony import */ var _reseller_reseller_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./reseller/reseller.module */ "./src/app/reseller/reseller.module.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./shared/shared.module */ "./src/app/shared/shared.module.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_auth_auth_interceptor__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./shared/auth/auth-interceptor */ "./src/app/shared/auth/auth-interceptor.ts");
/* harmony import */ var _shared_error_handling_error_interceptor__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./shared/error-handling/error-interceptor */ "./src/app/shared/error-handling/error-interceptor.ts");












function initializeApp(configService) {
    return () => configService.load();
}
let AppModule = class AppModule {
};
AppModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_3__["NgModule"])({
        declarations: [
            _app_component__WEBPACK_IMPORTED_MODULE_5__["AppComponent"],
        ],
        imports: [
            _angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__["BrowserModule"],
            _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_2__["BrowserAnimationsModule"],
            _app_routing_module__WEBPACK_IMPORTED_MODULE_4__["AppRoutingModule"],
            _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpClientModule"],
            _reseller_reseller_module__WEBPACK_IMPORTED_MODULE_6__["ResellerModule"],
            _shared_shared_module__WEBPACK_IMPORTED_MODULE_7__["SharedModule"],
            _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HttpClientXsrfModule"].withOptions({
                cookieName: 'csrftoken',
                headerName: 'X-CSRFToken'
            }),
        ],
        providers: [
            {
                provide: _angular_core__WEBPACK_IMPORTED_MODULE_3__["APP_INITIALIZER"],
                useFactory: initializeApp,
                deps: [_shared_config_config_service__WEBPACK_IMPORTED_MODULE_9__["ConfigService"]],
                multi: true
            },
            {
                provide: _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HTTP_INTERCEPTORS"],
                useClass: _shared_auth_auth_interceptor__WEBPACK_IMPORTED_MODULE_10__["AuthInterceptor"],
                multi: true,
            },
            {
                provide: _angular_common_http__WEBPACK_IMPORTED_MODULE_8__["HTTP_INTERCEPTORS"],
                useClass: _shared_error_handling_error_interceptor__WEBPACK_IMPORTED_MODULE_11__["ErrorInterceptor"],
                multi: true,
            }
        ],
        bootstrap: [_app_component__WEBPACK_IMPORTED_MODULE_5__["AppComponent"]]
    })
], AppModule);



/***/ }),

/***/ "./src/app/reseller/reseller-routing.module.ts":
/*!*****************************************************!*\
  !*** ./src/app/reseller/reseller-routing.module.ts ***!
  \*****************************************************/
/*! exports provided: ResellerRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResellerRoutingModule", function() { return ResellerRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _shared_auth_login_login_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../shared/auth/login/login.component */ "./src/app/shared/auth/login/login.component.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");
/* harmony import */ var _shared_error_handling_page_not_found_page_not_found_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../shared/error-handling/page-not-found/page-not-found.component */ "./src/app/shared/error-handling/page-not-found/page-not-found.component.ts");






const routes = [
    {
        path: '',
        loadChildren: () => Promise.all(/*! import() | dashboard-dashboard-module */[__webpack_require__.e("default~api-users-api-users-module~clients-clients-module~configurations-configurations-module~dashb~41d6bc1a"), __webpack_require__.e("common"), __webpack_require__.e("dashboard-dashboard-module")]).then(__webpack_require__.bind(null, /*! ./dashboard/dashboard.module */ "./src/app/reseller/dashboard/dashboard.module.ts")).then(mod => mod.DashboardModule),
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__["AuthGuard"]],
    },
    {
        path: 'clients-users',
        loadChildren: () => __webpack_require__.e(/*! import() | clients-users-clients-users-module */ "clients-users-clients-users-module").then(__webpack_require__.bind(null, /*! ./clients-users/clients-users.module */ "./src/app/reseller/clients-users/clients-users.module.ts")).then(mod => mod.ClientsUsersModule),
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__["AuthGuard"]],
    },
    {
        path: 'cloud',
        loadChildren: () => __webpack_require__.e(/*! import() | cloud-cloud-module */ "cloud-cloud-module").then(__webpack_require__.bind(null, /*! ./cloud/cloud.module */ "./src/app/reseller/cloud/cloud.module.ts")).then(mod => mod.CloudModule),
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__["AuthGuard"]],
    },
    {
        path: 'billing',
        loadChildren: () => __webpack_require__.e(/*! import() | billing-billing-module */ "billing-billing-module").then(__webpack_require__.bind(null, /*! ./billing/billing.module */ "./src/app/reseller/billing/billing.module.ts")).then(mod => mod.BillingModule),
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__["AuthGuard"]],
    },
    {
        path: 'settings',
        loadChildren: () => __webpack_require__.e(/*! import() | settings-settings-module */ "settings-settings-module").then(__webpack_require__.bind(null, /*! ./settings/settings.module */ "./src/app/reseller/settings/settings.module.ts")).then(mod => mod.SettingsModule),
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__["AuthGuard"]],
    },
    {
        path: 'user-profile',
        loadChildren: () => __webpack_require__.e(/*! import() | profile-profile-module */ "profile-profile-module").then(__webpack_require__.bind(null, /*! ./profile/profile.module */ "./src/app/reseller/profile/profile.module.ts")).then(mod => mod.ProfileModule),
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__["AuthGuard"]],
    },
    {
        path: 'login',
        component: _shared_auth_login_login_component__WEBPACK_IMPORTED_MODULE_3__["LoginComponent"],
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__["AuthGuard"]],
    },
    {
        path: '**',
        component: _shared_error_handling_page_not_found_page_not_found_component__WEBPACK_IMPORTED_MODULE_5__["PageNotFoundComponent"],
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_4__["AuthGuard"]],
    }
];
let ResellerRoutingModule = class ResellerRoutingModule {
};
ResellerRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
    })
], ResellerRoutingModule);



/***/ }),

/***/ "./src/app/reseller/reseller.module.ts":
/*!*********************************************!*\
  !*** ./src/app/reseller/reseller.module.ts ***!
  \*********************************************/
/*! exports provided: ResellerModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResellerModule", function() { return ResellerModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _reseller_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./reseller-routing.module */ "./src/app/reseller/reseller-routing.module.ts");
/* harmony import */ var _reseller_reseller_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./reseller/reseller.component */ "./src/app/reseller/reseller/reseller.component.ts");
/* harmony import */ var _shared_shared_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../shared/shared.module */ "./src/app/shared/shared.module.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _shared_ui_ui_module__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../shared/ui/ui.module */ "./src/app/shared/ui/ui.module.ts");








let ResellerModule = class ResellerModule {
};
ResellerModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _reseller_reseller_component__WEBPACK_IMPORTED_MODULE_4__["ResellerComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _shared_shared_module__WEBPACK_IMPORTED_MODULE_5__["SharedModule"],
            _reseller_routing_module__WEBPACK_IMPORTED_MODULE_3__["ResellerRoutingModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_6__["FlexLayoutModule"],
            _shared_ui_ui_module__WEBPACK_IMPORTED_MODULE_7__["UiModule"],
        ],
        bootstrap: [_reseller_reseller_component__WEBPACK_IMPORTED_MODULE_4__["ResellerComponent"]],
    })
], ResellerModule);



/***/ }),

/***/ "./src/app/reseller/reseller/reseller.component.scss":
/*!***********************************************************!*\
  !*** ./src/app/reseller/reseller/reseller.component.scss ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3Jlc2VsbGVyL3Jlc2VsbGVyLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/reseller/reseller.component.ts":
/*!*********************************************************!*\
  !*** ./src/app/reseller/reseller/reseller.component.ts ***!
  \*********************************************************/
/*! exports provided: ResellerComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ResellerComponent", function() { return ResellerComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let ResellerComponent = class ResellerComponent {
    constructor() {
    }
    ngOnInit() {
    }
};
ResellerComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-reseller',
        template: __webpack_require__(/*! raw-loader!./reseller.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/reseller/reseller.component.html"),
        styles: [__webpack_require__(/*! ./reseller.component.scss */ "./src/app/reseller/reseller/reseller.component.scss")]
    })
], ResellerComponent);



/***/ }),

/***/ "./src/app/shared/auth/auth-interceptor.ts":
/*!*************************************************!*\
  !*** ./src/app/shared/auth/auth-interceptor.ts ***!
  \*************************************************/
/*! exports provided: AuthInterceptor */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AuthInterceptor", function() { return AuthInterceptor; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _ui_api_notification_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");




// TODO(manu): move this logic to a new EncoderInterceptor
class CustomEncoder {
    encodeKey(key) {
        return encodeURIComponent(key);
    }
    encodeValue(value) {
        return encodeURIComponent(value);
    }
    decodeKey(key) {
        return decodeURIComponent(key);
    }
    decodeValue(value) {
        return decodeURIComponent(value);
    }
}
let AuthInterceptor = class AuthInterceptor {
    constructor(notificationService) {
        this.notificationService = notificationService;
    }
    intercept(req, next) {
        const params = new _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpParams"]({ encoder: new CustomEncoder(), fromString: req.params.toString() });
        const updatedRequest = req.clone({
            withCredentials: true,
            params
        });
        return next.handle(updatedRequest);
    }
};
AuthInterceptor.ctorParameters = () => [
    { type: _ui_api_notification_service__WEBPACK_IMPORTED_MODULE_3__["NotificationService"] }
];
AuthInterceptor = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Injectable"])()
], AuthInterceptor);



/***/ }),

/***/ "./src/app/shared/auth/auth.guard.ts":
/*!*******************************************!*\
  !*** ./src/app/shared/auth/auth.guard.ts ***!
  \*******************************************/
/*! exports provided: AuthGuard */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AuthGuard", function() { return AuthGuard; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _auth_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./auth.service */ "./src/app/shared/auth/auth.service.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../config/config.service */ "./src/app/shared/config/config.service.ts");






let AuthGuard = class AuthGuard {
    constructor(authService, config, router) {
        this.authService = authService;
        this.config = config;
        this.router = router;
    }
    // TODO: extend this to perform feature check on routes too
    canActivate(route, state) {
        return this.authService.checkIfLoggedIn().pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["map"])(isAuthenticated => {
            const isLoginPage = route.routeConfig.path === 'login';
            if (isAuthenticated && isLoginPage) {
                // we are on login page, but we are already authenticated, go to home page
                return this.router.parseUrl(this.config.getPanelHomeUrl());
            }
            if (route.data.config && route.data.config.feature) {
                if (this.authService.userData.features[route.data.config.feature] === false) {
                    return this.router.parseUrl(this.config.getPanelUrl('404'));
                }
            }
            if (!isAuthenticated && !isLoginPage) {
                // we are not authenticated and we are not on login page, redirect to login page
                return this.router.parseUrl(this.config.getPanelUrl('login'));
            }
            return true;
        }));
    }
};
AuthGuard.ctorParameters = () => [
    { type: _auth_service__WEBPACK_IMPORTED_MODULE_3__["AuthService"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] }
];
AuthGuard = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], AuthGuard);



/***/ }),

/***/ "./src/app/shared/auth/auth.module.ts":
/*!********************************************!*\
  !*** ./src/app/shared/auth/auth.module.ts ***!
  \********************************************/
/*! exports provided: AuthModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AuthModule", function() { return AuthModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _login_login_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./login/login.component */ "./src/app/shared/auth/login/login.component.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _angular_material_card__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/card */ "./node_modules/@angular/material/esm2015/card.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm2015/button.js");
/* harmony import */ var _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material/slide-toggle */ "./node_modules/@angular/material/esm2015/slide-toggle.js");
/* harmony import */ var _error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _ui_ui_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../ui/ui.module */ "./src/app/shared/ui/ui.module.ts");












let AuthModule = class AuthModule {
};
AuthModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _login_login_component__WEBPACK_IMPORTED_MODULE_3__["LoginComponent"]
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormsModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_4__["ReactiveFormsModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatFormFieldModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_6__["MatInputModule"],
            _angular_material_card__WEBPACK_IMPORTED_MODULE_7__["MatCardModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_8__["MatButtonModule"],
            _angular_material_slide_toggle__WEBPACK_IMPORTED_MODULE_9__["MatSlideToggleModule"],
            _error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_10__["ErrorHandlingModule"],
            _ui_ui_module__WEBPACK_IMPORTED_MODULE_11__["UiModule"],
        ]
    })
], AuthModule);



/***/ }),

/***/ "./src/app/shared/auth/auth.service.ts":
/*!*********************************************!*\
  !*** ./src/app/shared/auth/auth.service.ts ***!
  \*********************************************/
/*! exports provided: AuthService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AuthService", function() { return AuthService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");






let AuthService = class AuthService {
    constructor(httpClient, config) {
        this.httpClient = httpClient;
        this.config = config;
        // NOTE: user data should be refreshed from time to time
        this.userDataBS = new rxjs__WEBPACK_IMPORTED_MODULE_4__["BehaviorSubject"](null);
        this.isLoggedInBS = new rxjs__WEBPACK_IMPORTED_MODULE_4__["BehaviorSubject"](false);
        this.observableUserData = this.userDataBS.asObservable();
        this.isLoggedIn = this.isLoggedInBS.asObservable();
        this.userData = null;
        this.loginEndpoint = this.config.getPanelApiUrl('login');
        this.logoutEndpoint = this.config.getPanelApiUrl('logout');
        this.currentUserEndpoint = this.config.getPanelApiUrl('current-user');
    }
    feature(featureName) {
        if (this.userData && this.userData.features) {
            return !!this.userData.features[featureName];
        }
        // defaults to false if no feature found
        return false;
    }
    checkIfLoggedIn() {
        return this.httpClient.get(this.currentUserEndpoint).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(currentUserData => {
            this.userData = currentUserData;
            this.userDataBS.next(this.userData);
            const loggedIn = !!this.userData.user;
            this.isLoggedInBS.next(loggedIn);
            return loggedIn;
        }));
    }
    login(username, password, rememberMe) {
        return this.httpClient.post(this.loginEndpoint, {
            username,
            password,
            remember_me: rememberMe,
            sfa_params: null
        }).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(currentUserData => {
            this.userData = currentUserData;
            return { success: true, errorMessage: '' };
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["catchError"])((err) => {
            // TODO: find a way to use constants instead of codes here
            if (err.status === 401) {
                return Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["of"])({
                    success: false,
                    errorMessage: err.error.detail || 'Incorrect user name or password'
                });
            }
            return Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["throwError"])(err);
        }));
    }
    logout() {
        return this.httpClient.post(this.logoutEndpoint, {}).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_5__["map"])(response => {
            return response;
        }));
    }
    isImpersonating() {
        return this.userData && this.userData.impersonated;
    }
    stopImpersonating() {
        const staffBackendUrl = localStorage.getItem('fleio.flStaffBackend');
        const staffFrontendUrl = localStorage.getItem('fleio.flStaffUrl');
        this.httpClient.post(`${staffBackendUrl}/users/stop_impersonation`, {}).subscribe(() => {
            window.location.href = staffFrontendUrl;
        });
    }
};
AuthService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] }
];
AuthService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], AuthService);



/***/ }),

/***/ "./src/app/shared/auth/login/login.component.scss":
/*!********************************************************!*\
  !*** ./src/app/shared/auth/login/login.component.scss ***!
  \********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".login-card {\n  max-width: 348px;\n  margin-top: 60px;\n  position: relative;\n}\n\n.card-title {\n  font-weight: 300;\n}\n\nmat-form-field {\n  margin-top: 25px;\n  width: 100%;\n}\n\nmat-slide-toggle {\n  margin-top: 50px;\n}\n\nmat-card-actions > div {\n  margin-top: 20px;\n}\n\nmat-card-actions > div:last-child {\n  margin-bottom: 30px;\n}\n\n.login-button {\n  width: 60%;\n}\n\n.powered-by-link {\n  margin-top: 20px;\n  margin-bottom: 20px;\n  display: block;\n}\n\n@media screen and (max-width: 980px) {\n  .login-card {\n    margin-top: 0 !important;\n  }\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC9hdXRoL2xvZ2luL2xvZ2luLmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9zaGFyZWQvYXV0aC9sb2dpbi9sb2dpbi5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGdCQUFBO0VBQ0EsZ0JBQUE7RUFDQSxrQkFBQTtBQ0NGOztBREVBO0VBQ0UsZ0JBQUE7QUNDRjs7QURFQTtFQUNFLGdCQUFBO0VBQ0EsV0FBQTtBQ0NGOztBREVBO0VBQ0UsZ0JBQUE7QUNDRjs7QURFQTtFQUNFLGdCQUFBO0FDQ0Y7O0FERUE7RUFDRSxtQkFBQTtBQ0NGOztBREVBO0VBQ0UsVUFBQTtBQ0NGOztBREVBO0VBQ0UsZ0JBQUE7RUFDQSxtQkFBQTtFQUNBLGNBQUE7QUNDRjs7QURFQTtFQUNFO0lBQ0Usd0JBQUE7RUNDRjtBQUNGIiwiZmlsZSI6InNyYy9hcHAvc2hhcmVkL2F1dGgvbG9naW4vbG9naW4uY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIubG9naW4tY2FyZCB7XG4gIG1heC13aWR0aDogMzQ4cHg7XG4gIG1hcmdpbi10b3A6IDYwcHg7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbn1cblxuLmNhcmQtdGl0bGUge1xuICBmb250LXdlaWdodDogMzAwO1xufVxuXG5tYXQtZm9ybS1maWVsZCB7XG4gIG1hcmdpbi10b3A6IDI1cHg7XG4gIHdpZHRoOiAxMDAlO1xufVxuXG5tYXQtc2xpZGUtdG9nZ2xlIHtcbiAgbWFyZ2luLXRvcDogNTBweDtcbn1cblxubWF0LWNhcmQtYWN0aW9ucyA+IGRpdiB7XG4gIG1hcmdpbi10b3A6IDIwcHg7XG59XG5cbm1hdC1jYXJkLWFjdGlvbnMgPiBkaXY6bGFzdC1jaGlsZCB7XG4gIG1hcmdpbi1ib3R0b206IDMwcHg7XG59XG5cbi5sb2dpbi1idXR0b24ge1xuICB3aWR0aDogNjAlO1xufVxuXG4ucG93ZXJlZC1ieS1saW5rIHtcbiAgbWFyZ2luLXRvcDogMjBweDtcbiAgbWFyZ2luLWJvdHRvbTogMjBweDtcbiAgZGlzcGxheTogYmxvY2s7XG59XG5cbkBtZWRpYSBzY3JlZW4gYW5kIChtYXgtd2lkdGg6IDk4MHB4KXtcbiAgLmxvZ2luLWNhcmQge1xuICAgIG1hcmdpbi10b3A6IDAgIWltcG9ydGFudDtcbiAgfVxufVxuIiwiLmxvZ2luLWNhcmQge1xuICBtYXgtd2lkdGg6IDM0OHB4O1xuICBtYXJnaW4tdG9wOiA2MHB4O1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG59XG5cbi5jYXJkLXRpdGxlIHtcbiAgZm9udC13ZWlnaHQ6IDMwMDtcbn1cblxubWF0LWZvcm0tZmllbGQge1xuICBtYXJnaW4tdG9wOiAyNXB4O1xuICB3aWR0aDogMTAwJTtcbn1cblxubWF0LXNsaWRlLXRvZ2dsZSB7XG4gIG1hcmdpbi10b3A6IDUwcHg7XG59XG5cbm1hdC1jYXJkLWFjdGlvbnMgPiBkaXYge1xuICBtYXJnaW4tdG9wOiAyMHB4O1xufVxuXG5tYXQtY2FyZC1hY3Rpb25zID4gZGl2Omxhc3QtY2hpbGQge1xuICBtYXJnaW4tYm90dG9tOiAzMHB4O1xufVxuXG4ubG9naW4tYnV0dG9uIHtcbiAgd2lkdGg6IDYwJTtcbn1cblxuLnBvd2VyZWQtYnktbGluayB7XG4gIG1hcmdpbi10b3A6IDIwcHg7XG4gIG1hcmdpbi1ib3R0b206IDIwcHg7XG4gIGRpc3BsYXk6IGJsb2NrO1xufVxuXG5AbWVkaWEgc2NyZWVuIGFuZCAobWF4LXdpZHRoOiA5ODBweCkge1xuICAubG9naW4tY2FyZCB7XG4gICAgbWFyZ2luLXRvcDogMCAhaW1wb3J0YW50O1xuICB9XG59Il19 */"

/***/ }),

/***/ "./src/app/shared/auth/login/login.component.ts":
/*!******************************************************!*\
  !*** ./src/app/shared/auth/login/login.component.ts ***!
  \******************************************************/
/*! exports provided: LoginComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LoginComponent", function() { return LoginComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _auth_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../auth.service */ "./src/app/shared/auth/auth.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../config/config.service */ "./src/app/shared/config/config.service.ts");






let LoginComponent = class LoginComponent {
    constructor(formBuilder, router, auth, config) {
        this.formBuilder = formBuilder;
        this.router = router;
        this.auth = auth;
        this.config = config;
        this.loginForm = this.formBuilder.group({
            username: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            password: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            rememberMe: [false]
        });
    }
    ngOnInit() {
    }
    login() {
        this.auth.login(this.loginForm.controls.username.value, this.loginForm.controls.password.value, this.loginForm.controls.rememberMe.value).subscribe((authResult) => {
            if (authResult.success) {
                // TODO: see about this warning
                // TODO: go back instead of home if possible
                this.router.navigateByUrl(this.config.getPrevUrl()).then(() => { });
            }
            else {
                this.formErrors.showError(authResult.errorMessage);
            }
        });
    }
};
LoginComponent.ctorParameters = () => [
    { type: _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _auth_service__WEBPACK_IMPORTED_MODULE_3__["AuthService"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('formErrors', { static: false })
], LoginComponent.prototype, "formErrors", void 0);
LoginComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-login',
        template: __webpack_require__(/*! raw-loader!./login.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/auth/login/login.component.html"),
        styles: [__webpack_require__(/*! ./login.component.scss */ "./src/app/shared/auth/login/login.component.scss")]
    })
], LoginComponent);



/***/ }),

/***/ "./src/app/shared/config/config.module.ts":
/*!************************************************!*\
  !*** ./src/app/shared/config/config.module.ts ***!
  \************************************************/
/*! exports provided: ConfigModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigModule", function() { return ConfigModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./config.service */ "./src/app/shared/config/config.service.ts");





let ConfigModule = class ConfigModule {
    constructor(router, config) {
        this.router = router;
        this.config = config;
        this.config.subscribeToRouterEvents(router);
    }
};
ConfigModule.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
    { type: _config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] }
];
ConfigModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"]
        ]
    })
], ConfigModule);



/***/ }),

/***/ "./src/app/shared/config/config.service.ts":
/*!*************************************************!*\
  !*** ./src/app/shared/config/config.service.ts ***!
  \*************************************************/
/*! exports provided: ConfigService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigService", function() { return ConfigService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm2015/platform-browser.js");





const configFilesPath = 'assets/config/';
const appConfigFile = configFilesPath + 'app.config.json';
let ConfigService = class ConfigService {
    constructor(httpClient, title, locale) {
        this.httpClient = httpClient;
        this.title = title;
        this.locale = locale;
        this.isSubscribedToRouterEvents = false;
        this.panels = {};
        this.previousUrl = null;
    }
    _initShortcuts() {
        if (this.panels.hasOwnProperty('enduser')) {
            this.enduser = this.panels.enduser;
        }
        if (this.panels.hasOwnProperty('reseller')) {
            this.reseller = this.panels.reseller;
        }
        if (this.panels.hasOwnProperty('staff')) {
            this.staff = this.panels.staff;
        }
    }
    setActiveConfiguration(configurationName) {
        // update configuration
        this.current = this.panels[configurationName];
        // TODO: load this dynamically
        this.title.setTitle(configurationName);
    }
    setActiveUrl(url) {
        // update urls
        this.previousUrl = this.currentUrl;
        this.currentUrl = url;
    }
    subscribeToRouterEvents(router) {
        if (!this.isSubscribedToRouterEvents) {
            router.events.subscribe(event => {
                if (event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_3__["RouteConfigLoadStart"]) {
                    const routeConfigLoadStart = event;
                    if (routeConfigLoadStart.route.data && routeConfigLoadStart.route.data.configurationName) {
                        this.setActiveConfiguration(routeConfigLoadStart.route.data.configurationName);
                    }
                }
                if (event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_3__["NavigationEnd"]) {
                    this.setActiveUrl(event.url);
                }
            });
            this.isSubscribedToRouterEvents = true;
        }
    }
    getPanelApiUrl(endpoint) {
        return this.current.urls.backendApiUrl + endpoint;
    }
    getPanelUrl(fragment) {
        const url = this.current.urls.baseUrl + fragment;
        return url;
    }
    getPanelHomeUrl() {
        // TODO: rename homeUrl to home name and also rename this function
        return this.current.urls.homeUrl;
    }
    getImagePath(imageName) {
        return this.current.settings.imagesPath + imageName;
    }
    getPrevUrl(defaultFragment = null) {
        if (this.previousUrl != null) {
            return this.previousUrl;
        }
        else {
            return defaultFragment == null ? this.getPanelHomeUrl() : this.getPanelUrl(defaultFragment);
        }
    }
    getCurrentUrl() {
        return this.currentUrl;
    }
    loadPanelConfiguration(panelName, fileName) {
        return new Promise((resolve, reject) => {
            const panelConfigFile = configFilesPath + fileName;
            this.httpClient.get(panelConfigFile).toPromise().then((response) => {
                this.panels[panelName] = response;
                resolve();
            }).catch(() => {
                reject('Failed to load configuration file ${fileName} for panel ${panelName}');
            });
        });
    }
    load() {
        return new Promise((resolve, reject) => {
            this.httpClient.get(appConfigFile).toPromise().then((response) => {
                this.app = response;
                const promises = [];
                Object.keys(this.app.panels).map(panelName => {
                    const panel = this.app.panels[panelName];
                    promises.push(this.loadPanelConfiguration(panelName, panel.configFile));
                });
                Promise.all(promises).then(() => {
                    this._initShortcuts();
                    resolve();
                }).catch(() => {
                    reject('Failed to load panel configurations');
                });
            }).catch(() => {
                reject('Failed to load application configuration');
            });
        });
    }
};
ConfigService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] },
    { type: _angular_platform_browser__WEBPACK_IMPORTED_MODULE_4__["Title"] },
    { type: String, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"], args: [_angular_core__WEBPACK_IMPORTED_MODULE_1__["LOCALE_ID"],] }] }
];
ConfigService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__param"](2, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(_angular_core__WEBPACK_IMPORTED_MODULE_1__["LOCALE_ID"]))
], ConfigService);



/***/ }),

/***/ "./src/app/shared/error-handling/error-handling.module.ts":
/*!****************************************************************!*\
  !*** ./src/app/shared/error-handling/error-handling.module.ts ***!
  \****************************************************************/
/*! exports provided: ErrorHandlingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ErrorHandlingModule", function() { return ErrorHandlingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _page_not_found_page_not_found_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./page-not-found/page-not-found.component */ "./src/app/shared/error-handling/page-not-found/page-not-found.component.ts");
/* harmony import */ var _form_errors_form_errors_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./form-errors/form-errors.component */ "./src/app/shared/error-handling/form-errors/form-errors.component.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm2015/button.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");








let ErrorHandlingModule = class ErrorHandlingModule {
};
ErrorHandlingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _page_not_found_page_not_found_component__WEBPACK_IMPORTED_MODULE_3__["PageNotFoundComponent"],
            _form_errors_form_errors_component__WEBPACK_IMPORTED_MODULE_4__["FormErrorsComponent"]
        ],
        exports: [
            _form_errors_form_errors_component__WEBPACK_IMPORTED_MODULE_4__["FormErrorsComponent"]
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_5__["MatFormFieldModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_6__["MatButtonModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_7__["FlexLayoutModule"],
        ]
    })
], ErrorHandlingModule);



/***/ }),

/***/ "./src/app/shared/error-handling/error-interceptor.ts":
/*!************************************************************!*\
  !*** ./src/app/shared/error-handling/error-interceptor.ts ***!
  \************************************************************/
/*! exports provided: ErrorInterceptor */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ErrorInterceptor", function() { return ErrorInterceptor; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _ui_api_notification_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../ui-api/notification.service */ "./src/app/shared/ui-api/notification.service.ts");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _auth_auth_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../auth/auth.service */ "./src/app/shared/auth/auth.service.ts");









let ErrorInterceptor = class ErrorInterceptor {
    constructor(notificationService, configService, router, httpClient) {
        this.notificationService = notificationService;
        this.configService = configService;
        this.router = router;
        this.httpClient = httpClient;
    }
    initAuthService() {
        if (!this.authService) {
            this.authService = new _auth_auth_service__WEBPACK_IMPORTED_MODULE_8__["AuthService"](this.httpClient, this.configService);
        }
    }
    intercept(req, next) {
        return next.handle(req).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_4__["catchError"])(error => {
            if (error instanceof _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpErrorResponse"]) {
                const httpError = error;
                switch (httpError.status) {
                    case 401:
                        // authorization error
                        if (this.configService.getCurrentUrl() === this.configService.getPanelUrl('login')) {
                            // we are at login page, pass error
                            throw error;
                        }
                        console.warn('Unauthorized, redirecting to login');
                        this.notificationService.showMessage(error.error.detail);
                        this.initAuthService();
                        this.authService.logout().subscribe(() => {
                            this.router.navigateByUrl(this.configService.getPanelUrl('login')).then(() => { });
                        });
                        return rxjs__WEBPACK_IMPORTED_MODULE_3__["EMPTY"];
                    case 400:
                        // ignored errors, will be treated by caller
                        break;
                    default:
                        this.notificationService.showMessage(`HTTP Error ${httpError.status}: ${httpError.statusText}`);
                }
            }
            throw error;
        }));
    }
};
ErrorInterceptor.ctorParameters = () => [
    { type: _ui_api_notification_service__WEBPACK_IMPORTED_MODULE_5__["NotificationService"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_6__["ConfigService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_7__["Router"] },
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"] }
];
ErrorInterceptor = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Injectable"])()
], ErrorInterceptor);



/***/ }),

/***/ "./src/app/shared/error-handling/form-errors/form-errors.component.scss":
/*!******************************************************************************!*\
  !*** ./src/app/shared/error-handling/form-errors/form-errors.component.scss ***!
  \******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".content {\n  background-color: #f0f0ee;\n  padding: 10px;\n  overflow: auto;\n}\n\n.messages {\n  display: -webkit-box;\n  display: flex;\n  -webkit-box-align: center;\n          align-items: center;\n}\n\n.button {\n  display: -webkit-box;\n  display: flex;\n  -webkit-box-align: center;\n          align-items: center;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC9lcnJvci1oYW5kbGluZy9mb3JtLWVycm9ycy9mb3JtLWVycm9ycy5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvc2hhcmVkL2Vycm9yLWhhbmRsaW5nL2Zvcm0tZXJyb3JzL2Zvcm0tZXJyb3JzLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UseUJBQUE7RUFDQSxhQUFBO0VBQ0EsY0FBQTtBQ0NGOztBREVBO0VBQ0Usb0JBQUE7RUFBQSxhQUFBO0VBQ0EseUJBQUE7VUFBQSxtQkFBQTtBQ0NGOztBREVBO0VBQ0Usb0JBQUE7RUFBQSxhQUFBO0VBQ0EseUJBQUE7VUFBQSxtQkFBQTtBQ0NGIiwiZmlsZSI6InNyYy9hcHAvc2hhcmVkL2Vycm9yLWhhbmRsaW5nL2Zvcm0tZXJyb3JzL2Zvcm0tZXJyb3JzLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLmNvbnRlbnQge1xuICBiYWNrZ3JvdW5kLWNvbG9yOiAjZjBmMGVlO1xuICBwYWRkaW5nOiAxMHB4O1xuICBvdmVyZmxvdzogYXV0bztcbn1cblxuLm1lc3NhZ2VzIHtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cblxuLmJ1dHRvbiB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG59XG4iLCIuY29udGVudCB7XG4gIGJhY2tncm91bmQtY29sb3I6ICNmMGYwZWU7XG4gIHBhZGRpbmc6IDEwcHg7XG4gIG92ZXJmbG93OiBhdXRvO1xufVxuXG4ubWVzc2FnZXMge1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogY2VudGVyO1xufVxuXG4uYnV0dG9uIHtcbiAgZGlzcGxheTogZmxleDtcbiAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/shared/error-handling/form-errors/form-errors.component.ts":
/*!****************************************************************************!*\
  !*** ./src/app/shared/error-handling/form-errors/form-errors.component.ts ***!
  \****************************************************************************/
/*! exports provided: FormErrorsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FormErrorsComponent", function() { return FormErrorsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let FormErrorsComponent = class FormErrorsComponent {
    constructor() {
        this.visible = false;
    }
    ngOnInit() {
    }
    hide() {
        this.visible = false;
    }
    setBackendErrors(backendErrors) {
        if (typeof backendErrors === 'string') {
            this.showError(backendErrors);
            return;
        }
        const nonFieldErrors = [];
        Object.keys(backendErrors).map(fieldName => {
            const control = this.formGroup.get(fieldName);
            if (control && !control.disabled) {
                control.markAsTouched();
                control.setErrors({ backend: true });
            }
            else {
                nonFieldErrors.push(`${fieldName}: ${backendErrors[fieldName]}`);
            }
        });
        if (nonFieldErrors.length > 0) {
            this.showMultipleErrors(nonFieldErrors);
        }
    }
    showMultipleErrors(errorMessages) {
        this.errorMessages = errorMessages;
        this.visible = true;
    }
    showError(errorMessage) {
        this.showMultipleErrors([errorMessage]);
    }
};
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], FormErrorsComponent.prototype, "formGroup", void 0);
FormErrorsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-form-errors',
        template: __webpack_require__(/*! raw-loader!./form-errors.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/error-handling/form-errors/form-errors.component.html"),
        styles: [__webpack_require__(/*! ./form-errors.component.scss */ "./src/app/shared/error-handling/form-errors/form-errors.component.scss")]
    })
], FormErrorsComponent);



/***/ }),

/***/ "./src/app/shared/error-handling/page-not-found/page-not-found.component.scss":
/*!************************************************************************************!*\
  !*** ./src/app/shared/error-handling/page-not-found/page-not-found.component.scss ***!
  \************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC9lcnJvci1oYW5kbGluZy9wYWdlLW5vdC1mb3VuZC9wYWdlLW5vdC1mb3VuZC5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/shared/error-handling/page-not-found/page-not-found.component.ts":
/*!**********************************************************************************!*\
  !*** ./src/app/shared/error-handling/page-not-found/page-not-found.component.ts ***!
  \**********************************************************************************/
/*! exports provided: PageNotFoundComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PageNotFoundComponent", function() { return PageNotFoundComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let PageNotFoundComponent = class PageNotFoundComponent {
    constructor() {
    }
    ngOnInit() {
    }
};
PageNotFoundComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-page-not-found',
        template: __webpack_require__(/*! raw-loader!./page-not-found.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/error-handling/page-not-found/page-not-found.component.html"),
        styles: [__webpack_require__(/*! ./page-not-found.component.scss */ "./src/app/shared/error-handling/page-not-found/page-not-found.component.scss")]
    })
], PageNotFoundComponent);



/***/ }),

/***/ "./src/app/shared/fleio-data-controls/phone-input/phone-input.component.scss":
/*!***********************************************************************************!*\
  !*** ./src/app/shared/fleio-data-controls/phone-input/phone-input.component.scss ***!
  \***********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC9mbGVpby1kYXRhLWNvbnRyb2xzL3Bob25lLWlucHV0L3Bob25lLWlucHV0LmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/shared/fleio-data-controls/phone-input/phone-input.component.ts":
/*!*********************************************************************************!*\
  !*** ./src/app/shared/fleio-data-controls/phone-input/phone-input.component.ts ***!
  \*********************************************************************************/
/*! exports provided: PhoneInputComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PhoneInputComponent", function() { return PhoneInputComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let PhoneInputComponent = class PhoneInputComponent {
    constructor() {
        this.phoneNumber = '';
        this.changedPhone = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.error = null;
        this.countryCodes = {
            1: ['US', 'AG', 'AI', 'AS', 'BB', 'BM', 'BS', 'CA', 'DM', 'DO', 'GD', 'GU', 'JM', 'KN', 'KY', 'LC', 'MP',
                'MS', 'PR', 'SX', 'TC', 'TT', 'VC', 'VG', 'VI'],
            598: ['UY'], 7: ['RU', 'KZ'], 20: ['EG'], 27: ['ZA'], 30: ['GR'], 31: ['NL'], 32: ['BE'],
            33: ['FR'], 34: ['ES'], 36: ['HU'], 39: ['IT', 'VA'], 40: ['RO'], 41: ['CH'], 43: ['AT'],
            44: ['GB', 'GG', 'IM', 'JE'], 45: ['DK'], 46: ['SE'], 47: ['NO', 'SJ'], 48: ['PL'], 49: ['DE'],
            51: ['PE'], 52: ['MX'], 53: ['CU'], 54: ['AR'], 55: ['BR'], 56: ['CL'], 57: ['CO'], 58: ['VE'],
            60: ['MY'], 61: ['AU', 'CC', 'CX'], 62: ['ID'], 63: ['PH'], 64: ['NZ'], 65: ['SG'], 66: ['TH'],
            590: ['GP', 'BL', 'MF'], 591: ['BO'], 592: ['GY'], 81: ['JP'], 82: ['KR'], 595: ['PY'],
            84: ['VN'], 597: ['SR'], 86: ['CN'], 599: ['CW', 'BQ'], 90: ['TR'], 91: ['IN'], 92: ['PK'],
            93: ['AF'], 94: ['LK'], 95: ['MM'], 98: ['IR'], 870: ['001'], 670: ['TL'], 672: ['NF'],
            673: ['BN'], 674: ['NR'], 675: ['PG'], 676: ['TO'], 677: ['SB'], 678: ['VU'], 679: ['FJ'],
            680: ['PW'], 681: ['WF'], 682: ['CK'], 683: ['NU'], 685: ['WS'], 686: ['KI'], 687: ['NC'],
            688: ['TV'], 689: ['PF'], 690: ['TK'], 691: ['FM'], 692: ['MH'], 886: ['TW'], 888: ['001'],
            211: ['SS'], 212: ['MA', 'EH'], 213: ['DZ'], 216: ['TN'], 218: ['LY'], 220: ['GM'], 221: ['SN'],
            222: ['MR'], 223: ['ML'], 224: ['GN'], 225: ['CI'], 226: ['BF'], 227: ['NE'], 228: ['TG'],
            229: ['BJ'], 230: ['MU'], 231: ['LR'], 232: ['SL'], 233: ['GH'], 234: ['NG'], 235: ['TD'],
            236: ['CF'], 237: ['CM'], 238: ['CV'], 239: ['ST'], 240: ['GQ'], 241: ['GA'], 242: ['CG'],
            243: ['CD'], 244: ['AO'], 245: ['GW'], 246: ['IO'], 247: ['AC'], 248: ['SC'], 249: ['SD'],
            250: ['RW'], 251: ['ET'], 252: ['SO'], 253: ['DJ'], 254: ['KE'], 255: ['TZ'], 256: ['UG'],
            257: ['BI'], 258: ['MZ'], 260: ['ZM'], 261: ['MG'], 262: ['RE', 'YT'], 263: ['ZW'], 264: ['NA'],
            265: ['MW'], 266: ['LS'], 267: ['BW'], 268: ['SZ'], 269: ['KM'], 800: ['001'], 290: ['SH', 'TA'],
            291: ['ER'], 808: ['001'], 297: ['AW'], 298: ['FO'], 299: ['GL'], 882: ['001'], 850: ['KP'],
            852: ['HK'], 853: ['MO'], 855: ['KH'], 856: ['LA'], 350: ['GI'], 351: ['PT'], 352: ['LU'],
            353: ['IE'], 354: ['IS'], 355: ['AL'], 356: ['MT'], 357: ['CY'], 358: ['FI', 'AX'], 359: ['BG'],
            878: ['001'], 880: ['BD'], 881: ['001'], 370: ['LT'], 371: ['LV'], 372: ['EE'], 373: ['MD'],
            374: ['AM'], 375: ['BY'], 376: ['AD'], 377: ['MC'], 378: ['SM'], 380: ['UA'], 381: ['RS'],
            382: ['ME'], 383: ['XK'], 385: ['HR'], 386: ['SI'], 387: ['BA'], 389: ['MK'], 883: ['001'],
            420: ['CZ'], 421: ['SK'], 423: ['LI'], 960: ['MV'], 961: ['LB'], 962: ['JO'], 963: ['SY'],
            964: ['IQ'], 965: ['KW'], 966: ['SA'], 967: ['YE'], 968: ['OM'], 970: ['PS'], 971: ['AE'],
            972: ['IL'], 973: ['BH'], 974: ['QA'], 975: ['BT'], 976: ['MN'], 977: ['NP'], 979: ['001'],
            505: ['NI'], 992: ['TJ'], 993: ['TM'], 994: ['AZ'], 995: ['GE'], 996: ['KG'], 998: ['UZ'],
            593: ['EC'], 594: ['GF'], 500: ['FK'], 501: ['BZ'], 502: ['GT'], 503: ['SV'], 504: ['HN'],
            596: ['MQ'], 506: ['CR'], 507: ['PA'], 508: ['PM'], 509: ['HT']
        };
        this.countryCodeKeys = Object.keys(this.countryCodes);
    }
    changePhoneCountry() {
        if (this.phoneNumber && this.phoneNumber[0] === '+') {
            if (this.countryCodes.hasOwnProperty(this.phoneNumber.substring(1, 3))) {
                this.phoneNumber = this.phoneNumber.substring(3, this.phoneNumber.length);
                this.phoneNumber = '+' + this.flag + this.phoneNumber;
                return this.changedPhone.emit(this.phoneNumber);
            }
            else if (this.countryCodes.hasOwnProperty(this.phoneNumber.substring(1, 2))) {
                this.phoneNumber = this.phoneNumber.substring(2, this.phoneNumber.length);
                this.phoneNumber = '+' + this.flag + this.phoneNumber;
                return this.changedPhone.emit(this.phoneNumber);
            }
            else if (this.countryCodes.hasOwnProperty(this.phoneNumber.substring(1, 1))) {
                this.phoneNumber = this.phoneNumber.substring(1, this.phoneNumber.length);
                this.phoneNumber = '+' + this.flag + this.phoneNumber;
                return this.changedPhone.emit(this.phoneNumber);
            }
        }
        this.phoneNumber = '+' + this.flag + this.phoneNumber;
        this.changedPhone.emit(this.phoneNumber);
    }
    updateFlagOnPhoneChange(newPhone) {
        if (newPhone) {
            if (this.error) {
                this.error = null;
            }
            this.phoneNumber = newPhone;
        }
        this.changedPhone.emit(this.phoneNumber);
        if (this.phoneNumber && this.phoneNumber[0] === '+') {
            if (this.countryCodes.hasOwnProperty(this.phoneNumber.substring(1, 3))) {
                this.flag = this.phoneNumber.substring(1, 3);
            }
            else if (this.countryCodes.hasOwnProperty(this.phoneNumber.substring(1, 2))) {
                this.flag = this.phoneNumber.substring(1, 2);
            }
            else if (this.countryCodes.hasOwnProperty(this.phoneNumber.substring(1, 1))) {
                this.flag = this.phoneNumber.substring(1, 1);
            }
        }
    }
    ngOnInit() {
        this.updateFlagOnPhoneChange();
    }
};
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], PhoneInputComponent.prototype, "phoneNumber", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"])()
], PhoneInputComponent.prototype, "changedPhone", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('phoneNumberInput', { static: false })
], PhoneInputComponent.prototype, "phoneNumberInput", void 0);
PhoneInputComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-phone-input',
        template: __webpack_require__(/*! raw-loader!./phone-input.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/fleio-data-controls/phone-input/phone-input.component.html"),
        styles: [__webpack_require__(/*! ./phone-input.component.scss */ "./src/app/shared/fleio-data-controls/phone-input/phone-input.component.scss")]
    })
], PhoneInputComponent);



/***/ }),

/***/ "./src/app/shared/shared.module.ts":
/*!*****************************************!*\
  !*** ./src/app/shared/shared.module.ts ***!
  \*****************************************/
/*! exports provided: SharedModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SharedModule", function() { return SharedModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _auth_auth_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./auth/auth.module */ "./src/app/shared/auth/auth.module.ts");
/* harmony import */ var _error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _config_config_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./config/config.module */ "./src/app/shared/config/config.module.ts");
/* harmony import */ var _ui_api_ui_api_module__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./ui-api/ui-api.module */ "./src/app/shared/ui-api/ui-api.module.ts");







let SharedModule = class SharedModule {
};
SharedModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _auth_auth_module__WEBPACK_IMPORTED_MODULE_3__["AuthModule"],
            _error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_4__["ErrorHandlingModule"],
            _config_config_module__WEBPACK_IMPORTED_MODULE_5__["ConfigModule"],
            _ui_api_ui_api_module__WEBPACK_IMPORTED_MODULE_6__["UiApiModule"],
        ]
    })
], SharedModule);



/***/ }),

/***/ "./src/app/shared/ui-api/app-local-storage.service.ts":
/*!************************************************************!*\
  !*** ./src/app/shared/ui-api/app-local-storage.service.ts ***!
  \************************************************************/
/*! exports provided: AppLocalStorageService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppLocalStorageService", function() { return AppLocalStorageService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _auth_auth_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../auth/auth.service */ "./src/app/shared/auth/auth.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _route_helper__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./route-helper */ "./src/app/shared/ui-api/route-helper.ts");





let AppLocalStorageService = class AppLocalStorageService {
    constructor(authService, activatedRoute) {
        this.authService = authService;
        this.activatedRoute = activatedRoute;
    }
    setItem(item, value) {
        if (this.authService.userData.user && this.authService.userData.user.username) {
            localStorage.setItem(this.authService.userData.user.username + item, value);
        }
        else {
            localStorage.setItem(item, value);
        }
    }
    getItem(item) {
        if (this.authService.userData.user && this.authService.userData.user.username) {
            return localStorage.getItem(this.authService.userData.user.username + item);
        }
        else {
            return localStorage.getItem(item);
        }
    }
    setOrderingItem(orderingItem, routePath = null) {
        const routeHelper = new _route_helper__WEBPACK_IMPORTED_MODULE_4__["RouteHelper"](this.activatedRoute);
        this.setItem('-ordering-' + (routePath || routeHelper.getRoutePath()), JSON.stringify(orderingItem));
    }
    getOrderingItem(routePath = null) {
        const routeHelper = new _route_helper__WEBPACK_IMPORTED_MODULE_4__["RouteHelper"](this.activatedRoute);
        const savedValue = this.getItem('-ordering-' + (routePath || routeHelper.getRoutePath()));
        if (savedValue) {
            return JSON.parse(savedValue);
        }
        return null;
    }
    setCardsDisplay(cardsDisplay) {
        const routeHelper = new _route_helper__WEBPACK_IMPORTED_MODULE_4__["RouteHelper"](this.activatedRoute);
        this.setItem('-cardsdisplay-' + routeHelper.getRoutePath(), JSON.stringify(cardsDisplay));
    }
    getCardsDisplay() {
        const routeHelper = new _route_helper__WEBPACK_IMPORTED_MODULE_4__["RouteHelper"](this.activatedRoute);
        const savedValue = this.getItem('-cardsdisplay-' + routeHelper.getRoutePath());
        if (savedValue) {
            return JSON.parse(savedValue);
        }
        return null;
    }
};
AppLocalStorageService.ctorParameters = () => [
    { type: _auth_auth_service__WEBPACK_IMPORTED_MODULE_2__["AuthService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] }
];
AppLocalStorageService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], AppLocalStorageService);



/***/ }),

/***/ "./src/app/shared/ui-api/helpers/ordering-helper.ts":
/*!**********************************************************!*\
  !*** ./src/app/shared/ui-api/helpers/ordering-helper.ts ***!
  \**********************************************************/
/*! exports provided: OrderingHelper */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OrderingHelper", function() { return OrderingHelper; });
/* harmony import */ var _interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");

class OrderingHelper {
    static getOrderingValue(orderingOption) {
        switch (orderingOption.direction) {
            case _interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_0__["OrderingDirection"].Ascending:
                return orderingOption.field;
            case _interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_0__["OrderingDirection"].Descending:
                return '-' + orderingOption.field;
            default:
                return orderingOption.field;
        }
    }
    static getOrderingOptionFieldAndDirection(orderingValue) {
        if (orderingValue.startsWith('-')) {
            return {
                field: orderingValue.substr(1),
                direction: _interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_0__["OrderingDirection"].Descending
            };
        }
        return {
            field: orderingValue,
            direction: _interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_0__["OrderingDirection"].Ascending
        };
    }
    static isDescending(orderingOption) {
        switch (orderingOption.direction) {
            case _interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_0__["OrderingDirection"].Ascending:
                return false;
            case _interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_0__["OrderingDirection"].Descending:
                return true;
            default:
                return false;
        }
    }
    static fromSort(sort) {
        return {
            field: sort.active,
            display: null,
            direction: sort.direction === 'asc' ? _interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_0__["OrderingDirection"].Ascending : _interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_0__["OrderingDirection"].Descending,
        };
    }
    static toSort(orderingConfig) {
        return {
            active: orderingConfig.field,
            direction: orderingConfig.direction === _interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_0__["OrderingDirection"].Ascending ? 'asc' : 'desc',
        };
    }
}


/***/ }),

/***/ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts":
/*!******************************************************************************!*\
  !*** ./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts ***!
  \******************************************************************************/
/*! exports provided: OrderingDirection */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OrderingDirection", function() { return OrderingDirection; });
var OrderingDirection;
(function (OrderingDirection) {
    OrderingDirection[OrderingDirection["Ascending"] = 0] = "Ascending";
    OrderingDirection[OrderingDirection["Descending"] = 1] = "Descending";
})(OrderingDirection || (OrderingDirection = {}));


/***/ }),

/***/ "./src/app/shared/ui-api/notification.service.ts":
/*!*******************************************************!*\
  !*** ./src/app/shared/ui-api/notification.service.ts ***!
  \*******************************************************/
/*! exports provided: NotificationService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NotificationService", function() { return NotificationService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/material/snack-bar */ "./node_modules/@angular/material/esm2015/snack-bar.js");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");
/* harmony import */ var _yes_no_dialog_yes_no_dialog_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./yes-no-dialog/yes-no-dialog.component */ "./src/app/shared/ui-api/yes-no-dialog/yes-no-dialog.component.ts");





let NotificationService = class NotificationService {
    constructor(matSnackBar, matDialog) {
        this.matSnackBar = matSnackBar;
        this.matDialog = matDialog;
    }
    showMessage(message) {
        this.matSnackBar.open(message, 'Close', { duration: 2000 });
    }
    confirmDialog(yesNoData) {
        return this.matDialog.open(_yes_no_dialog_yes_no_dialog_component__WEBPACK_IMPORTED_MODULE_4__["YesNoDialogComponent"], {
            data: yesNoData,
        }).afterClosed();
    }
};
NotificationService.ctorParameters = () => [
    { type: _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_2__["MatSnackBar"] },
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_3__["MatDialog"] }
];
NotificationService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], NotificationService);



/***/ }),

/***/ "./src/app/shared/ui-api/ordering.service.ts":
/*!***************************************************!*\
  !*** ./src/app/shared/ui-api/ordering.service.ts ***!
  \***************************************************/
/*! exports provided: OrderingService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "OrderingService", function() { return OrderingService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _app_local_storage_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app-local-storage.service */ "./src/app/shared/ui-api/app-local-storage.service.ts");
/* harmony import */ var _helpers_ordering_helper__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./helpers/ordering-helper */ "./src/app/shared/ui-api/helpers/ordering-helper.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _route_helper__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./route-helper */ "./src/app/shared/ui-api/route-helper.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");








let OrderingService = class OrderingService {
    constructor(router, activatedRoute, appLocalStorage) {
        this.router = router;
        this.activatedRoute = activatedRoute;
        this.appLocalStorage = appLocalStorage;
        this.orderingBS = new rxjs__WEBPACK_IMPORTED_MODULE_5__["BehaviorSubject"](null);
        this.ordering$ = this.orderingBS.asObservable();
        router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_7__["filter"])((event) => {
            return event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_2__["NavigationEnd"];
        })).subscribe(() => {
            const snapshot = new _route_helper__WEBPACK_IMPORTED_MODULE_6__["RouteHelper"](activatedRoute).getFinalRoute().snapshot;
            if (snapshot && snapshot.queryParams) {
                const ordering = this.getOrderingConfig(snapshot.data, snapshot.queryParams);
                if (ordering) {
                    this.orderingBS.next(ordering);
                }
            }
        });
    }
    getOrderingConfig(data, queryParams) {
        if (!data.config) {
            return null;
        }
        const routeConfig = data.config;
        if (!routeConfig.ordering) {
            return null;
        }
        const ordering = Object.assign({}, routeConfig.ordering);
        if (queryParams.ordering) {
            const queryOrdering = _helpers_ordering_helper__WEBPACK_IMPORTED_MODULE_4__["OrderingHelper"].getOrderingOptionFieldAndDirection(queryParams.ordering);
            for (const orderOption of ordering.options) {
                if (orderOption.field === queryOrdering.field) {
                    ordering.default = orderOption;
                    ordering.default.direction = queryOrdering.direction;
                }
            }
        }
        else {
            const savedOrdering = this.appLocalStorage.getOrderingItem();
            if (savedOrdering) {
                ordering.default = this.appLocalStorage.getOrderingItem();
            }
        }
        return ordering;
    }
    orderBy(ordering) {
        if (ordering) {
            const orderingValue = _helpers_ordering_helper__WEBPACK_IMPORTED_MODULE_4__["OrderingHelper"].getOrderingValue(ordering);
            const queryParams = { ordering: undefined };
            Object.assign(queryParams, this.activatedRoute.snapshot.queryParams);
            const urlOrderingValue = queryParams.ordering;
            if (urlOrderingValue !== orderingValue) {
                queryParams.ordering = orderingValue ? orderingValue : undefined;
                this.appLocalStorage.setOrderingItem(ordering);
                this.router.navigate([], {
                    relativeTo: this.activatedRoute,
                    queryParams,
                }).then(() => { });
            }
        }
    }
    getQueryParams(routeUrl) {
        const ordering = this.appLocalStorage.getOrderingItem(routeUrl);
        if (ordering) {
            return {
                ordering: _helpers_ordering_helper__WEBPACK_IMPORTED_MODULE_4__["OrderingHelper"].getOrderingValue(ordering),
            };
        }
        return null;
    }
};
OrderingService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
    { type: _app_local_storage_service__WEBPACK_IMPORTED_MODULE_3__["AppLocalStorageService"] }
];
OrderingService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], OrderingService);



/***/ }),

/***/ "./src/app/shared/ui-api/route-helper.ts":
/*!***********************************************!*\
  !*** ./src/app/shared/ui-api/route-helper.ts ***!
  \***********************************************/
/*! exports provided: RouteHelper */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RouteHelper", function() { return RouteHelper; });
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");

class RouteHelper {
    constructor(route) {
        this.previousPath = null;
        this.previousQuery = null;
        this.route = route;
    }
    getFinalRoute() {
        let route = this.route;
        while (route.firstChild) {
            route = route.firstChild;
        }
        return route;
    }
    getRoutePath() {
        const route = this.getFinalRoute();
        const urlSegments = [];
        for (const routeSegment of route.pathFromRoot) {
            if (routeSegment.snapshot.url.length > 0) {
                urlSegments.push(routeSegment.snapshot.url[0].path);
            }
        }
        return urlSegments.join('/');
    }
    getRouteConfig() {
        const route = this.getFinalRoute();
        if (route.snapshot.data.config) {
            return route.snapshot.data.config;
        }
        return {};
    }
    getSearchConfig() {
        const routeConfig = this.getRouteConfig();
        if (routeConfig.search) {
            return routeConfig.search;
        }
        return { show: false, placeholder: undefined };
    }
    getUrlChanges(nextUrl) {
        const currentPath = this.getRoutePath();
        const parts = nextUrl.split('?');
        const nextPath = parts[0];
        const nextQuery = parts.length > 1 ? parts[1] : null;
        const changes = {
            path: this.previousPath !== nextPath,
            query: this.previousQuery !== nextQuery,
        };
        this.previousPath = nextPath;
        this.previousQuery = nextQuery;
        return changes;
    }
}
RouteHelper.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_0__["ActivatedRoute"] }
];


/***/ }),

/***/ "./src/app/shared/ui-api/search.service.ts":
/*!*************************************************!*\
  !*** ./src/app/shared/ui-api/search.service.ts ***!
  \*************************************************/
/*! exports provided: SearchService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SearchService", function() { return SearchService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");



let SearchService = class SearchService {
    constructor(router, route) {
        this.router = router;
        this.route = route;
    }
    search(searchText) {
        const queryParams = { search: undefined };
        Object.assign(queryParams, this.route.snapshot.queryParams);
        const urlSearchText = queryParams.search;
        if (urlSearchText !== searchText) {
            queryParams.search = searchText ? searchText : undefined;
            this.router.navigate([], {
                relativeTo: this.route,
                queryParams
            }).catch(() => {
                // TODO: handle navigation error
            });
        }
    }
};
SearchService.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] }
];
SearchService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], SearchService);



/***/ }),

/***/ "./src/app/shared/ui-api/ui-api.module.ts":
/*!************************************************!*\
  !*** ./src/app/shared/ui-api/ui-api.module.ts ***!
  \************************************************/
/*! exports provided: UiApiModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UiApiModule", function() { return UiApiModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _yes_no_dialog_yes_no_dialog_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./yes-no-dialog/yes-no-dialog.component */ "./src/app/shared/ui-api/yes-no-dialog/yes-no-dialog.component.ts");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");
/* harmony import */ var _angular_material_button__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/material/button */ "./node_modules/@angular/material/esm2015/button.js");
/* harmony import */ var _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/material/snack-bar */ "./node_modules/@angular/material/esm2015/snack-bar.js");







let UiApiModule = class UiApiModule {
};
UiApiModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [_yes_no_dialog_yes_no_dialog_component__WEBPACK_IMPORTED_MODULE_3__["YesNoDialogComponent"]],
        entryComponents: [_yes_no_dialog_yes_no_dialog_component__WEBPACK_IMPORTED_MODULE_3__["YesNoDialogComponent"]],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _angular_material_snack_bar__WEBPACK_IMPORTED_MODULE_6__["MatSnackBarModule"],
            _angular_material_dialog__WEBPACK_IMPORTED_MODULE_4__["MatDialogModule"],
            _angular_material_button__WEBPACK_IMPORTED_MODULE_5__["MatButtonModule"],
        ]
    })
], UiApiModule);



/***/ }),

/***/ "./src/app/shared/ui-api/yes-no-dialog/yes-no-dialog.component.scss":
/*!**************************************************************************!*\
  !*** ./src/app/shared/ui-api/yes-no-dialog/yes-no-dialog.component.scss ***!
  \**************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC91aS1hcGkveWVzLW5vLWRpYWxvZy95ZXMtbm8tZGlhbG9nLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/shared/ui-api/yes-no-dialog/yes-no-dialog.component.ts":
/*!************************************************************************!*\
  !*** ./src/app/shared/ui-api/yes-no-dialog/yes-no-dialog.component.ts ***!
  \************************************************************************/
/*! exports provided: YesNoDialogComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "YesNoDialogComponent", function() { return YesNoDialogComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/material/dialog */ "./node_modules/@angular/material/esm2015/dialog.js");



let YesNoDialogComponent = class YesNoDialogComponent {
    constructor(dialogRef, data) {
        this.dialogRef = dialogRef;
        this.data = data;
    }
    ngOnInit() {
    }
    close() {
        this.dialogRef.close('no');
    }
};
YesNoDialogComponent.ctorParameters = () => [
    { type: _angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MatDialogRef"] },
    { type: undefined, decorators: [{ type: _angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"], args: [_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"],] }] }
];
YesNoDialogComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-yes-no-dialog',
        template: __webpack_require__(/*! raw-loader!./yes-no-dialog.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui-api/yes-no-dialog/yes-no-dialog.component.html"),
        styles: [__webpack_require__(/*! ./yes-no-dialog.component.scss */ "./src/app/shared/ui-api/yes-no-dialog/yes-no-dialog.component.scss")]
    }),
    tslib__WEBPACK_IMPORTED_MODULE_0__["__param"](1, Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Inject"])(_angular_material_dialog__WEBPACK_IMPORTED_MODULE_2__["MAT_DIALOG_DATA"]))
], YesNoDialogComponent);



/***/ }),

/***/ "./src/app/shared/ui/common/icon/icon.component.scss":
/*!***********************************************************!*\
  !*** ./src/app/shared/ui/common/icon/icon.component.scss ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC91aS9jb21tb24vaWNvbi9pY29uLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/shared/ui/common/icon/icon.component.ts":
/*!*********************************************************!*\
  !*** ./src/app/shared/ui/common/icon/icon.component.ts ***!
  \*********************************************************/
/*! exports provided: IconComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "IconComponent", function() { return IconComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let IconComponent = class IconComponent {
    constructor() { }
    ngOnInit() {
    }
};
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], IconComponent.prototype, "icon", void 0);
IconComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-icon',
        template: __webpack_require__(/*! raw-loader!./icon.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/common/icon/icon.component.html"),
        styles: [__webpack_require__(/*! ./icon.component.scss */ "./src/app/shared/ui/common/icon/icon.component.scss")]
    })
], IconComponent);



/***/ }),

/***/ "./src/app/shared/ui/fl-backdrop/fl-backdrop.component.scss":
/*!******************************************************************!*\
  !*** ./src/app/shared/ui/fl-backdrop/fl-backdrop.component.scss ***!
  \******************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".fl-backdrop {\n  background-color: #fcfcfc;\n  opacity: 0.9;\n  width: 100%;\n  height: 100%;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  right: 0;\n  left: 0;\n  z-index: 3;\n}\n\n.fl-backdrop-progress {\n  position: absolute;\n  left: 45%;\n  margin-top: 16px;\n  top: 0;\n  bottom: 0;\n  z-index: 4;\n}\n\n.align-circle-middle.fl-backdrop-progress {\n  top: 37%;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC91aS9mbC1iYWNrZHJvcC9mbC1iYWNrZHJvcC5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvc2hhcmVkL3VpL2ZsLWJhY2tkcm9wL2ZsLWJhY2tkcm9wLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UseUJBQUE7RUFDQSxZQUFBO0VBQ0EsV0FBQTtFQUNBLFlBQUE7RUFDQSxrQkFBQTtFQUNBLE1BQUE7RUFDQSxTQUFBO0VBQ0EsUUFBQTtFQUNBLE9BQUE7RUFDQSxVQUFBO0FDQ0Y7O0FERUE7RUFDRSxrQkFBQTtFQUNBLFNBQUE7RUFDQSxnQkFBQTtFQUNBLE1BQUE7RUFDQSxTQUFBO0VBQ0EsVUFBQTtBQ0NGOztBREVBO0VBQ0UsUUFBQTtBQ0NGIiwiZmlsZSI6InNyYy9hcHAvc2hhcmVkL3VpL2ZsLWJhY2tkcm9wL2ZsLWJhY2tkcm9wLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLmZsLWJhY2tkcm9wIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogI2ZjZmNmYztcbiAgb3BhY2l0eTogMC45O1xuICB3aWR0aDogMTAwJTtcbiAgaGVpZ2h0OiAxMDAlO1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIHRvcDogMDtcbiAgYm90dG9tOiAwO1xuICByaWdodDogMDtcbiAgbGVmdDogMDtcbiAgei1pbmRleDogMztcbn1cblxuLmZsLWJhY2tkcm9wLXByb2dyZXNzIHtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICBsZWZ0OiA0NSU7XG4gIG1hcmdpbi10b3A6IDE2cHg7XG4gIHRvcDogMDtcbiAgYm90dG9tOiAwO1xuICB6LWluZGV4OiA0O1xufVxuXG4uYWxpZ24tY2lyY2xlLW1pZGRsZS5mbC1iYWNrZHJvcC1wcm9ncmVzcyB7XG4gIHRvcDogMzclO1xufVxuIiwiLmZsLWJhY2tkcm9wIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogI2ZjZmNmYztcbiAgb3BhY2l0eTogMC45O1xuICB3aWR0aDogMTAwJTtcbiAgaGVpZ2h0OiAxMDAlO1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIHRvcDogMDtcbiAgYm90dG9tOiAwO1xuICByaWdodDogMDtcbiAgbGVmdDogMDtcbiAgei1pbmRleDogMztcbn1cblxuLmZsLWJhY2tkcm9wLXByb2dyZXNzIHtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICBsZWZ0OiA0NSU7XG4gIG1hcmdpbi10b3A6IDE2cHg7XG4gIHRvcDogMDtcbiAgYm90dG9tOiAwO1xuICB6LWluZGV4OiA0O1xufVxuXG4uYWxpZ24tY2lyY2xlLW1pZGRsZS5mbC1iYWNrZHJvcC1wcm9ncmVzcyB7XG4gIHRvcDogMzclO1xufSJdfQ== */"

/***/ }),

/***/ "./src/app/shared/ui/fl-backdrop/fl-backdrop.component.ts":
/*!****************************************************************!*\
  !*** ./src/app/shared/ui/fl-backdrop/fl-backdrop.component.ts ***!
  \****************************************************************/
/*! exports provided: FlBackdropComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FlBackdropComponent", function() { return FlBackdropComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let FlBackdropComponent = class FlBackdropComponent {
    constructor() {
        this.spinnerDiameter = 70;
        this.verticalAlignMiddle = false;
    }
    ngOnInit() {
    }
};
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], FlBackdropComponent.prototype, "spinnerDiameter", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], FlBackdropComponent.prototype, "verticalAlignMiddle", void 0);
FlBackdropComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-fl-backdrop',
        template: __webpack_require__(/*! raw-loader!./fl-backdrop.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/fl-backdrop/fl-backdrop.component.html"),
        styles: [__webpack_require__(/*! ./fl-backdrop.component.scss */ "./src/app/shared/ui/fl-backdrop/fl-backdrop.component.scss")]
    })
], FlBackdropComponent);



/***/ }),

/***/ "./src/app/shared/ui/gravatar/gravatar.component.scss":
/*!************************************************************!*\
  !*** ./src/app/shared/ui/gravatar/gravatar.component.scss ***!
  \************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC91aS9ncmF2YXRhci9ncmF2YXRhci5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/shared/ui/gravatar/gravatar.component.ts":
/*!**********************************************************!*\
  !*** ./src/app/shared/ui/gravatar/gravatar.component.ts ***!
  \**********************************************************/
/*! exports provided: GravatarComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "GravatarComponent", function() { return GravatarComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ts-md5/dist/md5 */ "./node_modules/ts-md5/dist/md5.js");
/* harmony import */ var ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2__);



let GravatarComponent = class GravatarComponent {
    constructor() {
    }
    ngOnInit() {
        this.url = 'https://www.gravatar.com/avatar/';
        const md5 = new ts_md5_dist_md5__WEBPACK_IMPORTED_MODULE_2__["Md5"]();
        if (this.email) {
            this.url = this.url + md5.appendStr(this.email.trim().toLowerCase()).end() + '?default=identicon';
        }
    }
};
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], GravatarComponent.prototype, "email", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], GravatarComponent.prototype, "customStyle", void 0);
GravatarComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-gravatar',
        template: __webpack_require__(/*! raw-loader!./gravatar.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/gravatar/gravatar.component.html"),
        styles: [__webpack_require__(/*! ./gravatar.component.scss */ "./src/app/shared/ui/gravatar/gravatar.component.scss")]
    })
], GravatarComponent);



/***/ }),

/***/ "./src/app/shared/ui/logo/logo.component.scss":
/*!****************************************************!*\
  !*** ./src/app/shared/ui/logo/logo.component.scss ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "a {\n  vertical-align: sub;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC91aS9sb2dvL2xvZ28uY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3NoYXJlZC91aS9sb2dvL2xvZ28uY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxtQkFBQTtBQ0NGIiwiZmlsZSI6InNyYy9hcHAvc2hhcmVkL3VpL2xvZ28vbG9nby5jb21wb25lbnQuc2NzcyIsInNvdXJjZXNDb250ZW50IjpbImEge1xuICB2ZXJ0aWNhbC1hbGlnbjogc3ViO1xufVxuIiwiYSB7XG4gIHZlcnRpY2FsLWFsaWduOiBzdWI7XG59Il19 */"

/***/ }),

/***/ "./src/app/shared/ui/logo/logo.component.ts":
/*!**************************************************!*\
  !*** ./src/app/shared/ui/logo/logo.component.ts ***!
  \**************************************************/
/*! exports provided: LogoComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LogoComponent", function() { return LogoComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../config/config.service */ "./src/app/shared/config/config.service.ts");



let LogoComponent = class LogoComponent {
    constructor(config) {
        this.config = config;
        this.withLink = true;
    }
    ngOnInit() {
        if (this.dark) {
            this.logoPath = this.config.getImagePath('logo.svg');
        }
        else {
            this.logoPath = this.config.getImagePath('logo-dark.svg');
        }
    }
};
LogoComponent.ctorParameters = () => [
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], LogoComponent.prototype, "dark", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], LogoComponent.prototype, "withLink", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], LogoComponent.prototype, "customStyle", void 0);
LogoComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-logo',
        template: __webpack_require__(/*! raw-loader!./logo.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/logo/logo.component.html"),
        styles: [__webpack_require__(/*! ./logo.component.scss */ "./src/app/shared/ui/logo/logo.component.scss")]
    })
], LogoComponent);



/***/ }),

/***/ "./src/app/shared/ui/menu/menu-item-container/menu-item-container.component.scss":
/*!***************************************************************************************!*\
  !*** ./src/app/shared/ui/menu/menu-item-container/menu-item-container.component.scss ***!
  \***************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".menu-item-container {\n  position: relative;\n  margin: 0;\n  padding-left: 16px;\n  border-radius: 0;\n  width: 100%;\n  height: 48px;\n  font-weight: normal;\n  text-transform: none;\n  font-size: 15px;\n  color: rgba(0, 0, 0, 0.7);\n  line-height: 50px;\n  vertical-align: middle;\n  display: block;\n  z-index: 10;\n  text-align: left;\n  -webkit-transition: box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);\n  transition: box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);\n}\n\n.menu-item-container mat-icon {\n  position: absolute;\n  top: 12px;\n  right: 5px;\n  color: rgba(0, 0, 0, 0.54);\n  -webkit-user-select: none;\n  -moz-user-select: none;\n  -ms-user-select: none;\n  user-select: none;\n}\n\n.menu-item-container:hover {\n  background-color: rgba(0, 0, 0, 0.2);\n  -webkit-transition: box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);\n  transition: box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC91aS9tZW51L21lbnUtaXRlbS1jb250YWluZXIvbWVudS1pdGVtLWNvbnRhaW5lci5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvc2hhcmVkL3VpL21lbnUvbWVudS1pdGVtLWNvbnRhaW5lci9tZW51LWl0ZW0tY29udGFpbmVyLmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0Usa0JBQUE7RUFDQSxTQUFBO0VBQ0Esa0JBQUE7RUFDQSxnQkFBQTtFQUNBLFdBQUE7RUFDQSxZQUFBO0VBQ0EsbUJBQUE7RUFDQSxvQkFBQTtFQUNBLGVBQUE7RUFDQSx5QkFBQTtFQUNBLGlCQUFBO0VBQ0Esc0JBQUE7RUFDQSxjQUFBO0VBQ0EsV0FBQTtFQUNBLGdCQUFBO0VBQ0EsNEhBQUE7RUFBQSxvSEFBQTtBQ0NGOztBREVBO0VBQ0Usa0JBQUE7RUFDQSxTQUFBO0VBQ0EsVUFBQTtFQUNBLDBCQUFBO0VBQ0EseUJBQUE7RUFDQSxzQkFBQTtFQUNBLHFCQUFBO0VBQ0EsaUJBQUE7QUNDRjs7QURFQTtFQUNFLG9DQUFBO0VBQ0EsNEhBQUE7RUFBQSxvSEFBQTtBQ0NGIiwiZmlsZSI6InNyYy9hcHAvc2hhcmVkL3VpL21lbnUvbWVudS1pdGVtLWNvbnRhaW5lci9tZW51LWl0ZW0tY29udGFpbmVyLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLm1lbnUtaXRlbS1jb250YWluZXIge1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIG1hcmdpbjogMDtcbiAgcGFkZGluZy1sZWZ0OiAxNnB4O1xuICBib3JkZXItcmFkaXVzOiAwO1xuICB3aWR0aDogMTAwJTtcbiAgaGVpZ2h0OiA0OHB4O1xuICBmb250LXdlaWdodDogbm9ybWFsO1xuICB0ZXh0LXRyYW5zZm9ybTogbm9uZTtcbiAgZm9udC1zaXplOiAxNXB4O1xuICBjb2xvcjogcmdiYSgwLCAwLCAwLCAwLjcpO1xuICBsaW5lLWhlaWdodDogNTBweDtcbiAgdmVydGljYWwtYWxpZ246IG1pZGRsZTtcbiAgZGlzcGxheTogYmxvY2s7XG4gIHotaW5kZXg6IDEwO1xuICB0ZXh0LWFsaWduOiBsZWZ0O1xuICB0cmFuc2l0aW9uOiBib3gtc2hhZG93IDAuNHMgY3ViaWMtYmV6aWVyKDAuMjUsIDAuOCwgMC4yNSwgMSksIGJhY2tncm91bmQtY29sb3IgMC40cyBjdWJpYy1iZXppZXIoMC4yNSwgMC44LCAwLjI1LCAxKTtcbn1cblxuLm1lbnUtaXRlbS1jb250YWluZXIgbWF0LWljb24ge1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIHRvcDogMTJweDtcbiAgcmlnaHQ6IDVweDtcbiAgY29sb3I6IHJnYmEoMCwwLDAsMC41NCk7XG4gIC13ZWJraXQtdXNlci1zZWxlY3Q6IG5vbmU7XG4gIC1tb3otdXNlci1zZWxlY3Q6IG5vbmU7XG4gIC1tcy11c2VyLXNlbGVjdDogbm9uZTtcbiAgdXNlci1zZWxlY3Q6IG5vbmU7XG59XG5cbi5tZW51LWl0ZW0tY29udGFpbmVyOmhvdmVyIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogcmdiYSgwLDAsMCwwLjIpO1xuICB0cmFuc2l0aW9uOiBib3gtc2hhZG93IDAuNHMgY3ViaWMtYmV6aWVyKDAuMjUsIDAuOCwgMC4yNSwgMSksIGJhY2tncm91bmQtY29sb3IgMC40cyBjdWJpYy1iZXppZXIoMC4yNSwgMC44LCAwLjI1LCAxKTtcbn1cbiIsIi5tZW51LWl0ZW0tY29udGFpbmVyIHtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xuICBtYXJnaW46IDA7XG4gIHBhZGRpbmctbGVmdDogMTZweDtcbiAgYm9yZGVyLXJhZGl1czogMDtcbiAgd2lkdGg6IDEwMCU7XG4gIGhlaWdodDogNDhweDtcbiAgZm9udC13ZWlnaHQ6IG5vcm1hbDtcbiAgdGV4dC10cmFuc2Zvcm06IG5vbmU7XG4gIGZvbnQtc2l6ZTogMTVweDtcbiAgY29sb3I6IHJnYmEoMCwgMCwgMCwgMC43KTtcbiAgbGluZS1oZWlnaHQ6IDUwcHg7XG4gIHZlcnRpY2FsLWFsaWduOiBtaWRkbGU7XG4gIGRpc3BsYXk6IGJsb2NrO1xuICB6LWluZGV4OiAxMDtcbiAgdGV4dC1hbGlnbjogbGVmdDtcbiAgdHJhbnNpdGlvbjogYm94LXNoYWRvdyAwLjRzIGN1YmljLWJlemllcigwLjI1LCAwLjgsIDAuMjUsIDEpLCBiYWNrZ3JvdW5kLWNvbG9yIDAuNHMgY3ViaWMtYmV6aWVyKDAuMjUsIDAuOCwgMC4yNSwgMSk7XG59XG5cbi5tZW51LWl0ZW0tY29udGFpbmVyIG1hdC1pY29uIHtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICB0b3A6IDEycHg7XG4gIHJpZ2h0OiA1cHg7XG4gIGNvbG9yOiByZ2JhKDAsIDAsIDAsIDAuNTQpO1xuICAtd2Via2l0LXVzZXItc2VsZWN0OiBub25lO1xuICAtbW96LXVzZXItc2VsZWN0OiBub25lO1xuICAtbXMtdXNlci1zZWxlY3Q6IG5vbmU7XG4gIHVzZXItc2VsZWN0OiBub25lO1xufVxuXG4ubWVudS1pdGVtLWNvbnRhaW5lcjpob3ZlciB7XG4gIGJhY2tncm91bmQtY29sb3I6IHJnYmEoMCwgMCwgMCwgMC4yKTtcbiAgdHJhbnNpdGlvbjogYm94LXNoYWRvdyAwLjRzIGN1YmljLWJlemllcigwLjI1LCAwLjgsIDAuMjUsIDEpLCBiYWNrZ3JvdW5kLWNvbG9yIDAuNHMgY3ViaWMtYmV6aWVyKDAuMjUsIDAuOCwgMC4yNSwgMSk7XG59Il19 */"

/***/ }),

/***/ "./src/app/shared/ui/menu/menu-item-container/menu-item-container.component.ts":
/*!*************************************************************************************!*\
  !*** ./src/app/shared/ui/menu/menu-item-container/menu-item-container.component.ts ***!
  \*************************************************************************************/
/*! exports provided: MenuItemContainerComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MenuItemContainerComponent", function() { return MenuItemContainerComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _menu_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../menu.service */ "./src/app/shared/ui/menu/menu.service.ts");
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/animations */ "./node_modules/@angular/animations/fesm2015/animations.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ui_api_route_helper__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../ui-api/route-helper */ "./src/app/shared/ui-api/route-helper.ts");






let MenuItemContainerComponent = class MenuItemContainerComponent {
    constructor(menuService, activatedRoute) {
        this.menuService = menuService;
        this.activatedRoute = activatedRoute;
        this.expanded = false;
    }
    toggle() {
        if (this.menuService.expandedMenuItemContainer === this.menuItemContainer.display) {
            return this.menuService.expandedMenuItemContainer = null;
        }
        this.expand();
    }
    expand() {
        this.menuService.expandedMenuItemContainer = this.menuItemContainer.display;
    }
    getExpanded() {
        return this.menuService.expandedMenuItemContainer === this.menuItemContainer.display;
    }
    ngOnInit() {
        const routePath = '/' + new _ui_api_route_helper__WEBPACK_IMPORTED_MODULE_5__["RouteHelper"](this.activatedRoute).getRoutePath();
        for (const menuItem of this.menuItemContainer.items) {
            if (menuItem.route === routePath) {
                this.expand();
            }
        }
    }
};
MenuItemContainerComponent.ctorParameters = () => [
    { type: _menu_service__WEBPACK_IMPORTED_MODULE_2__["MenuService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], MenuItemContainerComponent.prototype, "menuItemContainer", void 0);
MenuItemContainerComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-menu-item-container',
        template: __webpack_require__(/*! raw-loader!./menu-item-container.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/menu/menu-item-container/menu-item-container.component.html"),
        animations: [
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["trigger"])('openCloseDropdown', [
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["state"])('open', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["style"])({
                    transform: 'rotate(90deg)',
                })),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["transition"])('open => closed', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["animate"])('0.2s ease-in-out')
                ]),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["transition"])('closed => open', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["animate"])('0.2s ease-in-out')
                ]),
            ]),
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["trigger"])('openCloseItems', [
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["state"])('closed', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["style"])({
                    height: '0',
                })),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["state"])('open', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["style"])({
                    height: '*',
                })),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["transition"])('open => closed', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["animate"])('230ms')
                ]),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["transition"])('closed => open', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["animate"])('230ms')
                ]),
            ]),
        ],
        styles: [__webpack_require__(/*! ./menu-item-container.component.scss */ "./src/app/shared/ui/menu/menu-item-container/menu-item-container.component.scss")]
    })
], MenuItemContainerComponent);



/***/ }),

/***/ "./src/app/shared/ui/menu/menu-item/menu-item.component.scss":
/*!*******************************************************************!*\
  !*** ./src/app/shared/ui/menu/menu-item/menu-item.component.scss ***!
  \*******************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".menu-link {\n  margin: 0;\n  padding-left: 16px;\n  border-radius: 0;\n  width: 100%;\n  height: 48px;\n  font-weight: normal;\n  text-transform: none;\n  font-size: 15px;\n  color: rgba(0, 0, 0, 0.7);\n  line-height: 50px;\n  vertical-align: middle;\n  display: block;\n  text-align: left;\n  -webkit-transition: box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);\n  transition: box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);\n}\n\n.menu-link mat-icon {\n  vertical-align: middle;\n  margin-right: 18px;\n  color: rgba(0, 0, 0, 0.54);\n  margin-bottom: 3px;\n  -webkit-user-select: none;\n  -moz-user-select: none;\n  -ms-user-select: none;\n  user-select: none;\n}\n\n.menu-link:hover {\n  background-color: rgba(0, 0, 0, 0.2);\n  -webkit-transition: box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);\n  transition: box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), background-color 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC91aS9tZW51L21lbnUtaXRlbS9tZW51LWl0ZW0uY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3NoYXJlZC91aS9tZW51L21lbnUtaXRlbS9tZW51LWl0ZW0uY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxTQUFBO0VBQ0Esa0JBQUE7RUFDQSxnQkFBQTtFQUNBLFdBQUE7RUFDQSxZQUFBO0VBQ0EsbUJBQUE7RUFDQSxvQkFBQTtFQUNBLGVBQUE7RUFDQSx5QkFBQTtFQUNBLGlCQUFBO0VBQ0Esc0JBQUE7RUFDQSxjQUFBO0VBQ0EsZ0JBQUE7RUFDQSw0SEFBQTtFQUFBLG9IQUFBO0FDQ0Y7O0FERUE7RUFDRSxzQkFBQTtFQUNBLGtCQUFBO0VBQ0EsMEJBQUE7RUFDQSxrQkFBQTtFQUNBLHlCQUFBO0VBQ0Esc0JBQUE7RUFDQSxxQkFBQTtFQUNBLGlCQUFBO0FDQ0Y7O0FERUE7RUFDRSxvQ0FBQTtFQUNBLDRIQUFBO0VBQUEsb0hBQUE7QUNDRiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC91aS9tZW51L21lbnUtaXRlbS9tZW51LWl0ZW0uY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIubWVudS1saW5rIHtcbiAgbWFyZ2luOiAwO1xuICBwYWRkaW5nLWxlZnQ6IDE2cHg7XG4gIGJvcmRlci1yYWRpdXM6IDA7XG4gIHdpZHRoOiAxMDAlO1xuICBoZWlnaHQ6IDQ4cHg7XG4gIGZvbnQtd2VpZ2h0OiBub3JtYWw7XG4gIHRleHQtdHJhbnNmb3JtOiBub25lO1xuICBmb250LXNpemU6IDE1cHg7XG4gIGNvbG9yOiByZ2JhKDAsIDAsIDAsIDAuNyk7XG4gIGxpbmUtaGVpZ2h0OiA1MHB4O1xuICB2ZXJ0aWNhbC1hbGlnbjogbWlkZGxlO1xuICBkaXNwbGF5OiBibG9jaztcbiAgdGV4dC1hbGlnbjogbGVmdDtcbiAgdHJhbnNpdGlvbjogYm94LXNoYWRvdyAwLjRzIGN1YmljLWJlemllcigwLjI1LCAwLjgsIDAuMjUsIDEpLCBiYWNrZ3JvdW5kLWNvbG9yIDAuNHMgY3ViaWMtYmV6aWVyKDAuMjUsIDAuOCwgMC4yNSwgMSk7XG59XG5cbi5tZW51LWxpbmsgbWF0LWljb24ge1xuICB2ZXJ0aWNhbC1hbGlnbjogbWlkZGxlO1xuICBtYXJnaW4tcmlnaHQ6IDE4cHg7XG4gIGNvbG9yOiByZ2JhKDAsMCwwLDAuNTQpO1xuICBtYXJnaW4tYm90dG9tOiAzcHg7XG4gIC13ZWJraXQtdXNlci1zZWxlY3Q6IG5vbmU7XG4gIC1tb3otdXNlci1zZWxlY3Q6IG5vbmU7XG4gIC1tcy11c2VyLXNlbGVjdDogbm9uZTtcbiAgdXNlci1zZWxlY3Q6IG5vbmU7XG59XG5cbi5tZW51LWxpbms6aG92ZXIge1xuICBiYWNrZ3JvdW5kLWNvbG9yOiByZ2JhKDAsMCwwLDAuMik7XG4gIHRyYW5zaXRpb246IGJveC1zaGFkb3cgMC40cyBjdWJpYy1iZXppZXIoMC4yNSwgMC44LCAwLjI1LCAxKSwgYmFja2dyb3VuZC1jb2xvciAwLjRzIGN1YmljLWJlemllcigwLjI1LCAwLjgsIDAuMjUsIDEpO1xufVxuIiwiLm1lbnUtbGluayB7XG4gIG1hcmdpbjogMDtcbiAgcGFkZGluZy1sZWZ0OiAxNnB4O1xuICBib3JkZXItcmFkaXVzOiAwO1xuICB3aWR0aDogMTAwJTtcbiAgaGVpZ2h0OiA0OHB4O1xuICBmb250LXdlaWdodDogbm9ybWFsO1xuICB0ZXh0LXRyYW5zZm9ybTogbm9uZTtcbiAgZm9udC1zaXplOiAxNXB4O1xuICBjb2xvcjogcmdiYSgwLCAwLCAwLCAwLjcpO1xuICBsaW5lLWhlaWdodDogNTBweDtcbiAgdmVydGljYWwtYWxpZ246IG1pZGRsZTtcbiAgZGlzcGxheTogYmxvY2s7XG4gIHRleHQtYWxpZ246IGxlZnQ7XG4gIHRyYW5zaXRpb246IGJveC1zaGFkb3cgMC40cyBjdWJpYy1iZXppZXIoMC4yNSwgMC44LCAwLjI1LCAxKSwgYmFja2dyb3VuZC1jb2xvciAwLjRzIGN1YmljLWJlemllcigwLjI1LCAwLjgsIDAuMjUsIDEpO1xufVxuXG4ubWVudS1saW5rIG1hdC1pY29uIHtcbiAgdmVydGljYWwtYWxpZ246IG1pZGRsZTtcbiAgbWFyZ2luLXJpZ2h0OiAxOHB4O1xuICBjb2xvcjogcmdiYSgwLCAwLCAwLCAwLjU0KTtcbiAgbWFyZ2luLWJvdHRvbTogM3B4O1xuICAtd2Via2l0LXVzZXItc2VsZWN0OiBub25lO1xuICAtbW96LXVzZXItc2VsZWN0OiBub25lO1xuICAtbXMtdXNlci1zZWxlY3Q6IG5vbmU7XG4gIHVzZXItc2VsZWN0OiBub25lO1xufVxuXG4ubWVudS1saW5rOmhvdmVyIHtcbiAgYmFja2dyb3VuZC1jb2xvcjogcmdiYSgwLCAwLCAwLCAwLjIpO1xuICB0cmFuc2l0aW9uOiBib3gtc2hhZG93IDAuNHMgY3ViaWMtYmV6aWVyKDAuMjUsIDAuOCwgMC4yNSwgMSksIGJhY2tncm91bmQtY29sb3IgMC40cyBjdWJpYy1iZXppZXIoMC4yNSwgMC44LCAwLjI1LCAxKTtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/shared/ui/menu/menu-item/menu-item.component.ts":
/*!*****************************************************************!*\
  !*** ./src/app/shared/ui/menu/menu-item/menu-item.component.ts ***!
  \*****************************************************************/
/*! exports provided: MenuItemComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MenuItemComponent", function() { return MenuItemComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let MenuItemComponent = class MenuItemComponent {
    constructor() {
        this.isAlone = true;
        this.activeOptions = {};
    }
    ngOnInit() {
        if (this.isAlone) {
            this.activeOptions = { exact: true };
        }
    }
};
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], MenuItemComponent.prototype, "menuItem", void 0);
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], MenuItemComponent.prototype, "isAlone", void 0);
MenuItemComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-menu-item',
        template: __webpack_require__(/*! raw-loader!./menu-item.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/menu/menu-item/menu-item.component.html"),
        styles: [__webpack_require__(/*! ./menu-item.component.scss */ "./src/app/shared/ui/menu/menu-item/menu-item.component.scss")]
    })
], MenuItemComponent);



/***/ }),

/***/ "./src/app/shared/ui/menu/menu.service.ts":
/*!************************************************!*\
  !*** ./src/app/shared/ui/menu/menu.service.ts ***!
  \************************************************/
/*! exports provided: MenuService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MenuService", function() { return MenuService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let MenuService = class MenuService {
    constructor() {
        this.expandedMenuItemContainer = null;
    }
};
MenuService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], MenuService);



/***/ }),

/***/ "./src/app/shared/ui/menu/side-nav-menu/side-nav-menu.component.scss":
/*!***************************************************************************!*\
  !*** ./src/app/shared/ui/menu/side-nav-menu/side-nav-menu.component.scss ***!
  \***************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC91aS9tZW51L3NpZGUtbmF2LW1lbnUvc2lkZS1uYXYtbWVudS5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/shared/ui/menu/side-nav-menu/side-nav-menu.component.ts":
/*!*************************************************************************!*\
  !*** ./src/app/shared/ui/menu/side-nav-menu/side-nav-menu.component.ts ***!
  \*************************************************************************/
/*! exports provided: SideNavMenuComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SideNavMenuComponent", function() { return SideNavMenuComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _auth_auth_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../auth/auth.service */ "./src/app/shared/auth/auth.service.ts");
/* harmony import */ var _ui_api_ordering_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../ui-api/ordering.service */ "./src/app/shared/ui-api/ordering.service.ts");





let SideNavMenuComponent = class SideNavMenuComponent {
    constructor(config, authService, orderingService) {
        this.config = config;
        this.authService = authService;
        this.orderingService = orderingService;
    }
    canAddMenuItem(feature) {
        return !!(this.authService.userData && this.authService.userData.features[feature]);
    }
    canShowMenuItemContainer(menuItemContainer) {
        let itemsNotShownCount = 0;
        for (const item of menuItemContainer.items) {
            if (typeof item === 'boolean' && item === false) {
                itemsNotShownCount += 1;
            }
        }
        return menuItemContainer.items.length !== itemsNotShownCount;
    }
    ngOnInit() {
        this.orderingService.ordering$.subscribe(() => {
            this.refreshMenu();
        });
    }
    refreshMenu() {
        // TODO: load this from backend
        this.menu = {
            items: [
                {
                    type: 'menuItem',
                    route: this.config.getPanelHomeUrl(),
                    routeDisplay: 'Dashboard',
                    icon: 'dashboard',
                    iconClass: 'fl-icons'
                },
                {
                    type: 'menuItemContainer',
                    display: 'Clients & users',
                    items: [
                        (this.canAddMenuItem('clients&users.users') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('clients-users/users'),
                            queryParams: this.orderingService.getQueryParams('clients-users/users'),
                            routeDisplay: 'Users',
                            icon: 'users',
                            iconClass: 'fl-icons'
                        }),
                        (this.canAddMenuItem('clients&users.clients') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('clients-users/clients'),
                            queryParams: this.orderingService.getQueryParams('clients-users/clients'),
                            routeDisplay: 'Clients',
                            icon: 'clients',
                            iconClass: 'fl-icons'
                        }),
                    ]
                },
                {
                    type: 'menuItemContainer',
                    display: 'Cloud',
                    items: [
                        (this.canAddMenuItem('openstack.instances') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('cloud/instances'),
                            queryParams: this.orderingService.getQueryParams('cloud/instances'),
                            routeDisplay: 'Instances',
                            icon: 'instances',
                            iconClass: 'fl-icons'
                        }),
                        (this.canAddMenuItem('openstack.flavors') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('cloud/flavors'),
                            queryParams: this.orderingService.getQueryParams('cloud/flavors'),
                            routeDisplay: 'Flavors',
                            icon: 'flavors',
                            iconClass: 'fl-icons'
                        }),
                        (this.canAddMenuItem('openstack.sshkeys') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('cloud/ssh-keys'),
                            queryParams: this.orderingService.getQueryParams('cloud/ssh-keys'),
                            routeDisplay: 'SSH keys',
                            icon: 'keys',
                            iconClass: 'fl-icons'
                        }),
                        (this.canAddMenuItem('openstack.volumes') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('cloud/volumes'),
                            queryParams: this.orderingService.getQueryParams('cloud/volumes'),
                            routeDisplay: 'Volumes',
                            icon: 'volumes',
                            iconClass: 'fl-icons'
                        }),
                        (this.canAddMenuItem('openstack.images') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('cloud/images'),
                            queryParams: this.orderingService.getQueryParams('cloud/images'),
                            routeDisplay: 'Images',
                            icon: 'images',
                            iconClass: 'fl-icons'
                        }),
                        (this.canAddMenuItem('openstack.apiusers') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('cloud/api-users'),
                            queryParams: this.orderingService.getQueryParams('cloud/api-users'),
                            routeDisplay: 'API Users',
                            icon: 'group',
                            iconClass: 'fl-icons'
                        })
                    ]
                },
                {
                    type: 'menuItemContainer',
                    display: 'Billing',
                    items: [
                        (this.canAddMenuItem('billing.invoices') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('billing/invoices'),
                            queryParams: this.orderingService.getQueryParams('billing/invoices'),
                            routeDisplay: 'Invoices',
                            icon: 'invoice_item',
                            iconClass: 'fl-icons'
                        }),
                        (this.canAddMenuItem('billing.services') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('billing/services'),
                            queryParams: this.orderingService.getQueryParams('billing/services'),
                            routeDisplay: 'Services',
                            icon: 'services',
                            iconClass: 'fl-icons'
                        }),
                        (this.canAddMenuItem('billing.history') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('billing/history'),
                            queryParams: this.orderingService.getQueryParams('billing/history'),
                            routeDisplay: 'Billing history',
                            icon: 'tax_rules',
                            iconClass: 'fl-icons'
                        })
                    ],
                },
                {
                    type: 'menuItemContainer',
                    display: 'Settings',
                    items: [
                        (this.canAddMenuItem('openstack.plans') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('settings/openstack-plans'),
                            queryParams: this.orderingService.getQueryParams('settings/openstack-plans'),
                            routeDisplay: 'OpenStack plans',
                            icon: 'openstack',
                            iconClass: 'fl-icons'
                        }),
                        (this.canAddMenuItem('settings.configurations') && {
                            type: 'menuItem',
                            route: this.config.getPanelUrl('settings/configurations'),
                            queryParams: this.orderingService.getQueryParams('settings/configurations'),
                            routeDisplay: 'Configurations',
                            icon: 'tiled_grid',
                            iconClass: 'fl-icons'
                        }),
                    ]
                }
            ]
        };
    }
};
SideNavMenuComponent.ctorParameters = () => [
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] },
    { type: _auth_auth_service__WEBPACK_IMPORTED_MODULE_3__["AuthService"] },
    { type: _ui_api_ordering_service__WEBPACK_IMPORTED_MODULE_4__["OrderingService"] }
];
SideNavMenuComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-side-nav-menu',
        template: __webpack_require__(/*! raw-loader!./side-nav-menu.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/menu/side-nav-menu/side-nav-menu.component.html"),
        styles: [__webpack_require__(/*! ./side-nav-menu.component.scss */ "./src/app/shared/ui/menu/side-nav-menu/side-nav-menu.component.scss")]
    })
], SideNavMenuComponent);



/***/ }),

/***/ "./src/app/shared/ui/panel-layout/panel-layout.component.scss":
/*!********************************************************************!*\
  !*** ./src/app/shared/ui/panel-layout/panel-layout.component.scss ***!
  \********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".app-container {\n  position: absolute;\n  width: 100%;\n}\n\n.topbar-container {\n  width: 100%;\n  height: 64px;\n  z-index: 30;\n  position: fixed;\n  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.2), 0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 2px 1px -1px rgba(0, 0, 0, 0.12);\n}\n\n.content-container {\n  width: 100%;\n  top: 64px;\n  padding-left: 237px;\n  position: relative;\n  transition: 430ms ease-in-out;\n  -webkit-transition: 430ms ease-in-out;\n}\n\n.content-container-full {\n  padding-left: 0;\n  transition: 430ms ease-in-out;\n  -webkit-transition: 430ms ease-in-out;\n}\n\n.sidenav-container {\n  display: -webkit-box;\n  display: flex;\n  -webkit-box-orient: vertical;\n  -webkit-box-direction: normal;\n          flex-direction: column;\n  width: 237px;\n  height: calc(100% - 64px);\n  position: fixed;\n  left: 0;\n  z-index: 10;\n  overflow-y: auto;\n}\n\n.sidenav-container::-webkit-scrollbar {\n  height: 8px;\n  width: 8px;\n}\n\n.sidenav-container::-webkit-scrollbar-thumb {\n  background: rgba(0, 0, 0, 0.26);\n}\n\n.powered-text {\n  position: relative;\n  display: -webkit-box;\n  display: flex;\n  -webkit-box-align: end;\n          align-items: flex-end;\n  -webkit-box-flex: 1;\n          flex-grow: 1;\n  bottom: 0;\n  left: 0;\n  color: #9A9A9A;\n  font-size: 14px;\n  background: #f1f1f1;\n  z-index: 25;\n  padding: 10px 0 12px 15px;\n}\n\n.main-content-container {\n  width: 100%;\n  height: 100%;\n  padding-top: 48px;\n  margin: 0 auto;\n  max-width: 1380px;\n}\n\n.switch-sidebar-button {\n  background: none;\n  border: 0;\n  outline: none;\n  margin-right: 10px;\n}\n\n.loader {\n  position: absolute;\n  top: 0;\n  left: 0;\n  height: 2px;\n}\n\n.main-content-container-overlay:hover {\n  cursor: pointer;\n}\n\n@media screen and (max-width: 1280px) {\n  .content-container {\n    padding-left: 0 !important;\n  }\n\n  .main-content-container-overlay {\n    display: block;\n    height: 100%;\n    position: fixed;\n    top: 0;\n    left: 0;\n    z-index: 5;\n    width: 100%;\n    background-color: rgba(0, 0, 0, 0.5);\n  }\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC91aS9wYW5lbC1sYXlvdXQvcGFuZWwtbGF5b3V0LmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9zaGFyZWQvdWkvcGFuZWwtbGF5b3V0L3BhbmVsLWxheW91dC5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGtCQUFBO0VBQ0EsV0FBQTtBQ0NGOztBREVBO0VBQ0UsV0FBQTtFQUNBLFlBQUE7RUFDQSxXQUFBO0VBQ0EsZUFBQTtFQUNBLCtHQUFBO0FDQ0Y7O0FERUE7RUFDRSxXQUFBO0VBQ0EsU0FBQTtFQUNBLG1CQUFBO0VBQ0Esa0JBQUE7RUFDQSw2QkFBQTtFQUNBLHFDQUFBO0FDQ0Y7O0FERUE7RUFDRSxlQUFBO0VBQ0EsNkJBQUE7RUFDQSxxQ0FBQTtBQ0NGOztBREVBO0VBQ0Usb0JBQUE7RUFBQSxhQUFBO0VBQ0EsNEJBQUE7RUFBQSw2QkFBQTtVQUFBLHNCQUFBO0VBQ0EsWUFBQTtFQUNBLHlCQUFBO0VBQ0EsZUFBQTtFQUNBLE9BQUE7RUFDQSxXQUFBO0VBQ0EsZ0JBQUE7QUNDRjs7QURFQTtFQUNFLFdBQUE7RUFDQSxVQUFBO0FDQ0Y7O0FERUE7RUFDRSwrQkFBQTtBQ0NGOztBREVBO0VBQ0Usa0JBQUE7RUFDQSxvQkFBQTtFQUFBLGFBQUE7RUFDQSxzQkFBQTtVQUFBLHFCQUFBO0VBQ0EsbUJBQUE7VUFBQSxZQUFBO0VBQ0EsU0FBQTtFQUNBLE9BQUE7RUFDQSxjQUFBO0VBQ0EsZUFBQTtFQUNBLG1CQUFBO0VBQ0EsV0FBQTtFQUNBLHlCQUFBO0FDQ0Y7O0FERUE7RUFDRSxXQUFBO0VBQ0EsWUFBQTtFQUNBLGlCQUFBO0VBQ0EsY0FBQTtFQUNBLGlCQUFBO0FDQ0Y7O0FERUE7RUFDRSxnQkFBQTtFQUNBLFNBQUE7RUFDQSxhQUFBO0VBQ0Esa0JBQUE7QUNDRjs7QURFQTtFQUNFLGtCQUFBO0VBQ0EsTUFBQTtFQUNBLE9BQUE7RUFDQSxXQUFBO0FDQ0Y7O0FERUE7RUFDRSxlQUFBO0FDQ0Y7O0FERUE7RUFDRTtJQUNFLDBCQUFBO0VDQ0Y7O0VEQ0E7SUFDRSxjQUFBO0lBQ0EsWUFBQTtJQUNBLGVBQUE7SUFDQSxNQUFBO0lBQ0EsT0FBQTtJQUNBLFVBQUE7SUFDQSxXQUFBO0lBQ0Esb0NBQUE7RUNFRjtBQUNGIiwiZmlsZSI6InNyYy9hcHAvc2hhcmVkL3VpL3BhbmVsLWxheW91dC9wYW5lbC1sYXlvdXQuY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIuYXBwLWNvbnRhaW5lciB7XG4gIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgd2lkdGg6IDEwMCU7XG59XG5cbi50b3BiYXItY29udGFpbmVyIHtcbiAgd2lkdGg6IDEwMCU7XG4gIGhlaWdodDogNjRweDtcbiAgei1pbmRleDogMzA7XG4gIHBvc2l0aW9uOiBmaXhlZDtcbiAgYm94LXNoYWRvdzogMCAxcHggM3B4IDAgcmdiYSgwLDAsMCwuMiksIDAgMXB4IDFweCAwIHJnYmEoMCwwLDAsLjE0KSwgMCAycHggMXB4IC0xcHggcmdiYSgwLDAsMCwuMTIpO1xufVxuXG4uY29udGVudC1jb250YWluZXIge1xuICB3aWR0aDogMTAwJTtcbiAgdG9wOiA2NHB4O1xuICBwYWRkaW5nLWxlZnQ6IDIzN3B4O1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIHRyYW5zaXRpb246IDQzMG1zIGVhc2UtaW4tb3V0O1xuICAtd2Via2l0LXRyYW5zaXRpb246IDQzMG1zIGVhc2UtaW4tb3V0O1xufVxuXG4uY29udGVudC1jb250YWluZXItZnVsbCB7XG4gIHBhZGRpbmctbGVmdDogMDtcbiAgdHJhbnNpdGlvbjogNDMwbXMgZWFzZS1pbi1vdXQ7XG4gIC13ZWJraXQtdHJhbnNpdGlvbjogNDMwbXMgZWFzZS1pbi1vdXQ7XG59XG5cbi5zaWRlbmF2LWNvbnRhaW5lciB7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XG4gIHdpZHRoOiAyMzdweDtcbiAgaGVpZ2h0OiBjYWxjKDEwMCUgLSA2NHB4KTtcbiAgcG9zaXRpb246IGZpeGVkO1xuICBsZWZ0OiAwO1xuICB6LWluZGV4OiAxMDtcbiAgb3ZlcmZsb3cteTogYXV0bztcbn1cblxuLnNpZGVuYXYtY29udGFpbmVyOjotd2Via2l0LXNjcm9sbGJhciB7XG4gIGhlaWdodDogOHB4O1xuICB3aWR0aDogOHB4O1xufVxuXG4uc2lkZW5hdi1jb250YWluZXI6Oi13ZWJraXQtc2Nyb2xsYmFyLXRodW1iIHtcbiAgYmFja2dyb3VuZDogcmdiYSgwLDAsMCwuMjYpO1xufVxuXG4ucG93ZXJlZC10ZXh0IHtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xuICBkaXNwbGF5OiBmbGV4O1xuICBhbGlnbi1pdGVtczogZmxleC1lbmQ7XG4gIGZsZXgtZ3JvdzogMTtcbiAgYm90dG9tOiAwO1xuICBsZWZ0OiAwO1xuICBjb2xvcjogIzlBOUE5QTtcbiAgZm9udC1zaXplOiAxNHB4O1xuICBiYWNrZ3JvdW5kOiAjZjFmMWYxO1xuICB6LWluZGV4OiAyNTtcbiAgcGFkZGluZzogMTBweCAwIDEycHggMTVweDtcbn1cblxuLm1haW4tY29udGVudC1jb250YWluZXIge1xuICB3aWR0aDogMTAwJTtcbiAgaGVpZ2h0OiAxMDAlO1xuICBwYWRkaW5nLXRvcDogNDhweDtcbiAgbWFyZ2luOiAwIGF1dG87XG4gIG1heC13aWR0aDogMTM4MHB4O1xufVxuXG4uc3dpdGNoLXNpZGViYXItYnV0dG9uIHtcbiAgYmFja2dyb3VuZDogbm9uZTtcbiAgYm9yZGVyOiAwO1xuICBvdXRsaW5lOiBub25lO1xuICBtYXJnaW4tcmlnaHQ6IDEwcHg7XG59XG5cbi5sb2FkZXIge1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIHRvcDogMDtcbiAgbGVmdDogMDtcbiAgaGVpZ2h0OiAycHg7XG59XG5cbi5tYWluLWNvbnRlbnQtY29udGFpbmVyLW92ZXJsYXk6aG92ZXIge1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbkBtZWRpYSBzY3JlZW4gYW5kIChtYXgtd2lkdGg6IDEyODBweCkge1xuICAuY29udGVudC1jb250YWluZXIge1xuICAgIHBhZGRpbmctbGVmdDogMCAhaW1wb3J0YW50O1xuICB9XG4gIC5tYWluLWNvbnRlbnQtY29udGFpbmVyLW92ZXJsYXkge1xuICAgIGRpc3BsYXk6IGJsb2NrO1xuICAgIGhlaWdodDogMTAwJTtcbiAgICBwb3NpdGlvbjogZml4ZWQ7XG4gICAgdG9wOiAwO1xuICAgIGxlZnQ6IDA7XG4gICAgei1pbmRleDogNTtcbiAgICB3aWR0aDogMTAwJTtcbiAgICBiYWNrZ3JvdW5kLWNvbG9yOiByZ2JhKDAsMCwwLC41KTtcbiAgfVxufVxuIiwiLmFwcC1jb250YWluZXIge1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIHdpZHRoOiAxMDAlO1xufVxuXG4udG9wYmFyLWNvbnRhaW5lciB7XG4gIHdpZHRoOiAxMDAlO1xuICBoZWlnaHQ6IDY0cHg7XG4gIHotaW5kZXg6IDMwO1xuICBwb3NpdGlvbjogZml4ZWQ7XG4gIGJveC1zaGFkb3c6IDAgMXB4IDNweCAwIHJnYmEoMCwgMCwgMCwgMC4yKSwgMCAxcHggMXB4IDAgcmdiYSgwLCAwLCAwLCAwLjE0KSwgMCAycHggMXB4IC0xcHggcmdiYSgwLCAwLCAwLCAwLjEyKTtcbn1cblxuLmNvbnRlbnQtY29udGFpbmVyIHtcbiAgd2lkdGg6IDEwMCU7XG4gIHRvcDogNjRweDtcbiAgcGFkZGluZy1sZWZ0OiAyMzdweDtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xuICB0cmFuc2l0aW9uOiA0MzBtcyBlYXNlLWluLW91dDtcbiAgLXdlYmtpdC10cmFuc2l0aW9uOiA0MzBtcyBlYXNlLWluLW91dDtcbn1cblxuLmNvbnRlbnQtY29udGFpbmVyLWZ1bGwge1xuICBwYWRkaW5nLWxlZnQ6IDA7XG4gIHRyYW5zaXRpb246IDQzMG1zIGVhc2UtaW4tb3V0O1xuICAtd2Via2l0LXRyYW5zaXRpb246IDQzMG1zIGVhc2UtaW4tb3V0O1xufVxuXG4uc2lkZW5hdi1jb250YWluZXIge1xuICBkaXNwbGF5OiBmbGV4O1xuICBmbGV4LWRpcmVjdGlvbjogY29sdW1uO1xuICB3aWR0aDogMjM3cHg7XG4gIGhlaWdodDogY2FsYygxMDAlIC0gNjRweCk7XG4gIHBvc2l0aW9uOiBmaXhlZDtcbiAgbGVmdDogMDtcbiAgei1pbmRleDogMTA7XG4gIG92ZXJmbG93LXk6IGF1dG87XG59XG5cbi5zaWRlbmF2LWNvbnRhaW5lcjo6LXdlYmtpdC1zY3JvbGxiYXIge1xuICBoZWlnaHQ6IDhweDtcbiAgd2lkdGg6IDhweDtcbn1cblxuLnNpZGVuYXYtY29udGFpbmVyOjotd2Via2l0LXNjcm9sbGJhci10aHVtYiB7XG4gIGJhY2tncm91bmQ6IHJnYmEoMCwgMCwgMCwgMC4yNik7XG59XG5cbi5wb3dlcmVkLXRleHQge1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBmbGV4LWVuZDtcbiAgZmxleC1ncm93OiAxO1xuICBib3R0b206IDA7XG4gIGxlZnQ6IDA7XG4gIGNvbG9yOiAjOUE5QTlBO1xuICBmb250LXNpemU6IDE0cHg7XG4gIGJhY2tncm91bmQ6ICNmMWYxZjE7XG4gIHotaW5kZXg6IDI1O1xuICBwYWRkaW5nOiAxMHB4IDAgMTJweCAxNXB4O1xufVxuXG4ubWFpbi1jb250ZW50LWNvbnRhaW5lciB7XG4gIHdpZHRoOiAxMDAlO1xuICBoZWlnaHQ6IDEwMCU7XG4gIHBhZGRpbmctdG9wOiA0OHB4O1xuICBtYXJnaW46IDAgYXV0bztcbiAgbWF4LXdpZHRoOiAxMzgwcHg7XG59XG5cbi5zd2l0Y2gtc2lkZWJhci1idXR0b24ge1xuICBiYWNrZ3JvdW5kOiBub25lO1xuICBib3JkZXI6IDA7XG4gIG91dGxpbmU6IG5vbmU7XG4gIG1hcmdpbi1yaWdodDogMTBweDtcbn1cblxuLmxvYWRlciB7XG4gIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgdG9wOiAwO1xuICBsZWZ0OiAwO1xuICBoZWlnaHQ6IDJweDtcbn1cblxuLm1haW4tY29udGVudC1jb250YWluZXItb3ZlcmxheTpob3ZlciB7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuQG1lZGlhIHNjcmVlbiBhbmQgKG1heC13aWR0aDogMTI4MHB4KSB7XG4gIC5jb250ZW50LWNvbnRhaW5lciB7XG4gICAgcGFkZGluZy1sZWZ0OiAwICFpbXBvcnRhbnQ7XG4gIH1cblxuICAubWFpbi1jb250ZW50LWNvbnRhaW5lci1vdmVybGF5IHtcbiAgICBkaXNwbGF5OiBibG9jaztcbiAgICBoZWlnaHQ6IDEwMCU7XG4gICAgcG9zaXRpb246IGZpeGVkO1xuICAgIHRvcDogMDtcbiAgICBsZWZ0OiAwO1xuICAgIHotaW5kZXg6IDU7XG4gICAgd2lkdGg6IDEwMCU7XG4gICAgYmFja2dyb3VuZC1jb2xvcjogcmdiYSgwLCAwLCAwLCAwLjUpO1xuICB9XG59Il19 */"

/***/ }),

/***/ "./src/app/shared/ui/panel-layout/panel-layout.component.ts":
/*!******************************************************************!*\
  !*** ./src/app/shared/ui/panel-layout/panel-layout.component.ts ***!
  \******************************************************************/
/*! exports provided: PanelLayoutComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PanelLayoutComponent", function() { return PanelLayoutComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _auth_auth_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../auth/auth.service */ "./src/app/shared/auth/auth.service.ts");
/* harmony import */ var _angular_animations__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/animations */ "./node_modules/@angular/animations/fesm2015/animations.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ui_api_route_helper__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../ui-api/route-helper */ "./src/app/shared/ui-api/route-helper.ts");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _environments_version__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../environments/version */ "./src/environments/version.ts");








let PanelLayoutComponent = class PanelLayoutComponent {
    constructor(auth, router, activatedRoute) {
        this.auth = auth;
        this.router = router;
        this.activatedRoute = activatedRoute;
        this.showTopBar = true;
        this.loading = false;
        this.version = _environments_version__WEBPACK_IMPORTED_MODULE_7__["VERSION"].version;
        this.routeHelper = new _ui_api_route_helper__WEBPACK_IMPORTED_MODULE_5__["RouteHelper"](activatedRoute);
    }
    ngOnInit() {
        this.innerWidth = window.innerWidth;
        this.isLoggedInSubscription = this.auth.isLoggedIn.subscribe(isLoggedIn => {
            this.innerWidth = window.innerWidth;
            if (this.innerWidth > 1280) {
                // show sidebar on web page enter only for large screens
                this.showSidebar = isLoggedIn;
            }
            else {
                this.showSidebar = false;
            }
            this.showTopBar = isLoggedIn;
        });
        this.routerEventsSubscription = this.router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_6__["delay"])(0)).subscribe((event) => {
            switch (true) {
                case event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_4__["NavigationStart"]: {
                    const urlChanges = this.routeHelper.getUrlChanges(event.url);
                    this.loading = urlChanges.path || urlChanges.query;
                    break;
                }
                case event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_4__["NavigationEnd"]:
                case event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_4__["NavigationCancel"]:
                case event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_4__["NavigationError"]: {
                    this.loading = false;
                    break;
                }
                default: {
                    break;
                }
            }
        });
    }
    ngOnDestroy() {
        this.isLoggedInSubscription.unsubscribe();
        this.routerEventsSubscription.unsubscribe();
    }
};
PanelLayoutComponent.ctorParameters = () => [
    { type: _auth_auth_service__WEBPACK_IMPORTED_MODULE_2__["AuthService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["ActivatedRoute"] }
];
PanelLayoutComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-panel-layout',
        template: __webpack_require__(/*! raw-loader!./panel-layout.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/panel-layout/panel-layout.component.html"),
        animations: [
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["trigger"])('openCloseSidebar', [
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["state"])('closed', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["style"])({
                    left: '-237px',
                })),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["transition"])('open => closed', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["animate"])('430ms ease-in-out')
                ]),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["transition"])('closed => open', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["animate"])('430ms ease-in-out')
                ]),
            ]),
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["trigger"])('alignContent', [
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["state"])('closed', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["style"])({
                    paddingLeft: '0px',
                })),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["transition"])('open => closed', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["animate"])('430ms ease-in-out')
                ]),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["transition"])('closed => open', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["animate"])('430ms ease-in-out')
                ]),
            ]),
            Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["trigger"])('openCloseTopBar', [
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["state"])('closed', Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["style"])({
                    marginTop: '-67px',
                })),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["transition"])('open => closed', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["animate"])('430ms ease-in-out')
                ]),
                Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["transition"])('closed => open', [
                    Object(_angular_animations__WEBPACK_IMPORTED_MODULE_3__["animate"])('430ms ease-in-out')
                ]),
            ]),
        ],
        styles: [__webpack_require__(/*! ./panel-layout.component.scss */ "./src/app/shared/ui/panel-layout/panel-layout.component.scss")]
    })
], PanelLayoutComponent);



/***/ }),

/***/ "./src/app/shared/ui/top-bar/breadcrumbs/breadcrumbs.component.scss":
/*!**************************************************************************!*\
  !*** ./src/app/shared/ui/top-bar/breadcrumbs/breadcrumbs.component.scss ***!
  \**************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".br {\n  font-weight: 300;\n}\n\n.br span {\n  text-transform: capitalize;\n}\n\n.breadcrumb-icon {\n  margin-top: -4px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC91aS90b3AtYmFyL2JyZWFkY3J1bWJzL2JyZWFkY3J1bWJzLmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9zaGFyZWQvdWkvdG9wLWJhci9icmVhZGNydW1icy9icmVhZGNydW1icy5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGdCQUFBO0FDQ0Y7O0FERUE7RUFDRSwwQkFBQTtBQ0NGOztBREVBO0VBQ0UsZ0JBQUE7QUNDRiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC91aS90b3AtYmFyL2JyZWFkY3J1bWJzL2JyZWFkY3J1bWJzLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLmJyIHtcbiAgZm9udC13ZWlnaHQ6IDMwMDtcbn1cblxuLmJyIHNwYW4ge1xuICB0ZXh0LXRyYW5zZm9ybTogY2FwaXRhbGl6ZTtcbn1cblxuLmJyZWFkY3J1bWItaWNvbiB7XG4gIG1hcmdpbi10b3A6IC00cHg7XG59XG4iLCIuYnIge1xuICBmb250LXdlaWdodDogMzAwO1xufVxuXG4uYnIgc3BhbiB7XG4gIHRleHQtdHJhbnNmb3JtOiBjYXBpdGFsaXplO1xufVxuXG4uYnJlYWRjcnVtYi1pY29uIHtcbiAgbWFyZ2luLXRvcDogLTRweDtcbn0iXX0= */"

/***/ }),

/***/ "./src/app/shared/ui/top-bar/breadcrumbs/breadcrumbs.component.ts":
/*!************************************************************************!*\
  !*** ./src/app/shared/ui/top-bar/breadcrumbs/breadcrumbs.component.ts ***!
  \************************************************************************/
/*! exports provided: BreadcrumbsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BreadcrumbsComponent", function() { return BreadcrumbsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _ui_api_route_helper__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../ui-api/route-helper */ "./src/app/shared/ui-api/route-helper.ts");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _ui_api_ordering_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../ui-api/ordering.service */ "./src/app/shared/ui-api/ordering.service.ts");






let BreadcrumbsComponent = class BreadcrumbsComponent {
    constructor(router, activatedRoute, config, ordering) {
        this.router = router;
        this.activatedRoute = activatedRoute;
        this.config = config;
        this.ordering = ordering;
        this.breadCrumbs = [];
    }
    changeBreads() {
        const homeUrl = this.config.getPanelUrl(this.config.getPanelHomeUrl());
        let routePath;
        if (this.config.getPanelHomeUrl() === '') {
            routePath = this.routeHelper.getRoutePath();
        }
        else {
            routePath = this.routeHelper.getRoutePath().replace(homeUrl, '');
        }
        // parse path into a list of strings
        this.breadCrumbsDisplay = routePath.split('/');
        // remove first item (e.g. cloud)
        const routeParent = this.breadCrumbsDisplay.splice(0, 1);
        // determine and add the home bread crumb
        let homeBreadCrumbDisplay;
        if (homeUrl === '/') {
            homeBreadCrumbDisplay = 'home';
        }
        else {
            homeBreadCrumbDisplay = homeUrl.replace('/', '');
        }
        this.breadCrumbsDisplay.unshift(homeBreadCrumbDisplay);
        if (this.breadCrumbsDisplay[2]) {
            const finalRoute = this.routeHelper.getFinalRoute();
            if (finalRoute.snapshot.data.config && finalRoute.snapshot.data.config.getBreadCrumbDetail) {
                try {
                    this.breadCrumbsDisplay[2] = finalRoute.snapshot.data.config.getBreadCrumbDetail(finalRoute.snapshot.data);
                }
                catch (e) {
                    console.error('Exception when getting breadcrumb details: ' + e.message);
                }
            }
            else {
                console.error('You need to define route config && getBreadCrumbDetails in route data');
                this.breadCrumbsDisplay[2] = 'n/a';
            }
        }
        let breadCrumb;
        let i = 0;
        this.breadCrumbs = [];
        for (const breadCrumbDisplay of this.breadCrumbsDisplay) {
            breadCrumb = { display: breadCrumbDisplay };
            if (this.breadCrumbsDisplay.length > 1) {
                // set url for breadcrumbs
                if (i === 0) {
                    breadCrumb.url = homeUrl;
                }
                else if (i < this.breadCrumbsDisplay.length - 1) {
                    const urlFragment = routeParent + '/' + breadCrumbDisplay;
                    breadCrumb.url = this.config.getPanelUrl(urlFragment);
                    breadCrumb.queryParams = this.ordering.getQueryParams(urlFragment);
                }
            }
            this.breadCrumbs.push(breadCrumb);
            i = i + 1;
        }
    }
    ngOnInit() {
        this.routeHelper = new _ui_api_route_helper__WEBPACK_IMPORTED_MODULE_3__["RouteHelper"](this.activatedRoute);
        this.changeBreads();
        this.router.events.subscribe(() => {
            this.changeBreads();
        });
    }
};
BreadcrumbsComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] },
    { type: _ui_api_ordering_service__WEBPACK_IMPORTED_MODULE_5__["OrderingService"] }
];
BreadcrumbsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-breadcrumbs',
        template: __webpack_require__(/*! raw-loader!./breadcrumbs.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/top-bar/breadcrumbs/breadcrumbs.component.html"),
        styles: [__webpack_require__(/*! ./breadcrumbs.component.scss */ "./src/app/shared/ui/top-bar/breadcrumbs/breadcrumbs.component.scss")]
    })
], BreadcrumbsComponent);



/***/ }),

/***/ "./src/app/shared/ui/top-bar/hello-user-button/hello-user-button.component.scss":
/*!**************************************************************************************!*\
  !*** ./src/app/shared/ui/top-bar/hello-user-button/hello-user-button.component.scss ***!
  \**************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".hello-user-button {\n  font-size: 20px;\n  font-weight: 400;\n  display: -webkit-box;\n  display: flex;\n  -webkit-box-align: center;\n          align-items: center;\n  -webkit-box-orient: horizontal;\n  -webkit-box-direction: normal;\n          flex-direction: row;\n  width: 100%;\n  cursor: pointer;\n}\n\n.hello-user-first-menu-item {\n  padding: 15px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC91aS90b3AtYmFyL2hlbGxvLXVzZXItYnV0dG9uL2hlbGxvLXVzZXItYnV0dG9uLmNvbXBvbmVudC5zY3NzIiwic3JjL2FwcC9zaGFyZWQvdWkvdG9wLWJhci9oZWxsby11c2VyLWJ1dHRvbi9oZWxsby11c2VyLWJ1dHRvbi5jb21wb25lbnQuc2NzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtFQUNFLGVBQUE7RUFDQSxnQkFBQTtFQUNBLG9CQUFBO0VBQUEsYUFBQTtFQUNBLHlCQUFBO1VBQUEsbUJBQUE7RUFDQSw4QkFBQTtFQUFBLDZCQUFBO1VBQUEsbUJBQUE7RUFDQSxXQUFBO0VBQ0EsZUFBQTtBQ0NGOztBREVBO0VBQ0UsYUFBQTtBQ0NGIiwiZmlsZSI6InNyYy9hcHAvc2hhcmVkL3VpL3RvcC1iYXIvaGVsbG8tdXNlci1idXR0b24vaGVsbG8tdXNlci1idXR0b24uY29tcG9uZW50LnNjc3MiLCJzb3VyY2VzQ29udGVudCI6WyIuaGVsbG8tdXNlci1idXR0b24ge1xuICBmb250LXNpemU6IDIwcHg7XG4gIGZvbnQtd2VpZ2h0OiA0MDA7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGZsZXgtZGlyZWN0aW9uOiByb3c7XG4gIHdpZHRoOiAxMDAlO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbi5oZWxsby11c2VyLWZpcnN0LW1lbnUtaXRlbSB7XG4gIHBhZGRpbmc6IDE1cHg7XG59XG4iLCIuaGVsbG8tdXNlci1idXR0b24ge1xuICBmb250LXNpemU6IDIwcHg7XG4gIGZvbnQtd2VpZ2h0OiA0MDA7XG4gIGRpc3BsYXk6IGZsZXg7XG4gIGFsaWduLWl0ZW1zOiBjZW50ZXI7XG4gIGZsZXgtZGlyZWN0aW9uOiByb3c7XG4gIHdpZHRoOiAxMDAlO1xuICBjdXJzb3I6IHBvaW50ZXI7XG59XG5cbi5oZWxsby11c2VyLWZpcnN0LW1lbnUtaXRlbSB7XG4gIHBhZGRpbmc6IDE1cHg7XG59Il19 */"

/***/ }),

/***/ "./src/app/shared/ui/top-bar/hello-user-button/hello-user-button.component.ts":
/*!************************************************************************************!*\
  !*** ./src/app/shared/ui/top-bar/hello-user-button/hello-user-button.component.ts ***!
  \************************************************************************************/
/*! exports provided: HelloUserButtonComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HelloUserButtonComponent", function() { return HelloUserButtonComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _auth_auth_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../auth/auth.service */ "./src/app/shared/auth/auth.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../config/config.service */ "./src/app/shared/config/config.service.ts");





let HelloUserButtonComponent = class HelloUserButtonComponent {
    constructor(authService, router, config) {
        this.authService = authService;
        this.router = router;
        this.config = config;
    }
    logout() {
        this.authService.logout().subscribe(() => {
            this.router.navigateByUrl(this.config.getPanelUrl('login')).then(() => { });
        });
    }
    ngOnInit() {
    }
};
HelloUserButtonComponent.ctorParameters = () => [
    { type: _auth_auth_service__WEBPACK_IMPORTED_MODULE_2__["AuthService"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
    { type: _config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] }
];
HelloUserButtonComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-hello-user-button',
        template: __webpack_require__(/*! raw-loader!./hello-user-button.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/top-bar/hello-user-button/hello-user-button.component.html"),
        styles: [__webpack_require__(/*! ./hello-user-button.component.scss */ "./src/app/shared/ui/top-bar/hello-user-button/hello-user-button.component.scss")]
    })
], HelloUserButtonComponent);



/***/ }),

/***/ "./src/app/shared/ui/top-bar/search-box/search-box.component.scss":
/*!************************************************************************!*\
  !*** ./src/app/shared/ui/top-bar/search-box/search-box.component.scss ***!
  \************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".search-container {\n  max-height: 55px;\n  margin-top: -25px;\n  margin-left: 30px;\n  width: 600px;\n  position: relative;\n}\n\n.search-container input {\n  position: relative;\n  font-size: 18px;\n  box-sizing: border-box;\n  width: 100%;\n  line-height: 40px;\n  color: rgba(255, 255, 255, 0.87);\n  height: 40px;\n  border: 0;\n  border-radius: 3px;\n  padding-left: 50px;\n  padding-top: 25px;\n  padding-bottom: 22px;\n  background: rgba(0, 0, 0, 0.1);\n}\n\n.search-container:hover {\n  background: rgba(255, 255, 255, 0.1);\n}\n\n.search-container input:focus {\n  outline: none;\n}\n\n.search-container input::-webkit-input-placeholder {\n  color: rgba(255, 255, 255, 0.4);\n  opacity: 1;\n}\n\n.search-container input::-moz-placeholder {\n  color: rgba(255, 255, 255, 0.4);\n  opacity: 1;\n}\n\n.search-container input::-ms-input-placeholder {\n  color: rgba(255, 255, 255, 0.4);\n  opacity: 1;\n}\n\n.search-container input::placeholder {\n  color: rgba(255, 255, 255, 0.4);\n  opacity: 1;\n}\n\n.search-container input:-ms-input-placeholder {\n  color: rgba(255, 255, 255, 0.4);\n}\n\n.search-container input::-ms-input-placeholder {\n  color: rgba(255, 255, 255, 0.4);\n}\n\n.search-container::after {\n  position: absolute;\n  left: 10px;\n  top: 5px;\n  font-family: \"Fleio-Icons\", monospace;\n  font-size: 25px;\n  line-height: 35px;\n  content: \"search\";\n  letter-spacing: 0 !important;\n}\n\n.close-search-button {\n  position: absolute;\n  right: 2px;\n  top: 3px;\n}\n\n.search-container-mobile {\n  position: absolute;\n  right: 165px;\n  top: 20px;\n}\n\n.search-container-mobile input {\n  width: 93%;\n  position: fixed;\n  left: 2.5%;\n  height: 40px;\n  z-index: 20;\n  top: 11px;\n  border-radius: 5px;\n  outline: none;\n  padding-left: 15px;\n  background: #fff;\n  border: 0;\n}\n\n.search-container-mobile mat-icon {\n  cursor: pointer;\n}\n\n.search-container-mobile-close {\n  position: fixed;\n  z-index: 25;\n  color: gray !important;\n  right: 20px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC91aS90b3AtYmFyL3NlYXJjaC1ib3gvc2VhcmNoLWJveC5jb21wb25lbnQuc2NzcyIsInNyYy9hcHAvc2hhcmVkL3VpL3RvcC1iYXIvc2VhcmNoLWJveC9zZWFyY2gtYm94LmNvbXBvbmVudC5zY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0VBQ0UsZ0JBQUE7RUFDQSxpQkFBQTtFQUNBLGlCQUFBO0VBQ0EsWUFBQTtFQUNBLGtCQUFBO0FDQ0Y7O0FERUE7RUFDRSxrQkFBQTtFQUNBLGVBQUE7RUFDQSxzQkFBQTtFQUNBLFdBQUE7RUFDQSxpQkFBQTtFQUNBLGdDQUFBO0VBQ0EsWUFBQTtFQUNBLFNBQUE7RUFDQSxrQkFBQTtFQUNBLGtCQUFBO0VBQ0EsaUJBQUE7RUFDQSxvQkFBQTtFQUNBLDhCQUFBO0FDQ0Y7O0FERUE7RUFDRSxvQ0FBQTtBQ0NGOztBREVBO0VBQ0UsYUFBQTtBQ0NGOztBREVBO0VBQ0UsK0JBQUE7RUFDQSxVQUFBO0FDQ0Y7O0FESEE7RUFDRSwrQkFBQTtFQUNBLFVBQUE7QUNDRjs7QURIQTtFQUNFLCtCQUFBO0VBQ0EsVUFBQTtBQ0NGOztBREhBO0VBQ0UsK0JBQUE7RUFDQSxVQUFBO0FDQ0Y7O0FERUE7RUFDRSwrQkFBQTtBQ0NGOztBREVBO0VBQ0UsK0JBQUE7QUNDRjs7QURFQTtFQUNFLGtCQUFBO0VBQ0EsVUFBQTtFQUNBLFFBQUE7RUFDQSxxQ0FBQTtFQUNBLGVBQUE7RUFDQSxpQkFBQTtFQUNBLGlCQUFBO0VBQ0EsNEJBQUE7QUNDRjs7QURFQTtFQUNFLGtCQUFBO0VBQ0EsVUFBQTtFQUNBLFFBQUE7QUNDRjs7QURFQTtFQUNFLGtCQUFBO0VBQ0EsWUFBQTtFQUNBLFNBQUE7QUNDRjs7QURFQTtFQUNFLFVBQUE7RUFDQSxlQUFBO0VBQ0EsVUFBQTtFQUNBLFlBQUE7RUFDQSxXQUFBO0VBQ0EsU0FBQTtFQUNBLGtCQUFBO0VBQ0EsYUFBQTtFQUNBLGtCQUFBO0VBQ0EsZ0JBQUE7RUFDQSxTQUFBO0FDQ0Y7O0FERUE7RUFDRSxlQUFBO0FDQ0Y7O0FERUE7RUFDRSxlQUFBO0VBQ0EsV0FBQTtFQUNBLHNCQUFBO0VBQ0EsV0FBQTtBQ0NGIiwiZmlsZSI6InNyYy9hcHAvc2hhcmVkL3VpL3RvcC1iYXIvc2VhcmNoLWJveC9zZWFyY2gtYm94LmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLnNlYXJjaC1jb250YWluZXIge1xuICBtYXgtaGVpZ2h0OiA1NXB4O1xuICBtYXJnaW4tdG9wOiAtMjVweDtcbiAgbWFyZ2luLWxlZnQ6IDMwcHg7XG4gIHdpZHRoOiA2MDBweDtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xufVxuXG4uc2VhcmNoLWNvbnRhaW5lciBpbnB1dCB7XG4gIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgZm9udC1zaXplOiAxOHB4O1xuICBib3gtc2l6aW5nOiBib3JkZXItYm94O1xuICB3aWR0aDogMTAwJTtcbiAgbGluZS1oZWlnaHQ6IDQwcHg7XG4gIGNvbG9yOiByZ2JhKDI1NSwgMjU1LCAyNTUsIDAuODcpO1xuICBoZWlnaHQ6IDQwcHg7XG4gIGJvcmRlcjogMDtcbiAgYm9yZGVyLXJhZGl1czogM3B4O1xuICBwYWRkaW5nLWxlZnQ6IDUwcHg7XG4gIHBhZGRpbmctdG9wOiAyNXB4O1xuICBwYWRkaW5nLWJvdHRvbTogMjJweDtcbiAgYmFja2dyb3VuZDogcmdiYSgwLCAwLCAwLCAuMSk7XG59XG5cbi5zZWFyY2gtY29udGFpbmVyOmhvdmVyIHtcbiAgYmFja2dyb3VuZDogcmdiYSgyNTUsIDI1NSwgMjU1LCAuMSk7XG59XG5cbi5zZWFyY2gtY29udGFpbmVyIGlucHV0OmZvY3VzIHtcbiAgb3V0bGluZTogbm9uZTtcbn1cblxuLnNlYXJjaC1jb250YWluZXIgaW5wdXQ6OnBsYWNlaG9sZGVyIHtcbiAgY29sb3I6IHJnYmEoMjU1LCAyNTUsIDI1NSwgMC40KTtcbiAgb3BhY2l0eTogMTtcbn1cblxuLnNlYXJjaC1jb250YWluZXIgaW5wdXQ6LW1zLWlucHV0LXBsYWNlaG9sZGVyIHtcbiAgY29sb3I6IHJnYmEoMjU1LCAyNTUsIDI1NSwgMC40KTtcbn1cblxuLnNlYXJjaC1jb250YWluZXIgaW5wdXQ6Oi1tcy1pbnB1dC1wbGFjZWhvbGRlciB7XG4gIGNvbG9yOiByZ2JhKDI1NSwgMjU1LCAyNTUsIDAuNCk7XG59XG5cbi5zZWFyY2gtY29udGFpbmVyOjphZnRlciB7XG4gIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgbGVmdDogMTBweDtcbiAgdG9wOiA1cHg7XG4gIGZvbnQtZmFtaWx5OiBcIkZsZWlvLUljb25zXCIsIG1vbm9zcGFjZTtcbiAgZm9udC1zaXplOiAyNXB4O1xuICBsaW5lLWhlaWdodDogMzVweDtcbiAgY29udGVudDogJ3NlYXJjaCc7XG4gIGxldHRlci1zcGFjaW5nOiAwICFpbXBvcnRhbnQ7XG59XG5cbi5jbG9zZS1zZWFyY2gtYnV0dG9uIHtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICByaWdodDogMnB4O1xuICB0b3A6IDNweDtcbn1cblxuLnNlYXJjaC1jb250YWluZXItbW9iaWxlIHtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICByaWdodDogMTY1cHg7XG4gIHRvcDogMjBweDtcbn1cblxuLnNlYXJjaC1jb250YWluZXItbW9iaWxlIGlucHV0IHtcbiAgd2lkdGg6IDkzJTtcbiAgcG9zaXRpb246IGZpeGVkO1xuICBsZWZ0OiAyLjUlO1xuICBoZWlnaHQ6IDQwcHg7XG4gIHotaW5kZXg6IDIwO1xuICB0b3A6IDExcHg7XG4gIGJvcmRlci1yYWRpdXM6IDVweDtcbiAgb3V0bGluZTogbm9uZTtcbiAgcGFkZGluZy1sZWZ0OiAxNXB4O1xuICBiYWNrZ3JvdW5kOiAjZmZmO1xuICBib3JkZXI6IDA7XG59XG5cbi5zZWFyY2gtY29udGFpbmVyLW1vYmlsZSBtYXQtaWNvbiB7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuLnNlYXJjaC1jb250YWluZXItbW9iaWxlLWNsb3NlIHtcbiAgcG9zaXRpb246IGZpeGVkO1xuICB6LWluZGV4OiAyNTtcbiAgY29sb3I6IGdyYXkgIWltcG9ydGFudDtcbiAgcmlnaHQ6IDIwcHg7XG59XG4iLCIuc2VhcmNoLWNvbnRhaW5lciB7XG4gIG1heC1oZWlnaHQ6IDU1cHg7XG4gIG1hcmdpbi10b3A6IC0yNXB4O1xuICBtYXJnaW4tbGVmdDogMzBweDtcbiAgd2lkdGg6IDYwMHB4O1xuICBwb3NpdGlvbjogcmVsYXRpdmU7XG59XG5cbi5zZWFyY2gtY29udGFpbmVyIGlucHV0IHtcbiAgcG9zaXRpb246IHJlbGF0aXZlO1xuICBmb250LXNpemU6IDE4cHg7XG4gIGJveC1zaXppbmc6IGJvcmRlci1ib3g7XG4gIHdpZHRoOiAxMDAlO1xuICBsaW5lLWhlaWdodDogNDBweDtcbiAgY29sb3I6IHJnYmEoMjU1LCAyNTUsIDI1NSwgMC44Nyk7XG4gIGhlaWdodDogNDBweDtcbiAgYm9yZGVyOiAwO1xuICBib3JkZXItcmFkaXVzOiAzcHg7XG4gIHBhZGRpbmctbGVmdDogNTBweDtcbiAgcGFkZGluZy10b3A6IDI1cHg7XG4gIHBhZGRpbmctYm90dG9tOiAyMnB4O1xuICBiYWNrZ3JvdW5kOiByZ2JhKDAsIDAsIDAsIDAuMSk7XG59XG5cbi5zZWFyY2gtY29udGFpbmVyOmhvdmVyIHtcbiAgYmFja2dyb3VuZDogcmdiYSgyNTUsIDI1NSwgMjU1LCAwLjEpO1xufVxuXG4uc2VhcmNoLWNvbnRhaW5lciBpbnB1dDpmb2N1cyB7XG4gIG91dGxpbmU6IG5vbmU7XG59XG5cbi5zZWFyY2gtY29udGFpbmVyIGlucHV0OjpwbGFjZWhvbGRlciB7XG4gIGNvbG9yOiByZ2JhKDI1NSwgMjU1LCAyNTUsIDAuNCk7XG4gIG9wYWNpdHk6IDE7XG59XG5cbi5zZWFyY2gtY29udGFpbmVyIGlucHV0Oi1tcy1pbnB1dC1wbGFjZWhvbGRlciB7XG4gIGNvbG9yOiByZ2JhKDI1NSwgMjU1LCAyNTUsIDAuNCk7XG59XG5cbi5zZWFyY2gtY29udGFpbmVyIGlucHV0OjotbXMtaW5wdXQtcGxhY2Vob2xkZXIge1xuICBjb2xvcjogcmdiYSgyNTUsIDI1NSwgMjU1LCAwLjQpO1xufVxuXG4uc2VhcmNoLWNvbnRhaW5lcjo6YWZ0ZXIge1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIGxlZnQ6IDEwcHg7XG4gIHRvcDogNXB4O1xuICBmb250LWZhbWlseTogXCJGbGVpby1JY29uc1wiLCBtb25vc3BhY2U7XG4gIGZvbnQtc2l6ZTogMjVweDtcbiAgbGluZS1oZWlnaHQ6IDM1cHg7XG4gIGNvbnRlbnQ6IFwic2VhcmNoXCI7XG4gIGxldHRlci1zcGFjaW5nOiAwICFpbXBvcnRhbnQ7XG59XG5cbi5jbG9zZS1zZWFyY2gtYnV0dG9uIHtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICByaWdodDogMnB4O1xuICB0b3A6IDNweDtcbn1cblxuLnNlYXJjaC1jb250YWluZXItbW9iaWxlIHtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICByaWdodDogMTY1cHg7XG4gIHRvcDogMjBweDtcbn1cblxuLnNlYXJjaC1jb250YWluZXItbW9iaWxlIGlucHV0IHtcbiAgd2lkdGg6IDkzJTtcbiAgcG9zaXRpb246IGZpeGVkO1xuICBsZWZ0OiAyLjUlO1xuICBoZWlnaHQ6IDQwcHg7XG4gIHotaW5kZXg6IDIwO1xuICB0b3A6IDExcHg7XG4gIGJvcmRlci1yYWRpdXM6IDVweDtcbiAgb3V0bGluZTogbm9uZTtcbiAgcGFkZGluZy1sZWZ0OiAxNXB4O1xuICBiYWNrZ3JvdW5kOiAjZmZmO1xuICBib3JkZXI6IDA7XG59XG5cbi5zZWFyY2gtY29udGFpbmVyLW1vYmlsZSBtYXQtaWNvbiB7XG4gIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuLnNlYXJjaC1jb250YWluZXItbW9iaWxlLWNsb3NlIHtcbiAgcG9zaXRpb246IGZpeGVkO1xuICB6LWluZGV4OiAyNTtcbiAgY29sb3I6IGdyYXkgIWltcG9ydGFudDtcbiAgcmlnaHQ6IDIwcHg7XG59Il19 */"

/***/ }),

/***/ "./src/app/shared/ui/top-bar/search-box/search-box.component.ts":
/*!**********************************************************************!*\
  !*** ./src/app/shared/ui/top-bar/search-box/search-box.component.ts ***!
  \**********************************************************************/
/*! exports provided: SearchBoxComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SearchBoxComponent", function() { return SearchBoxComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _ui_api_search_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../ui-api/search.service */ "./src/app/shared/ui-api/search.service.ts");
/* harmony import */ var _ui_api_route_helper__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../ui-api/route-helper */ "./src/app/shared/ui-api/route-helper.ts");







let SearchBoxComponent = class SearchBoxComponent {
    constructor(route, router, searchService) {
        this.route = route;
        this.router = router;
        this.searchService = searchService;
        this.searchText = new _angular_forms__WEBPACK_IMPORTED_MODULE_4__["FormControl"]('searchText');
        this.showMobileInput = false;
    }
    ngOnInit() {
        this.setSearchText();
        this.searchText.valueChanges.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["map"])(() => this.searchText.value), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_2__["debounceTime"])(1000)).subscribe(searchText => {
            this.searchService.search(searchText);
        });
    }
    setSearchText() {
        const routeSnapshot = new _ui_api_route_helper__WEBPACK_IMPORTED_MODULE_6__["RouteHelper"](this.route).getFinalRoute().snapshot;
        if (routeSnapshot.queryParams.search) {
            this.searchText.setValue(routeSnapshot.queryParams.search, { emitEvent: false });
        }
        else {
            this.searchText.setValue(undefined, { emitEvent: false });
        }
    }
    clearSearch() {
        this.searchText.setValue(undefined, { emitEvent: false });
        this.searchService.search(undefined);
    }
};
SearchBoxComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
    { type: _ui_api_search_service__WEBPACK_IMPORTED_MODULE_5__["SearchService"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Input"])()
], SearchBoxComponent.prototype, "searchConfig", void 0);
SearchBoxComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-search-box',
        template: __webpack_require__(/*! raw-loader!./search-box.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/top-bar/search-box/search-box.component.html"),
        styles: [__webpack_require__(/*! ./search-box.component.scss */ "./src/app/shared/ui/top-bar/search-box/search-box.component.scss")]
    })
], SearchBoxComponent);



/***/ }),

/***/ "./src/app/shared/ui/top-bar/stop-impersonating-button/stop-impersonating-button.component.scss":
/*!******************************************************************************************************!*\
  !*** ./src/app/shared/ui/top-bar/stop-impersonating-button/stop-impersonating-button.component.scss ***!
  \******************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3NoYXJlZC91aS90b3AtYmFyL3N0b3AtaW1wZXJzb25hdGluZy1idXR0b24vc3RvcC1pbXBlcnNvbmF0aW5nLWJ1dHRvbi5jb21wb25lbnQuc2NzcyJ9 */"

/***/ }),

/***/ "./src/app/shared/ui/top-bar/stop-impersonating-button/stop-impersonating-button.component.ts":
/*!****************************************************************************************************!*\
  !*** ./src/app/shared/ui/top-bar/stop-impersonating-button/stop-impersonating-button.component.ts ***!
  \****************************************************************************************************/
/*! exports provided: StopImpersonatingButtonComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "StopImpersonatingButtonComponent", function() { return StopImpersonatingButtonComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _auth_auth_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../auth/auth.service */ "./src/app/shared/auth/auth.service.ts");



let StopImpersonatingButtonComponent = class StopImpersonatingButtonComponent {
    constructor(auth) {
        this.auth = auth;
    }
    ngOnInit() {
    }
    closeImpersonation() {
        this.auth.stopImpersonating();
    }
};
StopImpersonatingButtonComponent.ctorParameters = () => [
    { type: _auth_auth_service__WEBPACK_IMPORTED_MODULE_2__["AuthService"] }
];
StopImpersonatingButtonComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-stop-impersonating-button',
        template: __webpack_require__(/*! raw-loader!./stop-impersonating-button.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/top-bar/stop-impersonating-button/stop-impersonating-button.component.html"),
        styles: [__webpack_require__(/*! ./stop-impersonating-button.component.scss */ "./src/app/shared/ui/top-bar/stop-impersonating-button/stop-impersonating-button.component.scss")]
    })
], StopImpersonatingButtonComponent);



/***/ }),

/***/ "./src/app/shared/ui/top-bar/top-bar.component.scss":
/*!**********************************************************!*\
  !*** ./src/app/shared/ui/top-bar/top-bar.component.scss ***!
  \**********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".topbar-items-container {\n  padding-top: 18px;\n}\n\n.topbar-items-container > div {\n  display: inline-block;\n}\n\n.topbar-items-container > div:last-child {\n  float: right;\n}\n\n.breadcrumbs-container {\n  border-left: 1px solid rgba(255, 255, 255, 0.2);\n  padding-left: 16px;\n}\n\n.buttons-container {\n  padding-bottom: 16px;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi9ob21lL2dpdGxhYi1ydW5uZXIvYnVpbGRzLzFVZkJYU1M2LzEvZmxlaW8vZmxlaW8vbmdmcm9udGVuZC9zcmMvYXBwL3NoYXJlZC91aS90b3AtYmFyL3RvcC1iYXIuY29tcG9uZW50LnNjc3MiLCJzcmMvYXBwL3NoYXJlZC91aS90b3AtYmFyL3RvcC1iYXIuY29tcG9uZW50LnNjc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxpQkFBQTtBQ0NGOztBRENBO0VBQ0UscUJBQUE7QUNFRjs7QURDQTtFQUNFLFlBQUE7QUNFRjs7QURDQTtFQUNFLCtDQUFBO0VBQ0Esa0JBQUE7QUNFRjs7QURDQTtFQUNJLG9CQUFBO0FDRUoiLCJmaWxlIjoic3JjL2FwcC9zaGFyZWQvdWkvdG9wLWJhci90b3AtYmFyLmNvbXBvbmVudC5zY3NzIiwic291cmNlc0NvbnRlbnQiOlsiLnRvcGJhci1pdGVtcy1jb250YWluZXIge1xuICBwYWRkaW5nLXRvcDogMThweDtcbn1cbi50b3BiYXItaXRlbXMtY29udGFpbmVyID4gZGl2IHtcbiAgZGlzcGxheTogaW5saW5lLWJsb2NrO1xufVxuXG4udG9wYmFyLWl0ZW1zLWNvbnRhaW5lciA+IGRpdjpsYXN0LWNoaWxkIHtcbiAgZmxvYXQ6IHJpZ2h0O1xufVxuXG4uYnJlYWRjcnVtYnMtY29udGFpbmVyIHtcbiAgYm9yZGVyLWxlZnQ6IDFweCBzb2xpZCByZ2JhKDI1NSwgMjU1LCAyNTUsIDAuMik7XG4gIHBhZGRpbmctbGVmdDogMTZweDtcbn1cblxuLmJ1dHRvbnMtY29udGFpbmVyIHtcbiAgICBwYWRkaW5nLWJvdHRvbTogMTZweDtcbn1cbiIsIi50b3BiYXItaXRlbXMtY29udGFpbmVyIHtcbiAgcGFkZGluZy10b3A6IDE4cHg7XG59XG5cbi50b3BiYXItaXRlbXMtY29udGFpbmVyID4gZGl2IHtcbiAgZGlzcGxheTogaW5saW5lLWJsb2NrO1xufVxuXG4udG9wYmFyLWl0ZW1zLWNvbnRhaW5lciA+IGRpdjpsYXN0LWNoaWxkIHtcbiAgZmxvYXQ6IHJpZ2h0O1xufVxuXG4uYnJlYWRjcnVtYnMtY29udGFpbmVyIHtcbiAgYm9yZGVyLWxlZnQ6IDFweCBzb2xpZCByZ2JhKDI1NSwgMjU1LCAyNTUsIDAuMik7XG4gIHBhZGRpbmctbGVmdDogMTZweDtcbn1cblxuLmJ1dHRvbnMtY29udGFpbmVyIHtcbiAgcGFkZGluZy1ib3R0b206IDE2cHg7XG59Il19 */"

/***/ }),

/***/ "./src/app/shared/ui/top-bar/top-bar.component.ts":
/*!********************************************************!*\
  !*** ./src/app/shared/ui/top-bar/top-bar.component.ts ***!
  \********************************************************/
/*! exports provided: TopBarComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TopBarComponent", function() { return TopBarComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _ui_api_route_helper__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../ui-api/route-helper */ "./src/app/shared/ui-api/route-helper.ts");
/* harmony import */ var _auth_auth_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../auth/auth.service */ "./src/app/shared/auth/auth.service.ts");






let TopBarComponent = class TopBarComponent {
    constructor(router, activatedRoute, auth) {
        this.router = router;
        this.activatedRoute = activatedRoute;
        this.auth = auth;
        this.routeHelper = new _ui_api_route_helper__WEBPACK_IMPORTED_MODULE_4__["RouteHelper"](activatedRoute);
    }
    ngOnInit() {
        this.routerEventSubscription = this.router.events.pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["filter"])((event) => {
            return event instanceof _angular_router__WEBPACK_IMPORTED_MODULE_2__["NavigationEnd"];
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(() => {
            return this.routeHelper.getSearchConfig();
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["startWith"])(this.routeHelper.getSearchConfig())).subscribe(searchConfig => {
            this.searchConfig = searchConfig;
            if (this.searchConfig.show && this.searchBox && this.routeHelper.getUrlChanges(this.router.url).query) {
                this.searchBox.setSearchText();
            }
        });
    }
    ngOnDestroy() {
        this.routerEventSubscription.unsubscribe();
    }
};
TopBarComponent.ctorParameters = () => [
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
    { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"] },
    { type: _auth_auth_service__WEBPACK_IMPORTED_MODULE_5__["AuthService"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["ViewChild"])('searchBox', { static: false })
], TopBarComponent.prototype, "searchBox", void 0);
TopBarComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-top-bar',
        template: __webpack_require__(/*! raw-loader!./top-bar.component.html */ "./node_modules/raw-loader/index.js!./src/app/shared/ui/top-bar/top-bar.component.html"),
        styles: [__webpack_require__(/*! ./top-bar.component.scss */ "./src/app/shared/ui/top-bar/top-bar.component.scss")]
    })
], TopBarComponent);



/***/ }),

/***/ "./src/app/shared/ui/ui.module.ts":
/*!****************************************!*\
  !*** ./src/app/shared/ui/ui.module.ts ***!
  \****************************************/
/*! exports provided: UiModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UiModule", function() { return UiModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _panel_layout_panel_layout_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./panel-layout/panel-layout.component */ "./src/app/shared/ui/panel-layout/panel-layout.component.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm2015/flex-layout.js");
/* harmony import */ var _menu_side_nav_menu_side_nav_menu_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./menu/side-nav-menu/side-nav-menu.component */ "./src/app/shared/ui/menu/side-nav-menu/side-nav-menu.component.ts");
/* harmony import */ var _angular_material_tree__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/material/tree */ "./node_modules/@angular/material/esm2015/tree.js");
/* harmony import */ var _top_bar_top_bar_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./top-bar/top-bar.component */ "./src/app/shared/ui/top-bar/top-bar.component.ts");
/* harmony import */ var _angular_material__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/material */ "./node_modules/@angular/material/esm2015/material.js");
/* harmony import */ var _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material/icon */ "./node_modules/@angular/material/esm2015/icon.js");
/* harmony import */ var _logo_logo_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./logo/logo.component */ "./src/app/shared/ui/logo/logo.component.ts");
/* harmony import */ var _menu_menu_item_menu_item_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./menu/menu-item/menu-item.component */ "./src/app/shared/ui/menu/menu-item/menu-item.component.ts");
/* harmony import */ var _menu_menu_item_container_menu_item_container_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./menu/menu-item-container/menu-item-container.component */ "./src/app/shared/ui/menu/menu-item-container/menu-item-container.component.ts");
/* harmony import */ var _angular_material_progress_bar__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/progress-bar */ "./node_modules/@angular/material/esm2015/progress-bar.js");
/* harmony import */ var _top_bar_search_box_search_box_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./top-bar/search-box/search-box.component */ "./src/app/shared/ui/top-bar/search-box/search-box.component.ts");
/* harmony import */ var _top_bar_breadcrumbs_breadcrumbs_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./top-bar/breadcrumbs/breadcrumbs.component */ "./src/app/shared/ui/top-bar/breadcrumbs/breadcrumbs.component.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm2015/form-field.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm2015/input.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _gravatar_gravatar_component__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./gravatar/gravatar.component */ "./src/app/shared/ui/gravatar/gravatar.component.ts");
/* harmony import */ var _top_bar_hello_user_button_hello_user_button_component__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./top-bar/hello-user-button/hello-user-button.component */ "./src/app/shared/ui/top-bar/hello-user-button/hello-user-button.component.ts");
/* harmony import */ var _common_icon_icon_component__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./common/icon/icon.component */ "./src/app/shared/ui/common/icon/icon.component.ts");
/* harmony import */ var _top_bar_stop_impersonating_button_stop_impersonating_button_component__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./top-bar/stop-impersonating-button/stop-impersonating-button.component */ "./src/app/shared/ui/top-bar/stop-impersonating-button/stop-impersonating-button.component.ts");
/* harmony import */ var _fl_backdrop_fl_backdrop_component__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ./fl-backdrop/fl-backdrop.component */ "./src/app/shared/ui/fl-backdrop/fl-backdrop.component.ts");
/* harmony import */ var _angular_material_progress_spinner__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! @angular/material/progress-spinner */ "./node_modules/@angular/material/esm2015/progress-spinner.js");
/* harmony import */ var _fleio_data_controls_phone_input_phone_input_component__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ../fleio-data-controls/phone-input/phone-input.component */ "./src/app/shared/fleio-data-controls/phone-input/phone-input.component.ts");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm2015/select.js");






























let UiModule = class UiModule {
};
UiModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [
            _panel_layout_panel_layout_component__WEBPACK_IMPORTED_MODULE_3__["PanelLayoutComponent"],
            _menu_side_nav_menu_side_nav_menu_component__WEBPACK_IMPORTED_MODULE_6__["SideNavMenuComponent"],
            _top_bar_top_bar_component__WEBPACK_IMPORTED_MODULE_8__["TopBarComponent"],
            _logo_logo_component__WEBPACK_IMPORTED_MODULE_11__["LogoComponent"],
            _menu_menu_item_menu_item_component__WEBPACK_IMPORTED_MODULE_12__["MenuItemComponent"],
            _menu_menu_item_container_menu_item_container_component__WEBPACK_IMPORTED_MODULE_13__["MenuItemContainerComponent"],
            _top_bar_search_box_search_box_component__WEBPACK_IMPORTED_MODULE_15__["SearchBoxComponent"],
            _top_bar_breadcrumbs_breadcrumbs_component__WEBPACK_IMPORTED_MODULE_16__["BreadcrumbsComponent"],
            _gravatar_gravatar_component__WEBPACK_IMPORTED_MODULE_20__["GravatarComponent"],
            _top_bar_hello_user_button_hello_user_button_component__WEBPACK_IMPORTED_MODULE_21__["HelloUserButtonComponent"],
            _common_icon_icon_component__WEBPACK_IMPORTED_MODULE_22__["IconComponent"],
            _fl_backdrop_fl_backdrop_component__WEBPACK_IMPORTED_MODULE_24__["FlBackdropComponent"],
            _top_bar_stop_impersonating_button_stop_impersonating_button_component__WEBPACK_IMPORTED_MODULE_23__["StopImpersonatingButtonComponent"],
            _fleio_data_controls_phone_input_phone_input_component__WEBPACK_IMPORTED_MODULE_26__["PhoneInputComponent"],
        ],
        exports: [
            _panel_layout_panel_layout_component__WEBPACK_IMPORTED_MODULE_3__["PanelLayoutComponent"],
            _common_icon_icon_component__WEBPACK_IMPORTED_MODULE_22__["IconComponent"],
            _logo_logo_component__WEBPACK_IMPORTED_MODULE_11__["LogoComponent"],
            _gravatar_gravatar_component__WEBPACK_IMPORTED_MODULE_20__["GravatarComponent"],
            _fl_backdrop_fl_backdrop_component__WEBPACK_IMPORTED_MODULE_24__["FlBackdropComponent"],
            _fleio_data_controls_phone_input_phone_input_component__WEBPACK_IMPORTED_MODULE_26__["PhoneInputComponent"],
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"],
            _angular_flex_layout__WEBPACK_IMPORTED_MODULE_5__["FlexLayoutModule"],
            _angular_material_tree__WEBPACK_IMPORTED_MODULE_7__["MatTreeModule"],
            _angular_material__WEBPACK_IMPORTED_MODULE_9__["MatToolbarModule"],
            _angular_material_icon__WEBPACK_IMPORTED_MODULE_10__["MatIconModule"],
            _angular_material__WEBPACK_IMPORTED_MODULE_9__["MatButtonModule"],
            _angular_material_progress_bar__WEBPACK_IMPORTED_MODULE_14__["MatProgressBarModule"],
            _angular_material_form_field__WEBPACK_IMPORTED_MODULE_17__["MatFormFieldModule"],
            _angular_material_input__WEBPACK_IMPORTED_MODULE_18__["MatInputModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_19__["ReactiveFormsModule"],
            _angular_material__WEBPACK_IMPORTED_MODULE_9__["MatMenuModule"],
            _angular_material__WEBPACK_IMPORTED_MODULE_9__["MatRippleModule"],
            _angular_material_progress_spinner__WEBPACK_IMPORTED_MODULE_25__["MatProgressSpinnerModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_19__["FormsModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_27__["MatSelectModule"],
        ]
    })
], UiModule);



/***/ }),

/***/ "./src/environments/environment.ts":
/*!*****************************************!*\
  !*** ./src/environments/environment.ts ***!
  \*****************************************/
/*! exports provided: environment */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "environment", function() { return environment; });
// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.
const environment = {
    production: false
};
/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.


/***/ }),

/***/ "./src/environments/version.ts":
/*!*************************************!*\
  !*** ./src/environments/version.ts ***!
  \*************************************/
/*! exports provided: VERSION */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VERSION", function() { return VERSION; });
const VERSION = {
    version: '2019.12.0',
    build: null
};


/***/ }),

/***/ "./src/main.ts":
/*!*********************!*\
  !*** ./src/main.ts ***!
  \*********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser-dynamic */ "./node_modules/@angular/platform-browser-dynamic/fesm2015/platform-browser-dynamic.js");
/* harmony import */ var _app_app_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./app/app.module */ "./src/app/app.module.ts");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./environments/environment */ "./src/environments/environment.ts");
/* harmony import */ var hammerjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! hammerjs */ "./node_modules/hammerjs/hammer.js");
/* harmony import */ var hammerjs__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(hammerjs__WEBPACK_IMPORTED_MODULE_4__);





if (_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].production) {
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["enableProdMode"])();
}
Object(_angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_1__["platformBrowserDynamic"])().bootstrapModule(_app_app_module__WEBPACK_IMPORTED_MODULE_2__["AppModule"])
    .catch(err => console.error(err));


/***/ }),

/***/ 0:
/*!***************************!*\
  !*** multi ./src/main.ts ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /home/gitlab-runner/builds/1UfBXSS6/1/fleio/fleio/ngfrontend/src/main.ts */"./src/main.ts");


/***/ })

},[[0,"runtime","vendor"]]]);
//# sourceMappingURL=main-es2015.js.map