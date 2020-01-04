 (function () {
   'use strict';

   angular.module('fleioStaff')
     .component('pluginsTicketsSignatures', {
       templateUrl: 'staff/plugins/tickets/signatures/signatures.html',
       controller: FlStaffSignaturesController,
       bindings: {
         signatures: '<',
         departments: '<',
       }
     });

   FlStaffSignaturesController.$inject = ['gettextCatalog', 'FlNotificationService', 'PluginsTicketsSignaturesApi', 'CONFIG', '$mdDialog', 'FlResolveErrorHandler', 'FlUiUtilsService'];

   function FlStaffSignaturesController(gettextCatalog, FlNotificationService, PluginsTicketsSignaturesApi, CONFIG, $mdDialog, FlResolveErrorHandler, FlUiUtilsService) {
     var $ctrl = this;

     $ctrl.$onInit = function $onInit() {
        $ctrl.savingSignatures = false;
        $ctrl.tinymceOptions = CONFIG.tiny_mce_options;
     };

     function refreshSignatures() {
        PluginsTicketsSignaturesApi.get({
            'action': 'get_signatures_for_current_user'
        }).$promise.then(function(data){
            $ctrl.signatures = data;
            $ctrl.savingSignatures = false;
        }).catch(FlResolveErrorHandler.handleError);
     }

     $ctrl.addGlobalSignature = function addGlobalSignature() {
        PluginsTicketsSignaturesApi.post({
            'action': 'add_global_signature'
        }).$promise.then(function(data){
            FlNotificationService.add(gettextCatalog.getString('Default signature successfully added'));
            refreshSignatures();
        });
     };

     $ctrl.addNewDepartmentSignature = function addNewDepartmentSignature() {
        if (!$ctrl.selectedDepartment) {
            FlNotificationService.add(gettextCatalog.getString('Please select a department'));
            return ;
        }
        PluginsTicketsSignaturesApi.post({
            'department': $ctrl.selectedDepartment,
            'content': '',
        }).$promise.then(function(data){
            FlNotificationService.add(gettextCatalog.getString('Signature successfully added'));
            refreshSignatures();
        }).catch(function(err) {
            if (err.data.non_field_errors) {
                FlUiUtilsService.messagesDlg(err.data.non_field_errors, gettextCatalog.getString('Cannot add signature'));
            } else {
                FlResolveErrorHandler.handleError(err);
            }
        });
     };

     $ctrl.deleteSignature = function deleteSignature(signature) {
         return FlUiUtilsService.yesNoDlg(gettextCatalog.getString('Are you sure?'),
            gettextCatalog.getString('Delete signature'),
            gettextCatalog.getString('Delete signature')).then(function () {
            return PluginsTicketsSignaturesApi.delete({
              'id': signature.id
            }).$promise.then(function () {
              refreshSignatures();
              FlNotificationService.add(gettextCatalog.getString('Signature successfully deleted'));
            }).catch(function(error){
                FlResolveErrorHandler.handleError(error);
            });
          }).catch(function(){});
     };

     $ctrl.saveSignatures = function saveSignatures() {
        $ctrl.savingSignatures = true;
        return PluginsTicketsSignaturesApi.post({
            'action': 'save_signatures',
            'objects': $ctrl.signatures.objects
        }).$promise.then(function(data){
            refreshSignatures();
            FlNotificationService.add(gettextCatalog.getString('Signatures successfully updated'));
        }).catch(function(error){
            $ctrl.savingSignatures = false;
            FlResolveErrorHandler.handleError(error);
        });
     };

   }

 })();
