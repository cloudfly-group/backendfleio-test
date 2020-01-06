(function () {
    'use strict';

    angular.module('fleio')
        .component('pluginsDomainsDomainsActions',{
            templateUrl: 'site/plugins/domains/domains_actions/domainssactions.html',
            controller: pluginsDomainsDomainsActionsController,
            bindings: {
                domain: '<',
                addButton: '<',
                onDomainDeleted: '&',
                onDomainChanged: '&',
                onDomainAdded: '&'
            }
        });

    pluginsDomainsDomainsActionsController.$inject = ['gettextCatalog', '$mdDialog', 'FlUiUtilsService',
        'PluginsDomainsDomainsApi', 'FlNotificationService'];
    function pluginsDomainsDomainsActionsController(gettextCatalog, $mdDialog, FlUiUtilsService,
                                                       PluginsDomainsDomainsApi, FlNotificationService) {
        var $ctrl = this;
    }
})();

