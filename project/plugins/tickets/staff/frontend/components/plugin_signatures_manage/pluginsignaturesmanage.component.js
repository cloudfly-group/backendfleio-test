(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsTicketsPluginSignaturesManage', {
      templateUrl: 'staff/plugins/tickets/plugin_signatures_manage/pluginsignaturesmanage.html',
      controller: pluginsTicketsPluginSignaturesManageController,
      bindings: {
          data: '<'
      }
    });
    pluginsTicketsPluginSignaturesManageController.$inject = [];
    function pluginsTicketsPluginSignaturesManageController() {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {

    };
    }

})();
