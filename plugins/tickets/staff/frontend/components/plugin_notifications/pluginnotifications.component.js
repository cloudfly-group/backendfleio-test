(function () {
  'use strict';

    angular.module('fleioStaff')
        .factory('TicketsPluginNotificationsService', TicketsPluginNotificationsService);
    TicketsPluginNotificationsService.$inject = [];
    function TicketsPluginNotificationsService() {
        return {
            loaded: false,
            count: 0
        }
    }

  angular.module('fleioStaff')
    .component('pluginsTicketsPluginNotifications', {
      templateUrl: 'staff/plugins/tickets/plugin_notifications/pluginnotifications.html',
      controller: PluginsTicketsPluginsNotificationsController,
      bindings: {
          data: '<'
      }
    });
    PluginsTicketsPluginsNotificationsController.$inject = ['$state', 'PluginsTicketsTicketsApi', 'TicketsPluginNotificationsService', 'FlOsTimer', 'FlGlobalRefresh', 'FlAuthService'];
    function PluginsTicketsPluginsNotificationsController($state, PluginsTicketsTicketsApi, TicketsPluginNotificationsService, FlOsTimer, FlGlobalRefresh, FlAuthService) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {
        $ctrl.globalRefresh = FlGlobalRefresh;
        $ctrl.notificationsService = TicketsPluginNotificationsService;
        if ($ctrl.notificationsService.loaded !== true) {
            $ctrl.notificationsService.loaded = true;
            $ctrl.refreshTimer = FlOsTimer(refreshNotifications, 30000);
            $ctrl.refreshTimer.start();
            $ctrl.globalRefresh.timers['tickets'] = $ctrl.refreshTimer;
            if (FlAuthService.userInfo.user) {
                PluginsTicketsTicketsApi.get({
                    'action': 'get_current_user_tickets_count'
                }).$promise.then(function (data) {
                    $ctrl.notificationsService.count = data.count;
                });
            }
            $ctrl.$onDestroy = onDestroy;
        }
    };

    function onDestroy() {
        $ctrl.refreshTimer.teardown();
    }

    function refreshNotifications() {
        if (FlAuthService.userInfo.user) {
            return PluginsTicketsTicketsApi.get({
                'action': 'get_current_user_tickets_count'
            }).$promise.then(function (data) {
                return $ctrl.notificationsService.count = data.count;
            });
        }
    }

  }

})();
