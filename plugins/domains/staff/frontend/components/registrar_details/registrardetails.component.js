(function(){
  'use strict';
  angular.module('fleioStaff')
    .component('pluginsDomainsRegistrarDetails', {
        templateUrl: 'staff/plugins/domains/registrars/registrardetails.html',
        controller: PluginsDomainsRegistrarDetailsController,
        bindings: {
            registrar: '<'
        }
    });

  PluginsDomainsRegistrarDetailsController.$inject = ['$state', 'gettextCatalog', 'PluginsDomainsRegistrarsApi',
    'FlNotificationService', 'FlResolveErrorHandler'];
  function PluginsDomainsRegistrarDetailsController($state, gettextCatalog, PluginsDomainsRegistrarsApi,
                                            FlNotificationService, FlResolveErrorHandler) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
    };

    $ctrl.onRegistrarDeleted = function onRegistrarDeleted() {
      $state.go('pluginsDomainsRegistrars');
    };

    $ctrl.refreshRegistrar = function refreshRegistrar() {
      PluginsDomainsRegistrarsApi.get({'id':$ctrl.registrar.id}).$promise
        .then(function (data) {
            $ctrl.registrar = data;
        }).catch(FlResolveErrorHandler.handleError);
    };

  }
})();
