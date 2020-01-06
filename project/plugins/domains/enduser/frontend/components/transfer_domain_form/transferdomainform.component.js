(function () {
  'use strict';

  angular.module('fleio')
    .component('pluginsDomainsTransferDomainForm', {
      templateUrl: 'site/plugins/domains/transfer_domain_from/transferdomainform.html',
      controller: PluginsDomainsTransferDomainFormController,
      bindings: {
      }
    });

  PluginsDomainsTransferDomainFormController.$inject = ['gettext',
      'PluginsDomainsOrderDomainApi', 'FlNotificationService', '$state'];
  function PluginsDomainsTransferDomainFormController(gettext, PluginsDomainsOrderDomainApi,
                                                  FlNotificationService, $state){
    var $ctrl = this;
    $ctrl.operation = 'register';
    $ctrl.checkAvailabilityInProgress = false;
    $ctrl.domain = {
        operation: 'transfer'
    };

    $ctrl.$onInit = function $onInit() {
        if ($ctrl.data) {
            $ctrl.domain.name = $ctrl.data.domain_name;
            if ($ctrl.data.clientCreateOptions) {
                $ctrl.clientCreateOptions = $ctrl.data.clientCreateOptions;
            }
            $ctrl.checkIfDomainIsAvailable();
        }
    };

    $ctrl.checkIfDomainIsAvailable = function checkIfDomainIsAvailable() {
        $ctrl.checkResults = {};
        $ctrl.checkAvailabilityInProgress = true;
        PluginsDomainsOrderDomainApi.get({
            action:'is_available_for_transfer',
            domain_name: $ctrl.domain.name
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
            action: 'transfer_domain'
        }).$promise.then(function (value) {
            $state.go('cart');
        }).catch(function (reason) {
        })
    }
  }
})();
