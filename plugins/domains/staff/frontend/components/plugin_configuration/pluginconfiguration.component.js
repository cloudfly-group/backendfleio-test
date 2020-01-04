(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsDomainsPluginConfiguration', {
      templateUrl: 'staff/plugins/domains/plugin_configuration/pluginconfiguration.html',
      controller: PluginsDomainsPluginConfigurationController,
      bindings: {
          data: '='
      }
    });

  PluginsDomainsPluginConfigurationController.$inject = ['FlUiUtilsService', 'FlConfigurationsApi',
      'FlNotificationService', 'FlResolveErrorHandler'];
  function PluginsDomainsPluginConfigurationController(FlUiUtilsService, FlConfigurationsApi,
                                                      FlNotificationService, FlResolveErrorHandler) {
    var $ctrl = this;
    $ctrl.$onInit = $onInit;
    $ctrl.goBackOrToState = FlUiUtilsService.goBackOrToState;

    function $onInit() {
        FlConfigurationsApi.get({'id': $ctrl.data.id, 'section':'domains'}).$promise
            .then(function (value) {
              $ctrl.domainsSettings = value
            })
            .catch(FlResolveErrorHandler.handleError);
    }

    $ctrl.saveSettings = function (settingsID) {
      if ($ctrl.submitPending || $ctrl.domainsSettingsForm.$invalid) { return; }
      $ctrl.submitPending = true;
      $ctrl.backendErrors = null;

      FlConfigurationsApi.update({'id': $ctrl.data.id, 'section':'domains'}, $ctrl.domainsSettings).$promise
        .then(function(data) {
          FlNotificationService.add(data.detail);
          if (data.settings) { $ctrl.domainsSettings = data.settings; }
        })
        .catch(function(error) { $ctrl.backendErrors = error.data })
        .finally(function() { $ctrl.submitPending = false })
    };
  }
})();
