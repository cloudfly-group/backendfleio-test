(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsTodoTodos', {
      templateUrl: 'staff/plugins/todo/todos/todos.html',
      controller: PluginsTodoTodosController,
      bindings: {
        todos: '<',
        createOptions: '<'
      }
    });

  PluginsTodoTodosController.$inject = ['gettext', 'FlSearchService'];
  function PluginsTodoTodosController(gettext, FlSearchService){
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {
      FlSearchService.info.enabled = true;
      FlSearchService.info.label = gettext('Search TODOs');
      FlSearchService.info.service = $ctrl.todos;
    };

    $ctrl.refreshTODOs = function refreshTODOs() {
      $ctrl.todos.fetchData();
    };
  }
})();
