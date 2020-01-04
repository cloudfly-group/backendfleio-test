(function(){
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsDomainsInputRegistrarConnector', {
      templateUrl: 'staff/plugins/domains/input_registrar_connector/inputregistrarconnector.html',
      controller: PluginsDomainsInputRegistrarConnectorController,
      bindings:  {
        registrarConnectorId: '=',
        onRegistrarConnectorChanged: '&'
      }
  });

  PluginsDomainsInputRegistrarConnectorController.$inject = ['$element', 'PluginsDomainsRegistrarConnectorsApi'];
  function PluginsDomainsInputRegistrarConnectorController($element, PluginsDomainsRegistrarConnectorsApi){
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
      if ($ctrl.registrarConnectorId) {
        PluginsDomainsRegistrarConnectorsApi.get({'id': $ctrl.registrarConnectorId}).$promise
          .then(function (registrarConnector) {
            $ctrl.registrarConnector = registrarConnector
          });
      }
    };

    $ctrl.selectedRegistrarConnectorChanged = function selectedRegistrarConnectorChanged(registrarConnector) {
      if (typeof registrarConnector !== 'undefined') {
        $ctrl.registrarConnectorId = registrarConnector.id;
      }
      else{
        $ctrl.registrarConnectorId = null;
      }
      $ctrl.onRegistrarConnectorChanged({registrarConnector:registrarConnector});
    };

    $ctrl.searchRegistrarConnector = function searchRegistrarConnector(input) {
      var params = {'search': input};
      return PluginsDomainsRegistrarConnectorsApi.get(params).$promise.then(function (data) {
        return data.objects;
      })
    };
  }
})();
