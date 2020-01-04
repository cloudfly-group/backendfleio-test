(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsDomainsRegistrars', {
      templateUrl: 'staff/plugins/domains/registrars/registrars.html',
      controller: PluginsDomainsRegistrarsController,
      bindings: {
          'registrars': '<'
      }
    });

  PluginsDomainsRegistrarsController.$inject = ['gettext', 'FlSearchService'];
  function PluginsDomainsRegistrarsController(gettext, FlSearchService){
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {
      FlSearchService.info.enabled = true;
      FlSearchService.info.label = gettext('Search Registrars');
      FlSearchService.info.service = $ctrl.registrars;
    };

    $ctrl.refreshRegistrars = function refreshDomains() {
      $ctrl.registrars.fetchData();
    };
  }
})();
