(function () {
  'use strict';

  angular.module('fleioStaff')
    .controller('PluginsDomainsContactEditController', PluginsDomainsContactEditController);

  PluginsDomainsContactEditController.$inject = ['$mdDialog', 'PluginsDomainsContactsApi',
    'contact', 'isEdit', 'tldName', 'createOptions'];
  function PluginsDomainsContactEditController($mdDialog, PluginsDomainsContactsApi,
                                         contact, isEdit, tldName, createOptions) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {
      $ctrl.isEdit = isEdit;
      $ctrl.tldName = tldName;
      $ctrl.createOptions = angular.copy(createOptions);
      $ctrl.countries = $ctrl.createOptions.countries ? $ctrl.createOptions.countries : [];
      $ctrl.contact = contact;
      if ($ctrl.createOptions) {
        $ctrl.customFieldsDefinition = $ctrl.createOptions.custom_fields;
      }
      if ($ctrl.contact && $ctrl.contact.country && $ctrl.countries.length) {
        var selected_country = $ctrl.countries.filter(
          function(country) { return country.value === $ctrl.contact.country }
        );
        $ctrl.selectedCountry = selected_country[0];
      }

      if (isEdit) {
        $ctrl.contact = angular.copy(contact);
      }
      else{
        $ctrl.contact = {
        };
      }
    };

    function createFilterFor(query) {
      // Client country search filter
      var lowercaseQuery = angular.lowercase(query);
      return function filterFn(country) {
        return (angular.lowercase(country.label).indexOf(lowercaseQuery) === 0);
      };
    }

    $ctrl.selectedCountryChange = function(country) {
      // Client country changed
      if (country) { $ctrl.contact.country = country.value; }
    };

    $ctrl.querySearch = function(query) {
      // Client country search
      return query ? $ctrl.countries.filter( createFilterFor(query) ) : $ctrl.countries;
    };

    $ctrl.saveContact = function () {
      document.activeElement.blur();
      if (!($ctrl.editContactForm.$invalid || $ctrl.submitPending)) {
        $ctrl.submitPending = true;
        if ($ctrl.isEdit) {
          return PluginsDomainsContactsApi.update({
            'id': $ctrl.contact.id
          }, $ctrl.contact).$promise.then(function (data) {
            $mdDialog.hide(data);
            return data;
          }).catch(function (error) {
            $ctrl.submitPending = false;
            $ctrl.backendErrors = error.data;
          });
        }
        else {
          return PluginsDomainsContactsApi.save($ctrl.contact)
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
