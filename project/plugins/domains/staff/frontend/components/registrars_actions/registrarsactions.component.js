(function () {
    'use strict';

    angular.module('fleioStaff')
        .component('pluginsDomainsRegistrarsActions',{
            templateUrl: 'staff/plugins/domains/registrars_actions/registrarssactions.html',
            controller: pluginsDomainsRegistrarsActionsController,
            bindings: {
                registrar: '<',
                addButton: '<',
                onRegistrarDeleted: '&',
                onRegistrarChanged: '&',
                onRegistrarAdded: '&'
            }
        });

    pluginsDomainsRegistrarsActionsController.$inject = ['gettextCatalog', '$mdDialog', 'FlUiUtilsService',
        'PluginsDomainsRegistrarsApi', 'FlNotificationService'];
    function pluginsDomainsRegistrarsActionsController(gettextCatalog, $mdDialog, FlUiUtilsService,
                                                       PluginsDomainsRegistrarsApi, FlNotificationService) {
        var $ctrl = this;

        $ctrl.deleteRegistrar = function deleteRegistrar() {
            FlUiUtilsService.yesNoDlg(
                gettextCatalog.getString('Are you sure?'),gettextCatalog.getString('Delete registrar'))
                .then(function () {
                    PluginsDomainsRegistrarsApi.delete({'id':$ctrl.registrar.id}).$promise
                        .then(function () {
                            FlNotificationService.add(gettextCatalog.getString('Registrar deleted'));
                            $ctrl.onRegistrarDeleted();
                        }).catch(function (reason) {
                            FlNotificationService.add(reason.data.detail);
                        });
                }).catch(function () {});
        };

        $ctrl.editRegistrar = function editRegistrar($event, edit) {
            return $mdDialog.show({
                templateUrl: 'staff/plugins/domains/registrars_actions/dialogs/registrar_edit/registraredit.html',
                controller: 'PluginsDomainsRegistrarEditController',
                controllerAs: '$ctrl',
                parent: angular.element(document.body),
                clickOutsideToClose: false,
                locals: {
                    registrar: $ctrl.registrar,
                    isEdit: edit
                },
                targetEvent: $event
            }).then(function () {
                if (edit) {
                    $ctrl.onRegistrarChanged();
                }
                else {
                    $ctrl.onRegistrarAdded();
                }

                FlNotificationService.add(
                    gettextCatalog.getString(edit ? 'Registrar updated' :  'Registrar added')
                );
            }).catch(function(){});
        };
    }
})();

