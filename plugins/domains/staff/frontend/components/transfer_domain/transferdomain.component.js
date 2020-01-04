(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsDomainsTransferDomain', {
      templateUrl: 'staff/plugins/domains/transfer_domain/transferdomain.html',
      controller: PluginsDomainsTransferDomainController,
      bindings: {
      }
    });

  PluginsDomainsTransferDomainController.$inject = ['gettext',
      'PluginsDomainsOrderDomainApi', 'FlNotificationService', '$state'];
  function PluginsDomainsTransferDomainController(gettext, PluginsDomainsOrderDomainApi,
                                                  FlNotificationService, $state){
    var $ctrl = this;
    $ctrl.operation = 'register';
    $ctrl.checkAvailabilityInProgress = false;
    $ctrl.domain = {
        operation: 'transfer'
    };

    $ctrl.$onInit = function $onInit() {
    };

    $ctrl.checkIfDomainIsAvailable = function checkIfDomainIsAvailable() {
        $ctrl.checkResults = {};
        $ctrl.checkAvailabilityInProgress = true;
        PluginsDomainsOrderDomainApi.get({
            action:'is_available_for_transfer',
            domain_name: $ctrl.domain.name,
            client_id: $ctrl.domain.client
        }).$promise.then(function (checkResults) {
            $ctrl.checkResults = checkResults;
            $ctrl.domain.name = $ctrl.checkResults.adjusted_name;
        }).catch(function (reason) {
            FlNotificationService.add(gettext('Error when checking if domain is available.'))
        }).finally(function () {
            $ctrl.checkAvailabilityInProgress = false;
        })
    };

    $ctrl.getYearsText = function getYearsText(years){
        var adjustedYears = years + 1;
        if (0 === adjustedYears){
            return '1 ' + gettext('year');
        }
        else {
            return adjustedYears + ' ' + gettext('years');
        }
    };

    $ctrl.transferDomain = function transferDomain() {
      if (!$ctrl.checkResults) {
        $ctrl.checkIfDomainIsAvailable();
      }
      if (!$ctrl.checkResults.available){
          return;
      }
        PluginsDomainsOrderDomainApi.save({
            domain: $ctrl.domain,
            action: 'transfer_domain',
            client_id: $ctrl.domain.client
        }).$promise.then(function (value) {
            var orderId = value.order_id;
            $state.go('billingOrderDetails', {id:orderId});
        }).catch(function (reason) {
        })
    };

    $ctrl.onClientChanged = function onClientChanged(client) {
        $ctrl.checkResults = {}
    }
  }
})();
