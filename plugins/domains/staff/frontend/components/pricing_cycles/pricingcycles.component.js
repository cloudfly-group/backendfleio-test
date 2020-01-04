(function () {
  'use strict';

  angular.module('fleioStaff')
    .component('pluginsDomainsPricingCycles', {
      templateUrl: 'staff/plugins/domains/pricing/pricingcycles.html',
      controller: pluginsDomainsPricingCycles,
      bindings: {
          priceCycles: '=',
          displayText: '@',
          setRelativePrices: '&',
          priceChanged: '&'
      }
    });

  pluginsDomainsPricingCycles.$inject = ['gettext'];
  function pluginsDomainsPricingCycles(gettext){
    var $ctrl = this;

    $ctrl.$onInit = function $onInit() {
    };

    $ctrl.getYearsText = function getYearsText(years){
        if (0 === years){
            return '1 ' + gettext('year');
        }
        else {
            return years + ' ' + gettext('years');
        }
    };

    $ctrl.getUseRelativePricesTooltip = function getUseRelativePricesTooltip(){
        if ($ctrl.priceCycles.currency.is_default) {
            return gettext('Relative prices cannot be applied to default currency.')
        } else {
            return gettext('Calculate prices based on default currency prices and and exchange rate.')
        }
    };

    $ctrl.autofillPrices = function autofillPrices() {
        var index, len;
        if ($ctrl.priceCycles.prices_per_years[0] !== null) {
          for (index = 1, len = $ctrl.priceCycles.prices_per_years.length; index < len; index++) {
              var newPrice = $ctrl.priceCycles.prices_per_years[0] * (1 + index);
              newPrice = parseFloat(newPrice.toFixed(2));
              $ctrl.priceCycles.prices_per_years[index] = newPrice;
          }
        } else {
          for (index = 1, len = $ctrl.priceCycles.prices_per_years.length; index < len; index++) {
              $ctrl.priceCycles.prices_per_years[index] = null;
          }
        }
        $ctrl.priceChanged();
    };

    $ctrl.relativePricesChanged = function relativePricesChanged() {
        if ($ctrl.priceCycles.relative_prices) {
            $ctrl.setRelativePrices();
        }
    };

    $ctrl.onPriceChanged = function onPriceChanged() {
        $ctrl.priceChanged();
    };
  }
})();
