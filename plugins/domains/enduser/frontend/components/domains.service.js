(function () {
  'use strict';

  angular.module('fleio')
    .factory('PluginsDomainsDomainsApi', PluginsDomainsDomainsApi);

  PluginsDomainsDomainsApi.$inject = ['FlResourceService', 'CONFIG'];
  function PluginsDomainsDomainsApi(FlResourceService, CONFIG) {
    return FlResourceService(CONFIG.api_url + "/plugins/domains/domains/:id/:action", {
      id: '@id',
      action: '@action'
    });
  }

})();
