(function () {
    'use strict';

    if (!String.prototype.endsWith) {
        String.prototype.endsWith = function (search, this_len) {
            if (this_len === undefined || this_len > this.length) {
                this_len = this.length;
            }
            return this.substring(this_len - search.length, this_len) === search;
        };
    }

    angular.module('fleio')
        .component('pluginsDomainsSelectDomain', {
            templateUrl: 'site/plugins/domains/select_domain/selectdomain.html',
            controller: PluginsDomainsDomainSelectDomainController,
            bindings: {
                data: '='
            }
        });

    PluginsDomainsDomainSelectDomainController.$inject = ['PluginsDomainsOrderDomainApi', '$state', '$scope'];

    function PluginsDomainsDomainSelectDomainController(PluginsDomainsOrderDomainApi, $state, $scope) {
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            $ctrl.domainOperation = '';
            /** @type {{valid_tlds: Array<string>}} **/
            $ctrl.selectDomainOptions = {};
            /** @type {String} **/
            $ctrl.selectedDomainName = '';
            $ctrl.loaded = false;
            PluginsDomainsOrderDomainApi.get({action: 'select_domain_options'}).$promise
                .then(function (data) {
                    $ctrl.selectDomainOptions = data;
                    $ctrl.loaded = true;
                });

            $scope.$watch('$ctrl.selectedDomainName', function () {
                $ctrl.hasErrors = false;
                $ctrl.domainNameOk = false;
                $ctrl.price_per_year = null;
                $ctrl.currency = null;
            });
        };

        $ctrl.typeChanged = function typeChanged() {
            $ctrl.selectedDomainName = '';
            $ctrl.shouldLookup = false;
            $ctrl.domainChecked = false;
        };

        $ctrl.hasValidTLD = function hasValidTLD() {
            for (var tldIndex = 0; tldIndex < $ctrl.selectDomainOptions.valid_tlds.length; tldIndex++) {
                if ($ctrl.selectedDomainName.endsWith($ctrl.selectDomainOptions.valid_tlds[tldIndex])) {
                    return true;
                }
            }

            return false;
        };

        $ctrl.canContinue = function canContinue() {
            if (!$ctrl.selectedDomainName) {
                // we must have a domain name
                return false;
            }

            $ctrl.hasTld = $ctrl.selectedDomainName.includes('.');
            if ($ctrl.domainOperation === 'use_external') {
                // almost no validation for external domain
                return $ctrl.selectedDomainName.includes('.') &&
                    !$ctrl.selectedDomainName.endsWith('.') &&
                    !$ctrl.selectedDomainName.startsWith('.');
            }

            if ($ctrl.domainOperation === 'use_existing' || $ctrl.domainOperation === 'use_in_cart') {
                // existing or in cart domains should already be validated
                return true;
            }

            $ctrl.shouldLookup = true;

            if ($ctrl.domainOperation === 'order_new') {
                $ctrl.lookupMethod = 'is_available_for_registration';
            }

            if ($ctrl.domainOperation === 'transfer') {
                $ctrl.lookupMethod = 'is_available_for_transfer';
            }

            return true;
        };

        $ctrl.newDomainSelected = function newDomainSelected() {
            return $ctrl.domainOperation === 'order_new' || $ctrl.domainOperation === 'transfer' ||
                $ctrl.domainOperation === 'use_external';
        };

        $ctrl.shouldCheckDomain = function shouldCheckDomain() {
            if ($ctrl.newDomainSelected()) {
                return !$ctrl.domainNameOk;
            } else {
                return false;
            }
        };

        $ctrl.canSubmit = function canSubmit() {
            if ($ctrl.newDomainSelected()) {
                if ($ctrl.domainChecked) {
                    return $ctrl.domainNameOk;
                } else {
                    return !!$ctrl.selectedDomainName;
                }
            } else {
                return !!$ctrl.selectedDomainName;
            }
        };

        $ctrl.goToConfigureProduct = function goToConfigureProduct() {
            var params = angular.copy($state.params);
            params.domain_name = $ctrl.selectedDomainName;
            params.domain_action = $ctrl.domainOperation;
            $state.go('orderProduct', params);
        };

        $ctrl.formSubmit = function formSubmit() {
            if ($ctrl.canSubmit()) {
                if ($ctrl.shouldCheckDomain()) {
                    $ctrl.hasTld = $ctrl.selectedDomainName.includes('.');

                    if (!$ctrl.hasTld) {
                        $ctrl.selectedDomainName += $ctrl.selectDomainOptions.default_tld;
                    }

                    if ($ctrl.domainOperation === 'use_external') {
                        // almost no validation for external domain
                        $ctrl.domainNameOk = $ctrl.selectedDomainName.includes('.') &&
                            !$ctrl.selectedDomainName.endsWith('.') &&
                            !$ctrl.selectedDomainName.startsWith('.');
                        return;
                    }

                    if ($ctrl.domainOperation === 'order_new') {
                        $ctrl.lookupMethod = 'is_available_for_registration';
                    }

                    if ($ctrl.domainOperation === 'transfer') {
                        $ctrl.lookupMethod = 'is_available_for_transfer';
                    }

                    PluginsDomainsOrderDomainApi.get({
                        action: $ctrl.lookupMethod,
                        domain_name: $ctrl.selectedDomainName
                    }).$promise.then(function (
                        /** @type{{
                        available: boolean,
                        error: string
                        }}**/
                        checkResults) {
                        if (checkResults.available) {
                            $ctrl.domainNameOk = true;
                            $ctrl.price_per_year = checkResults.prices.prices_per_years[0];
                            $ctrl.currency = checkResults.prices.currency.code;
                        } else {
                            $ctrl.errorText = checkResults.error;
                            $ctrl.hasErrors = true;
                        }
                    });
                } else {
                    $ctrl.goToConfigureProduct();
                }
            }
        };

        $ctrl.continueOrder = function continueOrder() {
            if (!$ctrl.hasTld) {
                $ctrl.selectedDomainName += $ctrl.selectDomainOptions.default_tld;
            }

            if ($ctrl.shouldLookup) {
                PluginsDomainsOrderDomainApi.get({
                    action: $ctrl.lookupMethod,
                    domain_name: $ctrl.selectedDomainName
                }).$promise.then(function (
                    /** @type{{
                available: boolean,
                error: string
                }}**/
                    checkResults) {
                    if (checkResults.available) {
                        $ctrl.goToConfigureProduct();
                    } else {
                        $ctrl.errorText = checkResults.error;
                        $ctrl.hasErrors = true;
                    }
                });
            } else {
                $ctrl.goToConfigureProduct();
            }
        }
    }
})();
