(function () {
  'use strict';

  angular.module('fleioStaff')
    .controller('PluginsTodoTodoEditController', PluginsTodoTodoEditController);

  PluginsTodoTodoEditController.$inject = ['$mdDialog', 'PluginsTodoTodoApi',
    'todo', 'isEdit', 'createOptions'];
  function PluginsTodoTodoEditController($mdDialog, PluginsTodoTodoApi,
                                         todo, isEdit, createOptions) {
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {
      $ctrl.isEdit = isEdit;
      $ctrl.createOptions = angular.copy(createOptions);
      $ctrl.statusesKeys = Object.keys($ctrl.createOptions.statuses);
      if (isEdit) {
        $ctrl.todo = angular.copy(todo);
      }
      else{
        $ctrl.todo = {
          'status':'open'
        };
      }
    };

    $ctrl.saveTODO = function () {
      document.activeElement.blur();
      if (!($ctrl.editTODO.$invalid || $ctrl.submitPending)) {
        $ctrl.submitPending = true;
        if ($ctrl.isEdit) {
          return PluginsTodoTodoApi.update({
            'id': $ctrl.todo.id
          }, $ctrl.todo).$promise.then(function (data) {
            $mdDialog.hide(data);
            return data;
          }).catch(function (error) {
            $ctrl.submitPending = false;
            $ctrl.backendErrors = error.data;
          });
        }
        else {
          return PluginsTodoTodoApi.save($ctrl.todo)
            .$promise.then(function (data) {
              $mdDialog.hide(data);
              return data;
            }).catch(function (error) {
              $ctrl.submitPending = false;
              $ctrl.backendErrors = error.data;
            });
        }
      }
    };

    $ctrl.close = function () {
      return $mdDialog.cancel();
    };
  }

})();
