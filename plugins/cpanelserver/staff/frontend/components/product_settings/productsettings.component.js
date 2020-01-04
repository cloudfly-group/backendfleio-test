(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsCpanelserverProductSettings', {
      templateUrl: 'staff/plugins/cpanelserver/product_settings/productsettings.html',
      controller: PluginsCpanelserverProductSettingsController,
      bindings: {
          data: '='
      },
      require: {
        parentForm: '^form'
      }
    });

  PluginsCpanelserverProductSettingsController.$inject = ['FlServersApi'];
  function PluginsCpanelserverProductSettingsController(FlServersApi) {
    var $ctrl = this;
    $ctrl.$onInit = $onInit;

    function $onInit() {
      $ctrl.data['moduleConfigurationForm'] = 'cpanelserver_product_settings';
      var groups = FlServersApi.ServerGroups.get()
        .$promise.then(function (data) {
          $ctrl.groups = data;
        }).catch(function(error) {
          console.error(error);
        });
        if (!$ctrl.data.cpanelserver_product_settings) {
            $ctrl.data.cpanelserver_product_settings = {};
        }
    }
  }
})();
