(function () {
  'use strict';

  angular.module('fleioStaff')
    .factory('PluginsDomainsTLDsApi', PluginsDomainsTLDsApi);

  PluginsDomainsTLDsApi.$inject = ['FlResourceService', 'CONFIG'];
  function PluginsDomainsTLDsApi(FlResourceService, CONFIG) {
    return FlResourceService(CONFIG.api_url + "/plugins/domains/tlds/:id/:action", {
      id: '@id',
      action: '@action'
    });
  }

})();
