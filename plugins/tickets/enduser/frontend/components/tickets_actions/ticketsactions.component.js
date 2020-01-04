(function () {
    'use strict';

    angular.module('fleio')
        .component('pluginsTicketsTicketsActions',{
            templateUrl: 'enduser/plugins/tickets/tickets/ticketsactions.html',
            controller: PluginsTicketsTicketsActionsController,
            bindings: {
                ticket: '=',
                addButton: '<'
            }
        });

    PluginsTicketsTicketsActionsController.$inject = ['$state', 'FlNotificationService', 'gettextCatalog', 'PluginsTicketsTicketsApi', 'FlResolveErrorHandler'];
    function PluginsTicketsTicketsActionsController($state, FlNotificationService, gettextCatalog, PluginsTicketsTicketsApi, FlResolveErrorHandler) {
        var $ctrl = this;

        $ctrl.editTicket = function editTicket() {
            $state.go('pluginsTicketsTicketsEdit', {
                'id': $ctrl.ticket.id
            });
        };

        $ctrl.refreshTicket = function refreshTicket() {
            PluginsTicketsTicketsApi.get({'id':$ctrl.ticket.id}).$promise
                .then(function (data) {
                    $ctrl.ticket = data;
                }).catch(FlResolveErrorHandler.handleError);
        };

        $ctrl.reopenTicket = function reopenTicket() {
            PluginsTicketsTicketsApi.post({
                'id': $ctrl.ticket.id,
                'action': 'reopen_ticket'
            }).$promise.then(function(data){
                FlNotificationService.add(gettextCatalog.getString('Ticket reopened.'));
                $ctrl.refreshTicket();
            });
        };

        $ctrl.closeTicket = function closeTicket() {
            PluginsTicketsTicketsApi.post({
                'id': $ctrl.ticket.id,
                'action': 'close_ticket'
            }).$promise.then(function(data){
                FlNotificationService.add(gettextCatalog.getString('Ticket closed.'));
                $ctrl.refreshTicket();
            });
        };

    }
})();

