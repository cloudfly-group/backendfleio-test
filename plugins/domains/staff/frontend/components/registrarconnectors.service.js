(function () {
  'use strict';

  angular.module('fleioStaff')
    .factory('PluginsDomainsRegistrarConnectorsApi', PluginsDomainsRegistrarConnectorsApi);

  PluginsDomainsRegistrarConnectorsApi.$inject = ['FlResourceService', 'CONFIG'];
  function PluginsDomainsRegistrarConnectorsApi(FlResourceService, CONFIG) {
    return FlResourceService(CONFIG.api_url + "/plugins/domains/registrar_connectors/:id/:action", {
      id: '@id',
      action: '@action'
    });
  }

})();
