(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["configurations-configurations-module"],{

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/configuration-create/configuration-create.component.html":
/*!*************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/configurations/configuration-create/configuration-create.component.html ***!
  \*************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-sm']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/configuration-details/configuration-details.component.html":
/*!***************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/configurations/configuration-details/configuration-details.component.html ***!
  \***************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-lg']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/configuration-edit/configuration-edit.component.html":
/*!*********************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/configurations/configuration-edit/configuration-edit.component.html ***!
  \*********************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-object-details [objectController]=\"objectController\" [additionalClasses]=\"['fl-card-fixed-sm']\">\n</app-object-details>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/configuration-list/configuration-list.component.html":
/*!*********************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/configurations/configuration-list/configuration-list.component.html ***!
  \*********************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<app-objects-view [objectsListController]=\"objectListController\"></app-objects-view>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/tabs/configuration-details-billing-form/configuration-details-billing-form.component.html":
/*!**********************************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/configurations/tabs/configuration-details-billing-form/configuration-details-billing-form.component.html ***!
  \**********************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form [formGroup]=\"configurationBillingForm\">\n  <app-form-errors #formErrors [formGroup]=\"configurationBillingForm\"></app-form-errors>\n\n  <mat-accordion>\n    <mat-expansion-panel>\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"fl-subheader full-width\">\n          Billing\n        </mat-panel-title>\n      </mat-expansion-panel-header>\n      <div fxLayout=\"row\">\n        <div fxLayout=\"column\" fxFlex=\"33\">\n          <mat-form-field>\n            <input matInput placeholder=\"Required credit for new services\" type=\"number\"\n                   formControlName=\"credit_required\" required>\n            <mat-error>{{backendErrors['credit_required'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <input matInput placeholder=\"Credit limit\" type=\"number\"\n                   formControlName=\"credit_limit\" required>\n            <mat-error>{{backendErrors['credit_limit'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <input matInput placeholder=\"Minimum up to date credit to be left after paying an invoice\" type=\"number\"\n                   formControlName=\"minim_uptodate_credit_for_invoice_payment\" required>\n            <mat-error>\n              {{backendErrors['minim_uptodate_credit_for_invoice_payment'] || 'This field is required!' }}\n            </mat-error>\n          </mat-form-field>\n        </div>\n        <div fxLayout=\"column\" fxFlex=\"66\">\n          <div class=\"fl-help-text\">\n            <h3>Required credit for new services</h3>\n            <p>Once a client has reached this limit, he will no longer be able to create or upgrade resources.</p>\n            <p>Already created cloud resources will not be suspended based on this threshold.</p>\n            <p>Positive and negative values are allowed.</p>\n          </div>\n          <div class=\"fl-help-text\">\n            <h3>Credit limit</h3>\n            <p>Based on credit limit you can configure suspension and termination rules.</p>\n            <p>Positive and negative values are allowed.</p>\n          </div>\n          <div class=\"fl-help-text\">\n            <h3>Minimum up to date credit to be left after paying an invoice</h3>\n            <p>\n              Based on this setting a user is not allowed to pay an invoice from his up to date credit (default\n              currency)\n              <br> if the remaining up to date credit after invoice payment is lower than this value.\n            </p>\n          </div>\n        </div>\n      </div>\n    </mat-expansion-panel>\n\n    <mat-expansion-panel>\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"fl-subheader full-width\">\n          Limits for clients with agreements\n        </mat-panel-title>\n      </mat-expansion-panel-header>\n      <div fxLayout=\"row\">\n        <div fxLayout=\"column\" fxFlex=\"33\">\n          <mat-form-field>\n            <input matInput placeholder=\"Required credit for new services\" type=\"number\"\n                   formControlName=\"credit_required_with_agreement\" required>\n            <mat-error>{{backendErrors['credit_required_with_agreement'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <input matInput placeholder=\"Required credit for new services\" type=\"number\"\n                   formControlName=\"credit_limit_with_agreement\" required>\n            <mat-error>{{backendErrors['credit_limit_with_agreement'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n        </div>\n        <div fxLayout=\"column\" fxFlex=\"66\">\n          <div class=\"fl-help-text\">\n            <h3>Required credit for new services when on agreement</h3>\n            <p>Once a client with a credit card on file with us has reached this limit, he will no longer be\n              able to create or upgrade resources.</p>\n            <p>Already created cloud resources will not be suspended based on this threshold.</p>\n            <p>Positive and negative values are allowed.</p>\n          </div>\n          <div class=\"fl-help-text\">\n            <h3>Required credit for new services when on agreement</h3>\n            <p>Once a client with a credit card on file with us has reached this limit, he will no longer be\n              able to create or upgrade resources.</p>\n            <p>Already created cloud resources will not be suspended based on this threshold.</p>\n            <p>Positive and negative values are allowed.</p>\n          </div>\n        </div>\n      </div>\n    </mat-expansion-panel>\n\n    <mat-expansion-panel>\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"fl-subheader full-width\">\n          Billing cycles\n        </mat-panel-title>\n      </mat-expansion-panel-header>\n      <div fxLayout=\"row\">\n        <div fxLayout=\"column\" fxFlex=\"33\">\n          <mat-checkbox formControlName=\"billing_cycle_as_calendar_month\" color=\"primary\">\n            Billing cycle as calendar month\n          </mat-checkbox>\n        </div>\n        <div fxLayout=\"column\" fxFlex=\"66\">\n          <div class=\"fl-help-text\">\n            <h3>Billing cycle as calendar month</h3>\n            <p>Consider a calendar month as billing cycle.</p>\n            <p>\n              Not checking this option will use the default: each client has his own anniversary date based on\n              the date he signed up.\n            </p>\n          </div>\n        </div>\n      </div>\n    </mat-expansion-panel>\n\n    <mat-expansion-panel>\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"fl-subheader full-width\">\n          General\n        </mat-panel-title>\n      </mat-expansion-panel-header>\n      <div fxLayout=\"row\">\n        <div fxLayout=\"column\" fxFlex=\"33\">\n          <mat-form-field>\n            <textarea matInput rows=\"3\" maxlength=\"255\"\n                      placeholder=\"Company info\" type=\"text\" formControlName=\"company_info\" required>\n            </textarea>\n            <mat-error>{{backendErrors['company_info'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <input matInput placeholder=\"Notifications sender name\" type=\"text\" formControlName=\"sender_name\">\n            <mat-error>{{backendErrors['sender_name']}}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <input matInput placeholder=\"Notifications sender email\" type=\"text\" formControlName=\"sender_email\">\n            <mat-error>{{backendErrors['sender_email']}}</mat-error>\n          </mat-form-field>\n        </div>\n        <div fxLayout=\"column\" fxFlex=\"66\">\n          <div class=\"fl-help-text\">\n            <h3>Company info</h3>\n            <p>Company information like name and other billing details.</p>\n            <p>This information is shown on invoices.</p>\n          </div>\n          <div class=\"fl-help-text\">\n            <h3>Notifications sender name</h3>\n            <p>The name to send the notifications from.</p>\n            <p>Leaving this blank will use just the <strong>Notifications sender email</strong>.</p>\n          </div>\n          <div class=\"fl-help-text\">\n            <h3>Notifications sender email</h3>\n            <p>The e-mail address the notifications are sent from.</p>\n            <p>Leaving this blank will use the Fleio DEFAULT_FROM_EMAIL setting.</p>\n          </div>\n        </div>\n      </div>\n    </mat-expansion-panel>\n\n    <mat-expansion-panel>\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"fl-subheader full-width\">\n          MaxMind fraud check\n        </mat-panel-title>\n      </mat-expansion-panel-header>\n      <div fxLayout=\"row\">\n        <div fxLayout=\"column\" fxFlex=\"33\">\n          <mat-checkbox formControlName=\"fraud_check\" color=\"primary\">\n            Enable MaxMind fraud check\n          </mat-checkbox>\n          <mat-checkbox formControlName=\"enable_maxmind_insights\" color=\"primary\">\n            Enable insights results\n          </mat-checkbox>\n          <mat-form-field>\n            <input matInput placeholder=\"Manual review score\" type=\"number\"\n                   formControlName=\"maxmind_manual_review_score\">\n            <mat-error>{{backendErrors['maxmind_manual_review_score'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <input matInput placeholder=\"Fraud score\" type=\"number\"\n                   formControlName=\"maxmind_fraud_score\">\n            <mat-error>{{backendErrors['maxmind_fraud_score'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n        </div>\n        <div fxLayout=\"column\" fxFlex=\"66\">\n          <div class=\"fl-help-text\">\n            <h3>MaxMind fraud check</h3>\n            <p>Enable or disable MaxMind fraud checking on new orders.</p>\n            <p>To completely enable this module, make sure you have the MAXMIND_CLIENTID and MAXMIND_LICENSE\n              options set in settings.py</p>\n            <p>The score for manual review can be set or when an order is automatically marked as fraud.</p>\n          </div>\n        </div>\n      </div>\n    </mat-expansion-panel>\n\n    <mat-expansion-panel>\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"fl-subheader full-width\">\n          Client signup automation\n        </mat-panel-title>\n      </mat-expansion-panel-header>\n      <div fxLayout=\"row\">\n        <div fxLayout=\"column\" fxFlex=\"33\">\n          <mat-checkbox formControlName=\"auto_create_order\" color=\"primary\">\n            Auto create new order on signup\n          </mat-checkbox>\n          <mat-form-field>\n            <mat-select formControlName=\"auto_order_service\" placeholder=\"Auto order service\">\n              <mat-option *ngFor=\"let product of billingConfiguration.products\"\n                          [value]=\"product.id\">\n                {{product.name}}\n              </mat-option>\n            </mat-select>\n            <mat-error>{{backendErrors['auto_order_service'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <mat-select formControlName=\"auto_order_service_cycle\" placeholder=\"Auto order service cycle\">\n              <ng-container *ngIf=\"autoOrderProduct\">\n                <mat-option *ngFor=\"let cycle of autoOrderProduct.cycles\"\n                            [value]=\"cycle.id\">\n                  {{cycle.display_name}}\n                </mat-option>\n              </ng-container>\n            </mat-select>\n            <mat-error>{{backendErrors['auto_order_service_cycle'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <textarea matInput rows=\"3\" maxlength=\"255\"\n                      placeholder=\"Auto order parameters as JSON\"\n                      type=\"text\" formControlName=\"auto_order_service_params\">\n            </textarea>\n            <mat-error>{{backendErrors['auto_order_service_params'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <input matInput placeholder=\"Client initial credit (default currency)\" type=\"number\"\n                   formControlName=\"client_initial_credit\">\n            <mat-error>{{backendErrors['client_initial_credit'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n        </div>\n        <div fxLayout=\"column\" fxFlex=\"66\">\n          <div class=\"fl-help-text\">\n            <h3>Client signup automation</h3>\n            <p>Define what happens after a client is created from staff or signs up.</p>\n            <p>Fraud checking will be performed on signup if the option is enabled.</p>\n            <p>When a new Client signs up, an order will be automatically created for him.</p>\n            <p>Additional parameters can be set as JSON to be sent to the service module on creation.</p>\n            <p>\n              Use \"Client initial credit (default currency)\" if you wish to have newly created clients\n              have a starting credit of the amount you define (if client has another currency than default one,\n              the amount is converted).\n            </p>\n          </div>\n        </div>\n      </div>\n    </mat-expansion-panel>\n\n    <mat-expansion-panel>\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"fl-subheader full-width\">\n          Invoicing\n        </mat-panel-title>\n      </mat-expansion-panel-header>\n      <div fxLayout=\"row\">\n        <div fxLayout=\"column\" fxFlex=\"33\">\n          <mat-checkbox formControlName=\"generate_invoices\" color=\"primary\">\n            Generate invoices\n          </mat-checkbox>\n          <mat-checkbox formControlName=\"send_notifications_for_unpaid_invoices\" color=\"primary\">\n            Notify on unpaid invoices\n          </mat-checkbox>\n          <mat-checkbox formControlName=\"create_todo_on_invoice_payment\" color=\"primary\">\n            Create TODO on invoice payment\n          </mat-checkbox>\n          <mat-checkbox formControlName=\"auto_settle_usage\" color=\"primary\">\n            Enable automatic settlements\n          </mat-checkbox>\n          <mat-checkbox formControlName=\"auto_pay_invoice_only_when_enough_credit\" color=\"primary\">\n            Auto pay invoice only when enough credit\n          </mat-checkbox>\n          <div class=\"fl-radio-group\">\n            <mat-label>Invoicing options</mat-label>\n            <mat-radio-group formControlName=\"invoicing_option\">\n              <mat-radio-button class=\"full-width\" value=\"fiscal_on_paid\" color=\"primary\">\n                Issue proforma invoices and make them fiscal when paid\n              </mat-radio-button>\n              <mat-radio-button class=\"full-width\" value=\"always_fiscal\" color=\"primary\">\n                Always issue fiscal invoices with sequential numbers\n              </mat-radio-button>\n              <mat-radio-button class=\"full-width\" value=\"only_proforma\" color=\"primary\">\n                Use only proforma invoices with random numbers\n              </mat-radio-button>\n            </mat-radio-group>\n          </div>\n          <mat-form-field>\n            <input matInput placeholder=\"Next fiscal invoice number\" type=\"number\"\n                   formControlName=\"next_paid_invoice_number\" required>\n            <mat-error>{{backendErrors['next_paid_invoice_number'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <input matInput placeholder=\"Next fiscal invoice number format\" type=\"text\"\n                   formControlName=\"next_paid_invoice_number_format\" required>\n            <mat-error>{{backendErrors['next_paid_invoice_number_format']}}</mat-error>\n          </mat-form-field>\n          <mat-checkbox formControlName=\"limit_billable_seconds_per_month\" color=\"primary\">\n            Limit billable seconds per month\n          </mat-checkbox>\n          <mat-form-field>\n            <input matInput placeholder=\"Billable seconds per month\" type=\"number\"\n                   formControlName=\"billable_seconds_per_month\" required>\n            <mat-error>{{backendErrors['billable_seconds_per_month'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-checkbox formControlName=\"issue_invoice_before_next_due_date\" color=\"primary\">\n            Issue invoice before service due date\n          </mat-checkbox>\n          <mat-form-field>\n            <input matInput placeholder=\"Next invoice date offset\" type=\"number\"\n                   formControlName=\"next_invoice_date_offset\" required>\n            <mat-error>{{backendErrors['next_invoice_date_offset'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-checkbox formControlName=\"auto_eu_tax_exemption\" color=\"primary\">\n            Auto set tax exemption for EU customers\n          </mat-checkbox>\n        </div>\n        <div fxLayout=\"column\" fxFlex=\"66\">\n          <div class=\"fl-help-text\">\n            <h3>Generate invoice</h3>\n            <p>An invoice will be generated for used services</p>\n            <h3>Notify on unpaid invoices</h3>\n            <p>\n              If an invoice is generated and it not automatically settled an notification containing invoice\n              details will be sent to the customer.\n            </p>\n            <h3>Create TODO on invoice payment</h3>\n            <p>\n              If an user manually pays an invoice a TODO will be created to make staff users aware of the payment.\n            </p>\n            <h3>Enable automatic settlements</h3>\n            <p>\n              Existing usage will be automatically settled using client credit. If an invoice exists it will\n              be paid using client credit.\n            </p>\n            <h3>Auto pay invoice only when enough credit</h3>\n            <p>\n              If automatic settlements are enabled the invoices will be paid only if after paying the invoice\n              the uptodate credit will be greater or equal than minimum up to date credit to be left after paying an\n              invoice setting.\n            </p>\n            <h3>Invoicing</h3>\n            <ul style=\"padding-left: 20px;\">\n              <li>\n                Issue proforma invoices and make them fiscal when paid. The fiscal invoice date will be set\n                to the date when the invoice becomes paid.\n              </li>\n              <li>\n                Always issue fiscal invoices with sequential numbers - choose when you want all issued\n                invoices to have consecutive numbers and it does not bother you that all invoices will be issued as\n                fiscal,\n                even if not paid. The fiscal invoice date will be the same as the invoice issue date.\n              </li>\n              <li>\n                Use only proforma invoices with random numbers - you can choose this when your fiscal rules\n                do not require invoices with sequential numbers.\n              </li>\n            </ul>\n            <p>Enable sequential numbering for paid invoices.</p>\n            <h3>Next fiscal invoice number</h3>\n            <p>The next number that will be allocated for a paid invoice.</p>\n            <p>This option only takes effect if sequential invoice numbering is enabled.</p>\n            <h3>Next fiscal invoice number format</h3>\n            <p>Customize the next invoice number by using\n              <span ngNonBindable>{{ number }}, {{ year }}, {{ month }}, {{ day }}.</span>\n            </p>\n            <h3>Limit billable seconds per month</h3>\n            <p>\n              Specifies the number of seconds per month that should be billed for clients.\n              The remaining seconds after this limit is reached will not be billed.\n            </p>\n            <h3>Issue invoice before next due date</h3>\n            <p>Allows issuing invoices a specified number of days before service due date.</p>\n            <h3>Auto set tax exemption for EU customers</h3>\n            <p>\n              With this option enabled, an European Union Client will be marked as non taxable if he has a\n              valid EU vat ID.\n            </p>\n          </div>\n        </div>\n      </div>\n    </mat-expansion-panel>\n\n    <mat-expansion-panel>\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"fl-subheader full-width\">\n          Credit notifications\n        </mat-panel-title>\n      </mat-expansion-panel-header>\n      <div fxLayout=\"row\">\n        <div fxLayout=\"column\" fxFlex=\"33\">\n          <mat-checkbox formControlName=\"credit_notifications_enabled\" color=\"primary\">\n            Enable credit notifications\n          </mat-checkbox>\n          <mat-checkbox formControlName=\"credit_notifications_when_agreement_enabled\" color=\"primary\">\n            Send notifications to customers having billing agreements\n          </mat-checkbox>\n          <div fxLayout=\"row\">\n            <mat-form-field fxFlex=\"33\">\n              <input matInput placeholder=\"Hours remaining\" type=\"number\"\n                     formControlName=\"first_credit_remaining_hours\" required>\n              <mat-error>{{backendErrors['first_credit_remaining_hours'] || 'This field is required!' }}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"66\">\n              <mat-select formControlName=\"first_credit_notification_template\" placeholder=\"Notification template\">\n                <mat-option *ngFor=\"let notification of billingConfiguration.notification_templates\"\n                            [value]=\"notification[0]\">\n                  {{notification[0]}}\n                </mat-option>\n              </mat-select>\n            </mat-form-field>\n          </div>\n          <div fxLayout=\"row\">\n            <mat-form-field fxFlex=\"33\">\n              <input matInput placeholder=\"Hours remaining\" type=\"number\"\n                     formControlName=\"second_credit_remaining_hours\" required>\n              <mat-error>{{backendErrors['second_credit_remaining_hours'] || 'This field is required!' }}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"66\">\n              <mat-select formControlName=\"second_credit_notification_template\" placeholder=\"Notification template\">\n                <mat-option *ngFor=\"let notification of billingConfiguration.notification_templates\"\n                            [value]=\"notification[0]\">\n                  {{notification[0]}}\n                </mat-option>\n              </mat-select>\n            </mat-form-field>\n          </div>\n          <div fxLayout=\"row\">\n            <mat-form-field fxFlex=\"33\">\n              <input matInput placeholder=\"Hours remaining\" type=\"number\"\n                     formControlName=\"third_credit_remaining_hours\" required>\n              <mat-error>{{backendErrors['third_credit_remaining_hours'] || 'This field is required!' }}</mat-error>\n            </mat-form-field>\n            <mat-form-field fxFlex=\"66\">\n              <mat-select formControlName=\"third_credit_notification_template\" placeholder=\"Notification template\">\n                <mat-option *ngFor=\"let notification of billingConfiguration.notification_templates\"\n                            [value]=\"notification[0]\">\n                  {{notification[0]}}\n                </mat-option>\n              </mat-select>\n            </mat-form-field>\n          </div>\n        </div>\n        <div fxLayout=\"column\" fxFlex=\"66\">\n          <div class=\"fl-help-text\">\n            <h3>Enable credit notification</h3>\n            <p>Send notifications when a client's remaining hours with his current credit is reached</p>\n          </div>\n          <div class=\"fl-help-text\">\n            <h3 translate=\"\">Send notifications to customers having billing agreements</h3>\n            <p translate=\"\">Send notifications when a client has a billing agreement enabled</p>\n          </div>\n          <div class=\"fl-help-text\">\n            <h3 translate=\"\">Hours remaining &amp; notification template</h3>\n            <p translate=\"\">How many hours until the client reaches the credit limit with his current usage.\n              Select a notification template to send. Selecting the blank notification will disable it.</p>\n          </div>\n        </div>\n      </div>\n    </mat-expansion-panel>\n\n    <mat-expansion-panel>\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"fl-subheader full-width\">\n          Suspension\n        </mat-panel-title>\n      </mat-expansion-panel-header>\n      <div fxLayout=\"row\">\n        <div fxLayout=\"column\" fxFlex=\"33\">\n          <mat-checkbox formControlName=\"auto_suspend\" color=\"primary\">\n            Enable automatic suspension\n          </mat-checkbox>\n          <mat-checkbox formControlName=\"auto_suspend_delay_hours_enabled\" color=\"primary\">\n            Enable delay by hours\n          </mat-checkbox>\n          <mat-form-field>\n            <input matInput placeholder=\"Delay(hours)\" type=\"number\"\n                   formControlName=\"auto_suspend_delay_hours\" required>\n            <mat-error>{{backendErrors['auto_suspend_delay_hours'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-checkbox formControlName=\"auto_suspend_delay_credit_enabled\" color=\"primary\">\n            Enable delay until credit is used\n          </mat-checkbox>\n          <mat-form-field>\n            <input matInput placeholder=\"Delay(credit)\" type=\"number\"\n                   formControlName=\"auto_suspend_delay_credit\" required>\n            <mat-error>{{backendErrors['auto_suspend_delay_credit'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <mat-select formControlName=\"auto_suspend_notification_template\" placeholder=\"Notification template\">\n              <mat-option *ngFor=\"let notification of billingConfiguration.notification_templates\"\n                          [value]=\"notification[0]\">\n                {{notification[0]}}\n              </mat-option>\n            </mat-select>\n          </mat-form-field>\n        </div>\n        <div fxLayout=\"column\" fxFlex=\"66\">\n          <div class=\"fl-help-text\">\n            <h3>Enable automatic suspension</h3>\n            <p>Automatically suspend a client when he reaches the credit limit.</p>\n            <p>The actual suspension can be postponed by a few hours when <strong>Delay by hours</strong>\n              is checked or until client is under the credit limit by a specified amount when\n              <strong>Delay until credit is used</strong> is checked.</p>\n            <p>Selecting a <strong>Notification template</strong> will send a notification to the\n              client on suspension.</p>\n          </div>\n        </div>\n      </div>\n    </mat-expansion-panel>\n\n    <mat-expansion-panel>\n      <mat-expansion-panel-header>\n        <mat-panel-title class=\"fl-subheader full-width\">\n          Termination\n        </mat-panel-title>\n      </mat-expansion-panel-header>\n      <div fxLayout=\"row\">\n        <div fxLayout=\"column\" fxFlex=\"33\">\n          <mat-checkbox formControlName=\"suspend_instead_of_terminate\" color=\"primary\">\n            Suspend the client instead of termination\n          </mat-checkbox>\n          <p *ngIf=\"!configurationBillingForm.controls.suspend_instead_of_terminate.value\" class=\"fl-important-text\">\n            Un-checking suspend instead of terminate allows clients and service termination and may cause accidental\n            data loss. However, you can remove permissions for service/client deletion on authorization page and this\n            will prevent accidental data loss.\n          </p>\n          <mat-checkbox formControlName=\"auto_terminate\" color=\"primary\">\n            Enable automatic termination\n          </mat-checkbox>\n          <mat-form-field>\n            <input matInput placeholder=\"Delay(hours)\" type=\"number\"\n                   formControlName=\"auto_terminate_delay_hours\" required>\n            <mat-error>{{backendErrors['auto_terminate_delay_hours'] || 'This field is required!' }}</mat-error>\n          </mat-form-field>\n          <mat-form-field>\n            <mat-select formControlName=\"auto_terminate_notification_template\" placeholder=\"Notification template\">\n              <mat-option *ngFor=\"let notification of billingConfiguration.notification_templates\"\n                          [value]=\"notification[0]\">\n                {{notification[0]}}\n              </mat-option>\n            </mat-select>\n          </mat-form-field>\n        </div>\n        <div fxLayout=\"column\" fxFlex=\"66\">\n          <div class=\"fl-help-text\">\n            <h3>Enable automatic termination</h3>\n            <p>Automatically terminates a service after certain time (defined in delay field) passed\n              since service suspension.</p>\n            <p>A <strong>Delay</strong> for service termination can be set (in hours) to postpone the actual\n              termination after service was suspended.</p>\n            <p>The client can be notified about the termination if a <strong>Notification template</strong> is\n              selected.</p>\n          </div>\n        </div>\n      </div>\n    </mat-expansion-panel>\n  </mat-accordion>\n\n</form>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/tabs/configuration-edit-form/configuration-edit-form.component.html":
/*!************************************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/reseller/settings/configurations/tabs/configuration-edit-form/configuration-edit-form.component.html ***!
  \************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div [formGroup]=\"configurationForm\" fxLayout=\"column\">\n  <app-form-errors #formErrors [formGroup]=\"configurationForm\"></app-form-errors>\n  <mat-form-field>\n    <input matInput placeholder=\"Name\" type=\"text\" formControlName=\"name\" required>\n    <mat-error>{{backendErrors['name'] || 'This field is required!' }}</mat-error>\n  </mat-form-field>\n  <mat-form-field>\n    <input matInput placeholder=\"Description\" type=\"text\" formControlName=\"description\">\n    <mat-error>{{backendErrors['description']}}</mat-error>\n  </mat-form-field>\n  <mat-checkbox formControlName=\"is_default\" [color]=\"'primary'\">Is default</mat-checkbox>\n</div>\n"

/***/ }),

