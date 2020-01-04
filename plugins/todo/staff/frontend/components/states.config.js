(function () {
    'use strict';

    function getStates(CONFIG, gettext) {
        var todoTodosState = {
            name: 'pluginsTodoTodos',
            url: CONFIG.base_url + 'todo?page_size?ordering?search?filtering',
            component: 'pluginsTodoTodos',
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
                    value: 'assigned_to:null+assigned_to:current_user+status:open+status:in progress',
                    squash: true
                }
            },
            resolve: {
                todos: [
                    '$stateParams', 'FlObjectList', 'PluginsTodoTodoApi', '$state', 'gettextCatalog', function (
                        $stateParams,
                        FlObjectList,
                        PluginsTodoTodoApi,
                        $state,
                        gettextCatalog,
                    ) {
                        PluginsTodoTodoApi.get({
                          'action': 'filter_options'
                        }).$promise.then(function (data) {
                          var fetched_statuses = data.statuses;
                          var statuses_choices = [];
                          gettextCatalog.getString('In progress');
                          gettextCatalog.getString('In Progress');
                          for (var i = 0, len = fetched_statuses.length; i < len; ++i) {
                            statuses_choices.push({
                              'display': gettextCatalog.getString(fetched_statuses[i].display),
                              'value': fetched_statuses[i].value
                            });
                          }
                          $state.get('pluginsTodoTodos').data.filtering.status.choices = statuses_choices;
                        });
                        return FlObjectList(PluginsTodoTodoApi, $stateParams)
                    }
                ],
                createOptions: [
                    '$stateParams', 'PluginsTodoTodoApi', function (
                        $stateParams,
                        PluginsTodoTodoApi
                    ) {
                        return PluginsTodoTodoApi.get({'action': 'create_options'}).$promise;
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('TODOs'),
                    parent: 'dashboard'
                },
                feature: 'plugins.todo',
                orderOptions: {
                    assigned_to: gettext('Assigned to'),
                    created_at: gettext('Created at'),
                    created_by: gettext('Created by'),
                    status: gettext('Status'),
                    title: gettext('Title')
                },
                filtering: {
                    assigned_to: {
                        display: gettext('assigned to'),
                        field_name: 'assigned_to',
                        type: 'user'
                    },
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
                            // loaded dynamically in resolve
                        ]
                    }
                }
            }
        };

        var todoTodoDetailsState = {
            name: 'pluginsTodoTodoDetails',
            url: CONFIG.base_url + 'todo/:id',
            component: 'pluginsTodoTodoDetails',
            authenticate: true,
            resolve: {
                todo: [
                    'PluginsTodoTodoApi', '$stateParams', 'FlResolveErrorHandler',
                    function (PluginsTodoTodoApi, $stateParams, FlResolveErrorHandler) {
                        return PluginsTodoTodoApi.get($stateParams).$promise
                            .then(function (data) {
                                return data;
                            }).catch(FlResolveErrorHandler.handleError);
                    }
                ],
                createOptions: [
                    '$stateParams', 'PluginsTodoTodoApi', function (
                        $stateParams,
                        PluginsTodoTodoApi
                    ) {
                        return PluginsTodoTodoApi.get({'action': 'create_options'}).$promise;
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('TODO Details'),
                    parent: 'pluginsTodoTodos'
                },
                feature: 'plugins.todo'
            }
        };

        return [todoTodosState, todoTodoDetailsState];
    }

    pluginsTodoConfig.$inject = ['$stateProvider', 'CONFIG', 'gettext'];

    function pluginsTodoConfig($stateProvider, CONFIG, gettext) {
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
        angular.module('fleioStaff').config(pluginsTodoConfig);
    }
})();
