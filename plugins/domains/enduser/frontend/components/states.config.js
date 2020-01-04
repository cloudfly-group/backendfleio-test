(function () {
    'use strict';

    function getStates(CONFIG, gettext) {
        var domainsDomainsState = {
            name: 'pluginsDomainsDomains',
            url: CONFIG.base_url + 'domains?page_size?ordering?search?filtering',
            component: 'pluginsDomainsDomains',
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
                domains: [
                    '$stateParams', 'FlObjectList', 'PluginsDomainsDomainsApi', function (
                        $stateParams,
                        FlObjectList,
                        PluginsDomainsDomainsApi
                    ) {
                        return FlObjectList(PluginsDomainsDomainsApi, $stateParams)
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Domains'),
                    parent: 'dashboard'
                },
                feature: 'plugins.domains',
                orderOptions: {
                    name: gettext('Name'),
                    created_at: gettext('Created at')
                },
                filtering: {
                    created_at: {
                        display: gettext('created at'),
                        field_name: 'created_at',
                        type: 'date'
                    },
                    registration_date: {
                        display: gettext('registration date'),
                        field_name: 'registration_date',
                        type: 'date'
                    },
                    expiry_date: {
                        display: gettext('expiry date'),
                        field_name: 'expiry_date',
                        type: 'date'
                    },
                    registration_period: {
                        display: gettext('Registration period'),
                        field_name: 'registration_period',
                        type: 'decimal'
                    }
                }
            }
        };

        var domainsDomainDetailsState = {
            name: 'pluginsDomainsDomainDetails',
            url: CONFIG.base_url + 'domains/:id',
            component: 'pluginsDomainsDomainDetails',
            authenticate: true,
            resolve: {
                domain: [
                    'PluginsDomainsDomainsApi', '$stateParams', 'FlResolveErrorHandler',
                    function (PluginsDomainsDomainsApi, $stateParams, FlResolveErrorHandler) {
                        return PluginsDomainsDomainsApi.get($stateParams).$promise
                            .then(function (data) {
                                return data;
                            }).catch(FlResolveErrorHandler.handleError);
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Domain Details'),
                    parent: 'pluginsDomainsDomains'
                },
                feature: 'plugins.domains'
            }
        };

        var domainsRegisterDomainState = {
            name: 'pluginsDomainsRegisterDomain',
            url: CONFIG.base_url + 'domains/register-domain',
            component: 'pluginsDomainsRegisterDomain',
            authenticate: true,
            params: {
            },
            resolve: {
                clientCreateOptions: [
                  'FlClientApi', function (FlClientApi) {
                    return FlClientApi.get({options: 'create_options'}).$promise;
                  }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Register domain'),
                    parent: 'dashboard'
                },
                feature: 'plugins.domains',
                orderOptions: {
                },
                filtering: {
                }
            }
        };

        var domainsTransferDomainState = {
            name: 'pluginsDomainsTransferDomain',
            url: CONFIG.base_url + 'domains/transfer-domain',
            component: 'pluginsDomainsTransferDomain',
            authenticate: true,
            params: {
            },
            resolve: {
            },
            data: {
                stateInfo: {
                    'display': gettext('Transfer domain'),
                    parent: 'dashboard'
                },
                feature: 'plugins.domains',
                orderOptions: {
                },
                filtering: {
                }
            }
        };

        var domainsContactsState = {
            name: 'pluginsDomainsContacts',
            url: CONFIG.base_url + 'domains/contacts?page_size?ordering?search?filtering',
            component: 'pluginsDomainsContacts',
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
                contacts: [
                    '$stateParams', 'FlObjectList', 'PluginsDomainsContactsApi', function (
                        $stateParams,
                        FlObjectList,
                        PluginsDomainsContactsApi
                    ) {
                        return FlObjectList(PluginsDomainsContactsApi, $stateParams)
                    }
                ],
                createOptions: [
                  'PluginsDomainsContactsApi', function (PluginsDomainsContactsApi) {
                    return PluginsDomainsContactsApi.get({action: 'create_options'}).$promise;
                  }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Contacts'),
                    parent: 'dashboard'
                },
                feature: 'plugins.domains',
                orderOptions: {
                  created_at: gettext('Created at'),
                  first_name: gettext('First name'),
                  last_name: gettext('Last name'),
                  id: gettext('ID'),
                  email: gettext('Email'),
                  company: gettext('Company'),
                  city: gettext('City'),
                  country: gettext('Country'),
                  state: gettext('State')
                },
                filtering: {
                  created_at: {
                    display: gettext('Date created'),
                    field_name: 'created_at',
                    type: 'date'
                  }
                }
            }
        };

        return [
            domainsDomainsState,
            domainsDomainDetailsState,
            domainsRegisterDomainState,
            domainsTransferDomainState,

            domainsContactsState
        ];
    }

    pluginsDomainsConfig.$inject = ['$stateProvider', 'CONFIG', 'gettext'];
    function pluginsDomainsConfig($stateProvider, CONFIG, gettext) {
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
        angular.module('fleio').config(pluginsDomainsConfig);
    }
})();
