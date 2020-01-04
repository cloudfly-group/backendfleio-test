(function(){
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsDomainsInputRegistrar', {
      templateUrl: 'staff/plugins/domains/input_registrar/inputregistrar.html',
      controller: PluginsDomainsInputRegistrarController,
      bindings:  {
        priceDomainId: '<',
        registrarId: '=',
        onRegistrarChanged: '&',
      }
  });

  PluginsDomainsInputRegistrarController.$inject = ['$element', 'PluginsDomainsRegistrarsApi'];
  function PluginsDomainsInputRegistrarController($element, PluginsDomainsRegistrarsApi){
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
      if ($ctrl.registrarId) {
        PluginsDomainsRegistrarsApi.get({'id': $ctrl.registrarId, 'priceDomainId': $ctrl.priceDomainId}).$promise
          .then(function (registrar) {
            $ctrl.registrar = registrar
          });
      }
    };

    $ctrl.selectedRegistrarChanged = function selectedRegistrarChanged(registrar) {
      if (typeof registrar !== 'undefined') {
        $ctrl.registrarId = registrar.id;
      }
      else{
        $ctrl.registrarId = null;
      }
      $ctrl.onRegistrarChanged({registrar:registrar});
    };

    $ctrl.searchRegistrar = function searchRegistrar(input) {
      var params = {'search': input, 'priceDomainId': $ctrl.priceDomainId};
      return PluginsDomainsRegistrarsApi.get(params).$promise.then(function (data) {
        return data.objects;
      })
    };
  }
})();
