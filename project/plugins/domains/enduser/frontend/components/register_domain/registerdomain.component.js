(function () {
  'use strict';

  angular.module('fleio')
    .component('pluginsDomainsRegisterDomain', {
      templateUrl: 'site/plugins/domains/register_domain/registerdomain.html',
      controller: PluginsDomainsRegisterDomainController,
      bindings: {
          clientCreateOptions: '<'
      }
    });

  PluginsDomainsRegisterDomainController.$inject = [];
  function PluginsDomainsRegisterDomainController(){
  }
})();
