(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsTodoPluginConfiguration', {
      templateUrl: 'staff/plugins/todo/plugin_configuration/pluginconfiguration.html',
      controller: PluginsTodoPluginConfigurationController,
      bindings: {
          data: '='
      }
    });

  PluginsTodoPluginConfigurationController.$inject = ['FlUiUtilsService'];
  function PluginsTodoPluginConfigurationController(FlUiUtilsService) {
    var $ctrl = this;
    $ctrl.$onInit = $onInit;
    $ctrl.goBackOrToState = FlUiUtilsService.goBackOrToState;

    function $onInit() {
        $ctrl.configuration = angular.copy($ctrl.data);
    }
  }
})();
