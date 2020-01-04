(function () {
    'use strict';

    angular.module('fleioStaff')
        .controller('PluginsDomainsDomainEditController', PluginsDomainsDomainEditController);

    PluginsDomainsDomainEditController.$inject = ['$mdDialog', 'PluginsDomainsDomainsApi',
        'domain', 'isEdit'];
    function PluginsDomainsDomainEditController($mdDialog, PluginsDomainsDomainsApi,
        domain, isEdit) {
        var $ctrl = this;
        $ctrl.submitPending = false;

        $ctrl.$onInit = function $onInit() {
            $ctrl.isEdit = isEdit;
            if (isEdit) {
                $ctrl.domain = angular.copy(domain);
            }
            else {
                $ctrl.domain = {
                };
            }
            $ctrl.statuses = {};
            PluginsDomainsDomainsApi.get({action:'create_options'}).$promise
            .then(function (data) {
                $ctrl.statuses = data.statuses;
            }).catch(function (reason) {

            });
        };

        $ctrl.saveDomain = function saveDomain() {
            document.activeElement.blur();
            if (!($ctrl.editDomain.$invalid || $ctrl.submitPending)) {
                $ctrl.submitPending = true;
                if ($ctrl.isEdit) {
                    return PluginsDomainsDomainsApi.update({
                        'id': $ctrl.domain.id
                    }, $ctrl.domain).$promise.then(function (data) {
                        $mdDialog.hide(data);
                        return data;
                    }).catch(function (error) {
                        $ctrl.submitPending = false;
                        $ctrl.backendErrors = error.data;
                    });
                }
                else {
                    return PluginsDomainsDomainsApi.save($ctrl.domain)
                        .$promise.then(function (data) {
                            $mdDialog.hide(data);
                            return data;
                        }).catch(function (error) {
                            $ctrl.submitPending = false;
                            $ctrl.backendErrors = error.data;
                        });
                }
            }
        };

        $ctrl.close = function () {
            return $mdDialog.cancel();
        };
    }

})();
