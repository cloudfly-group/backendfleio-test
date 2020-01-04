(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsCpanelPluginConfiguration', {
      templateUrl: 'staff/plugins/cpanel/plugin_configuration/pluginconfiguration.html',
      controller: PluginsCpanelPluginConfigurationController,
      bindings: {
          data: '='
      }
    });

  PluginsCpanelPluginConfigurationController.$inject = ['FlUiUtilsService'];
  function PluginsCpanelPluginConfigurationController(FlUiUtilsService) {
    var $ctrl = this;
    $ctrl.$onInit = $onInit;
    $ctrl.goBackOrToState = FlUiUtilsService.goBackOrToState;

    function $onInit() {
        $ctrl.configuration = angular.copy($ctrl.data);
    }
  }
})();
