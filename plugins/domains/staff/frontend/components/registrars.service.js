(function () {
  'use strict';

  angular.module('fleioStaff')
    .factory('PluginsDomainsRegistrarsApi', PluginsDomainsRegistrarsApi);

  PluginsDomainsRegistrarsApi.$inject = ['FlResourceService', 'CONFIG'];
  function PluginsDomainsRegistrarsApi(FlResourceService, CONFIG) {
    return FlResourceService(CONFIG.api_url + "/plugins/domains/registrars/:id/:action", {
      id: '@id',
      action: '@action'
    });
  }

})();
