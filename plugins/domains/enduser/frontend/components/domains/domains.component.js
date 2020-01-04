(function () {
  'use strict';

  angular.module('fleio')
    .component('pluginsDomainsDomains', {
      templateUrl: 'site/plugins/domains/domains/domains.html',
      controller: PluginsDomainsDomainsController,
      bindings: {
          domains: '<'
      }
    });

  PluginsDomainsDomainsController.$inject = ['gettext', 'FlSearchService'];
  function PluginsDomainsDomainsController(gettext, FlSearchService){
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {
      FlSearchService.info.enabled = true;
      FlSearchService.info.label = gettext('Search Domains');
      FlSearchService.info.service = $ctrl.domains;
    };

    $ctrl.refreshDomains = function refreshDomains() {
      $ctrl.domains.fetchData();
    };
  }
})();
