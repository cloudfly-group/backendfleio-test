(function () {
    'use strict';

    angular.module('fleio')
        .factory('PluginsTicketsTicketUpdatesApi', PluginsTicketsTicketUpdatesApi);

    PluginsTicketsTicketUpdatesApi.$inject = ['FlResourceService', 'CONFIG'];
    function PluginsTicketsTicketUpdatesApi(FlResourceService, CONFIG) {
        return FlResourceService(CONFIG.api_url + "/plugins/tickets/ticket_updates/:id/:action", {
            id: '@id',
            action: '@action'
        });
    }

})();
