(function () {
  'use strict';

  angular.module('fleioStaff')
    .factory('PluginsRegistrarPricesApi', PluginsRegistrarPricesApi);

  PluginsRegistrarPricesApi.$inject = ['FlResourceService', 'CONFIG'];
  function PluginsRegistrarPricesApi(FlResourceService, CONFIG) {
    return FlResourceService(CONFIG.api_url + "/plugins/domains/registrar_prices/:id/:action", {
      action: '@action'
    });
  }

})();