/***/ "./src/app/reseller/settings/configurations/configuration-create/configuration-create.component.scss":
/*!***********************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configuration-create/configuration-create.component.scss ***!
  \***********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2NvbmZpZ3VyYXRpb25zL2NvbmZpZ3VyYXRpb24tY3JlYXRlL2NvbmZpZ3VyYXRpb24tY3JlYXRlLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/settings/configurations/configuration-create/configuration-create.component.ts":
/*!*********************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configuration-create/configuration-create.component.ts ***!
  \*********************************************************************************************************/
/*! exports provided: ConfigurationCreateComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationCreateComponent", function() { return ConfigurationCreateComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _configuration_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../configuration-list-ui.service */ "./src/app/reseller/settings/configurations/configuration-list-ui.service.ts");





var ConfigurationCreateComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ConfigurationCreateComponent, _super);
    function ConfigurationCreateComponent(activatedRoute, configurationListUIService) {
        var _this = _super.call(this, activatedRoute, configurationListUIService, 'create', null) || this;
        _this.activatedRoute = activatedRoute;
        _this.configurationListUIService = configurationListUIService;
        return _this;
    }
    ConfigurationCreateComponent.prototype.ngOnInit = function () {
        _super.prototype.ngOnInit.call(this);
    };
    ConfigurationCreateComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _configuration_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ConfigurationListUIService"] }
    ]; };
    ConfigurationCreateComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-configuration-create',
            template: __webpack_require__(/*! raw-loader!./configuration-create.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/configuration-create/configuration-create.component.html"),
            styles: [__webpack_require__(/*! ./configuration-create.component.scss */ "./src/app/reseller/settings/configurations/configuration-create/configuration-create.component.scss")]
        })
    ], ConfigurationCreateComponent);
    return ConfigurationCreateComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



