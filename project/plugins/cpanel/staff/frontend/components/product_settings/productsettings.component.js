(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsCpanelProductSettings', {
      templateUrl: 'staff/plugins/cpanel/product_settings/productsettings.html',
      controller: PluginsCPanelProductSettingsController,
      bindings: {
          data: '='
      },
      require: {
        parentForm: '^form'
      }
    });

  PluginsCPanelProductSettingsController.$inject = [];
  function PluginsCPanelProductSettingsController() {
    var $ctrl = this;
    $ctrl.$onInit = function onInit() {
        $ctrl.data['moduleConfigurationForm'] = 'cpanel_product_settings';
        if (!$ctrl.data.cpanel_product_settings) {
            $ctrl.data.cpanel_product_settings = {};
        }
    }
  }
})();
