(function () {
  'use strict';

  angular.module('fleio')
    .component('pluginsDomainsDashboardServicesRows', {
      templateUrl: 'plugins/domains/enduser/frontend/components/dashboard_services_rows/dashboardservicesrows.html',
      controller: PluginsDomainsDashboardServicesRowsController,
      bindings: {
          data: '<'
      }
    });
    PluginsDomainsDashboardServicesRowsController.$inject = ['$state', 'PluginsDomainsDomainsApi'];
    function PluginsDomainsDashboardServicesRowsController($state, PluginsDomainsDomainsApi) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {
        $ctrl.loaded = false;
        PluginsDomainsDomainsApi.get({
            'action': 'get_summary'
        }).$promise.then(function(data){
            $ctrl.summary = data;
            $ctrl.loaded = true;
        });
    };

  }

})();
