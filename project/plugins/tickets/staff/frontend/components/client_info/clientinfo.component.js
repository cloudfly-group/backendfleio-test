(function(){
  'use strict';
  angular.module('fleioStaff')
  .component('pluginsTicketsClientInfo', {
    templateUrl: 'staff/plugins/tickets/client_info/clientinfo.html',
    controller: PluginsTicketsClientInfoController,
    bindings: {
      data: '<'
    }
  });

  PluginsTicketsClientInfoController.$inject = ['PluginsTicketsTicketsApi', 'FlResolveErrorHandler'];
  function PluginsTicketsClientInfoController(PluginsTicketsTicketsApi, FlResolveErrorHandler) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
        $ctrl.currentPage = 1;
        $ctrl.nextPage = false;
        $ctrl.previousPage = false;
        $ctrl.loading = true;
        PluginsTicketsTicketsApi.get({
          'client_id': $ctrl.data.id,
          'action': 'get_client_related_tickets',
          'page': $ctrl.currentPage
        }).$promise.then(function(data){
            $ctrl.loading = false;
            $ctrl.nextPage = !!data.next;
            $ctrl.previousPage = !!data.previous;
            $ctrl.tickets = data.objects;
        }).catch(FlResolveErrorHandler.handleError);
    };

    $ctrl.refreshTickets = function refreshTickets() {
      $ctrl.loading = true;
      PluginsTicketsTicketsApi.get({
          client_id: $ctrl.data.id,
          action: 'get_client_related_tickets',
          page: $ctrl.currentPage
      }).$promise.then(function (data) {
        $ctrl.loading = false;
        $ctrl.nextPage = !!data.next;
        $ctrl.previousPage = !!data.previous;
        $ctrl.tickets = data.objects;
      })
    };

    $ctrl.changePage = function changePage(action){
        if (action === 'next') {
            $ctrl.currentPage = $ctrl.currentPage + 1;
            $ctrl.refreshTickets();
        }
        if (action === 'previous') {
            $ctrl.currentPage = $ctrl.currentPage - 1;
            $ctrl.refreshTickets();
        }
    };

  }
})();
