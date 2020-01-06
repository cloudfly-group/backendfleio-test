(function(){
  'use strict';
  angular.module('fleioStaff')
  .component('pluginsDomainsDomainDetails', {
    templateUrl: 'staff/plugins/domains/domain_details/domaindetails.html',
    controller: PluginsDomainsDomainDetailsController,
    bindings: {
      domain: '<'
    }
  });

  PluginsDomainsDomainDetailsController.$inject = [
      '$state', 'gettextCatalog', 'PluginsDomainsDomainsApi',
      'FlNotificationService', 'FlResolveErrorHandler', 'FlUiUtilsService', 'PluginsDomainsContactsActionsService',
      '$mdDialog'
  ];
  function PluginsDomainsDomainDetailsController(
      $state, gettextCatalog, PluginsDomainsDomainsApi,
      FlNotificationService, FlResolveErrorHandler, FlUiUtilsService, PluginsDomainsContactsActionsService,
      $mdDialog
  ) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
      $ctrl.commentText = '';
      $ctrl.nameservers = {};
      $ctrl.refreshNameservers();
      $ctrl.submitPending = false;
      if ($ctrl.domain.status === 'active' ){
          $ctrl.refreshWhoisFields();
      }
    };

    $ctrl.refreshWhoisFields = function refreshWhoisFields() {
      $ctrl.whoisFields = null;
      $ctrl.whoisData = null;
      PluginsDomainsDomainsApi.get({
          'id':$ctrl.domain.id,
          'action':'get_whois_fields'
      }).$promise
        .then(function (response) {
            $ctrl.whoisFields = response.whois_fields;
            $ctrl.whoisData = response.whois_data;
        }).catch(function (reason) {
            FlNotificationService.add(reason.data.detail)
      });
    };

    $ctrl.saveWhoisData = function saveWhoisData() {
      PluginsDomainsDomainsApi.save({
          id:$ctrl.domain.id,
          action:'save_whois_data',
          whois_data: $ctrl.whoisData
      }).$promise
        .then(function () {
            FlNotificationService.add(gettextCatalog.getString('Whois data saved'))
        }).catch(function (reason) {
            FlNotificationService.add(reason.data.details)
      });
    };

    $ctrl.refreshNameservers = function refreshNameservers(){
        if ($ctrl.domain.nameservers.length > 3){
          $ctrl.nameservers.nameserver4 = $ctrl.domain.nameservers[3].host_name;
        }
        if ($ctrl.domain.nameservers.length > 2){
          $ctrl.nameservers.nameserver3 = $ctrl.domain.nameservers[2].host_name;
        }
        if ($ctrl.domain.nameservers.length > 1){
          $ctrl.nameservers.nameserver2 = $ctrl.domain.nameservers[1].host_name;
        }
        if ($ctrl.domain.nameservers.length > 0){
          $ctrl.nameservers.nameserver1 = $ctrl.domain.nameservers[0].host_name;
        }
    };

    $ctrl.onDomainDeleted = function onDomainDeleted() {
      $state.go('pluginsDomainsRegistrars');
    };

    $ctrl.refreshDomain = function refreshDomain() {
      $ctrl.actionStatusMessage = '';
      PluginsDomainsDomainsApi.get({'id':$ctrl.domain.id}).$promise
        .then(function (data) {
            $ctrl.domain = data;
            $ctrl.refreshNameservers();
            $ctrl.refreshDomainInfo();
        }).catch(FlResolveErrorHandler.handleError);
    };

    $ctrl.saveDomain = function saveDomain() {
      return PluginsDomainsDomainsApi.update({'id': $ctrl.domain.id}, $ctrl.domain)
        .$promise.then(function () {
            FlNotificationService.add(gettextCatalog.getString('Domain updated'));
            $ctrl.refreshDomain();
        }).catch(function (error) {
        });
    };

    $ctrl.refreshDomainInfo = function refreshDomainInfo(registrar) {
      var registrar_id;
      if (registrar){
          registrar_id = registrar.id;
      } else {
          registrar_id = $ctrl.domain.last_registrar;
      }
      if (!registrar_id){
          $ctrl.domainActions = [];
          return;
      }
      PluginsDomainsDomainsApi.get({
          'id':$ctrl.domain.id,
          'action':'get_info',
          'registrar_id': registrar_id
      }).$promise
        .then(function (response) {
            $ctrl.domainActions = response.actions;
        }).catch(function (reason) {
            FlNotificationService.add(reason.data.details)
      });
    };

    $ctrl.executeAction = function executeAction(domain_action, action_display_name) {
      var dialog_message = action_display_name + ' ' + $ctrl.domain.name;
      var dialog_title = action_display_name;
      var dialog_ok = action_display_name;

      $ctrl.actionStatusMessage = '';
      FlUiUtilsService.yesNoDlg(dialog_message, dialog_title, dialog_ok).then(function () {
        $ctrl.executingDomainAction = true;
          PluginsDomainsDomainsApi.save({
              'id':$ctrl.domain.id,
              'action':'execute_action',
              'domain_action':domain_action,
              'registrar_id': $ctrl.domain.last_registrar
          }).$promise
            .then(function (response) {
                $ctrl.refreshDomain();
                $ctrl.refreshDomainInfo();
                FlNotificationService.add(response.details);
                $ctrl.actionStatus = response.action_status;
                $ctrl.actionStatusMessage = response.action_status_message;
            }).catch(function (reason) {
                FlNotificationService.add(reason.data.details);
                $ctrl.actionStatus = reason.data.action_status;
                $ctrl.actionStatusMessage = reason.data.action_status_message;
          }).finally(function() {
            $ctrl.executingDomainAction = false;
          });
      });
    };

    $ctrl.saveNameservers = function saveNameservers() {
      if ($ctrl.submitPending || $ctrl.editNameserversForm.$invalid) {
        return;
      }
      $ctrl.submitPending = true;
      $ctrl.backendErrors = null;

      PluginsDomainsDomainsApi.save({
          'id':$ctrl.domain.id,
          'action':'save_nameservers'
      }, $ctrl.nameservers).$promise
        .then(function (response) {
            FlNotificationService.add(response.details);
            $ctrl.submitPending = false;
        }).catch(function (reason) {
            $ctrl.backendErrors = reason.data;
            $ctrl.submitPending = false;
      });
    };

    $ctrl.editContact = function editDomainContact($event) {
      return PluginsDomainsContactsActionsService.editContact(
          $event, true, $ctrl.domain.contact, $ctrl.domain.tld.name
      ).then(function (value) {
      });
    };


    $ctrl.editClient = function editClient(ev){
      return $mdDialog.show({
        templateUrl: 'staff/apps/clients/clienteditdlg/clientedit.html',
        controller: 'EditClientController',
        controllerAs: '$ctrl',
        parent: angular.element(document.body),
        clickOutsideToClose: true,
        bindToController: true,
        locals: {
          isDialog: true
        },
        resolve: {
          client: ['FlClientApi', 'FlUiUtilsService', '$stateParams', 'FlResolveErrorHandler',
            function(FlClientApi, FlUiUtilsService, $stateParams, FlResolveErrorHandler) {
              return FlClientApi.get({
                  id: $ctrl.domain.client_id
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
          $ctrl.refreshDomain();
      }).catch(function(){});
    };
  }
})();
