(function(){
    'use strict';
    angular.module('fleioStaff')
        .component('pluginsTicketsTicketsEdit', {
            templateUrl: 'staff/plugins/tickets/tickets_edit/ticketsedit.html',
            controller: PluginsTicketsTicketsEditController,
            bindings: {
                ticket: '<',
                createOptions: '<'
            }
        });

    PluginsTicketsTicketsEditController.$inject = ['$state', 'gettextCatalog', 'PluginsTicketsTicketsApi',
        'FlNotificationService', 'FlResolveErrorHandler', 'FlClientApi', 'CONFIG',
        'PluginsTicketsTicketAttachmentsApi', 'PluginsTicketsDepartmentsApi', 'FlUiUtilsService'];
    function PluginsTicketsTicketsEditController($state, gettextCatalog, PluginsTicketsTicketsApi,
                                                   FlNotificationService, FlResolveErrorHandler, FlClientApi, CONFIG,
                                                   PluginsTicketsTicketAttachmentsApi, PluginsTicketsDepartmentsApi, FlUiUtilsService) {
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            $ctrl.statusesKeys = Object.keys($ctrl.createOptions.statuses);
            $ctrl.internalStatusesKeys = Object.keys($ctrl.createOptions.internal_statuses);
            $ctrl.prioritiesKeys = Object.keys($ctrl.createOptions.priorities);
            $ctrl.tinymceOptions = CONFIG.tiny_mce_options;
            $ctrl.tinymceOptions['height'] = 300;
            if ($ctrl.ticket.client) {
                FlClientApi.get({'id': $ctrl.ticket.client}).$promise.then(function (data) {
                    $ctrl.selectedClient = data;
                });
            }
            if ($ctrl.ticket.department) {
                PluginsTicketsDepartmentsApi.get({'id': $ctrl.ticket.department}).$promise.then(function (data) {
                    $ctrl.selectedDepartment = data;
                });
            }
            $ctrl.goBackOrToState = FlUiUtilsService.goBackOrToState;
        };

        $ctrl.departmentChanged = function () {
            if ($ctrl.selectedDepartment) {
                $ctrl.ticket.department = $ctrl.selectedDepartment.id;
            } else {
                $ctrl.ticket.department = null;
            }
        };

        $ctrl.saveTicket = function () {
            document.activeElement.blur();
            if (!($ctrl.editTicket.$invalid || $ctrl.submitPending)) {
                $ctrl.submitPending = true;
                if ($ctrl.selectedClient) {
                    $ctrl.ticket.client = $ctrl.selectedClient.id;
                } else {
                    $ctrl.ticket.client = null;
                }

                if (!$ctrl.selectedDepartment) {
                    $ctrl.noValidDepartment = true;
                    $ctrl.submitPending = false;
                    return;
                }

                return PluginsTicketsTicketsApi.update($ctrl.ticket)
                    .$promise.then(function (data) {
                        $ctrl.submitPending = false;
                        $state.go('pluginsTicketsTicketsDetails', {
                            'id': data.id
                        });
                        FlNotificationService.add(gettextCatalog.getString('Ticket successfully updated.'));
                        return data;
                    }).catch(function (error) {
                        $ctrl.submitPending = false;
                        $ctrl.backendErrors = error.data;
                    });
            }
        };

        $ctrl.searchClient = function searchClient(input) {
            return FlClientApi.get({'search': input}).$promise.then(function (data) {
                return data.objects;
            })
        };

        $ctrl.searchDepartment = function searchDepartment(input) {
            $ctrl.noValidDepartment = false;
            return PluginsTicketsDepartmentsApi.get({'search': input}).$promise.then(function (data) {
                return data.objects;
            })
        };

    }
})();
