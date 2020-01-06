(function () {
  'use strict';

  angular.module('fleio')
    .component('pluginsDomainsContacts', {
      templateUrl: 'site/plugins/domains/contacts/contacts.html',
      controller: PluginsDomainsContactsController,
      bindings: {
        contacts: '<',
        createOptions: '<'
      }
    });

  PluginsDomainsContactsController.$inject = ['FlSearchService', 'gettext', 'FlDetectIdleService', 'FlOsTimer'];
  function PluginsDomainsContactsController(FlSearchService, gettext) {
    var $ctrl = this;

    $ctrl.$onInit = function onInit() {
      FlSearchService.info.enabled = true;
      FlSearchService.info.label = gettext('Search contacts');
      FlSearchService.info.service = $ctrl.contacts;
    };

    $ctrl.refreshContacts = function refreshContacts() {
      $ctrl.contacts.fetchData();
    };
  }

})();
