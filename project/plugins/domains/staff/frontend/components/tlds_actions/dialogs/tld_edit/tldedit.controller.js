(function () {
    'use strict';

    angular.module('fleioStaff')
        .controller('PluginsDomainsTldEditController', PluginsDomainsTldEditController);

    PluginsDomainsTldEditController.$inject = ['$mdDialog', 'PluginsDomainsTLDsApi',
        'tld', 'isEdit'];
    function PluginsDomainsTldEditController($mdDialog, PluginsDomainsTLDsApi,
        tld, isEdit) {
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            $ctrl.isEdit = isEdit;
            if (isEdit) {
                $ctrl.tld = angular.copy(tld);
            }
            else {
                $ctrl.tld = {
                };
            }
        };

        $ctrl.saveTLD = function () {
            document.activeElement.blur();
            if (!($ctrl.editTLD.$invalid || $ctrl.submitPending)) {
                $ctrl.submitPending = true;
                if ($ctrl.isEdit) {
                    return PluginsDomainsTLDsApi.update({
                        'id': $ctrl.tld.id
                    }, $ctrl.tld).$promise.then(function (data) {
                        $mdDialog.hide(data);
                        return data;
                    }).catch(function (error) {
                        $ctrl.submitPending = false;
                        $ctrl.backendErrors = error.data;
                    });
                }
                else {
                    return PluginsDomainsTLDsApi.save($ctrl.tld)
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
