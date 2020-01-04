(function () {
  'use strict';

  angular.module('fleio')
    .component('pluginsDomainsRegisterDomainForm', {
      templateUrl: 'site/plugins/domains/register_domain_form/registerdomainform.html',
      controller: PluginsDomainsRegisterDomainFormController,
      bindings: {
          data: '=',
          clientCreateOptions: '<'
      }
    });

  PluginsDomainsRegisterDomainFormController.$inject = ['gettext',
      'PluginsDomainsOrderDomainApi', 'FlNotificationService', '$state', '$mdDialog',
      'PluginsDomainsContactsActionsService'];
  function PluginsDomainsRegisterDomainFormController(gettext, PluginsDomainsOrderDomainApi, FlNotificationService,
                                                  $state, $mdDialog, PluginsDomainsContactsActionsService){
    var $ctrl = this;
    $ctrl.checkAvailabilityInProgress = false;
    $ctrl.domain = {
        operation: 'register'
    };

    $ctrl.$onInit = function $onInit() {
        if ($ctrl.data) {
            $ctrl.domain.name = $ctrl.data.domain_name;
            if ($ctrl.data.clientCreateOptions) {
                $ctrl.clientCreateOptions = $ctrl.data.clientCreateOptions;
            }
            $ctrl.checkIfDomainIsAvailable();
        }
    };

    $ctrl.checkIfDomainIsAvailable = function checkIfDomainIsAvailable() {
        $ctrl.checkResults = {};
        $ctrl.checkAvailabilityInProgress = true;
        PluginsDomainsOrderDomainApi.get({
            action:'is_available_for_registration',
            domain_name: $ctrl.domain.name
        }).$promise.then(function (checkResults) {
            $ctrl.checkResults = checkResults;
            if ($ctrl.checkResults && $ctrl.checkResults.available) {
                $ctrl.domain.name = $ctrl.checkResults.adjusted_name;
                $ctrl.checkCustomFieldsForClient();
            }
            if ($ctrl.checkResults.config){
                $ctrl.domain.use_default_nameservers = $ctrl.checkResults.config.enable_default_nameservers;
                if ($ctrl.checkResults.config.enable_default_nameservers){
                    $ctrl.domain.nameserver1 = $ctrl.checkResults.config.default_nameserver1;
                    $ctrl.domain.nameserver2 = $ctrl.checkResults.config.default_nameserver2;
                    $ctrl.domain.nameserver3 = $ctrl.checkResults.config.default_nameserver3;
                    $ctrl.domain.nameserver4 = $ctrl.checkResults.config.default_nameserver4;
                } else {
                    $ctrl.domain.use_default_nameservers = false;
                }
            }
            for (var index =0; index < $ctrl.checkResults.prices.prices_per_years.length; index++){
                if ($ctrl.checkResults.prices.prices_per_years[index] !== null){
                    $ctrl.domain.years = index;
                    break
                }
            }
            $ctrl.updateOptionPrices();
        }).catch(function (reason) {
        }).finally(function () {
            $ctrl.checkAvailabilityInProgress = false;
        })
    };

    $ctrl.getYearsText = function getYearsText(years){
        var adjustedYears = years + 1;
        if (0 === adjustedYears){
            return '1 ' + gettext('year');
        }
        else {
            return adjustedYears + ' ' + gettext('years');
        }
    };

    $ctrl.setDefaultNameservers = function setDefaultNameservers() {
       $ctrl.domain.nameserver1 = $ctrl.checkResults.config.default_nameserver1;
       $ctrl.domain.nameserver2 = $ctrl.checkResults.config.default_nameserver2;
       $ctrl.domain.nameserver3 = $ctrl.checkResults.config.default_nameserver3;
       $ctrl.domain.nameserver4 = $ctrl.checkResults.config.default_nameserver4;
    };

    $ctrl.registerDomain = function registerDomain() {
        if (!($ctrl.checkResults && $ctrl.checkResults.available)){
          $ctrl.registerDomainForm.$setSubmitted(false);  // NOTE(tomo): enter pressed but no results available
          $ctrl.registerDomainForm.$setPristine(true);    // NOTE(tomo): not ok to validate if results are not present
          return;
        }
        if ($ctrl.registerDomainForm.$invalid || $ctrl.submitPending) {
          return;
        }

        $ctrl.submitPending = true;
        if ($ctrl.contact && $ctrl.domain_contact_type === 'contact') {
            $ctrl.domain.contact_id = $ctrl.contact.id;
        }

        PluginsDomainsOrderDomainApi.save({
            domain: $ctrl.domain,
            action: 'register_domain'
        }).$promise.then(function (value) {
            $state.go('cart');
        }).catch(function (reason) {
            $ctrl.backendErrors = reason.data;
        }).finally(function() {
          $ctrl.submitPending = false;
        })
    };

    $ctrl.contactTypeChanged = function contactTypeChanged() {
        if ($ctrl.domain_contact_type === 'client') {
            $ctrl.checkCustomFieldsForClient();
        } else {
            if ($ctrl.contact){
                $ctrl.checkCustomFieldsForContact($ctrl.contactId);
            } else {
                if ($ctrl.customFieldsResults) {
                    $ctrl.customFieldsResults.missing_fields = false;
                }
            }
        }
    };

    $ctrl.checkCustomFieldsForClient = function checkCustomFieldsForClient() {
        PluginsDomainsOrderDomainApi.get({
            action:'check_custom_fields',
            domain_name: $ctrl.domain.name,
            contact_type: 'client'
        }).$promise.then(function (checkResults) {
            $ctrl.customFieldsResults = checkResults;
        }).catch(function (reason) {
            FlNotificationService.add(gettext('Error when checking custom fields.'))
        })
    };

    $ctrl.editClient = function editClient(ev){
      return $mdDialog.show({
        templateUrl: 'apps/clients/clienteditdlg/clientedit.html',
        controller: 'EditClientController',
        controllerAs: '$ctrl',
        parent: angular.element(document.body),
        clickOutsideToClose: true,
        bindToController: true,
        locals: {
          createOptions: $ctrl.clientCreateOptions,
          isDialog: true,
          tldName: $ctrl.checkResults.tld.name
        },
        resolve: {
          client: ['FlClientApi', 'FlUiUtilsService', '$stateParams', 'FlResolveErrorHandler',
            function(FlClientApi, FlUiUtilsService, $stateParams, FlResolveErrorHandler) {
              return FlClientApi.get({
                  id: $ctrl.checkResults.client_id
              }).$promise.catch(FlResolveErrorHandler.handleError);
          }]
        },
        targetEvent: ev
      }).then(function () {
          $ctrl.checkCustomFieldsForClient();
      }).catch(function(){});
    };

    $ctrl.domainNameKeyUp = function domainNameKeyUp($event) {
        if ($event.keyCode === 13){
            $ctrl.checkIfDomainIsAvailable();
        } else {
            if ($ctrl.checkResults){
                $ctrl.checkResults.available = false;
            }
        }
    };

    $ctrl.checkCustomFieldsForContact = function checkCustomFieldsForContact(contactId) {
        PluginsDomainsOrderDomainApi.get({
            action:'check_custom_fields',
            domain_name: $ctrl.domain.name,
            contact_type: 'contact',
            contact_id: contactId
        }).$promise.then(function (checkResults) {
            $ctrl.customFieldsResults = checkResults;
        }).catch(function (reason) {
            FlNotificationService.add(gettext('Error when checking custom fields.'))
        })
    };

    $ctrl.onContactSelected = function onContactSelected(contact){
        $ctrl.contact = contact;
        if (typeof contact !== 'undefined') {
            $ctrl.checkCustomFieldsForContact(contact.id);
        }
    };

    $ctrl.createDomainContact = function createDomainContact($event) {
      return PluginsDomainsContactsActionsService.editContact(
          $event, false, $ctrl.contact, $ctrl.checkResults.tld.name
      );
    };

    $ctrl.editDomainContact = function editDomainContact($event) {
      return PluginsDomainsContactsActionsService.editContact(
          $event, true, $ctrl.contact, $ctrl.checkResults.tld.name
      ).then(function (value) {
          $ctrl.checkCustomFieldsForContact($ctrl.contact.id);
      });
    };

    $ctrl.canAddToCart = function canAddToCart() {
        if (!$ctrl.checkResults.available){
            return false;
        }

        if ($ctrl.registerDomainForm.$invalid){
            return false;
        }

        if ($ctrl.domain_contact_type === 'contact'){
            if (!$ctrl.contact) {
                return false;
            }
        }

        if ($ctrl.customFieldsResults) {
            return !$ctrl.customFieldsResults.missing_fields
        }
        else {
            return false;
        }
    };

    $ctrl.updateOptionPrices = function updateOptionPrices(){
        if ($ctrl.checkResults.dns_prices.prices_per_years[$ctrl.domain.years] === null){
            $ctrl.dns_management_price = '';
            $ctrl.dns_management_available = false;
            $ctrl.domain.dns_management = false;
        } else {
            $ctrl.dns_management_price = $ctrl.checkResults.dns_prices.prices_per_years[$ctrl.domain.years] + ' '
                + $ctrl.checkResults.dns_prices.currency.code;
            $ctrl.dns_management_available = true;
        }
        if ($ctrl.checkResults.email_prices.prices_per_years[$ctrl.domain.years] === null){
            $ctrl.email_forwarding_price = '';
            $ctrl.email_forwarding_available = false;
            $ctrl.domain.email_forwarding = false;
        } else {
            $ctrl.email_forwarding_price = $ctrl.checkResults.email_prices.prices_per_years[$ctrl.domain.years] + ' '
                + $ctrl.checkResults.email_prices.currency.code;
            $ctrl.email_forwarding_available = true;
        }
        if ($ctrl.checkResults.id_prices.prices_per_years[$ctrl.domain.years] === null){
            $ctrl.id_protection_price = '';
            $ctrl.id_protection_available = false;
            $ctrl.domain.id_protection = false;
        } else {
            $ctrl.id_protection_price = $ctrl.checkResults.id_prices.prices_per_years[$ctrl.domain.years] + ' '
                + $ctrl.checkResults.id_prices.currency.code;
            $ctrl.id_protection_available = true;
        }
    }
  }
})();
