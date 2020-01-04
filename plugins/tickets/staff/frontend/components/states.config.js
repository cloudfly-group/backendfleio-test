(function () {
    'use strict';

    function getStates(CONFIG, gettext) {
        var ticketsTicketsState = {
            name: 'pluginsTicketsTickets',
            url: CONFIG.base_url + 'tickets?page_size?ordering?search?filtering',
            component: 'pluginsTicketsTickets',
            authenticate: true,
            showSearch: true,
            reloadOnSearch: false,
            params: {
                page_size: {
                    value: CONFIG.paginate_by,
                    squash: true
                },
                ordering: {
                    value: '-last_reply_at',
                    squash: true
                },
                filtering: {
                    value: 'internal_status__ne:done',
                    squash: true
                }
            },
            resolve: {
                tickets: [
                    '$stateParams', 'FlObjectList', 'PluginsTicketsTicketsApi', '$state', 'gettextCatalog', function (
                        $stateParams,
                        FlObjectList,
                        PluginsTicketsTicketsApi,
                        $state,
                        gettextCatalog,
                    ) {
                        $state.get('pluginsTicketsTickets').data.filtering.status.choices = [
                            {
                                'display': gettextCatalog.getString('Open'),
                                'value': 'open'
                            },
                            {
                                'display': gettextCatalog.getString('Done'),
                                'value': 'done'
                            },
                            {
                                'display': gettextCatalog.getString('On hold'),
                                'value': 'on hold'
                            },
                            {
                                'display': gettextCatalog.getString('In progress'),
                                'value': 'in progress'
                            }
                        ];
                        $state.get('pluginsTicketsTickets').data.filtering.internal_status.choices = [
                            {
                                'display': gettextCatalog.getString('None'),
                                'value': 'null'
                            },
                            {
                                'display': gettextCatalog.getString('Open'),
                                'value': 'open'
                            },
                            {
                                'display': gettextCatalog.getString('Done'),
                                'value': 'done'
                            },
                            {
                                'display': gettextCatalog.getString('On hold'),
                                'value': 'on hold'
                            },
                            {
                                'display': gettextCatalog.getString('In progress'),
                                'value': 'in progress'
                            }
                        ];
                        return FlObjectList(PluginsTicketsTicketsApi, $stateParams)
                    }
                ],
                createOptions: [
                    '$stateParams', 'PluginsTicketsTicketsApi', function (
                        $stateParams,
                        PluginsTicketsTicketsApi
                    ) {
                        return PluginsTicketsTicketsApi.get({'action': 'create_options'}).$promise;
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Tickets'),
                    parent: 'dashboard'
                },
                feature: 'plugins.tickets',
                orderOptions: {
                    last_reply_at: gettext('Last Updated'),
                    assigned_to: gettext('Assigned to'),
                    created_at: gettext('Created at'),
                    created_by: gettext('Created by'),
                    internal_status: gettext('Internal status'),
                    status: gettext('Status'),
                    title: gettext('Title'),
                    department: gettext('Department'),
                    priority: gettext('Priority')
                },
                filtering: {
                    assigned_to: {
                        display: gettext('assigned to'),
                        field_name: 'assigned_to',
                        type: 'user',
                        is_staff: true
                    },
                    created_at: {
                        display: gettext('created at'),
                        field_name: 'created_at',
                        type: 'date'
                    },
                    internal_status: {
                        display: gettext('internal status'),
                        field_name: 'internal_status',
                        type: 'choices',
                        choices: [
                            // added from resolve
                        ]
                    },
                    status: {
                        display: gettext('status'),
                        field_name: 'status',
                        type: 'choices',
                        choices: [
                            // added from resolve
                        ]
                    },
                    priority: {
                        display: gettext('priority'),
                        field_name: 'priority',
                        type: 'choices',
                        choices: [
                            {
                                'display': gettext('High'),
                                'value': 'high'
                            },
                            {
                                'display': gettext('Medium'),
                                'value': 'medium'
                            },
                            {
                                'display': gettext('Low'),
                                'value': 'low'
                            }
                        ]
                    },
                    client: {
                        display: gettext('client'),
                        field_name: 'client',
                        type: 'client'
                    },
                    department: {
                        display: gettext('department'),
                        field_name: 'department',
                        type: 'customModelInstance',
                        service: 'PluginsTicketsDepartmentsApi'
                    }
                }
            }
        };

        var ticketsDepartmentsState = {
            name: 'pluginsTicketsDepartments',
            url: CONFIG.base_url + 'tickets/departments?page_size?ordering?search?filtering',
            component: 'pluginsTicketsDepartments',
            authenticate: true,
            showSearch: true,
            reloadOnSearch: false,
            params: {
                page_size: {
                    value: CONFIG.paginate_by,
                    squash: true
                },
                ordering: {
                    value: '-created_at',
                    squash: true
                },
                filtering: {
                    value: '',
                    squash: true
                }
            },
            resolve: {
                departments: [
                    '$stateParams', 'FlObjectList', 'PluginsTicketsDepartmentsApi', function (
                        $stateParams,
                        FlObjectList,
                        PluginsTicketsDepartmentsApi
                    ) {
                        return FlObjectList(PluginsTicketsDepartmentsApi, $stateParams)
                    }
                ],
                createOptions: [
                    '$stateParams', 'PluginsTicketsDepartmentsApi', function (
                        $stateParams,
                        PluginsTicketsDepartmentsApi
                    ) {
                        return PluginsTicketsDepartmentsApi.get({'action': 'create_options'}).$promise;
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Departments'),
                    parent: 'dashboard'
                },
                feature: 'plugins.tickets',
                orderOptions: {
                    created_at: gettext('Created at'),
                    email: gettext('Email address'),
                    name: gettext('Name')
                },
                filtering: {
                    created_at: {
                        display: gettext('created at'),
                        field_name: 'created_at',
                        type: 'date'
                    }
                }
            }
        };

        var ticketsDepartmentDetailsState = {
            name: 'pluginsTicketsDepartmentDetails',
            url: CONFIG.base_url + 'tickets/departments/:id',
            component: 'pluginsTicketsDepartmentDetails',
            authenticate: true,
            resolve: {
                department: [
                    'PluginsTicketsDepartmentsApi', '$stateParams', 'FlResolveErrorHandler', 'FlBreadCrumbService',
                    function (PluginsTicketsDepartmentsApi, $stateParams, FlResolveErrorHandler, FlBreadCrumbService) {
                        return PluginsTicketsDepartmentsApi.get($stateParams).$promise
                            .then(function (data) {
                                FlBreadCrumbService.setParams({'name': data.name});
                                return data;
                            }).catch(FlResolveErrorHandler.handleError);
                    }
                ],
                createOptions: [
                    'PluginsTicketsDepartmentsApi', '$stateParams', 'FlResolveErrorHandler',
                    function (PluginsTicketsDepartmentsApi, $stateParams, FlResolveErrorHandler) {
                        return PluginsTicketsDepartmentsApi.get({
                            'action': 'create_options'
                        }).$promise
                            .then(function (data) {
                                return data;
                            }).catch(FlResolveErrorHandler.handleError);
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Department {:name}'),
                    parent: 'pluginsTicketsDepartments',
                    'default': gettext('Edit department')
                },
                feature: 'plugins.tickets'
            }
        };

        var ticketsDepartmentCreateState = {
            name: 'pluginsTicketsDepartmentCreate',
            url: CONFIG.base_url + 'tickets/departments/create',
            component: 'pluginsTicketsDepartmentCreate',
            authenticate: true,
            resolve: {
                createOptions: [
                    'PluginsTicketsDepartmentsApi', '$stateParams', 'FlResolveErrorHandler',
                    function (PluginsTicketsDepartmentsApi, $stateParams, FlResolveErrorHandler) {
                        return PluginsTicketsDepartmentsApi.get({
                            'action': 'create_options'
                        }).$promise
                            .then(function (data) {
                                return data;
                            }).catch(FlResolveErrorHandler.handleError);
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Create department'),
                    parent: 'pluginsTicketsDepartments'
                },
                feature: 'plugins.tickets'
            }
        };

        var ticketsTicketsDetailsState = {
            name: 'pluginsTicketsTicketsDetails',
            url: CONFIG.base_url + 'tickets/:id',
            component: 'pluginsTicketsTicketsDetails',
            authenticate: true,
            resolve: {
                ticket: [
                    'PluginsTicketsTicketsApi', '$stateParams', 'FlResolveErrorHandler',
                    function (PluginsTicketsTicketsApi, $stateParams, FlResolveErrorHandler) {
                        return PluginsTicketsTicketsApi.get($stateParams).$promise
                            .then(function (data) {
                                return data;
                            }).catch(FlResolveErrorHandler.handleError);
                    }
                ],
                createOptions: [
                    '$stateParams', 'PluginsTicketsTicketsApi', function (
                        $stateParams,
                        PluginsTicketsTicketsApi
                    ) {
                        return PluginsTicketsTicketsApi.get({
                            'action': 'create_options',
                            'ticket_id': $stateParams.id
                        }).$promise.then(function(data){
                            return data;
                        }).catch(function(err){
                            // this fails when ticket doesn't exist, do not handle error
                        });
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Ticket details'),
                    parent: 'pluginsTicketsTickets'
                },
                feature: 'plugins.tickets'
            }
        };

        var ticketsTicketsCreateState = {
            name: 'pluginsTicketsTicketsCreate',
            url: CONFIG.base_url + 'tickets/open-new-ticket?preselectedClient',
            component: 'pluginsTicketsTicketsCreate',
            authenticate: true,
            resolve: {
                createOptions: [
                    '$stateParams', 'PluginsTicketsTicketsApi', function (
                        $stateParams,
                        PluginsTicketsTicketsApi
                    ) {
                        return PluginsTicketsTicketsApi.get({
                            'action': 'create_options',
                            'ticket_id': $stateParams.id
                        }).$promise;
                    }
                ],
                preselectedClient: [
                    '$stateParams', 'PluginsTicketsTicketsApi', function (
                        $stateParams,
                    ) {
                        if ($stateParams.preselectedClient) {
                            return $stateParams.preselectedClient;
                        } else {
                            return null;
                        }
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Open ticket'),
                    parent: 'pluginsTicketsTickets'
                },
                feature: 'plugins.tickets'
            }
        };

        var ticketsTicketsEditState = {
            name: 'pluginsTicketsTicketsEdit',
            url: CONFIG.base_url + 'tickets/edit-ticket/:id',
            component: 'pluginsTicketsTicketsEdit',
            authenticate: true,
            resolve: {
                ticket: [
                    'PluginsTicketsTicketsApi', '$stateParams', 'FlResolveErrorHandler',
                    function (PluginsTicketsTicketsApi, $stateParams, FlResolveErrorHandler) {
                        return PluginsTicketsTicketsApi.get($stateParams).$promise
                            .then(function (data) {
                                return data;
                            }).catch(FlResolveErrorHandler.handleError);
                    }
                ],
                createOptions: [
                    '$stateParams', 'PluginsTicketsTicketsApi', function (
                        $stateParams,
                        PluginsTicketsTicketsApi
                    ) {
                        return PluginsTicketsTicketsApi.get({
                            'action': 'create_options',
                            'ticket_id': $stateParams.id
                        }).$promise;
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Edit ticket'),
                    parent: 'pluginsTicketsTickets'
                },
                feature: 'plugins.tickets'
            }
        };

        var staffSignaturesState =  {
            name: 'staffSignaturesEdit',
            url: CONFIG.base_url + 'tickets/user_signatures',
            component: 'pluginsTicketsSignatures',
            authenticate: true,
            resolve: {
                signatures: [
                    '$stateParams', 'PluginsTicketsSignaturesApi', function (
                        $stateParams,
                        PluginsTicketsSignaturesApi
                    ) {
                        return PluginsTicketsSignaturesApi.get({
                            'action': 'get_signatures_for_current_user'
                        }).$promise;
                    }
                ],
                departments: [
                    '$stateParams', 'PluginsTicketsDepartmentsApi', function (
                        $stateParams,
                        PluginsTicketsDepartmentsApi
                    ) {
                        return PluginsTicketsDepartmentsApi.get({}).$promise;
                    }
                ]
            },
            data: {
                feature: 'plugins.tickets',
                stateInfo: {
                    'display': gettext('Edit user signatures'),
                    parent: 'userprofile',
                    'default': gettext('Edit signatures')
                }
            }
        };

        return [ticketsTicketsState, ticketsDepartmentsState, ticketsDepartmentDetailsState, ticketsDepartmentCreateState,
            ticketsTicketsDetailsState, ticketsTicketsCreateState, ticketsTicketsEditState, staffSignaturesState];
    }

    pluginsTicketsConfig.$inject = ['$stateProvider', 'CONFIG', 'gettext'];

    function pluginsTicketsConfig($stateProvider, CONFIG, gettext) {
        var states = getStates(CONFIG, gettext);
        for (var stateIndex = 0; stateIndex < states.length; stateIndex++) {
            $stateProvider.state(states[stateIndex]);
        }
    }

    if ($stateRegistry) {
        var states = getStates(CONFIG, gettext);
        for (var stateIndex = 0; stateIndex < states.length; stateIndex++) {
            if (!$stateRegistry.get(states[stateIndex].name)) {
                $stateRegistry.register(states[stateIndex]);
            }
        }
    }
    else {
        angular.module('fleioStaff').config(pluginsTicketsConfig);
    }
})();
