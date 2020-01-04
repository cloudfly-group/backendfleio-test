(function(){
  'use strict';
  angular.module('fleioStaff')
    .component('pluginsTodoTodoDetails', {
      templateUrl: 'staff/plugins/todo/todos/tododetails.html',
      controller: PluginsTodoTodoDetailsController,
      bindings: {
        todo: '<',
        createOptions: '<',
        onDelete: '&'
      }
    });

  PluginsTodoTodoDetailsController.$inject = ['$state', 'gettextCatalog', 'PluginsTodoTodoApi',
    'FlNotificationService', 'FlResolveErrorHandler'];
  function PluginsTodoTodoDetailsController($state, gettextCatalog, PluginsTodoTodoApi,
                                            FlNotificationService, FlResolveErrorHandler) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit(){
      $ctrl.commentText = '';
    };

    $ctrl.onTODODeleted = function onTODODeleted() {
      $state.go('pluginsTodoTodos');
    };

    $ctrl.refreshTODO = function refreshTodo() {
      PluginsTodoTodoApi.get({'id':$ctrl.todo.id}).$promise
        .then(function (data) {
            $ctrl.todo = data;
        }).catch(FlResolveErrorHandler.handleError);
    };

    $ctrl.comment = function comment(closeTodo){
        PluginsTodoTodoApi.post({
          'id': $ctrl.todo.id,
          'action': 'add_comment',
          'comment_text': $ctrl.commentText,
          'close_todo': closeTodo
        }).$promise.then(function () {
          FlNotificationService.add(gettextCatalog.getString('Comment added'));
          $ctrl.commentText ='';
          $ctrl.refreshTODO();
        });
    };
  }
})();
