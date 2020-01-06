(function () {
  'use strict';

  angular.module('fleioStaff')
    .factory('PluginsTodoTodoApi', PluginsTodoTodoApi);

  PluginsTodoTodoApi.$inject = ['FlResourceService', 'CONFIG'];
  function PluginsTodoTodoApi(FlResourceService, CONFIG) {
    return FlResourceService(CONFIG.api_url + "/plugins/todo/todo/:id/:action", {
      id: '@id',
      action: '@action'
    });
  }

})();