/***/ }),

/***/ "./src/app/reseller/settings/configurations/configuration-details/configuration-details.component.scss":
/*!*************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configuration-details/configuration-details.component.scss ***!
  \*************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2NvbmZpZ3VyYXRpb25zL2NvbmZpZ3VyYXRpb24tZGV0YWlscy9jb25maWd1cmF0aW9uLWRldGFpbHMuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/settings/configurations/configuration-details/configuration-details.component.ts":
/*!***********************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configuration-details/configuration-details.component.ts ***!
  \***********************************************************************************************************/
/*! exports provided: ConfigurationDetailsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationDetailsComponent", function() { return ConfigurationDetailsComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _configuration_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../configuration-list-ui.service */ "./src/app/reseller/settings/configurations/configuration-list-ui.service.ts");





var ConfigurationDetailsComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ConfigurationDetailsComponent, _super);
    function ConfigurationDetailsComponent(route, configurationListUIService) {
        return _super.call(this, route, configurationListUIService, 'details', 'configuration', ['billingConfiguration']) || this;
    }
    ConfigurationDetailsComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _configuration_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ConfigurationListUIService"] }
    ]; };
    ConfigurationDetailsComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-configuration-details',
            template: __webpack_require__(/*! raw-loader!./configuration-details.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/configuration-details/configuration-details.component.html"),
            styles: [__webpack_require__(/*! ./configuration-details.component.scss */ "./src/app/reseller/settings/configurations/configuration-details/configuration-details.component.scss")]
        })
    ], ConfigurationDetailsComponent);
    return ConfigurationDetailsComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



