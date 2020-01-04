(function () {
    'use strict';

    angular.module('fleioStaff')
        .component('pluginsTicketsDepartmentsActions',{
            templateUrl: 'staff/plugins/tickets/departments_actions/departmentsactions.html',
            controller: PluginsTicketsDepartmentsActionsController,
            bindings: {
                department: '<',
                addButton: '<',
                editButton: '<',
                createOptions: '<',
                onDepartmentDeleted: '&',
                onDepartmentChanged: '&',
                onDepartmentAdded: '&'
            }
        });

    PluginsTicketsDepartmentsActionsController.$inject = ['gettextCatalog', '$mdDialog', 'FlUiUtilsService', 'PluginsTicketsDepartmentsApi', 'FlNotificationService'];
    function PluginsTicketsDepartmentsActionsController(gettextCatalog, $mdDialog, FlUiUtilsService, PluginsTicketsDepartmentsApi, FlNotificationService) {
        var $ctrl = this;

        $ctrl.deleteDepartment = function deleteDepartment() {
            FlUiUtilsService.yesNoDlg(gettextCatalog.getString('Are you sure?'), gettextCatalog.getString('Delete department'))
                .then(function () {
                    PluginsTicketsDepartmentsApi.delete({'id':$ctrl.department.id}).$promise
                        .then(function () {
                            FlNotificationService.add(gettextCatalog.getString('Department deleted'));
                            $ctrl.onDepartmentDeleted();
                        });
                }).catch(function () {});
        };

    }
})();

