(function () {
  'use strict';

  angular.module('fleioStaff')
    .factory('PluginsDomainsPricingApi', PluginsDomainsPricingApi);

  PluginsDomainsPricingApi.$inject = ['FlResourceService', 'CONFIG'];
  function PluginsDomainsPricingApi(FlResourceService, CONFIG) {
    return FlResourceService(CONFIG.api_url + "/plugins/domains/pricing/:id/:action", {
      action: '@action'
    });
  }

})();
