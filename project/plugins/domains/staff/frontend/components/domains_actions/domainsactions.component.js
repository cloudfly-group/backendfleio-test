(function () {
    'use strict';

    angular.module('fleioStaff')
        .component('pluginsDomainsDomainsActions', {
            templateUrl: 'staff/plugins/domains/domains_actions/domainssactions.html',
            controller: pluginsDomainsDomainsActionsController,
            bindings: {
                domain: '<',
                addButton: '<',
                onDomainDeleted: '&',
                onDomainChanged: '&',
                onDomainAdded: '&'
            }
        });

    pluginsDomainsDomainsActionsController.$inject = ['gettextCatalog', '$mdDialog', 'FlUiUtilsService',
        'PluginsDomainsDomainsApi', 'FlNotificationService'];

    function pluginsDomainsDomainsActionsController(gettextCatalog, $mdDialog, FlUiUtilsService,
                                                    PluginsDomainsDomainsApi, FlNotificationService) {
        var $ctrl = this;

        $ctrl.deleteDomain = function deleteDomain() {
            FlUiUtilsService.yesNoDlg(
              gettextCatalog.getString('Are you sure you wish to delete this domain from Fleio only ?'),
              gettextCatalog.getString('Delete domain'))
                .then(function () {
                    PluginsDomainsDomainsApi.delete({'id': $ctrl.domain.id}).$promise
                        .then(function (response) {
                            var message = response.detail || gettextCatalog.getString('Domain deleted from Fleio');
                            FlNotificationService.add(message);
                            $ctrl.onDomainDeleted();
                        }).catch(function(response) {
                    })
                }).catch(function(){
                    // Catch the delete domain confirmation dialog to prevent unnecessary error logging
            })
        };

        $ctrl.editDomain = function editDomain($event, edit) {
            return $mdDialog.show({
                templateUrl: 'staff/plugins/domains/domains_actions/dialogs/domain_edit/domainedit.html',
                controller: 'PluginsDomainsDomainEditController',
                controllerAs: '$ctrl',
                parent: angular.element(document.body),
                clickOutsideToClose: false,
                locals: {
                    domain: $ctrl.domain,
                    isEdit: edit
                },
                targetEvent: $event
            }).then(function () {
                if (edit) {
                    $ctrl.onDomainChanged();
                }
                else {
                    $ctrl.onDomainAdded();
                }

                FlNotificationService.add(
                    gettextCatalog.getString(edit ? 'Domain updated' : 'Domain added')
                );
            }).catch(function (reason) {
                // hide dialog errors
            });
        };
    }
})();

