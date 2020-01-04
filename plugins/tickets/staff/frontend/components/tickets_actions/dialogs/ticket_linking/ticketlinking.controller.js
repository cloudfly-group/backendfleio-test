(function () {
    'use strict';

    angular.module('fleioStaff')
        .controller('PluginsTicketsTicketLinkingController', PluginsTicketsTicketLinkingController);

    PluginsTicketsTicketLinkingController.$inject = ['$mdDialog', 'ticket', 'PluginsTicketsTicketLinkingApi',
        'PluginsTicketsTicketsApi', 'FlNotificationService', 'gettextCatalog'];
    function PluginsTicketsTicketLinkingController($mdDialog, ticket, PluginsTicketsTicketLinkingApi,
        PluginsTicketsTicketsApi, FlNotificationService, gettextCatalog) {
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            $ctrl.currentTicket = angular.copy(ticket);
            $ctrl.isSymmetrical = false;
        };

        $ctrl.searchTickets = function searchTickets(input) {
            return PluginsTicketsTicketsApi.post({
                'search': input,
                'action': 'get_tickets_for_linking',
                'ticket_id': $ctrl.currentTicket.id
            }).$promise.then(function (data) {
                return data.objects;
            });
        };

        $ctrl.linkTickets = function linkTickets() {
            if (!$ctrl.selectedTicket) {
                return FlNotificationService.add(gettextCatalog.getString('Please select a ticket first.'));
            }
            return PluginsTicketsTicketLinkingApi.save({
                'ticket': $ctrl.currentTicket.id,
                'linked_ticket': $ctrl.selectedTicket.id,
                'symmetrical': $ctrl.isSymmetrical
            }).$promise.then(function (data) {
                $mdDialog.hide(data);
                return data;
            }).catch(function (error) {
                $ctrl.backendErrors = error.data;
            });
        };

        $ctrl.close = function close() {
            return $mdDialog.cancel();
        };
    }

})();
