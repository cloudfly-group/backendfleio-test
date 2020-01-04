(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsOpenstackProductSettings', {
      templateUrl: 'staff/openstack/product_settings/productsettings.html',
      controller: PluginsOpenstackProductSettingsController,
      bindings: {
          data: '='
      },
      require: {
        parentForm: '^form'
      }
    });

  PluginsOpenstackProductSettingsController.$inject = ['FlRegionApi', 'FlResolveErrorHandler', '$scope'];
  function PluginsOpenstackProductSettingsController(FlRegionApi, FlResolveErrorHandler, $scope) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {
      $ctrl.data['moduleConfigurationForm'] = 'openstack_product_settings';
      FlRegionApi.get().$promise.then(function(data) {
        $ctrl.regions = data.objects;
      }).catch(FlResolveErrorHandler.handleError);

      $ctrl.RunGetMeANetworkChanged = function() {
          if ($ctrl.data.openstack_product_settings.run_get_me_a_network_on_auto_setup === true) {
             if ($ctrl.regions && $ctrl.regions.length === 1) {
                 $ctrl.data.openstack_product_settings.network_auto_allocated_topology_regions = [$ctrl.regions[0].id];
             }
          }
      }
    };

  }
})();