/***/ }),

/***/ "./src/app/reseller/settings/configurations/configuration-edit/configuration-edit.component.scss":
/*!*******************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configuration-edit/configuration-edit.component.scss ***!
  \*******************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2NvbmZpZ3VyYXRpb25zL2NvbmZpZ3VyYXRpb24tZWRpdC9jb25maWd1cmF0aW9uLWVkaXQuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/settings/configurations/configuration-edit/configuration-edit.component.ts":
/*!*****************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configuration-edit/configuration-edit.component.ts ***!
  \*****************************************************************************************************/
/*! exports provided: ConfigurationEditComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationEditComponent", function() { return ConfigurationEditComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/details-base */ "./src/app/shared/ui/objects-view/details-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _configuration_list_ui_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../configuration-list-ui.service */ "./src/app/reseller/settings/configurations/configuration-list-ui.service.ts");





var ConfigurationEditComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ConfigurationEditComponent, _super);
    function ConfigurationEditComponent(route, configurationListUIService) {
        return _super.call(this, route, configurationListUIService, 'edit', 'configuration') || this;
    }
    ConfigurationEditComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _configuration_list_ui_service__WEBPACK_IMPORTED_MODULE_4__["ConfigurationListUIService"] }
    ]; };
    ConfigurationEditComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-configuration-edit',
            template: __webpack_require__(/*! raw-loader!./configuration-edit.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/configuration-edit/configuration-edit.component.html"),
            styles: [__webpack_require__(/*! ./configuration-edit.component.scss */ "./src/app/reseller/settings/configurations/configuration-edit/configuration-edit.component.scss")]
        })
    ], ConfigurationEditComponent);
    return ConfigurationEditComponent;
}(_shared_ui_objects_view_details_base__WEBPACK_IMPORTED_MODULE_2__["DetailsBase"]));



/***/ }),

/***/ "./src/app/reseller/settings/configurations/configuration-list-ui.service.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configuration-list-ui.service.ts ***!
  \***********************************************************************************/
/*! exports provided: ConfigurationListUIService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationListUIService", function() { return ConfigurationListUIService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/ui/objects-view/interfaces/table-data/column-definition */ "./src/app/shared/ui/objects-view/interfaces/table-data/column-definition.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _shared_fleio_api_configurations_configurations_api_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../shared/fleio-api/configurations/configurations-api.service */ "./src/app/shared/fleio-api/configurations/configurations-api.service.ts");
/* harmony import */ var _configuration_ui_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./configuration-ui.service */ "./src/app/reseller/settings/configurations/configuration-ui.service.ts");








var ConfigurationListUIService = /** @class */ (function () {
    function ConfigurationListUIService(router, config, configurationsApiService) {
        this.router = router;
        this.config = config;
        this.configurationsApiService = configurationsApiService;
    }
    ConfigurationListUIService.prototype.getObjectUIService = function (object, permissions, state) {
        return new _configuration_ui_service__WEBPACK_IMPORTED_MODULE_7__["ConfigurationUiService"](object, permissions, state, this.router, this.config, this.configurationsApiService);
    };
    ConfigurationListUIService.prototype.getTableData = function (objectList) {
        var e_1, _a;
        var tableData = {
            header: {
                columns: [
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Name', enableSort: true, fieldName: 'name' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Labels', enableSort: false, fieldName: 'tags' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Value, displayName: 'Description', enableSort: false, fieldName: 'description' },
                    { type: _shared_ui_objects_view_interfaces_table_data_column_definition__WEBPACK_IMPORTED_MODULE_4__["ColumnType"].Actions, displayName: 'Actions', enableSort: false, fieldName: '(actions)' },
                ],
                columnNames: ['name', 'tags', 'description', '(actions)'],
                statusColumn: 'name'
            },
            rows: [],
        };
        try {
            for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](objectList.objects), _c = _b.next(); !_c.done; _c = _b.next()) {
                var configuration = _c.value;
                var rowUIService = this.getObjectUIService(configuration, objectList.permissions, 'table-view');
                var row = {
                    cells: {
                        name: { text: configuration.name },
                        tags: { tags: rowUIService.getCardTags() },
                        description: { text: configuration.description },
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
    ConfigurationListUIService.prototype.getActions = function (objectList) {
        return [
            new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_5__["RouterLinkAction"]({
                name: 'Create new configuration',
                tooltip: 'Create new configuration',
                icon: { name: 'add' },
                router: this.router,
                routerUrl: this.config.getPanelUrl('settings/configurations/create')
            })
        ];
    };
    ConfigurationListUIService.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_3__["ConfigService"] },
        { type: _shared_fleio_api_configurations_configurations_api_service__WEBPACK_IMPORTED_MODULE_6__["ConfigurationsApiService"] }
    ]; };
    ConfigurationListUIService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ConfigurationListUIService);
    return ConfigurationListUIService;
}());



/***/ }),

/***/ "./src/app/reseller/settings/configurations/configuration-list/configuration-list.component.scss":
/*!*******************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configuration-list/configuration-list.component.scss ***!
  \*******************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2NvbmZpZ3VyYXRpb25zL2NvbmZpZ3VyYXRpb24tbGlzdC9jb25maWd1cmF0aW9uLWxpc3QuY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/settings/configurations/configuration-list/configuration-list.component.ts":
/*!*****************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configuration-list/configuration-list.component.ts ***!
  \*****************************************************************************************************/
/*! exports provided: ConfigurationListComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationListComponent", function() { return ConfigurationListComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../shared/ui/objects-view/list-base */ "./src/app/shared/ui/objects-view/list-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../shared/ui-api/refresh.service */ "./src/app/shared/ui-api/refresh.service.ts");
/* harmony import */ var _configuration_list_ui_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../configuration-list-ui.service */ "./src/app/reseller/settings/configurations/configuration-list-ui.service.ts");






var ConfigurationListComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ConfigurationListComponent, _super);
    function ConfigurationListComponent(route, configurationListUIService, refreshService) {
        var _this = _super.call(this, route, configurationListUIService, refreshService, 'configurations') || this;
        _this.route = route;
        _this.configurationListUIService = configurationListUIService;
        _this.refreshService = refreshService;
        return _this;
    }
    ConfigurationListComponent.prototype.ngOnInit = function () {
        _super.prototype.ngOnInit.call(this);
    };
    ConfigurationListComponent.ctorParameters = function () { return [
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["ActivatedRoute"] },
        { type: _configuration_list_ui_service__WEBPACK_IMPORTED_MODULE_5__["ConfigurationListUIService"] },
        { type: _shared_ui_api_refresh_service__WEBPACK_IMPORTED_MODULE_4__["RefreshService"] }
    ]; };
    ConfigurationListComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-configuration-list',
            template: __webpack_require__(/*! raw-loader!./configuration-list.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/configuration-list/configuration-list.component.html"),
            styles: [__webpack_require__(/*! ./configuration-list.component.scss */ "./src/app/reseller/settings/configurations/configuration-list/configuration-list.component.scss")]
        })
    ], ConfigurationListComponent);
    return ConfigurationListComponent;
}(_shared_ui_objects_view_list_base__WEBPACK_IMPORTED_MODULE_2__["ListBase"]));



/***/ }),

/***/ "./src/app/reseller/settings/configurations/configuration-ui.service.ts":
/*!******************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configuration-ui.service.ts ***!
  \******************************************************************************/
