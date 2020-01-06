(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsHypanelServerSettings', {
      templateUrl: 'staff/plugins/hypanel/server_settings/serversettings.html',
      controller: PluginsHypanelServerSettingsController,
      bindings: {
        data: '='
      }
    });

  PluginsHypanelServerSettingsController.$inject = [];
  function PluginsHypanelServerSettingsController() {
    var $ctrl = this;

    $ctrl.$onInit = function onInit() { };
        if(!$ctrl.data) {
            $ctrl.data = {}
        }
    }
})();
