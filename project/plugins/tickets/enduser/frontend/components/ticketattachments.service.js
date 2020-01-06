(function () {
    'use strict';

    angular.module('fleio')
        .factory('PluginsTicketsTicketAttachmentsApi', PluginsTicketsTicketAttachmentsApi);

    PluginsTicketsTicketAttachmentsApi.$inject = ['FlResourceService', 'CONFIG'];
    function PluginsTicketsTicketAttachmentsApi(FlResourceService, CONFIG) {
        return FlResourceService(CONFIG.api_url + "/plugins/tickets/ticket_attachments/:id/:action", {
            id: '@id',
            action: '@action'
        }, {
            'upload': {
                method: 'POST',
                transformRequest: angular.identity,
                headers: {
                    'Content-Type': undefined
                }
            }
        });
    }

})();
