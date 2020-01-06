(function () {
    'use strict';

    angular.module('fleio')
        .component('pluginsTicketsTickets', {
            templateUrl: 'staff/plugins/tickets/tickets/tickets.html',
            controller: PluginsTicketsTicketsController,
            bindings: {
                tickets: '<',
                createOptions: '<'
            }
        });

    PluginsTicketsTicketsController.$inject = ['gettext', 'FlSearchService', 'FlOsTimer', 'FlDetectIdleService'];
    function PluginsTicketsTicketsController(gettext, FlSearchService, FlOsTimer, FlDetectIdleService){
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            FlSearchService.info.enabled = true;
            FlSearchService.info.label = gettext('Search tickets');
            FlSearchService.info.service = $ctrl.tickets;
            $ctrl.refreshTimer = FlOsTimer($ctrl.refreshTickets, 30000);
            $ctrl.refreshTimer.start();
            FlDetectIdleService.init(function () {
                return $ctrl.refreshTimer.start();
            }, function () {
                return $ctrl.refreshTimer.stop();
            });
        };

        $ctrl.$onDestroy = function onDestroy() {
            $ctrl.refreshTimer.teardown();
            FlDetectIdleService.uninit();
        };

        $ctrl.refreshTickets = function refreshTickets() {
            $ctrl.tickets.fetchData();
        };

        $ctrl.onTicketDeleted = function onTicketDeleted() {

        };
    }
})();
