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
                    created_at: gettext('Created at'),
                    status: gettext('Status'),
                    tld: gettext('TLD')
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
                    },
                    status: {
                        display: gettext('status'),
                        field_name: 'status',
                        type: 'choices',
                        choices: [
                            {
                                'display': gettext('Active'),
                                'value': 'active'
                            },
                            {
                                'display': gettext('Cancelled'),
                                'value': 'cancelled'
                            },
                            {
                                'display': gettext('Expired'),
                                'value': 'expired'
                            },
                            {
                                'display': gettext('Fraud'),
                                'value': 'fraud'
                            },
                            {
                                'display': gettext('Grace'),
                                'value': 'grace'
                            },
                            {
                                'display': gettext('Redemption'),
                                'value': 'redemption'
                            },
                            {
                                'display': gettext('Registration pending'),
                                'value': 'pending'
                            },
                            {
                                'display': gettext('Transfer pending'),
                                'value': 'pending_transfer'
                            },
                            {
                                'display': gettext('Transferred away'),
                                'value': 'transferred_away'
                            },
                            {
                                'display': gettext('Undefined'),
                                'value': 'undefined'
                            },
                            {
                                'display': gettext('Unmanaged'),
                                'value': 'unmanaged'
                            }
                        ]
                    },
                    tld: {
                        display: gettext('top level domain'),
                        field_name: 'tld',
                        type: 'customModelInstance',
                        service: 'PluginsDomainsTLDsApi'
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

        var domainsRegistrarsState = {
            name: 'pluginsDomainsRegistrars',
            url: CONFIG.base_url + 'domains/registrars?page_size?ordering?search?filtering',
            component: 'pluginsDomainsRegistrars',
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
                }
            },
            resolve: {
                registrars: [
                    '$stateParams', 'FlObjectList', 'PluginsDomainsRegistrarsApi', function (
                        $stateParams,
                        FlObjectList,
                        PluginsDomainsRegistrarsApi
                    ) {
                        return FlObjectList(PluginsDomainsRegistrarsApi, $stateParams)
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Registrars'),
                    parent: 'dashboard'
                },
                feature: 'plugins.domains',
                orderOptions: {
                    created_at: gettext('Created at'),
                    name: gettext('Name')
                }
            }
        };

        var domainsRegistrarDetailsState = {
            name: 'pluginsDomainsRegistrarDetails',
            url: CONFIG.base_url + 'domains/registrar/:id',
            component: 'pluginsDomainsRegistrarDetails',
            authenticate: true,
            resolve: {
                registrar: [
                    'PluginsDomainsRegistrarsApi', '$stateParams', 'FlResolveErrorHandler',
                    function (PluginsDomainsRegistrarsApi, $stateParams, FlResolveErrorHandler) {
                        return PluginsDomainsRegistrarsApi.get($stateParams).$promise
                            .then(function (data) {
                                return data;
                            }).catch(FlResolveErrorHandler.handleError);
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('Registrar Details'),
                    parent: 'pluginsDomainsRegistrars'
                },
                feature: 'plugins.domains'
            }
        };

        var domainsTldsState = {
            name: 'pluginsDomainsTlds',
            url: CONFIG.base_url + 'domains/tlds?page_size?ordering?search?filtering',
            component: 'pluginsDomainsTlds',
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
                tlds: [
                    '$stateParams', 'FlObjectList', 'PluginsDomainsTLDsApi', function (
                        $stateParams,
                        FlObjectList,
                        PluginsDomainsTLDsApi
                    ) {
                        return FlObjectList(PluginsDomainsTLDsApi, $stateParams)
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('TLDs'),
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
                    premium_domains_available: {
                        display: gettext('Premium domains available'),
                        field_name: 'premium_domains_available',
                        type: 'bool'
                    },
                    requires_epp_for_transfer: {
                        display: gettext('Requires EPP for transfer'),
                        field_name: 'requires_epp_for_transfer',
                        type: 'bool'
                    },
                    default_registrar: {
                        display: gettext('Default registrar'),
                        field_name: 'default_registrar',
                        type: 'customModelInstance',
                        service: 'PluginsDomainsRegistrarsApi'
                    }
                }
            }
        };

        var domainsTldDetailsState = {
            name: 'pluginsDomainsTldDetails',
            url: CONFIG.base_url + 'domains/tlds/:id',
            component: 'pluginsDomainsTldDetails',
            authenticate: true,
            params: {
            },
            resolve: {
                tld: [
                    'PluginsDomainsTLDsApi', '$stateParams', 'FlResolveErrorHandler',
                    function (PluginsDomainsTLDsApi, $stateParams, FlResolveErrorHandler) {
                        return PluginsDomainsTLDsApi.get($stateParams).$promise
                            .then(function (data) {
                                return data;
                            }).catch(FlResolveErrorHandler.handleError);
                    }
                ]
            },
            data: {
                stateInfo: {
                    'display': gettext('TLD Pricing'),
                    parent: 'pluginsDomainsTlds'
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

        return [
            domainsDomainsState,
            domainsDomainDetailsState,

            domainsRegistrarsState,
            domainsRegistrarDetailsState,

            domainsTldsState,
            domainsTldDetailsState,

            domainsContactsState,

            domainsRegisterDomainState,
            domainsTransferDomainState
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
        angular.module('fleioStaff').config(pluginsDomainsConfig);
    }
})();
