(function(){
  'use strict';
  angular.module('fleioStaff')
  .component('pluginsDomainsClientInfo', {
    templateUrl: 'staff/plugins/domains/client_info/clientinfo.html',
    controller: PluginsDomainsClientInfoController,
    bindings: {
      data: '<'
    }
  });

  PluginsDomainsClientInfoController.$inject = ['$state', 'gettextCatalog', 'PluginsDomainsDomainsApi',
    'FlNotificationService', 'FlResolveErrorHandler'];
  function PluginsDomainsClientInfoController($state, gettextCatalog, PluginsDomainsDomainsApi,
                                            FlNotificationService, FlResolveErrorHandler) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
      $ctrl.currentPage = 1;
      $ctrl.nextPage = false;
      $ctrl.previousPage = false;
      $ctrl.loading = true;
      PluginsDomainsDomainsApi.get({
          client_id: $ctrl.data.id,
          action: 'get_client_domains',
          page: $ctrl.currentPage
      }).$promise.then(function (data) {
        $ctrl.loading = false;
        $ctrl.nextPage = !!data.next;
        $ctrl.previousPage = !!data.previous;
        $ctrl.domains = data.objects;
      }).catch(FlResolveErrorHandler.handleError);
    };

    $ctrl.refreshDomains = function refreshDomains() {
      $ctrl.loading = true;
      PluginsDomainsDomainsApi.get({
          client_id: $ctrl.data.id,
          action: 'get_client_domains',
          page: $ctrl.currentPage
      }).$promise.then(function (data) {
        $ctrl.loading = false;
        $ctrl.nextPage = !!data.next;
        $ctrl.previousPage = !!data.previous;
        $ctrl.domains = data.objects;
      })
    };

    $ctrl.changePage = function changePage(action){
        if (action === 'next') {
            $ctrl.currentPage = $ctrl.currentPage + 1;
            $ctrl.refreshDomains();
        }
        if (action === 'previous') {
            $ctrl.currentPage = $ctrl.currentPage - 1;
            $ctrl.refreshDomains();
        }
    };

  }
})();
