(function () {
    'use strict';

    angular.module('fleioStaff')
        .factory('PluginsTicketsTicketNotesApi', PluginsTicketsTicketNotesApi);

    PluginsTicketsTicketNotesApi.$inject = ['FlResourceService', 'CONFIG'];
    function PluginsTicketsTicketNotesApi(FlResourceService, CONFIG) {
        return FlResourceService(CONFIG.api_url + "/plugins/tickets/ticket_notes/:id/:action", {
            id: '@id',
            action: '@action'
        });
    }

})();
