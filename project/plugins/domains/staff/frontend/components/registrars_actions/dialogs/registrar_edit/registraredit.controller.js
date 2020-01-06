(function () {
    'use strict';

    angular.module('fleioStaff')
        .controller('PluginsDomainsRegistrarEditController', PluginsDomainsRegistrarEditController);

    PluginsDomainsRegistrarEditController.$inject = ['$mdDialog', 'PluginsDomainsRegistrarsApi',
        'registrar', 'isEdit'];
    function PluginsDomainsRegistrarEditController($mdDialog, PluginsDomainsRegistrarsApi,
        registrar, isEdit) {
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            $ctrl.isEdit = isEdit;
            if (isEdit) {
                $ctrl.registrar = angular.copy(registrar);
            }
            else {
                $ctrl.registrar = {
                };
            }
        };

        $ctrl.saveRegistrar = function () {
            document.activeElement.blur();
            if (!($ctrl.editRegistrar.$invalid || $ctrl.submitPending)) {
                $ctrl.submitPending = true;
                if ($ctrl.isEdit) {
                    return PluginsDomainsRegistrarsApi.update({
                        'id': $ctrl.registrar.id
                    }, $ctrl.registrar).$promise.then(function (data) {
                        $mdDialog.hide(data);
                        return data;
                    }).catch(function (error) {
                        $ctrl.submitPending = false;
                        $ctrl.backendErrors = error.data;
                    });
                }
                else {
                    return PluginsDomainsRegistrarsApi.save($ctrl.registrar)
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
