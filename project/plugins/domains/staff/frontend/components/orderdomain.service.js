(function () {
  'use strict';

  angular.module('fleioStaff')
    .factory('PluginsDomainsOrderDomainApi', PluginsDomainsOrderDomainApi);

  PluginsDomainsOrderDomainApi.$inject = ['FlResourceService', 'CONFIG'];
  function PluginsDomainsOrderDomainApi(FlResourceService, CONFIG) {
    return FlResourceService(CONFIG.api_url + "/plugins/domains/order-domain/:action", {
      action: '@action'
    });
  }

})();
