(function(){
    'use strict';
    angular.module('fleioStaff')
        .component('pluginsTicketsTicketsCreate', {
            templateUrl: 'enduser/plugins/tickets/tickets_create/ticketscreate.html',
            controller: PluginsTicketsTicketsCreateController,
            bindings: {
                createOptions: '<',
                preselectedClient: '<',
            }
        });

    PluginsTicketsTicketsCreateController.$inject = ['$state', 'gettextCatalog', 'PluginsTicketsTicketsApi',
        'FlNotificationService', 'FlResolveErrorHandler', 'FlClientApi', 'CONFIG',
        'PluginsTicketsTicketAttachmentsApi', 'PluginsTicketsDepartmentsApi', '$q', '$scope', 'FlLocalStorage'];
    function PluginsTicketsTicketsCreateController($state, gettextCatalog, PluginsTicketsTicketsApi,
        FlNotificationService, FlResolveErrorHandler, FlClientApi, CONFIG,
        PluginsTicketsTicketAttachmentsApi, PluginsTicketsDepartmentsApi, $q, $scope, FlLocalStorage) {
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            var defaultTicketTemplate = {
                'priority': 'medium',
                'status': 'open',
                'internal_status': null,
                'description': ''
            };
            $ctrl.statusesKeys = Object.keys($ctrl.createOptions.statuses);
            $ctrl.internalStatusesKeys = Object.keys($ctrl.createOptions.internal_statuses);
            $ctrl.prioritiesKeys = Object.keys($ctrl.createOptions.priorities);
            $ctrl.tinymceOptions = CONFIG.tiny_mce_options;
            $ctrl.tinymceOptions['height'] = 300;
            if (!$ctrl.preselectedClient) {
                var temporarySavedCreateForm = JSON.parse(FlLocalStorage.get('newTicket', true));
                if (temporarySavedCreateForm) {
                    $ctrl.ticket = temporarySavedCreateForm;
                    if (temporarySavedCreateForm.client) {
                        $ctrl.preselectClient(temporarySavedCreateForm.client);
                    }
                    if (temporarySavedCreateForm.department) {
                        $ctrl.preselectDepartment(temporarySavedCreateForm.department);
                    }
                } else {
                    $ctrl.ticket = defaultTicketTemplate;
                }
            } else {
                $ctrl.ticket = defaultTicketTemplate;
                $ctrl.preselectClient($ctrl.preselectedClient);
            }
            if (!$ctrl.ticket.description.length) {
                if ($ctrl.createOptions.user_signature) {
                    $ctrl.ticket.description = '<br>' + $ctrl.createOptions.user_signature;
                } else {
                    $ctrl.ticket.description = '';
                }
            }
            // get maximum allowed attachment file size
            $ctrl.maxFileSize = $ctrl.createOptions['MAX_TICKET_ATTACHMENT_SIZE'];
            var i = Math.floor(Math.log($ctrl.maxFileSize) / Math.log(1024));
            var sizes = ['B', 'KB', 'MB', 'GB'];
            $ctrl.maxFileSizeReadable = 'Max. ' + (
                ($ctrl.maxFileSize / Math.pow(1024, i)).toFixed(2) * 1 + ' ' + sizes[i]
            ) + ' / file';

            $scope.$watch("$ctrl.ticket", function(newValue, oldValue){
                FlLocalStorage.set('newTicket', JSON.stringify(newValue), true);
            }, true); // deep watch enabled
        };

        $ctrl.preselectClient = function(preselectedClientId) {
            FlClientApi.get({
                'id': preselectedClientId
            }).$promise.then(function(data) {
                $ctrl.selectedClient = data;
                $ctrl.ticket.client = data.id;
            }).catch(function(error) {
                FlNotificationService.add(gettextCatalog.getString('Could not preselect client'));
                delete $ctrl.ticket.client;
            });
        };

        $ctrl.preselectDepartment = function (preselectedDepartmentId) {
            if (preselectedDepartmentId) {
                PluginsTicketsDepartmentsApi.get({
                    'id': preselectedDepartmentId
                }).$promise.then(function (data) {
                    $ctrl.selectedDepartment = data;
                    $ctrl.departmentChanged();
                }).catch(function(error) {
                    delete $ctrl.ticket.department;
                    FlNotificationService.add(gettextCatalog.getString('Could not preselect department'));
                });
            }
        };

        $ctrl.departmentChanged = function () {
            if ($ctrl.selectedDepartment) {
                $ctrl.ticket.department = $ctrl.selectedDepartment.id;
            } else {
                $ctrl.ticket.department = null;
            }
        };

        $ctrl.selectedClientChange = function() {
            if ($ctrl.selectedClient) {
                $ctrl.ticket.client = $ctrl.selectedClient.id;
            } else {
                delete $ctrl.ticket.client;
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
                // Create a new ticket
                var files_to_upload = document.getElementById('ticket_attachment').files;
                if (files_to_upload.length) {
                    // if we have files to upload, upload them then create ticket and make the
                    // association in the backend
                    for (var i = 0; i < files_to_upload.length; i++) {
                        // check each file size
                        if (files_to_upload[i].size > $ctrl.maxFileSize) {
                            $ctrl.backendErrors = {
                                'detail': gettextCatalog.getString('Attachment file size is too big.')
                            };
                            $ctrl.submitPending = false;
                            return;
                        }
                    }
                    var queriesList = [];
                    $ctrl.uploadInProgress = true;
                    for (var j = 0; j < files_to_upload.length; j++) {
                        var file_to_process = files_to_upload[j];
                        var fd = new FormData();
                        fd.append('data', file_to_process);
                        fd.append('file_name', file_to_process.name);
                        queriesList.push(PluginsTicketsTicketAttachmentsApi.upload(fd).$promise);
                    }

                    $q.all(queriesList).then(function(data) {
                        var attachmentIds = '';
                        for (var data_pos = 0; data_pos < data.length; data_pos++) {
                            attachmentIds = attachmentIds + data[data_pos].id;
                            if (data_pos < data.length - 1) {
                                attachmentIds = attachmentIds + ',';
                            }
                        }
                        $ctrl.ticket.associated_attachment_ids = attachmentIds;
                        $ctrl.uploadInProgress = false;
                        return PluginsTicketsTicketsApi.save($ctrl.ticket).$promise.then(function (ticket) {
                            $ctrl.submitPending = false;
                            FlLocalStorage.removeItem('newTicket', true);
                            $state.go('pluginsTicketsTicketsDetails', {'id': ticket.id});
                            FlNotificationService.add(gettextCatalog.getString('Ticket successfully opened.'));
                        }).catch(function (err) {
                            $ctrl.submitPending = false;
                            $ctrl.backendErrors = err.data;
                        });
                    }).catch(function(error) {
                        $ctrl.submitPending = false;
                        $ctrl.uploadInProgress = false;
                        $ctrl.backendErrors = error.data;
                    });
                } else {
                    // TICKET CREATION WITHOUT ATTACHMENT
                    return PluginsTicketsTicketsApi.save($ctrl.ticket)
                        .$promise.then(function (data) {
                            $ctrl.submitPending = false;
                            $state.go('pluginsTicketsTicketsDetails', {'id': data.id});
                            FlNotificationService.add(gettextCatalog.getString('Ticket successfully opened.'));
                            FlLocalStorage.removeItem('newTicket', true);
                            return data;
                        }).catch(function (error) {
                            $ctrl.submitPending = false;
                            $ctrl.backendErrors = error.data;
                        });
                }
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

        $ctrl.close = function () {
            return $mdDialog.cancel();
        };

    }
})();
