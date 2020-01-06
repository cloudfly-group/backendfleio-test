(function(){
  'use strict';
  angular.module('fleio')
  .component('pluginsDomainsOrderProduct', {
    templateUrl: 'site/plugins/domains/order_product/orderproduct.html',
    controller: PluginsDomainsDomainOrderProductController,
    bindings: {
      data: '='
    },
    require: {
      parentForm: '^form'
    }
  });

  PluginsDomainsDomainOrderProductController.$inject = ['$state', 'gettextCatalog',
    'FlNotificationService', 'FlResolveErrorHandler', 'FlUiUtilsService',
      'PluginsDomainsContactsActionsService', 'PluginsDomainsOrderDomainApi', 'PluginUILoaderApi'];
  function PluginsDomainsDomainOrderProductController($state, gettextCatalog, FlNotificationService,
                                                      FlResolveErrorHandler, FlUiUtilsService,
                                                      PluginsDomainsContactsActionsService,
                                                      PluginsDomainsOrderDomainApi, PluginUILoaderApi) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
      if ($ctrl.data.contact_id > 0){
        $ctrl.domain_contact_type = 'contact';
        $ctrl.contactId = $ctrl.data.contact_id;
      } else {
        $ctrl.domain_contact_type = 'client'
      }
      $ctrl.checkIfDomainIsAvailable();
    };

    $ctrl.onContactSelected = function onContactSelected(contact){
      if (contact) {
          $ctrl.contact = contact;
          $ctrl.data.contact_id = contact.id;
          $ctrl.checkCustomFieldsForContact(contact.id);
      }
    };

    $ctrl.checkIfDomainIsAvailable = function checkIfDomainIsAvailable() {
        $ctrl.checkResults = {};
        $ctrl.checkAvailabilityInProgress = true;
        PluginsDomainsOrderDomainApi.get({
            action:'is_available_for_registration',
            domain_name: $ctrl.data.name
        }).$promise.then(function (checkResults) {
            $ctrl.checkResults = checkResults;
        }).catch(function (reason) {
        }).finally(function () {
            $ctrl.checkAvailabilityInProgress = false;
        })
    };

    $ctrl.setDefaultNameservers = function setDefaultNameservers() {
       $ctrl.data.nameserver1 = $ctrl.checkResults.config.default_nameserver1;
       $ctrl.data.nameserver2 = $ctrl.checkResults.config.default_nameserver2;
       $ctrl.data.nameserver3 = $ctrl.checkResults.config.default_nameserver3;
       $ctrl.data.nameserver4 = $ctrl.checkResults.config.default_nameserver4;
    };

    $ctrl.editDomainContact = function editDomainContact($event) {
      return PluginsDomainsContactsActionsService.editContact(
          $event, true, $ctrl.contact, $ctrl.checkResults.tld.name
      ).then(function (value) {
          $ctrl.checkCustomFieldsForContact($ctrl.contact.id);
      });
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
          isDialog: true,
          tldName: $ctrl.checkResults.tld.name
        },
        resolve: {
          client: ['FlClientApi', 'FlUiUtilsService', '$stateParams', 'FlResolveErrorHandler',
            function(FlClientApi, FlUiUtilsService, $stateParams, FlResolveErrorHandler) {
              return FlClientApi.get({
                  id: $ctrl.checkResults.client_id
              }).$promise.catch(FlResolveErrorHandler.handleError);
          }],
          createOptions: [
            'FlClientApi', function (FlClientApi) {
              return FlClientApi.get({options: 'create_options'}).$promise;
            }
          ]
        },
        targetEvent: ev
      }).then(function () {
          $ctrl.checkCustomFieldsForClient();
      }).catch(function(){});
    };

    $ctrl.contactTypeChanged = function contactTypeChanged() {
        if ($ctrl.domain_contact_type === 'client') {
            $ctrl.data.contact_id = 0;
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
            domain_name: $ctrl.data.name,
            contact_type: 'client'
        }).$promise.then(function (checkResults) {
            $ctrl.customFieldsResults = checkResults;
        }).catch(function (reason) {
            FlNotificationService.add(gettext('Error when checking custom fields.'))
        })
    };

    $ctrl.checkCustomFieldsForContact = function checkCustomFieldsForContact(contactId) {
        PluginsDomainsOrderDomainApi.get({
            action:'check_custom_fields',
            domain_name: $ctrl.data.name,
            contact_type: 'contact',
            contact_id: contactId
        }).$promise.then(function (checkResults) {
            $ctrl.customFieldsResults = checkResults;
        }).catch(function (reason) {
            FlNotificationService.add(gettext('Error when checking custom fields.'))
        })
    };

  }
})();
