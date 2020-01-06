(function(){
    'use strict';
    angular.module('fleioStaff')
        .component('pluginsTicketsTicketsDetails', {
            templateUrl: 'staff/plugins/tickets/tickets/ticketsdetails.html',
            controller: PluginsTicketsTicketsDetailsController,
            bindings: {
                ticket: '<',
                createOptions: '<'
            }
        });

    PluginsTicketsTicketsDetailsController.$inject = ['$state', 'gettextCatalog', 'PluginsTicketsTicketsApi',
        'FlNotificationService', 'FlResolveErrorHandler', 'PluginsTicketsTicketNotesApi', 'FlUiUtilsService', '$mdDialog', '$sce', 'CONFIG',
        'PluginsTicketsTicketUpdatesApi', 'PluginsTicketsTicketAttachmentsApi', 'FlAuthService', '$anchorScroll', '$q',
        'FlLocalStorage'];
    function PluginsTicketsTicketsDetailsController($state, gettextCatalog, PluginsTicketsTicketsApi,
        FlNotificationService, FlResolveErrorHandler, PluginsTicketsTicketNotesApi, FlUiUtilsService, $mdDialog, $sce, CONFIG,
        PluginsTicketsTicketUpdatesApi, PluginsTicketsTicketAttachmentsApi, FlAuthService, $anchorScroll, $q,
        FlLocalStorage) {
        var $ctrl = this;

        function getTicketLocalStorageReplyKey() {
            return 'ticket' + $ctrl.ticket.id + 'Reply';
        }

        $ctrl.$onInit = function $onInit(){
            var temporarySavedReply = FlLocalStorage.get(getTicketLocalStorageReplyKey(), true);
            if (temporarySavedReply) {
                $ctrl.replyText = temporarySavedReply;
            } else if ($ctrl.createOptions.user_signature) {
                $ctrl.replyText = '<br>' + $ctrl.createOptions.user_signature;
            } else {
                $ctrl.replyText = '';
            }
            $ctrl.hover = {};
            $ctrl.tinymceOptions = CONFIG.tiny_mce_options;
            $ctrl.tinymceOptions['height'] = 300;
            $ctrl.uploadWasSubmitted = false;
            $ctrl.maxFileSizeReadable = 'Max. ' + readableBytes(
                $ctrl.createOptions['MAX_TICKET_ATTACHMENT_SIZE']
            ) + ' / file';
            $ctrl.currentUser = FlAuthService.userInfo.user;
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

        $ctrl.reply = function reply(attachmentInputID) {
            var files_to_upload = document.getElementById(attachmentInputID).files;
            if (files_to_upload.length) {
                $ctrl.submitPending = true;
                $ctrl.uploadInProgress = true;
                // if we have files to upload, upload them then create reply and make the
                // association in the backend
                for (var i = 0; i < files_to_upload.length; i++) {
                    // check each file size
                    if (files_to_upload[i].size > $ctrl.createOptions['MAX_TICKET_ATTACHMENT_SIZE']) {
                        $ctrl.submitPending = false;
                        $ctrl.uploadInProgress = false;
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
                        if ($ctrl.createOptions.user_signature) {
                            $ctrl.replyText = '<br>' + $ctrl.createOptions.user_signature;
                        } else {
                            $ctrl.replyText = '';
                        }
                        $ctrl.uploadInProgress = false;
                        $ctrl.uploadWasSubmitted = true;
                        $ctrl.submitPending = false;
                    }).catch(function(error) {
                        $ctrl.uploadInProgress = false;
                        $ctrl.uploadWasSubmitted = true;
                        $ctrl.submitPending = false;
                        FlResolveErrorHandler.handleError(error);
                    });
                }).catch(function(error) {
                    $ctrl.uploadInProgress = false;
                    $ctrl.uploadWasSubmitted = true;
                    $ctrl.submitPending = false;
                    FlResolveErrorHandler.handleError(error);
                });

            } else {
                PluginsTicketsTicketsApi.post({
                    'id': $ctrl.ticket.id,
                    'action': 'add_reply',
                    'reply_text': $ctrl.replyText,
                }).$promise.then(function (data) {
                    FlNotificationService.add(gettextCatalog.getString('Reply added'));
                    FlLocalStorage.removeItem(getTicketLocalStorageReplyKey(), true);
                    $ctrl.refreshTicket();
                    if ($ctrl.createOptions.user_signature) {
                        $ctrl.replyText = '<br>' + $ctrl.createOptions.user_signature;
                    } else {
                        $ctrl.replyText = '';
                    }
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

        $ctrl.addNote = function addNote(attachmentInputID){
            var files_to_upload = document.getElementById(attachmentInputID).files;
            if (files_to_upload.length) {
                $ctrl.submitPending = true;
                $ctrl.uploadInProgress = true;
                // if we have files to upload, upload them then create reply and make the
                // association in the backend
                for (var i = 0; i < files_to_upload.length; i++) {
                    // check each file size
                    if (files_to_upload[i].size > $ctrl.createOptions['MAX_TICKET_ATTACHMENT_SIZE']) {
                        $ctrl.submitPending = false;
                        $ctrl.uploadInProgress = false;
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
                        'action': 'add_note',
                        'note_text': $ctrl.replyText,
                        'associated_attachments': attachmentIds,
                    }).$promise.then(function (data) {
                        FlNotificationService.add(gettextCatalog.getString('Note added'));
                        FlLocalStorage.removeItem(getTicketLocalStorageReplyKey(), true);
                        $ctrl.refreshTicket();
                        if ($ctrl.createOptions.user_signature) {
                            $ctrl.replyText = '<br>' + $ctrl.createOptions.user_signature;
                        } else {
                            $ctrl.replyText = '';
                        }
                        $ctrl.uploadInProgress = false;
                        $ctrl.uploadWasSubmitted = true;
                        $ctrl.submitPending = false;
                    }).catch(function(error) {
                        $ctrl.uploadInProgress = false;
                        $ctrl.uploadWasSubmitted = true;
                        $ctrl.submitPending = false;
                        FlResolveErrorHandler.handleError(error);
                    });
                }).catch(function(error) {
                    $ctrl.uploadInProgress = false;
                    $ctrl.uploadWasSubmitted = true;
                    $ctrl.submitPending = false;
                    FlResolveErrorHandler.handleError(error);
                });

            } else {
                PluginsTicketsTicketsApi.post({
                    'id': $ctrl.ticket.id,
                    'action': 'add_note',
                    'note_text': $ctrl.replyText
                }).$promise.then(function (data) {
                    $ctrl.submitPending = false;
                    FlNotificationService.add(gettextCatalog.getString('Note added'));
                    FlLocalStorage.removeItem(getTicketLocalStorageReplyKey(), true);
                    $ctrl.replyText = '';
                    $ctrl.refreshTicket();
                }).catch(function(error){
                    $ctrl.submitPending = false;
                    FlResolveErrorHandler.handleError(error);
                });
            }
        };

        $ctrl.changeInternalStatus = function changeInternalStatus(new_status) {
            $ctrl.ticket.internal_status = new_status;
            return PluginsTicketsTicketsApi.update($ctrl.ticket)
                .$promise.then(function (data) {
                    $ctrl.refreshTicket();
                    FlNotificationService.add(gettextCatalog.getString('Internal status successfully updated.'));
                    return data;
                }).catch(function (error) {
                    $ctrl.submitPending = false;
                    $ctrl.backendErrors = error.data;
                });
        };

        $ctrl.deleteMessage = function deleteMessage(message) {
            return FlUiUtilsService.yesNoDlg(
                gettextCatalog.getString('The message will permanently be deleted'),
                gettextCatalog.getString('Delete message?'),
                gettextCatalog.getString('Delete')).then(function () {
                    if (message['message_type'] === 'ticketupdate') {
                        PluginsTicketsTicketUpdatesApi.delete({
                            'id': message.id
                        }).$promise.then(function () {
                            FlNotificationService.add(gettextCatalog.getString('Reply deleted'));
                            $ctrl.refreshTicket();
                        })
                    } else {
                        PluginsTicketsTicketNotesApi.delete({
                            'id': message.id
                        }).$promise.then(function () {
                            FlNotificationService.add(gettextCatalog.getString('Note deleted'));
                            $ctrl.refreshTicket();
                        })
                    }
            }).catch(function(){});
        };

        $ctrl.updateNote = function updateNote(note){
            PluginsTicketsTicketNotesApi.update({
                'id': note.id,
                'note_text': note.note_text
            }).$promise.then(function () {
                FlNotificationService.add(gettextCatalog.getString('Note updated'));
                $ctrl.refreshTicket();
            });
        };

        $ctrl.editReply = function editReply(message) {
            return $mdDialog.show({
                templateUrl: 'staff/plugins/tickets/tickets_details/dialogs/tickets_updates_edit/ticketsupdatesedit.html',
                controller: 'PluginsTicketsTicketUpdatesEditController',
                controllerAs: '$ctrl',
                parent: angular.element(document.body),
                clickOutsideToClose: false,
                locals: {
                    message: message,
                },
            }).then(function () {
                FlNotificationService.add(gettextCatalog.getString('Message updated'));
                $ctrl.refreshTicket();
            }).catch(function(){});
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

        $ctrl.deleteAttachment = function deleteAttachment(attachmentID) {
            return FlUiUtilsService.yesNoDlg(gettextCatalog.getString('Are you sure you want to delete the attachment?'),
                gettextCatalog.getString('Delete attachment'),
                gettextCatalog.getString('Delete attachment')).then(function () {
                PluginsTicketsTicketAttachmentsApi.delete({
                    'id': attachmentID
                }).$promise.then(function () {
                    $ctrl.refreshTicket();
                    FlNotificationService.add(gettextCatalog.getString('Attachment deleted'));
                });
            }).catch(function(){});

        };

        $ctrl.downloadAttachment = function downloadAttachment(attachmentId) {
            var url = CONFIG.api_url + '/plugins/tickets/ticket_attachments/' + attachmentId + '/download_file';
            window.open(url);
        };

        $ctrl.openAttachment = function openAttachment(attachmentId) {
            var url = CONFIG.api_url + '/plugins/tickets/ticket_attachments/' + attachmentId + '/load_file';
            window.open(url);
        };

        $ctrl.removeLinking = function removeLinking(linked) {
            return $mdDialog.show({
                templateUrl: 'staff/plugins/tickets/tickets_details/dialogs/remove_linking/removelinking.html',
                controller: 'PluginsTicketsRemoveLinkingController',
                controllerAs: '$ctrl',
                parent: angular.element(document.body),
                clickOutsideToClose: false,
                locals: {
                    ticket: $ctrl.ticket.id,
                    linkedTicket: linked
                },
            }).then(function () {
                FlNotificationService.add(gettextCatalog.getString('Linking removed'));
                $ctrl.refreshTicket();
            }).catch(function(err){
                $ctrl.refreshTicket();
            });
        };

        $ctrl.getUrlForUser = function getUrlForUser(user, email){
            if (user) {
                return $state.href('user', {'id': user.id});
            } else if (email) {
                return ('mailto:' + email);
            }
        };

        $ctrl.onReplyInputChange = function () {
            FlLocalStorage.set(getTicketLocalStorageReplyKey(), $ctrl.replyText, true);
        };

    }
})();
