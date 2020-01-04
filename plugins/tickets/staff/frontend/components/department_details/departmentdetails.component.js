(function(){
    'use strict';
    angular.module('fleioStaff')
        .component('pluginsTicketsDepartmentDetails', {
            templateUrl: 'staff/plugins/tickets/department_details/departmentdetails.html',
            controller: PluginsTicketsDepartmentDetailsController,
            bindings: {
                department: '<',
                createOptions: '<',
            }
        });

    PluginsTicketsDepartmentDetailsController.$inject = ['$state', 'gettextCatalog', 'FlNotificationService',
        'FlResolveErrorHandler', 'PluginsTicketsDepartmentsApi', 'FlUiUtilsService'];
    function PluginsTicketsDepartmentDetailsController($state, gettextCatalog, FlNotificationService,
        FlResolveErrorHandler, PluginsTicketsDepartmentsApi, FlUiUtilsService) {
        var $ctrl = this;

        $ctrl.$onInit = function $onInit(){
            $ctrl.goBackOrToState = FlUiUtilsService.goBackOrToState;
        };

        $ctrl.addTicketIdShortKey = function(str) {
            if (typeof $ctrl.department.ticket_id_format === 'undefined') {
                $ctrl.department.ticket_id_format = '';
            }
            $ctrl.department.ticket_id_format = $ctrl.department.ticket_id_format + str;
        };

        $ctrl.goBackToList = function() {
            $state.go('pluginsTicketsDepartments');
        };

        $ctrl.saveDepartment = function () {
            document.activeElement.blur();
            if (!($ctrl.editDepartment.$invalid || $ctrl.submitPending)) {
                $ctrl.submitPending = true;

                return PluginsTicketsDepartmentsApi.update($ctrl.department)
                    .$promise.then(function (data) {
                        FlNotificationService.add(gettextCatalog.getString('Department successfully updated'));
                        return $state.go('pluginsTicketsDepartments');
                    }).catch(function (error) {
                        $ctrl.submitPending = false;
                        $ctrl.backendErrors = error.data;
                    });
            }
        };

    }
})();
