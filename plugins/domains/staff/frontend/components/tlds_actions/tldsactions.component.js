(function () {
    'use strict';

    angular.module('fleioStaff')
        .component('pluginsDomainsTldsActions',{
            templateUrl: 'staff/plugins/domains/tlds_actions/tldssactions.html',
            controller: pluginsDomainsTldsActionsController,
            bindings: {
                tld: '<',
                addButton: '<',
                onTldDeleted: '&',
                onTldChanged: '&',
                onTldAdded: '&'
            }
        });

    pluginsDomainsTldsActionsController.$inject = ['gettextCatalog', '$mdDialog', 'FlUiUtilsService',
        'PluginsDomainsTLDsApi', 'FlNotificationService'];
    function pluginsDomainsTldsActionsController(gettextCatalog, $mdDialog, FlUiUtilsService, PluginsDomainsTLDsApi,
                                                 FlNotificationService) {
        var $ctrl = this;

        $ctrl.deleteTLD = function deleteTLD() {
            FlUiUtilsService.yesNoDlg(
                gettextCatalog.getString('Are you sure?'),gettextCatalog.getString('Delete TLD'))
                .then(function () {
                    PluginsDomainsTLDsApi.delete({'id':$ctrl.tld.id}).$promise
                        .then(function () {
                            FlNotificationService.add(gettextCatalog.getString('TLD deleted'));
                            $ctrl.onTldDeleted();
                        });
                }).catch(function () {});
        };

        $ctrl.editTLD = function editTLD($event, edit) {
            return $mdDialog.show({
                templateUrl: 'staff/plugins/domains/tlds_actions/dialogs/tld_edit/tldedit.html',
                controller: 'PluginsDomainsTldEditController',
                controllerAs: '$ctrl',
                parent: angular.element(document.body),
                clickOutsideToClose: false,
                locals: {
                    tld: $ctrl.tld,
                    isEdit: edit
                },
                targetEvent: $event
            }).then(function () {
                if (edit) {
                    $ctrl.onTldChanged();
                }
                else {
                    $ctrl.onTldAdded();
                }

                FlNotificationService.add(
                    gettextCatalog.getString(edit ? 'TLD updated' :  'TLD added')
                );
            }).catch(function(){});
        };
    }
})();

