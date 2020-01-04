(function(){
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsDomainsInputTld', {
      templateUrl: 'staff/plugins/domains/input_tld/inputtld.html',
      controller: PluginsDomainsInputTldController,
      bindings:  {
        tldId: '=',
        onTldChanged: '&'
      }
  });

  PluginsDomainsInputTldController.$inject = ['$element', 'PluginsDomainsTLDsApi'];
  function PluginsDomainsInputTldController($element, PluginsDomainsTLDsApi){
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
      if ($ctrl.tldId) {
        PluginsDomainsTLDsApi.get({'id': $ctrl.tldId}).$promise
          .then(function (tld) {
            $ctrl.tld = tld
          });
      }
    };

    $ctrl.selectedTLDChanged = function selectedTLDChanged(tld) {
      if (typeof tld !== 'undefined') {
        $ctrl.tldId = tld.id;
      }
      else{
        $ctrl.tldId = null;
      }
      $ctrl.onTldChanged({tld:tld});
    };

    $ctrl.searchTLD = function searchTLD(input) {
      var params = {'search': input};
      if ($ctrl.staffOnly) {
        params['is_staff'] = true;
      }

      return PluginsDomainsTLDsApi.get(params).$promise.then(function (data) {
        return data.objects;
      })
    };
  }
})();