/*! exports provided: ConfigurationUiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationUiService", function() { return ConfigurationUiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../shared/ui/objects-view/object-ui-service-base */ "./src/app/shared/ui/objects-view/object-ui-service-base.ts");
/* harmony import */ var _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/router-link-action */ "./src/app/shared/ui/objects-view/actions/router-link-action.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/api-call-action */ "./src/app/shared/ui/objects-view/actions/api-call-action.ts");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/ui/objects-view/actions/callback-action */ "./src/app/shared/ui/objects-view/actions/callback-action.ts");
/* harmony import */ var _shared_fleio_api_configurations_configurations_api_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/configurations/configurations-api.service */ "./src/app/shared/fleio-api/configurations/configurations-api.service.ts");
/* harmony import */ var _tabs_configuration_edit_form_configuration_edit_form_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tabs/configuration-edit-form/configuration-edit-form.component */ "./src/app/reseller/settings/configurations/tabs/configuration-edit-form/configuration-edit-form.component.ts");
/* harmony import */ var _tabs_configuration_details_billing_form_configuration_details_billing_form_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs/configuration-details-billing-form/configuration-details-billing-form.component */ "./src/app/reseller/settings/configurations/tabs/configuration-details-billing-form/configuration-details-billing-form.component.ts");











var ConfigurationUiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ConfigurationUiService, _super);
    function ConfigurationUiService(configuration, permissions, state, router, config, configurationsApiService) {
        var _this = _super.call(this, configuration, permissions, state) || this;
        _this.router = router;
        _this.config = config;
        _this.configurationsApiService = configurationsApiService;
        _this.datePipe = new _angular_common__WEBPACK_IMPORTED_MODULE_6__["DatePipe"](_this.config.locale);
        return _this;
    }
    ConfigurationUiService.prototype.getIcon = function () {
        return null;
    };
    ConfigurationUiService.prototype.getStatus = function () {
        return null;
    };
    ConfigurationUiService.prototype.getTitle = function () {
        switch (this.state) {
            case 'details':
                return {
                    text: "Configuration " + this.object.name,
                    subText: this.object.client_count + " clients on this configuration",
                };
            case 'edit':
                return {
                    text: "Edit " + this.object.name,
                };
            case 'create':
                return {
                    text: "Create new configuration",
                };
            default:
                return {
                    text: "" + this.object.name,
                    subText: this.object.client_count + " clients on this configuration",
                };
        }
    };
    ConfigurationUiService.prototype.getActions = function () {
        var actions = [];
        actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
            icon: { name: 'edit', class: 'fl-icons' },
            name: 'Edit',
            tooltip: 'Edit configuration',
            routerUrl: this.config.getPanelUrl("settings/configurations/" + this.object.id + "/edit"),
            router: this.router,
        }));
        var deleteAction = new _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["ApiCallAction"]({
            object: this.object,
            icon: { name: 'delete' },
            tooltip: 'Delete configuration',
            name: 'Delete',
            confirmOptions: {
                confirm: true,
                title: 'Delete configuration',
                message: "Are you sure you want to delete configuration " + this.object.name,
            },
            apiService: this.configurationsApiService,
            callType: _shared_ui_objects_view_actions_api_call_action__WEBPACK_IMPORTED_MODULE_5__["CallType"].Delete,
        });
        if (this.object.is_default) {
            deleteAction.noPermissions = true;
            deleteAction.tooltip = 'Default configuration cannot be deleted';
        }
        actions.push(deleteAction);
        return actions;
    };
    ConfigurationUiService.prototype.getDetailsActions = function () {
        var actions = [];
        switch (this.state) {
            case 'create':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("settings/configurations"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Create' }));
                break;
            case 'edit':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Cancel',
                    routerUrl: this.config.getPrevUrl("settings/configurations"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Save' }));
                break;
            case 'details':
                actions.push(new _shared_ui_objects_view_actions_router_link_action__WEBPACK_IMPORTED_MODULE_2__["RouterLinkAction"]({
                    name: 'Back',
                    routerUrl: this.config.getPrevUrl("settings/configurations"),
                    router: this.router,
                }));
                actions.push(new _shared_ui_objects_view_actions_callback_action__WEBPACK_IMPORTED_MODULE_7__["CallbackAction"]({ name: 'Save' }));
                break;
            default:
                break;
        }
        return actions;
    };
    ConfigurationUiService.prototype.getDetailsLink = function () {
        return this.config.getPanelUrl("settings/configurations/" + this.object.id);
    };
    ConfigurationUiService.prototype.getCardFields = function () {
        var fields = [
            {
                value: this.object.description ? this.object.description : 'No description',
            },
        ];
        return fields;
    };
    ConfigurationUiService.prototype.getTabs = function () {
        switch (this.state) {
            case 'details':
                return [
                    {
                        tabName: 'Billing',
                        component: _tabs_configuration_details_billing_form_configuration_details_billing_form_component__WEBPACK_IMPORTED_MODULE_10__["ConfigurationDetailsBillingFormComponent"],
                    },
                ];
            case 'create':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_configuration_edit_form_configuration_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["ConfigurationEditFormComponent"],
                    },
                ];
            case 'edit':
                return [
                    {
                        tabName: 'Create',
                        component: _tabs_configuration_edit_form_configuration_edit_form_component__WEBPACK_IMPORTED_MODULE_9__["ConfigurationEditFormComponent"],
                    },
                ];
        }
    };
    ConfigurationUiService.prototype.getCardTags = function () {
        var tags = [];
        if (this.object.is_default) {
            tags.push('default');
        }
        return tags;
    };
    ConfigurationUiService.ctorParameters = function () { return [
        { type: undefined },
        { type: undefined },
        { type: String },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_3__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_4__["ConfigService"] },
        { type: _shared_fleio_api_configurations_configurations_api_service__WEBPACK_IMPORTED_MODULE_8__["ConfigurationsApiService"] }
    ]; };
    return ConfigurationUiService;
}(_shared_ui_objects_view_object_ui_service_base__WEBPACK_IMPORTED_MODULE_1__["ObjectUIServiceBase"]));



/***/ }),

/***/ "./src/app/reseller/settings/configurations/configurations-routing.module.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configurations-routing.module.ts ***!
  \***********************************************************************************/
/*! exports provided: ConfigurationsRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationsRoutingModule", function() { return ConfigurationsRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _configuration_list_configuration_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./configuration-list/configuration-list.component */ "./src/app/reseller/settings/configurations/configuration-list/configuration-list.component.ts");
/* harmony import */ var _shared_fleio_api_configurations_configuration_list_resolver__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../shared/fleio-api/configurations/configuration-list.resolver */ "./src/app/shared/fleio-api/configurations/configuration-list.resolver.ts");
/* harmony import */ var _configuration_create_configuration_create_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./configuration-create/configuration-create.component */ "./src/app/reseller/settings/configurations/configuration-create/configuration-create.component.ts");
/* harmony import */ var _configuration_details_configuration_details_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./configuration-details/configuration-details.component */ "./src/app/reseller/settings/configurations/configuration-details/configuration-details.component.ts");
/* harmony import */ var _shared_fleio_api_configurations_configuration_resolver__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../shared/fleio-api/configurations/configuration.resolver */ "./src/app/shared/fleio-api/configurations/configuration.resolver.ts");
/* harmony import */ var _shared_fleio_api_configurations_configuration_billing_resolver__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../../shared/fleio-api/configurations/configuration-billing.resolver */ "./src/app/shared/fleio-api/configurations/configuration-billing.resolver.ts");
/* harmony import */ var _configuration_edit_configuration_edit_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./configuration-edit/configuration-edit.component */ "./src/app/reseller/settings/configurations/configuration-edit/configuration-edit.component.ts");
/* harmony import */ var _shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/auth/auth.guard */ "./src/app/shared/auth/auth.guard.ts");
/* harmony import */ var _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/ui-api/interfaces/route-config/ordering-directions */ "./src/app/shared/ui-api/interfaces/route-config/ordering-directions.ts");












var routes = [
    {
        path: '',
        component: _configuration_list_configuration_list_component__WEBPACK_IMPORTED_MODULE_3__["ConfigurationListComponent"],
        resolve: {
            configurations: _shared_fleio_api_configurations_configuration_list_resolver__WEBPACK_IMPORTED_MODULE_4__["ConfigurationListResolver"],
        },
        canActivate: [_shared_auth_auth_guard__WEBPACK_IMPORTED_MODULE_10__["AuthGuard"]],
        data: {
            config: {
                feature: 'settings.configurations',
                search: {
                    show: true,
                    placeholder: 'Search configurations ...',
                },
                subheader: {
                    objectList: function (data) {
                        return data.configurations;
                    },
                    objectName: 'configuration',
                    objectNamePlural: 'configurations',
                },
                ordering: {
                    default: {
                        display: 'Name',
                        field: 'name',
                        direction: _shared_ui_api_interfaces_route_config_ordering_directions__WEBPACK_IMPORTED_MODULE_11__["OrderingDirection"].Ascending,
                    },
                    options: [
                        {
                            display: 'Name',
                            field: 'name',
                        }
                    ]
                }
            },
        },
        runGuardsAndResolvers: 'always'
    },
    {
        path: 'create',
        component: _configuration_create_configuration_create_component__WEBPACK_IMPORTED_MODULE_5__["ConfigurationCreateComponent"],
        resolve: {},
        data: {
            config: {
                getBreadCrumbDetail: function () {
                    return 'Create configuration';
                },
            },
        }
    },
    {
        path: ':id',
        component: _configuration_details_configuration_details_component__WEBPACK_IMPORTED_MODULE_6__["ConfigurationDetailsComponent"],
        resolve: {
            configuration: _shared_fleio_api_configurations_configuration_resolver__WEBPACK_IMPORTED_MODULE_7__["ConfigurationResolver"],
            billingConfiguration: _shared_fleio_api_configurations_configuration_billing_resolver__WEBPACK_IMPORTED_MODULE_8__["ConfigurationBillingResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: function (data) {
                    return data.configuration.name;
                },
            },
        }
    },
    {
        path: ':id/edit',
        component: _configuration_edit_configuration_edit_component__WEBPACK_IMPORTED_MODULE_9__["ConfigurationEditComponent"],
        resolve: {
            configuration: _shared_fleio_api_configurations_configuration_resolver__WEBPACK_IMPORTED_MODULE_7__["ConfigurationResolver"],
        },
        data: {
            config: {
                getBreadCrumbDetail: function (data) {
                    return "Edit configuration " + data.configuration.name;
                },
            },
        }
    },
];
var ConfigurationsRoutingModule = /** @class */ (function () {
    function ConfigurationsRoutingModule() {
    }
    ConfigurationsRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
        })
    ], ConfigurationsRoutingModule);
    return ConfigurationsRoutingModule;
}());



