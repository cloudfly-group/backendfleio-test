(function () {
    'use strict';

    angular.module('fleioStaff')
        .component('pluginsTicketsDepartments', {
            templateUrl: 'staff/plugins/tickets/departments/departments.html',
            controller: PluginsTicketsDepartmentsController,
            bindings: {
                departments: '<',
                createOptions: '<'
            }
        });

    PluginsTicketsDepartmentsController.$inject = ['gettext', 'FlSearchService'];
    function PluginsTicketsDepartmentsController(gettext, FlSearchService){
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            FlSearchService.info.enabled = true;
            FlSearchService.info.label = gettext('Search departments');
            FlSearchService.info.service = $ctrl.departments;
        };

        $ctrl.refreshDepartments = function refreshTickets() {
            $ctrl.departments.fetchData();
        };
    }
})();
