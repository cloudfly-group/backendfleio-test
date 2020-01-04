(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsTodoTodoActions',{
      templateUrl: 'staff/plugins/todo/todos/todoactions.html',
      controller: PluginsTodoTodoActionsController,
      bindings: {
        todo: '<',
        createOptions: '<',
        addButton: '<',
        onTodoDeleted: '&',
        onTodoChanged: '&',
        onTodoAdded: '&'
      }
    });

  PluginsTodoTodoActionsController.$inject = ['gettextCatalog', '$mdDialog', 'FlUiUtilsService',
      'PluginsTodoTodoApi', 'FlNotificationService'];
  function PluginsTodoTodoActionsController(gettextCatalog, $mdDialog, FlUiUtilsService,
                                            PluginsTodoTodoApi, FlNotificationService) {
    var $ctrl = this;

    $ctrl.deleteTODO = function deleteTODO() {
      FlUiUtilsService.yesNoDlg(gettextCatalog.getString('Are you sure?'), gettextCatalog.getString('Delete TODO'))
        .then(function () {
          PluginsTodoTodoApi.delete({'id':$ctrl.todo.id}).$promise
            .then(function () {
              $ctrl.onTodoDeleted();
            });
        }).catch(function () {});
    };

    $ctrl.editTODO = function editTODO($event, edit) {
      return $mdDialog.show({
        templateUrl: 'staff/plugins/todo/todos/todoedit.html',
        controller: 'PluginsTodoTodoEditController',
        controllerAs: '$ctrl',
        parent: angular.element(document.body),
        clickOutsideToClose: false,
        locals: {
          todo: $ctrl.todo,
          isEdit: edit,
          createOptions: $ctrl.createOptions
        },
        targetEvent: $event
      }).then(function () {
        if (edit) {
          $ctrl.onTodoChanged();
        }
        else {
          $ctrl.onTodoAdded();
        }

        FlNotificationService.add(
          gettextCatalog.getString(edit ? 'TODO updated' :  'TODO added')
        );
      }).catch(function(){});
    };
  }
})();

