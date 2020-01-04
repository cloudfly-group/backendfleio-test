(function(){
    'use strict';
    angular.module('fleioStaff')
        .component('pluginsTicketsDepartmentCreate', {
            templateUrl: 'staff/plugins/tickets/department_create/departmentcreate.html',
            controller: PluginsTicketsDepartmentCreateController,
            bindings: {
                createOptions: '<',
            }
        });

    PluginsTicketsDepartmentCreateController.$inject = ['$state', 'gettextCatalog', 'FlNotificationService',
        'FlResolveErrorHandler', 'PluginsTicketsDepartmentsApi', 'FlUiUtilsService'];
    function PluginsTicketsDepartmentCreateController($state, gettextCatalog, FlNotificationService,
                                                       FlResolveErrorHandler, PluginsTicketsDepartmentsApi, FlUiUtilsService) {
        var $ctrl = this;

        $ctrl.$onInit = function $onInit(){
            $ctrl.goBackOrToState = FlUiUtilsService.goBackOrToState;
            $ctrl.department = {
                ticket_id_format: $ctrl.createOptions.ticket_id_default_format,
            };
            var notifications = angular.copy($ctrl.createOptions['notifications']);
            for (var key in notifications) {
                if (notifications.hasOwnProperty(key)) {
                    $ctrl.department[key] = notifications[key];
                }
            }
        };

        $ctrl.addTicketIdShortKey = function(str) {
            if (typeof $ctrl.department.ticket_id_format === 'undefined') {
                $ctrl.department.ticket_id_format = '';
            }
            $ctrl.department.ticket_id_format = $ctrl.department.ticket_id_format + str;
        };

        $ctrl.saveDepartment = function () {
            document.activeElement.blur();
            if (!($ctrl.editDepartment.$invalid || $ctrl.submitPending)) {
                $ctrl.submitPending = true;
            }

            return PluginsTicketsDepartmentsApi.save($ctrl.department)
                .$promise.then(function (data) {
                    FlNotificationService.add(gettextCatalog.getString('Department successfully created'));
                    return $state.go('pluginsTicketsDepartments');
                }).catch(function (error) {
                    $ctrl.submitPending = false;
                    $ctrl.backendErrors = error.data;
                });
        };

    }
})();
