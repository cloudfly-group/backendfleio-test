(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsDomainsContacts', {
      templateUrl: 'staff/plugins/domains/contacts/contacts.html',
      controller: PluginsDomainsContactsController,
      bindings: {
        contacts: '<',
        createOptions: '<'
      }
    });

  PluginsDomainsContactsController.$inject = ['FlSearchService', 'gettext', 'FlDetectIdleService', 'FlOsTimer'];
  function PluginsDomainsContactsController(FlSearchService, gettext) {
    var $ctrl = this;
    var refreshTimer;

    $ctrl.$onInit = function onInit() {
      FlSearchService.info.enabled = true;
      FlSearchService.info.label = gettext('Search contacts');
      FlSearchService.info.service = $ctrl.contacts;
    };

    $ctrl.refreshContacts = function refreshContacts() {
      $ctrl.contacts.fetchData();
    };

    $ctrl.$onDestroy = function onDestroy() {
    };
  }

})();
