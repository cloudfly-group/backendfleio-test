(function () {
  'use strict';

  angular.module('fleio')
    .factory('PluginsDomainsContactsActionsService', PluginsDomainsContactsActionsService)
    .component('pluginsDomainsContactsActions',{
      templateUrl: 'site/plugins/domains/contacts/contactsactions.html',
      controller: PluginsDomainsContactsActionsController,
      bindings: {
        contact: '=',
        addButton: '<',
        onContactDeleted: '&',
        onContactChanged: '&',
        onContactAdded: '&'
      }
    });

  PluginsDomainsContactsActionsController.$inject = ['gettextCatalog', '$mdDialog', 'FlUiUtilsService',
      'PluginsDomainsContactsApi', 'FlNotificationService', 'PluginsDomainsContactsActionsService'];
  function PluginsDomainsContactsActionsController(gettextCatalog, $mdDialog, FlUiUtilsService,
                                                   PluginsDomainsContactsApi, FlNotificationService,
                                                   PluginsDomainsContactsActionsService) {
    var $ctrl = this;

    $ctrl.deleteContact = function deleteContact() {
      FlUiUtilsService.yesNoDlg(gettextCatalog.getString('Are you sure?'), gettextCatalog.getString('Delete Contact'))
        .then(function () {
          PluginsDomainsContactsApi.delete({'id':$ctrl.contact.id}).$promise
            .then(function () {
              $ctrl.onContactDeleted();
            }).catch(function (reason) {
                FlNotificationService.add(reason.data.detail);
            });
        }).catch(function () {});
    };

    $ctrl.editContact = function editContact($event, edit) {
      return PluginsDomainsContactsActionsService.editContact(
          $event, edit, $ctrl.contact, $ctrl.onContactChanged, null, $ctrl.onContactAdded
      );
    };
  }

  PluginsDomainsContactsActionsService.$inject = [
      '$mdDialog', 'gettextCatalog'];
  function PluginsDomainsContactsActionsService($mdDialog, gettextCatalog) {
      return {
          editContact: function editContact($event, edit, contact, tldName, onContactChanged, onContactAdded) {
              return $mdDialog.show({
                  templateUrl: 'site/plugins/domains/contacts/contactedit.html',
                  controller: 'PluginsDomainsContactEditController',
                  controllerAs: '$ctrl',
                  parent: angular.element(document.body),
                  clickOutsideToClose: false,
                  locals: {
                      contact: contact,
                      isEdit: edit,
                      tldName: tldName
                  },
                  resolve: {
                    createOptions: [
                      'PluginsDomainsContactsApi', function (PluginsDomainsContactsApi) {
                        return PluginsDomainsContactsApi.get({action: 'create_options'}).$promise;
                      }
                    ]
                  },
                  targetEvent: $event
              }).then(function () {
                  if (edit) {
                      onContactChanged();
                  }
                  else {
                      onContactAdded();
                  }

                  FlNotificationService.add(
                      gettextCatalog.getString(edit ? 'Contact updated' : 'Contact added')
                  );
              }).catch(function () {
              });
          }
      }
  }

})();