/***/ }),

/***/ "./src/app/reseller/settings/configurations/configurations.module.ts":
/*!***************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/configurations.module.ts ***!
  \***************************************************************************/
/*! exports provided: ConfigurationsModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationsModule", function() { return ConfigurationsModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm5/common.js");
/* harmony import */ var _configuration_list_configuration_list_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./configuration-list/configuration-list.component */ "./src/app/reseller/settings/configurations/configuration-list/configuration-list.component.ts");
/* harmony import */ var _configuration_details_configuration_details_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./configuration-details/configuration-details.component */ "./src/app/reseller/settings/configurations/configuration-details/configuration-details.component.ts");
/* harmony import */ var _configuration_create_configuration_create_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./configuration-create/configuration-create.component */ "./src/app/reseller/settings/configurations/configuration-create/configuration-create.component.ts");
/* harmony import */ var _configuration_edit_configuration_edit_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./configuration-edit/configuration-edit.component */ "./src/app/reseller/settings/configurations/configuration-edit/configuration-edit.component.ts");
/* harmony import */ var _tabs_configuration_edit_form_configuration_edit_form_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tabs/configuration-edit-form/configuration-edit-form.component */ "./src/app/reseller/settings/configurations/tabs/configuration-edit-form/configuration-edit-form.component.ts");
/* harmony import */ var _configurations_routing_module__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./configurations-routing.module */ "./src/app/reseller/settings/configurations/configurations-routing.module.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../../../shared/error-handling/error-handling.module */ "./src/app/shared/error-handling/error-handling.module.ts");
/* harmony import */ var _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../../../shared/ui/objects-view/objects-view.module */ "./src/app/shared/ui/objects-view/objects-view.module.ts");
/* harmony import */ var _angular_material_form_field__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/material/form-field */ "./node_modules/@angular/material/esm5/form-field.es5.js");
/* harmony import */ var _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @angular/material/checkbox */ "./node_modules/@angular/material/esm5/checkbox.es5.js");
/* harmony import */ var _angular_material_input__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @angular/material/input */ "./node_modules/@angular/material/esm5/input.es5.js");
/* harmony import */ var _tabs_configuration_details_billing_form_configuration_details_billing_form_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./tabs/configuration-details-billing-form/configuration-details-billing-form.component */ "./src/app/reseller/settings/configurations/tabs/configuration-details-billing-form/configuration-details-billing-form.component.ts");
/* harmony import */ var _angular_flex_layout__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @angular/flex-layout */ "./node_modules/@angular/flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm5/select.es5.js");
/* harmony import */ var _angular_material_radio__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @angular/material/radio */ "./node_modules/@angular/material/esm5/radio.es5.js");
/* harmony import */ var _angular_material_expansion__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @angular/material/expansion */ "./node_modules/@angular/material/esm5/expansion.es5.js");




















var ConfigurationsModule = /** @class */ (function () {
    function ConfigurationsModule() {
    }
    ConfigurationsModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            declarations: [
                _configuration_list_configuration_list_component__WEBPACK_IMPORTED_MODULE_3__["ConfigurationListComponent"],
                _configuration_details_configuration_details_component__WEBPACK_IMPORTED_MODULE_4__["ConfigurationDetailsComponent"],
                _configuration_create_configuration_create_component__WEBPACK_IMPORTED_MODULE_5__["ConfigurationCreateComponent"],
                _configuration_edit_configuration_edit_component__WEBPACK_IMPORTED_MODULE_6__["ConfigurationEditComponent"],
                _tabs_configuration_edit_form_configuration_edit_form_component__WEBPACK_IMPORTED_MODULE_7__["ConfigurationEditFormComponent"],
                _tabs_configuration_details_billing_form_configuration_details_billing_form_component__WEBPACK_IMPORTED_MODULE_15__["ConfigurationDetailsBillingFormComponent"],
            ],
            entryComponents: [
                _tabs_configuration_edit_form_configuration_edit_form_component__WEBPACK_IMPORTED_MODULE_7__["ConfigurationEditFormComponent"],
                _tabs_configuration_details_billing_form_configuration_details_billing_form_component__WEBPACK_IMPORTED_MODULE_15__["ConfigurationDetailsBillingFormComponent"],
            ],
            imports: [
                _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
                _configurations_routing_module__WEBPACK_IMPORTED_MODULE_8__["ConfigurationsRoutingModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_9__["ReactiveFormsModule"],
                _shared_error_handling_error_handling_module__WEBPACK_IMPORTED_MODULE_10__["ErrorHandlingModule"],
                _shared_ui_objects_view_objects_view_module__WEBPACK_IMPORTED_MODULE_11__["ObjectsViewModule"],
                _angular_material_form_field__WEBPACK_IMPORTED_MODULE_12__["MatFormFieldModule"],
                _angular_material_checkbox__WEBPACK_IMPORTED_MODULE_13__["MatCheckboxModule"],
                _angular_material_input__WEBPACK_IMPORTED_MODULE_14__["MatInputModule"],
                _angular_flex_layout__WEBPACK_IMPORTED_MODULE_16__["FlexLayoutModule"],
                _angular_material_select__WEBPACK_IMPORTED_MODULE_17__["MatSelectModule"],
                _angular_material_radio__WEBPACK_IMPORTED_MODULE_18__["MatRadioModule"],
                _angular_material_expansion__WEBPACK_IMPORTED_MODULE_19__["MatExpansionModule"],
            ]
        })
    ], ConfigurationsModule);
    return ConfigurationsModule;
}());



/***/ }),

/***/ "./src/app/reseller/settings/configurations/tabs/configuration-details-billing-form/configuration-details-billing-form.component.scss":
/*!********************************************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/tabs/configuration-details-billing-form/configuration-details-billing-form.component.scss ***!
  \********************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2NvbmZpZ3VyYXRpb25zL3RhYnMvY29uZmlndXJhdGlvbi1kZXRhaWxzLWJpbGxpbmctZm9ybS9jb25maWd1cmF0aW9uLWRldGFpbHMtYmlsbGluZy1mb3JtLmNvbXBvbmVudC5zY3NzIn0= */"

/***/ }),

/***/ "./src/app/reseller/settings/configurations/tabs/configuration-details-billing-form/configuration-details-billing-form.component.ts":
/*!******************************************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/tabs/configuration-details-billing-form/configuration-details-billing-form.component.ts ***!
  \******************************************************************************************************************************************/
/*! exports provided: ConfigurationDetailsBillingFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationDetailsBillingFormComponent", function() { return ConfigurationDetailsBillingFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _shared_fleio_api_configurations_configurations_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../../../shared/fleio-api/configurations/configurations-api.service */ "./src/app/shared/fleio-api/configurations/configurations-api.service.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");








var ConfigurationDetailsBillingFormComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ConfigurationDetailsBillingFormComponent, _super);
    function ConfigurationDetailsBillingFormComponent(formBuilder, configurationsApiService, router, config) {
        var _this = _super.call(this) || this;
        _this.formBuilder = formBuilder;
        _this.configurationsApiService = configurationsApiService;
        _this.router = router;
        _this.config = config;
        _this.configurationBillingForm = _this.formBuilder.group({
            // Billing
            credit_required: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            credit_limit: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            minim_uptodate_credit_for_invoice_payment: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            // Limits for clients with agreement
            credit_required_with_agreement: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            credit_limit_with_agreement: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            // Billing cycles
            billing_cycle_as_calendar_month: [''],
            // General
            company_info: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            sender_name: [''],
            sender_email: [''],
            // MaxMind fraud check
            fraud_check: [''],
            enable_maxmind_insights: [''],
            maxmind_fraud_score: [''],
            maxmind_manual_review_score: [''],
            // Client signup automation
            auto_create_order: [false],
            auto_order_service: [-1],
            auto_order_service_cycle: [-1],
            auto_order_service_params: [''],
            client_initial_credit: [0],
            // Invoicing
            generate_invoices: [''],
            send_notifications_for_unpaid_invoices: [''],
            create_todo_on_invoice_payment: [''],
            auto_settle_usage: [''],
            auto_pay_invoice_only_when_enough_credit: [''],
            invoicing_option: [''],
            next_paid_invoice_number: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            next_paid_invoice_number_format: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            limit_billable_seconds_per_month: [''],
            billable_seconds_per_month: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            issue_invoice_before_next_due_date: [''],
            next_invoice_date_offset: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            auto_eu_tax_exemption: [''],
            // Credit notifications
            credit_notifications_enabled: [''],
            credit_notifications_when_agreement_enabled: [''],
            first_credit_remaining_hours: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            first_credit_notification_template: [''],
            second_credit_remaining_hours: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            second_credit_notification_template: [''],
            third_credit_remaining_hours: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            third_credit_notification_template: [''],
            // Suspension
            auto_suspend: [''],
            auto_suspend_delay_hours_enabled: [''],
            auto_suspend_delay_hours: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            auto_suspend_delay_credit_enabled: [''],
            auto_suspend_delay_credit: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            auto_suspend_notification_template: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            // Termination
            auto_terminate: [''],
            suspend_instead_of_terminate: [''],
            auto_terminate_delay_hours: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
            auto_terminate_notification_template: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_3__["Validators"].required],
        });
        _this.updatingControls = false;
        return _this;
    }
    ConfigurationDetailsBillingFormComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.objectController.actionCallback = function () { return _this.saveConfiguration(); };
        this.billingConfiguration =
            this.objectController.additionalObjects.billingConfiguration;
        this.configurationBillingForm.valueChanges.subscribe(function () {
            if (!_this.updatingControls) {
                _this.updatingControls = true;
                _this.updateMaxMindControls();
                _this.updateClientSignupAutomationControls();
                _this.updateInvoicingControls();
                _this.updateCreditNotificationsControls();
                _this.updateSuspensionControls();
                _this.updateTerminationControls();
                _this.updatingControls = false;
            }
        });
        this.configurationBillingForm.patchValue(this.billingConfiguration);
    };
    ConfigurationDetailsBillingFormComponent.prototype.updateMaxMindControls = function () {
        var maxMindControls = this.configurationBillingForm.controls;
        if (maxMindControls.fraud_check.value) {
            maxMindControls.enable_maxmind_insights.enable();
            maxMindControls.maxmind_fraud_score.enable();
            maxMindControls.maxmind_manual_review_score.enable();
        }
        else {
            maxMindControls.enable_maxmind_insights.disable();
            maxMindControls.maxmind_fraud_score.disable();
            maxMindControls.maxmind_manual_review_score.disable();
        }
    };
    ConfigurationDetailsBillingFormComponent.prototype.updateClientSignupAutomationControls = function () {
        var e_1, _a;
        var clientSignupAutomationControls = this.configurationBillingForm.controls;
        if (clientSignupAutomationControls.auto_create_order.value) {
            clientSignupAutomationControls.auto_order_service.enable();
            clientSignupAutomationControls.auto_order_service_cycle.enable();
            clientSignupAutomationControls.auto_order_service_params.enable();
            clientSignupAutomationControls.client_initial_credit.enable();
            try {
                for (var _b = tslib__WEBPACK_IMPORTED_MODULE_0__["__values"](this.billingConfiguration.products), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var product = _c.value;
                    if (product.id === clientSignupAutomationControls.auto_order_service.value) {
                        this.autoOrderProduct = product;
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
        else {
            clientSignupAutomationControls.auto_order_service.disable();
            clientSignupAutomationControls.auto_order_service_cycle.disable();
            clientSignupAutomationControls.auto_order_service_params.disable();
            clientSignupAutomationControls.client_initial_credit.disable();
        }
    };
    ConfigurationDetailsBillingFormComponent.prototype.updateInvoicingControls = function () {
        var invoicingControls = this.configurationBillingForm.controls;
        if (invoicingControls.generate_invoices.value) {
            invoicingControls.send_notifications_for_unpaid_invoices.enable();
            invoicingControls.create_todo_on_invoice_payment.enable();
            invoicingControls.auto_settle_usage.enable();
            if (invoicingControls.auto_settle_usage.value) {
                invoicingControls.auto_pay_invoice_only_when_enough_credit.enable();
            }
            else {
                invoicingControls.auto_pay_invoice_only_when_enough_credit.disable();
            }
            invoicingControls.invoicing_option.enable();
            invoicingControls.next_paid_invoice_number.enable();
            invoicingControls.next_paid_invoice_number_format.enable();
            invoicingControls.limit_billable_seconds_per_month.enable();
            if (invoicingControls.limit_billable_seconds_per_month.value) {
                invoicingControls.billable_seconds_per_month.enable();
            }
            else {
                invoicingControls.billable_seconds_per_month.disable();
            }
            invoicingControls.issue_invoice_before_next_due_date.enable();
            if (invoicingControls.issue_invoice_before_next_due_date.value) {
                invoicingControls.next_invoice_date_offset.enable();
            }
            else {
                invoicingControls.next_invoice_date_offset.disable();
            }
            invoicingControls.auto_eu_tax_exemption.enable();
        }
        else {
            invoicingControls.send_notifications_for_unpaid_invoices.disable();
            invoicingControls.create_todo_on_invoice_payment.disable();
            invoicingControls.auto_settle_usage.disable();
            invoicingControls.auto_pay_invoice_only_when_enough_credit.disable();
            invoicingControls.invoicing_option.disable();
            invoicingControls.next_paid_invoice_number.disable();
            invoicingControls.next_paid_invoice_number_format.disable();
            invoicingControls.limit_billable_seconds_per_month.disable();
            invoicingControls.billable_seconds_per_month.disable();
            invoicingControls.issue_invoice_before_next_due_date.disable();
            invoicingControls.next_invoice_date_offset.disable();
            invoicingControls.auto_eu_tax_exemption.disable();
        }
    };
    ConfigurationDetailsBillingFormComponent.prototype.updateCreditNotificationsControls = function () {
        var creditNotificationsControls = this.configurationBillingForm.controls;
        if (creditNotificationsControls.credit_notifications_enabled.value) {
            creditNotificationsControls.credit_notifications_when_agreement_enabled.enable();
            creditNotificationsControls.first_credit_remaining_hours.enable();
            creditNotificationsControls.first_credit_notification_template.enable();
            creditNotificationsControls.second_credit_remaining_hours.enable();
            creditNotificationsControls.second_credit_notification_template.enable();
            creditNotificationsControls.third_credit_remaining_hours.enable();
            creditNotificationsControls.third_credit_notification_template.enable();
        }
        else {
            creditNotificationsControls.credit_notifications_when_agreement_enabled.disable();
            creditNotificationsControls.first_credit_remaining_hours.disable();
            creditNotificationsControls.first_credit_notification_template.disable();
            creditNotificationsControls.second_credit_remaining_hours.disable();
            creditNotificationsControls.second_credit_notification_template.disable();
            creditNotificationsControls.third_credit_remaining_hours.disable();
            creditNotificationsControls.third_credit_notification_template.disable();
        }
    };
    ConfigurationDetailsBillingFormComponent.prototype.updateSuspensionControls = function () {
        var suspensionControls = this.configurationBillingForm.controls;
        if (suspensionControls.auto_suspend.value) {
            suspensionControls.auto_suspend_delay_hours_enabled.enable();
            if (suspensionControls.auto_suspend_delay_hours_enabled.value) {
                suspensionControls.auto_suspend_delay_hours.enable();
            }
            else {
                suspensionControls.auto_suspend_delay_hours.disable();
            }
            suspensionControls.auto_suspend_delay_credit_enabled.enable();
            if (suspensionControls.auto_suspend_delay_credit_enabled.value) {
                suspensionControls.auto_suspend_delay_credit.enable();
            }
            else {
                suspensionControls.auto_suspend_delay_credit.disable();
            }
            suspensionControls.auto_suspend_notification_template.enable();
        }
        else {
            suspensionControls.auto_suspend_delay_hours_enabled.disable();
            suspensionControls.auto_suspend_delay_hours.disable();
            suspensionControls.auto_suspend_delay_credit_enabled.disable();
            suspensionControls.auto_suspend_delay_credit.disable();
            suspensionControls.auto_suspend_notification_template.disable();
        }
    };
    ConfigurationDetailsBillingFormComponent.prototype.updateTerminationControls = function () {
        var terminationControls = this.configurationBillingForm.controls;
        if (terminationControls.auto_terminate.value) {
            terminationControls.auto_terminate_delay_hours.enable();
            terminationControls.auto_terminate_notification_template.enable();
        }
        else {
            terminationControls.auto_terminate_delay_hours.disable();
            terminationControls.auto_terminate_notification_template.disable();
        }
    };
    ConfigurationDetailsBillingFormComponent.prototype.saveConfiguration = function () {
        var _this = this;
        var value = this.configurationBillingForm.value;
        var request;
        value.id = this.object.id;
        if (!value.auto_create_order) {
            value.auto_order_service = -1;
            value.auto_order_service_cycle = -1;
            value.auto_order_service_params = '';
        }
        request = this.configurationsApiService.objectPutAction(value.id, 'billing', value);
        request.subscribe(function () {
            _this.router.navigateByUrl(_this.config.getPrevUrl('settings/configurations')).catch(function () {
            });
        }, function (error) {
            _this.setErrors(error.error);
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_7__["of"])(null);
    };
    ConfigurationDetailsBillingFormComponent.ctorParameters = function () { return [
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_3__["FormBuilder"] },
        { type: _shared_fleio_api_configurations_configurations_api_service__WEBPACK_IMPORTED_MODULE_4__["ConfigurationsApiService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_5__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_6__["ConfigService"] }
    ]; };
    ConfigurationDetailsBillingFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-configuration-details-billing-form',
            template: __webpack_require__(/*! raw-loader!./configuration-details-billing-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/tabs/configuration-details-billing-form/configuration-details-billing-form.component.html"),
            styles: [__webpack_require__(/*! ./configuration-details-billing-form.component.scss */ "./src/app/reseller/settings/configurations/tabs/configuration-details-billing-form/configuration-details-billing-form.component.scss")]
        })
    ], ConfigurationDetailsBillingFormComponent);
    return ConfigurationDetailsBillingFormComponent;
}(_shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_2__["DetailsFormBase"]));



