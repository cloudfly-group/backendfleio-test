(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsTodoProductSettings', {
      templateUrl: 'staff/plugins/todo/product_settings/productsettings.html',
      controller: PluginsTodoProductSettingsController,
      bindings: {
          data: '='
      },
      require: {
        parentForm: '^form'
      }
    });

  PluginsTodoProductSettingsController.$inject = [];
  function PluginsTodoProductSettingsController() {
    var $ctrl = this;
    $ctrl.$onInit = $onInit;

    function $onInit() {
        if (!$ctrl.data.todo_product_settings) {
            $ctrl.data.todo_product_settings = {};
        }
    }
  }
})();
