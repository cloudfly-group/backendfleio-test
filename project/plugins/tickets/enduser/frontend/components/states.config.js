(function () {
    'use strict';

    function getStates(CONFIG, gettext) {
        const ticketsTicketsState = {
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
                    value: '-created_at',
                    squash: true
                },
                filtering: {
                    value: '',
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
                    created_at: {
                        display: gettext('created at'),
                        field_name: 'created_at',
                        type: 'date'
                    },
                    status: {
                        display: gettext('status'),
                        field_name: 'status',
                        type: 'choices',
                        choices: [
                            // added from resolve
                        ]
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

        const ticketsTicketsDetailsState = {
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
                        return PluginsTicketsTicketsApi.get({'action': 'create_options'}).$promise;
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


        const ticketsTicketsCreateState = {
            name: 'pluginsTicketsTicketsCreate',
            url: CONFIG.base_url + 'tickets/open-new-ticket',
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

        const ticketsTicketsEditState = {
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

        return [ticketsTicketsState, ticketsTicketsDetailsState, ticketsTicketsCreateState, ticketsTicketsEditState];
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
        angular.module('fleio').config(pluginsTicketsConfig);
    }
})();