/***/ }),

/***/ "./src/app/reseller/settings/configurations/tabs/configuration-edit-form/configuration-edit-form.component.scss":
/*!**********************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/tabs/configuration-edit-form/configuration-edit-form.component.scss ***!
  \**********************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL3Jlc2VsbGVyL3NldHRpbmdzL2NvbmZpZ3VyYXRpb25zL3RhYnMvY29uZmlndXJhdGlvbi1lZGl0LWZvcm0vY29uZmlndXJhdGlvbi1lZGl0LWZvcm0uY29tcG9uZW50LnNjc3MifQ== */"

/***/ }),

/***/ "./src/app/reseller/settings/configurations/tabs/configuration-edit-form/configuration-edit-form.component.ts":
/*!********************************************************************************************************************!*\
  !*** ./src/app/reseller/settings/configurations/tabs/configuration-edit-form/configuration-edit-form.component.ts ***!
  \********************************************************************************************************************/
/*! exports provided: ConfigurationEditFormComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationEditFormComponent", function() { return ConfigurationEditFormComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var _shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../../../shared/ui/objects-view/details-form-base */ "./src/app/shared/ui/objects-view/details-form-base.ts");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../../../../shared/config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var _shared_fleio_api_configurations_configurations_api_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../../../../shared/fleio-api/configurations/configurations-api.service */ "./src/app/shared/fleio-api/configurations/configurations-api.service.ts");








var ConfigurationEditFormComponent = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ConfigurationEditFormComponent, _super);
    function ConfigurationEditFormComponent(formBuilder, configurationsApiService, router, config) {
        var _this = _super.call(this) || this;
        _this.formBuilder = formBuilder;
        _this.configurationsApiService = configurationsApiService;
        _this.router = router;
        _this.config = config;
        _this.configurationForm = _this.formBuilder.group({
            name: ['', _angular_forms__WEBPACK_IMPORTED_MODULE_2__["Validators"].required],
            description: [''],
            is_default: [false]
        });
        return _this;
    }
    ConfigurationEditFormComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.objectController.actionCallback = function () { return _this.saveConfiguration(); };
        this.configurationForm.patchValue(this.object);
    };
    ConfigurationEditFormComponent.prototype.saveConfiguration = function () {
        var _this = this;
        var value = this.configurationForm.value;
        this.createOrUpdate(this.configurationsApiService, value).subscribe(function () {
            _this.router.navigateByUrl(_this.config.getPrevUrl('settings/configurations')).catch(function () { });
        });
        return Object(rxjs__WEBPACK_IMPORTED_MODULE_6__["of"])(null);
    };
    ConfigurationEditFormComponent.ctorParameters = function () { return [
        { type: _angular_forms__WEBPACK_IMPORTED_MODULE_2__["FormBuilder"] },
        { type: _shared_fleio_api_configurations_configurations_api_service__WEBPACK_IMPORTED_MODULE_7__["ConfigurationsApiService"] },
        { type: _angular_router__WEBPACK_IMPORTED_MODULE_4__["Router"] },
        { type: _shared_config_config_service__WEBPACK_IMPORTED_MODULE_5__["ConfigService"] }
    ]; };
    ConfigurationEditFormComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-configuration-edit-form',
            template: __webpack_require__(/*! raw-loader!./configuration-edit-form.component.html */ "./node_modules/raw-loader/index.js!./src/app/reseller/settings/configurations/tabs/configuration-edit-form/configuration-edit-form.component.html"),
            styles: [__webpack_require__(/*! ./configuration-edit-form.component.scss */ "./src/app/reseller/settings/configurations/tabs/configuration-edit-form/configuration-edit-form.component.scss")]
        })
    ], ConfigurationEditFormComponent);
    return ConfigurationEditFormComponent;
}(_shared_ui_objects_view_details_form_base__WEBPACK_IMPORTED_MODULE_3__["DetailsFormBase"]));



/***/ }),

/***/ "./src/app/shared/fleio-api/configurations/configuration-billing.resolver.ts":
/*!***********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/configurations/configuration-billing.resolver.ts ***!
  \***********************************************************************************/
/*! exports provided: ConfigurationBillingResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationBillingResolver", function() { return ConfigurationBillingResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _configurations_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./configurations-api.service */ "./src/app/shared/fleio-api/configurations/configurations-api.service.ts");





var ConfigurationBillingResolver = /** @class */ (function () {
    function ConfigurationBillingResolver(configurationApiService) {
        this.configurationApiService = configurationApiService;
    }
    ConfigurationBillingResolver.prototype.resolve = function (route, state) {
        return this.configurationApiService.objectGetAction(route.params.id, 'billing').pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(function (configurationBilling) {
            configurationBilling.id = route.params.id;
            return configurationBilling;
        }), Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    ConfigurationBillingResolver.ctorParameters = function () { return [
        { type: _configurations_api_service__WEBPACK_IMPORTED_MODULE_4__["ConfigurationsApiService"] }
    ]; };
    ConfigurationBillingResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ConfigurationBillingResolver);
    return ConfigurationBillingResolver;
}());



/***/ }),

/***/ "./src/app/shared/fleio-api/configurations/configuration-list.resolver.ts":
/*!********************************************************************************!*\
  !*** ./src/app/shared/fleio-api/configurations/configuration-list.resolver.ts ***!
  \********************************************************************************/
/*! exports provided: ConfigurationListResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationListResolver", function() { return ConfigurationListResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _configurations_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./configurations-api.service */ "./src/app/shared/fleio-api/configurations/configurations-api.service.ts");





var ConfigurationListResolver = /** @class */ (function () {
    function ConfigurationListResolver(configurationApiService) {
        this.configurationApiService = configurationApiService;
    }
    ConfigurationListResolver.prototype.resolve = function (route, state) {
        return this.configurationApiService.list(route.queryParams).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    ConfigurationListResolver.ctorParameters = function () { return [
        { type: _configurations_api_service__WEBPACK_IMPORTED_MODULE_4__["ConfigurationsApiService"] }
    ]; };
    ConfigurationListResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ConfigurationListResolver);
    return ConfigurationListResolver;
}());



/***/ }),

/***/ "./src/app/shared/fleio-api/configurations/configuration.resolver.ts":
/*!***************************************************************************!*\
  !*** ./src/app/shared/fleio-api/configurations/configuration.resolver.ts ***!
  \***************************************************************************/
/*! exports provided: ConfigurationResolver */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationResolver", function() { return ConfigurationResolver; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm5/index.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm5/operators/index.js");
/* harmony import */ var _configurations_api_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./configurations-api.service */ "./src/app/shared/fleio-api/configurations/configurations-api.service.ts");





var ConfigurationResolver = /** @class */ (function () {
    function ConfigurationResolver(configurationApiService) {
        this.configurationApiService = configurationApiService;
    }
    ConfigurationResolver.prototype.resolve = function (route, state) {
        return this.configurationApiService.get(route.params.id).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["catchError"])(function () { return Object(rxjs__WEBPACK_IMPORTED_MODULE_2__["of"])(null); }));
    };
    ConfigurationResolver.ctorParameters = function () { return [
        { type: _configurations_api_service__WEBPACK_IMPORTED_MODULE_4__["ConfigurationsApiService"] }
    ]; };
    ConfigurationResolver = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ConfigurationResolver);
    return ConfigurationResolver;
}());



/***/ }),

/***/ "./src/app/shared/fleio-api/configurations/configurations-api.service.ts":
/*!*******************************************************************************!*\
  !*** ./src/app/shared/fleio-api/configurations/configurations-api.service.ts ***!
  \*******************************************************************************/
/*! exports provided: ConfigurationsApiService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ConfigurationsApiService", function() { return ConfigurationsApiService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _config_config_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../config/config.service */ "./src/app/shared/config/config.service.ts");
/* harmony import */ var _fleio_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../fleio-api.service */ "./src/app/shared/fleio-api/fleio-api.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");





var ConfigurationsApiService = /** @class */ (function (_super) {
    tslib__WEBPACK_IMPORTED_MODULE_0__["__extends"](ConfigurationsApiService, _super);
    // noinspection JSUnusedGlobalSymbols
    function ConfigurationsApiService(httpClient, config) {
        var _this = _super.call(this, config.getPanelApiUrl('configurations')) || this;
        _this.httpClient = httpClient;
        _this.config = config;
        return _this;
    }
    ConfigurationsApiService.prototype.specificConfiguration = function (id, type) {
        return this.objectGetAction(id, type);
    };
    ConfigurationsApiService.ctorParameters = function () { return [
        { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"] },
        { type: _config_config_service__WEBPACK_IMPORTED_MODULE_2__["ConfigService"] }
    ]; };
    ConfigurationsApiService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], ConfigurationsApiService);
    return ConfigurationsApiService;
}(_fleio_api_service__WEBPACK_IMPORTED_MODULE_3__["FleioApiService"]));



/***/ })

}]);
//# sourceMappingURL=configurations-configurations-module-es5.js.map