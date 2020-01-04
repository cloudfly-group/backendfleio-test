(function () {
    'use strict';

    angular.module('fleio')
        .factory('PluginsTicketsDepartmentsApi', PluginsTicketsDepartmentsApi);

    PluginsTicketsDepartmentsApi.$inject = ['FlResourceService', 'CONFIG'];
    function PluginsTicketsDepartmentsApi(FlResourceService, CONFIG) {
        return FlResourceService(CONFIG.api_url + "/plugins/tickets/departments/:id/:action", {
            id: '@id',
            action: '@action'
        });
    }

})();
