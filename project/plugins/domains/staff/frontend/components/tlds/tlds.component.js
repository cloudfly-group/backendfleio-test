(function () {
    'use strict';

    angular.module('fleioStaff')
        .component('pluginsDomainsTlds', {
            templateUrl: 'staff/plugins/domains/tlds/tlds.html',
            controller: PluginsDomainsTldsController,
            bindings: {
                tlds: '<'
            }
        });

    PluginsDomainsTldsController.$inject = ['gettext', 'FlSearchService', 'FlOsTimer', 'FlDetectIdleService'];
    function PluginsDomainsTldsController(gettext, FlSearchService, FlOsTimer, FlDetectIdleService){
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            FlSearchService.info.enabled = true;
            FlSearchService.info.label = gettext('Search TLDs');
            FlSearchService.info.service = $ctrl.tlds;
            $ctrl.refreshTimer = FlOsTimer($ctrl.refreshTLDs, 30000);
            $ctrl.refreshTimer.start();
            FlDetectIdleService.init(function () {
                return $ctrl.refreshTimer.start();
            }, function () {
                return $ctrl.refreshTimer.stop();
            });
        };

        $ctrl.$onDestroy = function onDestroy() {
            $ctrl.refreshTimer.teardown();
            FlDetectIdleService.uninit();
        };

        $ctrl.refreshTLDs = function refreshTLDs() {
            $ctrl.tlds.fetchData();
        };

        $ctrl.onTLDDeleted = function onTLDDeleted() {

        };
    }
})();
