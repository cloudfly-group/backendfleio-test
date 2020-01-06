(function () {
    'use strict';

    angular.module('fleioStaff')
        .factory('PluginsTicketsTicketLinkingApi', PluginsTicketsTicketLinkingApi);

    PluginsTicketsTicketLinkingApi.$inject = ['FlResourceService', 'CONFIG'];
    function PluginsTicketsTicketLinkingApi(FlResourceService, CONFIG) {
        return FlResourceService(CONFIG.api_url + "/plugins/tickets/ticket_links/:id/:action", {
            id: '@id',
            action: '@action'
        });
    }

})();
