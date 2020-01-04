(function () {
    'use strict';

    angular.module('fleioStaff')
        .controller('PluginsTicketsRemoveLinkingController', PluginsTicketsRemoveLinkingController);

    PluginsTicketsRemoveLinkingController.$inject = ['$mdDialog', 'ticket', 'linkedTicket', 'PluginsTicketsTicketLinkingApi',
        'FlNotificationService', 'gettextCatalog'];
    function PluginsTicketsRemoveLinkingController($mdDialog, ticket, linkedTicket, PluginsTicketsTicketLinkingApi,
       FlNotificationService, gettextCatalog) {
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            $ctrl.loadingLink = true;
            $ctrl.ticket = angular.copy(ticket);
            $ctrl.linkedTicket = angular.copy(linkedTicket);
            PluginsTicketsTicketLinkingApi.get({
                'ticket': $ctrl.ticket,
                'linked_ticket': $ctrl.linkedTicket
            }).$promise.then(function (data) {
                $ctrl.loadingLink = false;
                $ctrl.link = data.objects[0].id;
            }).catch(function (err) {
                $ctrl.loadingLink = false;
                FlNotificationService.add(gettextCatalog.getString('Failed to retrieve the link'));
                console.error(err);
                return $mdDialog.cancel();
            });
            $ctrl.isSymmetrical = false;
        };

        $ctrl.removeLink = function removeLink() {
            $ctrl.submitPending = true;
            PluginsTicketsTicketLinkingApi.post({
                'id': $ctrl.link,
                'delete_symmetrical': $ctrl.isSymmetrical,
                'action': 'delete_link'
            }).$promise.then(function (data) {
                $mdDialog.hide(data);
                return data;
            }).catch(function (error) {
                $ctrl.submitPending = false;
                $ctrl.backendErrors = error.data;
            });
        };

        $ctrl.close = function close() {
            return $mdDialog.cancel();
        };
    }

})();
