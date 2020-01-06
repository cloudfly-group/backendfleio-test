(function () {
    'use strict';

    angular.module('fleioStaff')
        .component('pluginsTicketsTicketsActions',{
            templateUrl: 'staff/plugins/tickets/tickets/ticketsactions.html',
            controller: PluginsTicketsTicketsActionsController,
            bindings: {
                ticket: '=',
                addButton: '<',
                onTicketDeleted: '&',
            }
        });

    PluginsTicketsTicketsActionsController.$inject = ['gettextCatalog', '$state', 'FlUiUtilsService', 'PluginsTicketsTicketsApi', 'FlNotificationService', 'FlResolveErrorHandler', '$mdDialog'];
    function PluginsTicketsTicketsActionsController(gettextCatalog, $state, FlUiUtilsService, PluginsTicketsTicketsApi, FlNotificationService, FlResolveErrorHandler, $mdDialog) {
        var $ctrl = this;

        $ctrl.deleteTicket = function deleteTicket() {
            FlUiUtilsService.yesNoDlg(gettextCatalog.getString('Are you sure?'), gettextCatalog.getString('Delete ticket'))
                .then(function () {
                    PluginsTicketsTicketsApi.delete({'id':$ctrl.ticket.id}).$promise
                        .then(function () {
                            FlNotificationService.add(gettextCatalog.getString('Ticket deleted'));
                            $ctrl.onTicketDeleted();
                        });
                }).catch(function () {});
        };

        $ctrl.editTicket = function editTicket() {
            $state.go('pluginsTicketsTicketsEdit', {
                id: $ctrl.ticket.id
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

        $ctrl.addLinking = function addLinking() {
            return $mdDialog.show({
                templateUrl: 'staff/plugins/tickets/tickets_actions/dialogs/ticket_linking/ticketlinking.html',
                controller: 'PluginsTicketsTicketLinkingController',
                controllerAs: '$ctrl',
                parent: angular.element(document.body),
                clickOutsideToClose: false,
                locals: {
                    ticket: $ctrl.ticket,
                },
            }).then(function () {
                FlNotificationService.add(gettextCatalog.getString('Linking created'));
                $ctrl.refreshTicket();
            }).catch(function(){});
        };

    }
})();

