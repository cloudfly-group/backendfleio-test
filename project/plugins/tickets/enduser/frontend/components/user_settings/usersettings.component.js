(function () {
  'use strict';

  angular.module('fleio')
    .component('pluginsTicketsUserSettings', {
      templateUrl: 'site/plugins/tickets/user_settings/usersettings.html',
      controller: PluginsTicketsUserSettingsController,
      bindings: {
          data: '='
      },
      require: {
        parentForm: '^form'
      }
    });

  PluginsTicketsUserSettingsController.$inject = [];
  function PluginsTicketsUserSettingsController() {
    var $ctrl = this;
    $ctrl.$onInit = $onInit;

    function $onInit() {
        if (!$ctrl.data.tickets_user_settings) {
            $ctrl.data.tickets_user_settings = {};
        }
    }
  }
})();
