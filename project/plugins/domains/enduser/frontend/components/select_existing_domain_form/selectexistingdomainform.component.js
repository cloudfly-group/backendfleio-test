(function(){
  'use strict';
  angular.module('fleio')
  .component('pluginsDomainsSelectExistingDomainForm', {
    templateUrl: 'site/plugins/domains/select_existing_domain_form/selectexistingdomainform.html',
    controller: PluginsDomainsSelectExistingDomainFormController,
    bindings: {
      domains: '=',
      selectedDomainName: '='
    }
  });

  PluginsDomainsSelectExistingDomainFormController.$inject = [];
  function PluginsDomainsSelectExistingDomainFormController() {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
    };

    $ctrl.selectedDomainChanged = function selectedDomainChanged(domain) {
      if (typeof domain !== 'undefined') {
        $ctrl.selectedDomainName = domain.name;
      } else {
        $ctrl.selectedDomainName = ''
      }
    };

    $ctrl.searchDomain = function searchDomain(input) {
      return $ctrl.domains.filter(function(domain) {
        return domain.name.includes(input);
      });
    };
  }
})();
