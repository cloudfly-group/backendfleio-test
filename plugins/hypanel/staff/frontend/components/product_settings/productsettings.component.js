(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsHypanelProductSettings', {
      templateUrl: 'staff/plugins/hypanel/product_settings/productsettings.html',
      controller: PluginsHypanelProductSettingsController,
      bindings: {
          data: '='
      },
      require: {
        parentForm: '^form'
      }
    });

  PluginsHypanelProductSettingsController.$inject = ['FlServersApi'];
  function PluginsHypanelProductSettingsController(FlServersApi) {
    var $ctrl = this;
    $ctrl.$onInit = $onInit;

    function $onInit() {
      FlServersApi.Servers.get({
        'filtering': 'plugin__app_label:hypanel'
      }).$promise.then(function (data) {
          $ctrl.servers = data;
        }).catch(function(error) {
          console.error(error);
        });
        if (!$ctrl.data.hypanel_product_settings) {
            $ctrl.data.hypanel_product_settings = {
                'user': 'root',
                'machine_type': 'openvz',
                'ip_count': 1
            };
        }
    }

  }
})();
