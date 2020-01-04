(function () {
  'use strict';

  angular.module('fleio')
    .factory('PluginsDomainsContactsApi', PluginsDomainsContactsApi);

  PluginsDomainsContactsApi.$inject = ['FlResourceService', 'CONFIG'];
  function PluginsDomainsContactsApi(FlResourceService, CONFIG) {
    return FlResourceService(CONFIG.api_url + "/plugins/domains/contacts/:id/:action", {
      id: '@id',
      action: '@action'
    });
  }

})();
