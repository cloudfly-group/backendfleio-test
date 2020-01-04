(function () {
  'use strict';

    angular.module('fleioStaff')
        .factory('TodoPluginNotificationsService', TodoPluginNotificationsService);
    TodoPluginNotificationsService.$inject = [];
    function TodoPluginNotificationsService() {
        return {
            loaded: false,
            count: 0
        }
    }

  angular.module('fleioStaff')
    .component('pluginsTodoPluginNotifications', {
      templateUrl: 'staff/plugins/todo/count_todo/pluginnotifications.html',
      controller: PluginsTodoPluginsNotificationsController,
      bindings: {
          data: '<'
      }
    });

  PluginsTodoPluginsNotificationsController.$inject = ['$state', 'PluginsTodoTodoApi', 'TodoPluginNotificationsService', 'FlOsTimer', 'FlGlobalRefresh'];
  function PluginsTodoPluginsNotificationsController($state, PluginsTodoTodoApi, TodoPluginNotificationsService, FlOsTimer, FlGlobalRefresh) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {
    $ctrl.globalRefresh = FlGlobalRefresh;
        $ctrl.notificationsService = TodoPluginNotificationsService;
        if ($ctrl.notificationsService.loaded !== true) {
            $ctrl.notificationsService.loaded = true;
            $ctrl.refreshTimer = FlOsTimer(refreshNotifications, 30000);
            $ctrl.refreshTimer.start();
            $ctrl.globalRefresh.timers['todo'] = $ctrl.refreshTimer;
            PluginsTodoTodoApi.get({
                'action': 'get_current_user_todo_count'
            }).$promise.then(function(data){
                $ctrl.notificationsService.count = data.count;
            });
            $ctrl.$onDestroy = onDestroy;
        }
    };

    function onDestroy() {
        $ctrl.refreshTimer.teardown();
    }

    function refreshNotifications() {
      return PluginsTodoTodoApi.get({
          'action': 'get_current_user_todo_count'
      }).$promise.then(function(data){
          return $ctrl.notificationsService.count = data.count;
      });
    }

  }
})();
