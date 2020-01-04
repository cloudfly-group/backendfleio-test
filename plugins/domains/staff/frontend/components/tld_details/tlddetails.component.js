(function () {
  'use strict';
  angular.module('fleioStaff')
    .component('pluginsDomainsTldDetails', {
      templateUrl: 'staff/plugins/domains/tld_details/tlddetails.html',
      controller: pluginsDomainsTldDetails,
      bindings: {
          tld : '<'
      }
    });

  pluginsDomainsTldDetails.$inject = ['gettext', 'PluginsDomainsTLDsApi', 'FlNotificationService',
    'PluginsDomainsRegistrarConnectorsApi'];
  function pluginsDomainsTldDetails(gettext, PluginsDomainsTLDsApi, FlNotificationService,
                                    PluginsDomainsRegistrarConnectorsApi){
    var $ctrl = this;
    $ctrl.group_by = 'currency';

    $ctrl.$onInit = function $onInit() {
        PluginsDomainsTLDsApi.get({
            id: $ctrl.tld.id,
            action: 'get_prices'
        }).$promise
        .then(function (data) {
            $ctrl.domainPrices = data.domain_prices;
            $ctrl.domainAddonPrices = data.domain_addon_prices;
        });
        $ctrl.getRegistrarsPrices();

    };

    $ctrl.updateRegistrarPrices = function updateRegistrarPrices(connector_name) {
      var params = {action: 'update_registrar_prices', tld_name: $ctrl.tld.name};
      if (!!connector_name) {
        params['connector'] = connector_name;
      }
      PluginsDomainsRegistrarConnectorsApi.post(params).$promise
        .then(function(data) {
          $ctrl.getRegistrarsPrices();
          return data;
        }).catch(function (error){
          var message;
          if (error.data && error.data.length) {
            message = error.data[0];
          } else if (error.data && !error.data.length) {
            message = error.data;
          } else if (error.detail) {
            message = error.detail;
          }
          FlNotificationService.add(message)
      })
    };

    $ctrl.getRegistrarsPrices = function getRegistrarPrices() {
      PluginsDomainsRegistrarConnectorsApi.query({'action': 'registrar_prices', 'tld_name': $ctrl.tld.name}).$promise
        .then(function (data) {
          $ctrl.loadingRegistrarPrices = true;
          $ctrl.registrarsConnectorsPrices = data;
        })
        .finally(function() {
          $ctrl.loadingRegistrarPrices = false;
        })
    };

    $ctrl.setRelativePrices = function setRelativePrices(cycles_idx) {
        var default_price_cycle_index =
            $ctrl.domainPrices.default_price_cycles[$ctrl.domainPrices.price_cycles_list[cycles_idx].price_type];
        var default_price_cycles = $ctrl.domainPrices.price_cycles_list[default_price_cycle_index];

        var currency = $ctrl.domainPrices.price_cycles_list[cycles_idx].currency;
        for(var index = 0, len = $ctrl.domainPrices.price_cycles_list[cycles_idx].prices_per_years.length; index < len; index++){
            if (default_price_cycles.prices_per_years[index] === null){
                $ctrl.domainPrices.price_cycles_list[cycles_idx].prices_per_years[index] = null;
            } else {
                var default_year_price = default_price_cycles.prices_per_years[index];
                var newPrice = default_year_price * currency.rate;
                newPrice = parseFloat(newPrice.toFixed(2));
                $ctrl.domainPrices.price_cycles_list[cycles_idx].prices_per_years[index] = newPrice;
            }
        }
    };

    $ctrl.setAddonRelativePrices = function setAddonRelativePrices(cycles_idx) {
        var default_price_cycle_index =
            $ctrl.domainAddonPrices.default_price_cycles[$ctrl.domainAddonPrices.price_cycles_list[cycles_idx].price_type];
        var default_price_cycles = $ctrl.domainAddonPrices.price_cycles_list[default_price_cycle_index];

        var currency = $ctrl.domainAddonPrices.price_cycles_list[cycles_idx].currency;
        for(var index = 0, len = $ctrl.domainAddonPrices.price_cycles_list[cycles_idx].prices_per_years.length; index < len; index++){
            if (default_price_cycles.prices_per_years[index] === null){
                $ctrl.domainAddonPrices.price_cycles_list[cycles_idx].prices_per_years[index] = null;
            } else {
                var default_year_price = default_price_cycles.prices_per_years[index];
                var newPrice = default_year_price * currency.rate;
                newPrice = parseFloat(newPrice.toFixed(2));
                $ctrl.domainAddonPrices.price_cycles_list[cycles_idx].prices_per_years[index] = newPrice;
            }
        }
    };

    $ctrl.savePrices = function savePrices() {
        PluginsDomainsTLDsApi.save({
            id: $ctrl.tld.id,
            action: 'save_prices',
            domain_prices: $ctrl.domainPrices
        }).$promise
            .then( function(data) {
                FlNotificationService.add(gettext('Prices saved'));
                return data;
            })
            .catch( function(error) {
                FlNotificationService.add('Error saving prices')
            });
    };

    $ctrl.saveAddonPrices = function savePrices() {
        PluginsDomainsTLDsApi.save({
            id: $ctrl.tld.id,
            action: 'save_prices',
            domain_addon_prices: $ctrl.domainAddonPrices
        }).$promise
            .then( function(data) {
                FlNotificationService.add(gettext('Addon prices saved'));
                return data;
            })
            .catch( function(error) {
                FlNotificationService.add('Error saving addon prices')
            });
    };

    $ctrl.saveRegistrars = function saveRegistrars() {
        // TODO: this now saves whole TLD, ensure we have no issues with this
        PluginsDomainsTLDsApi.update($ctrl.tld).$promise
            .then(function(data) {
                FlNotificationService.add(gettext('Registrars saved'));
                $ctrl.getRegistrarsPrices();
                return data;
            })
            .catch(function(error) {
                FlNotificationService.add('Error saving registrars')
            });
    };

    $ctrl.priceChanged = function priceChanged(cycles_idx) {
        var changedPriceCycles = $ctrl.domainPrices.price_cycles_list[cycles_idx];
        if (changedPriceCycles.currency.is_default) {
            for (var cycles_index = 0; cycles_index < $ctrl.domainPrices.price_cycles_list.length; cycles_index++){
                var priceCycles = $ctrl.domainPrices.price_cycles_list[cycles_index];
                if ((priceCycles.price_type === changedPriceCycles.price_type) &&
                    !priceCycles.currency.is_default && priceCycles.relative_prices){
                    $ctrl.setRelativePrices(cycles_index);
                }
            }
        }
    };

    $ctrl.addonPriceChanged = function addonPriceChanged(cycles_idx) {
        var changedPriceCycles = $ctrl.domainAddonPrices.price_cycles_list[cycles_idx];
        if (changedPriceCycles.currency.is_default) {
            for (var cycles_index = 0; cycles_index < $ctrl.domainAddonPrices.price_cycles_list.length; cycles_index++){
                var priceCycles = $ctrl.domainAddonPrices.price_cycles_list[cycles_index];
                if ((priceCycles.price_type === changedPriceCycles.price_type) &&
                    !priceCycles.currency.is_default && priceCycles.relative_prices){
                    $ctrl.setAddonRelativePrices(cycles_index);
                }
            }
        }
    }
  }
})();
