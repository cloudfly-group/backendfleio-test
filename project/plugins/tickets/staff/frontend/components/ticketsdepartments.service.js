(function () {
    'use strict';

    angular.module('fleioStaff')
        .factory('PluginsTicketsDepartmentsApi', PluginsTicketsDepartmentsApi);

    PluginsTicketsDepartmentsApi.$inject = ['FlResourceService', 'CONFIG'];
    function PluginsTicketsDepartmentsApi(FlResourceService, CONFIG) {
        return FlResourceService(CONFIG.api_url + "/plugins/tickets/departments/:id/:action", {
            id: '@id',
            action: '@action'
        });
    }

    // staff signatures
    angular.module('fleioStaff')
        .factory('PluginsTicketsSignaturesApi', PluginsTicketsSignaturesApi);

    PluginsTicketsSignaturesApi.$inject = ['FlResourceService', 'CONFIG'];
    function PluginsTicketsSignaturesApi(FlResourceService, CONFIG) {
        return FlResourceService(CONFIG.api_url + "/plugins/tickets/staff_signatures/:id/:action", {
            id: '@id',
            action: '@action'
        });
    }

})();
