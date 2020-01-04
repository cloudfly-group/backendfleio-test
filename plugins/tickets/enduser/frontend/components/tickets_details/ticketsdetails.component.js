(function(){
    'use strict';
    angular.module('fleio')
        .component('pluginsTicketsTicketsDetails', {
            templateUrl: 'staff/plugins/tickets/tickets/ticketsdetails.html',
            controller: PluginsTicketsTicketsDetailsController,
            bindings: {
                ticket: '<',
                createOptions: '<'
            }
        });

    PluginsTicketsTicketsDetailsController.$inject = ['$state', 'gettextCatalog', 'PluginsTicketsTicketsApi',
        'FlNotificationService', 'FlResolveErrorHandler', 'FlUiUtilsService', '$mdDialog', '$sce', 'CONFIG',
        'PluginsTicketsTicketUpdatesApi', 'PluginsTicketsTicketAttachmentsApi', 'FlAuthService', '$anchorScroll', '$q',
        'FlLocalStorage'];
    function PluginsTicketsTicketsDetailsController($state, gettextCatalog, PluginsTicketsTicketsApi,
        FlNotificationService, FlResolveErrorHandler, FlUiUtilsService, $mdDialog, $sce, CONFIG,
        PluginsTicketsTicketUpdatesApi, PluginsTicketsTicketAttachmentsApi, FlAuthService, $anchorScroll, $q,
        FlLocalStorage) {
        var $ctrl = this;

        function getTicketLocalStorageReplyKey() {
            return 'ticket' + $ctrl.ticket.id + 'Reply';
        }

        $ctrl.$onInit = function $onInit(){
            $ctrl.currentUser = FlAuthService.userInfo.user;
            var temporarySavedReply = FlLocalStorage.get(getTicketLocalStorageReplyKey(), true);
            if (temporarySavedReply) {
                $ctrl.replyText = temporarySavedReply;
            } else {
                $ctrl.replyText = '';
            }
            $ctrl.tinymceOptions = CONFIG.tiny_mce_options;
            $ctrl.tinymceOptions['height'] = 300;
            $ctrl.uploadWasSubmitted = false;
            $ctrl.maxFileSizeReadable = 'Max. ' + readableBytes(
                $ctrl.createOptions['MAX_TICKET_ATTACHMENT_SIZE']
            ) + ' / file';
        };

        function readableBytes(bytes) {
            var i = Math.floor(Math.log(bytes) / Math.log(1024));
            var sizes = ['B', 'KB', 'MB', 'GB'];
            return (bytes / Math.pow(1024, i)).toFixed(2) * 1 + ' ' + sizes[i];
        }

        $ctrl.trustAsHtml = function(string) {
            return $sce.trustAsHtml(string);
        };

        $ctrl.onTicketsDeleted = function onTicketsDeleted() {
            $state.go('pluginsTicketsTickets');
        };

        $ctrl.refreshTicket = function refreshTicket() {
            PluginsTicketsTicketsApi.get({'id':$ctrl.ticket.id}).$promise
            .then(function (data) {
                $ctrl.ticket = data;
            }).catch(FlResolveErrorHandler.handleError);
        };

        $ctrl.reply = function reply(attachmentInputID){
            var files_to_upload = document.getElementById(attachmentInputID).files;
            if (files_to_upload.length) {
                $ctrl.submitPending = true;
                $ctrl.uploadInProgress = true;
                // if we have files to upload, upload them then create reply and make the
                // association in the backend
                for (var i = 0; i < files_to_upload.length; i++) {
                    // check each file size
                    if (files_to_upload[i].size > $ctrl.createOptions['MAX_TICKET_ATTACHMENT_SIZE']) {
                        $ctrl.uploadInProgress = false;
                        $ctrl.submitPending = false;
                        FlResolveErrorHandler.handleError({'data':
                                {'detail': gettextCatalog.getString('Attachment file size is too big.')}
                        });
                        return;
                    }
                }
                var queriesList = [];
                for (var j = 0; j < files_to_upload.length; j++) {
                    var fd = new FormData();
                    fd.append('data', files_to_upload[j]);
                    fd.append('file_name', files_to_upload[j].name);
                    queriesList.push(PluginsTicketsTicketAttachmentsApi.upload(fd).$promise);
                }

                $q.all(queriesList).then(function(data) {
                    var attachmentIds = '';
                    for (var data_pos = 0; data_pos < data.length; data_pos++) {
                        attachmentIds = attachmentIds + data[data_pos].id;
                        if (data_pos < data.length - 1) {
                            attachmentIds = attachmentIds + ',';
                        }
                    }
                    PluginsTicketsTicketsApi.post({
                        'id': $ctrl.ticket.id,
                        'action': 'add_reply',
                        'reply_text': $ctrl.replyText,
                        'associated_attachments': attachmentIds,
                    }).$promise.then(function (data) {
                        FlNotificationService.add(gettextCatalog.getString('Reply added'));
                        FlLocalStorage.removeItem(getTicketLocalStorageReplyKey(), true);
                        $ctrl.refreshTicket();
                        $ctrl.replyText = '';
                        $ctrl.submitPending = false;
                        $ctrl.uploadInProgress = false;
                        $ctrl.uploadWasSubmitted = true;
                    }).catch(function(error) {
                        $ctrl.submitPending = false;
                        $ctrl.uploadInProgress = false;
                        $ctrl.uploadWasSubmitted = true;
                        FlResolveErrorHandler.handleError(error);
                    });
                }).catch(function(error) {
                    $ctrl.submitPending = false;
                    $ctrl.uploadInProgress = false;
                    $ctrl.uploadWasSubmitted = true;
                    FlResolveErrorHandler.handleError(error);
                });

            } else {
                PluginsTicketsTicketsApi.post({
                    'id': $ctrl.ticket.id,
                    'action': 'add_reply',
                    'reply_text': $ctrl.replyText
                }).$promise.then(function (data) {
                    FlNotificationService.add(gettextCatalog.getString('Reply added'));
                    FlLocalStorage.removeItem(getTicketLocalStorageReplyKey(), true);
                    $ctrl.replyText = '';
                    $ctrl.refreshTicket();
                    $ctrl.submitPending = false;
                }).catch(function(error) {
                    $ctrl.submitPending = false;
                    FlResolveErrorHandler.handleError(error);
                });
            }
        };

        $ctrl.reopenTicket = function reopenTicket() {
            PluginsTicketsTicketsApi.post({
                'id': $ctrl.ticket.id,
                'action': 'reopen_ticket'
            }).$promise.then(function(data){
                $ctrl.refreshTicket();
            });
        };

        $ctrl.closeTicket = function closeTicket() {
            PluginsTicketsTicketsApi.post({
                'id': $ctrl.ticket.id,
                'action': 'close_ticket'
            }).$promise.then(function(data){
                $ctrl.refreshTicket();
            });
        };

        $ctrl.replyToReply = function replyToReply(quote, created_by) {
            quote = quote.split('\n');

            var newQuote = [];
            quote.forEach( function(element){
                element = element.replace('>', '> > ');
                newQuote.push(element);
            } );
            newQuote = newQuote.join('\n');
            if (created_by) {
                $ctrl.replyText = newQuote + '<em>' + gettextCatalog.getString('Quoted from ') + created_by.full_name +'</em><p></p>';
            } else {
                $ctrl.replyText = newQuote;
            }
            $anchorScroll('reply-box');
        };

        $ctrl.downloadAttachment = function downloadAttachment(attachmentId) {
            var url = CONFIG.api_url + '/plugins/tickets/ticket_attachments/' + attachmentId + '/download_file';
            window.open(url);
        };

        $ctrl.openAttachment = function openAttachment(attachmentId) {
            var url = CONFIG.api_url + '/plugins/tickets/ticket_attachments/' + attachmentId + '/load_file';
            window.open(url);
        };

        $ctrl.onReplyInputChange = function () {
            FlLocalStorage.set(getTicketLocalStorageReplyKey(), $ctrl.replyText, true);
        };

    }
})();
