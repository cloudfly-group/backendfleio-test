(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsOpenstackPluginConfiguration', {
      templateUrl: 'staff/plugins/openstack/plugin_configuration/pluginconfiguration.html',
      controller: PluginsOpenstackPluginConfigurationController,
      bindings: {
          data: '='
      }
    });

  PluginsOpenstackPluginConfigurationController.$inject = ['FlUiUtilsService', 'FlConfigurationsApi',
      'FlNotificationService', 'FlResolveErrorHandler', 'FlFeatureService'];
  function PluginsOpenstackPluginConfigurationController(FlUiUtilsService, FlConfigurationsApi, FlNotificationService,
                                                         FlResolveErrorHandler, FlFeatureService) {
    var $ctrl = this;
    $ctrl.$onInit = $onInit;
    $ctrl.goBackOrToState = FlUiUtilsService.goBackOrToState;

    function joinList(list) {
      if (angular.isArray(list)) {
        var list_str = '';
        list.forEach(function(elem) {
          if (list_str) {
            list_str += ', ';
          }
          list_str += elem;
        });
        return list_str
      }

      return list;
    }

    function $onInit() {
        FlConfigurationsApi.get({'id': $ctrl.data.id, 'section':'openstack'}).$promise
            .then(function (value) {
              $ctrl.openstackSettings = value;
              $ctrl.openstackSettings.auto_cleanup_image_types =
                  joinList($ctrl.openstackSettings.auto_cleanup_image_types);
            })
            .catch(FlResolveErrorHandler.handleError);
        $ctrl.features = FlFeatureService.features;
    }

    $ctrl.saveSettings = function (settingsID) {
      if ($ctrl.submitPending || $ctrl.openstackSettingsForm.$invalid) { return; }
      $ctrl.submitPending = true;
      $ctrl.backendErrors = null;

      var settingsToSave = angular.copy($ctrl.openstackSettings);
      if (angular.isString(settingsToSave.auto_cleanup_image_types)) {
        settingsToSave.auto_cleanup_image_types = settingsToSave.auto_cleanup_image_types.split(',')
          .filter(function(el) {
            el = el.replace(/^\s+|\s+$/g, '');
            return el.length !== 0
          });
      }

      FlConfigurationsApi.update({'id': $ctrl.data.id, 'section':'openstack'}, settingsToSave).$promise
        .then(function(data) {
          FlNotificationService.add(data.detail);
          if (data.settings) {
              $ctrl.openstackSettings = data.settings;
              $ctrl.openstackSettings.auto_cleanup_image_types =
                  joinList($ctrl.openstackSettings.auto_cleanup_image_types);
          }
        })
        .catch(function(error) { $ctrl.backendErrors = error.data })
        .finally(function() { $ctrl.submitPending = false })
    };
  }
})();
