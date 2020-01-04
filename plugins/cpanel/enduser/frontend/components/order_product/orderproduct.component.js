(function () {
  'use strict';
  angular.module('fleio')
    .component('pluginsCpanelOrderProduct', {
      templateUrl: 'site/plugins/cpanel/order_product/orderproduct.html',
      controller: PluginsCpanelOrderController,
      bindings: {
        data: '='
      }
    });

  PluginsCpanelOrderController.$inject = [];
  function PluginsCpanelOrderController() {

  }
})();
