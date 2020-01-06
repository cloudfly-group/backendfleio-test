(function(){
  'use strict';
  angular.module('fleio')
  .component('pluginsDomainsDomainDetails', {
    templateUrl: 'site/plugins/domains/domains/domaindetails.html',
    controller: PluginsDomainsDomainDetailsController,
    bindings: {
      domain: '<'
    }
  });

  PluginsDomainsDomainDetailsController.$inject = ['$state', 'gettextCatalog', 'PluginsDomainsDomainsApi',
    'FlNotificationService', 'FlResolveErrorHandler', 'FlUiUtilsService'];
  function PluginsDomainsDomainDetailsController($state, gettextCatalog, PluginsDomainsDomainsApi,
                                            FlNotificationService, FlResolveErrorHandler, FlUiUtilsService) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
      $ctrl.commentText = '';
      $ctrl.nameservers = {};
      $ctrl.refreshNameservers();
      $ctrl.refreshDomainInfo();
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

    $ctrl.refreshDomain = function refreshDomain() {
      PluginsDomainsDomainsApi.get({'id':$ctrl.domain.id}).$promise
        .then(function (data) {
            $ctrl.domain = data;
            $ctrl.refreshNameservers();
        }).catch(FlResolveErrorHandler.handleError);
    };

    $ctrl.refreshDomainInfo = function refreshDomainInfo() {
      PluginsDomainsDomainsApi.get({
          'id':$ctrl.domain.id,
          'action':'get_info'
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
              'domain_action':domain_action
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
    }
  }
})();
