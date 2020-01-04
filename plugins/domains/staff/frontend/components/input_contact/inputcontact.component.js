(function(){
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsDomainsInputContact', {
      templateUrl: 'staff/plugins/domains/input_contact/inputcontact.html',
      controller: PluginsDomainsInputContactController,
      bindings:  {
        contactId: '=',
        clientId: '<',
        onContactChanged: '&',
        placeholder: '@'
      }
  });

  PluginsDomainsInputContactController.$inject = ['$element', 'PluginsDomainsContactsApi', '$scope'];
  function PluginsDomainsInputContactController($element, PluginsDomainsContactsApi, $scope){
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
      if ($ctrl.contactId) {
        PluginsDomainsContactsApi.get({'id': $ctrl.contactId}).$promise
          .then(function (contact) {
            $ctrl.contact = contact
          });
      }
    };

    $ctrl.selectedContactChanged = function selectedContactChanged(contact) {
      if (typeof contact !== 'undefined') {
        $ctrl.contactId = contact.id;
      }
      else{
        $ctrl.contactId = null;
      }
      $ctrl.onContactChanged({contact:contact});
    };

    $ctrl.searchContact = function searchContact(input) {
      var params = {
        'search': input,
        'client': $ctrl.clientId
      };
      return PluginsDomainsContactsApi.get(params).$promise.then(function (data) {
        return data.objects;
      })
    };
  }
})();
