(function () {
    'use strict';

    angular.module('fleioStaff')
        .controller('PluginsTicketsTicketUpdatesEditController', PluginsTicketsTicketUpdatesEditController);

    PluginsTicketsTicketUpdatesEditController.$inject = ['$mdDialog', 'message', 'PluginsTicketsTicketUpdatesApi', 'PluginsTicketsTicketNotesApi', 'CONFIG'];
    function PluginsTicketsTicketUpdatesEditController($mdDialog, message, PluginsTicketsTicketUpdatesApi, PluginsTicketsTicketNotesApi, CONFIG) {
        var $ctrl = this;

        $ctrl.$onInit = function $onInit() {
            $ctrl.message = angular.copy(message);
            $ctrl.tinymceOptions = CONFIG.tiny_mce_options;
        };

        $ctrl.saveReply = function () {
            document.activeElement.blur();
            if (!($ctrl.editReply.$invalid || $ctrl.submitPending)) {
                $ctrl.submitPending = true;
                if ($ctrl.message['message_type'] === 'ticketupdate') {
                    return PluginsTicketsTicketUpdatesApi.update({
                        'id': $ctrl.message.id,
                        'reply_text': $ctrl.message.message
                    }).$promise.then(function (data) {
                        $mdDialog.hide(data);
                        return data;
                    }).catch(function (error) {
                        $ctrl.submitPending = false;
                        $ctrl.backendErrors = error.data;
                    });
                } else {
                    return PluginsTicketsTicketNotesApi.update({
                        'id': $ctrl.message.id,
                        'note_text': $ctrl.message.message
                    }).$promise.then(function (data) {
                        $mdDialog.hide(data);
                        return data;
                    }).catch(function (error) {
                        $ctrl.submitPending = false;
                        $ctrl.backendErrors = error.data;
                    });
                }
            }
        };

        $ctrl.close = function close() {
            return $mdDialog.cancel();
        };
    }

})();
