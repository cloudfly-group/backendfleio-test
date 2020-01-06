import re

from itertools import chain
from operator import attrgetter

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from plugins.tickets.models import Ticket
from plugins.tickets.models.ticket_update import TicketUpdate
from plugins.tickets.models import TicketNote
from plugins.tickets.models.ticket import TicketPriority
from plugins.tickets.models.ticket import TicketStatus
from plugins.tickets.models.ticket import TicketLink
from plugins.tickets.models.department import Department
from plugins.tickets.models.attachment import Attachment

from fleio.core.models import AppUser
from fleio.core.serializers import UserMinSerializer
from plugins.tickets.staff.tickets.attachments_serializers import AttachmentBriefSerializer, AttachmentSerializerDetail


class TicketLinkSerializer(serializers.ModelSerializer):
    symmetrical = serializers.BooleanField(write_only=True)

    class Meta:
        model = TicketLink
        fields = '__all__'


class TicketNoteSerializer(serializers.ModelSerializer):
    created_by = UserMinSerializer(read_only=True, default=serializers.CurrentUserDefault())
    created_at = serializers.ReadOnlyField()
    last_edited_by = UserMinSerializer(read_only=True)
    attachments = AttachmentSerializerDetail(many=True, required=False, read_only=True)

    class Meta:
        model = TicketNote
        fields = '__all__'


class TicketUpdateUpdateSerializer(serializers.ModelSerializer):
    created_by = UserMinSerializer(read_only=True, default=serializers.CurrentUserDefault())
    created_at = serializers.ReadOnlyField()
    last_edited_by = UserMinSerializer(read_only=True)
    attachments = AttachmentSerializerDetail(many=True, required=False, read_only=True)

    class Meta:
        model = TicketUpdate
        fields = '__all__'


class RepliesAndNotesSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.IntegerField(read_only=True)
    message_type = serializers.SerializerMethodField(read_only=True)
    created_by = UserMinSerializer(read_only=True, default=serializers.CurrentUserDefault())
    created_by_display = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.ReadOnlyField()
    last_edited_by = UserMinSerializer(read_only=True)
    attachments = AttachmentSerializerDetail(many=True, required=False, read_only=True)
    message = serializers.SerializerMethodField(read_only=True)
    message_owner_email = serializers.SerializerMethodField(read_only=True)
    ticket_activity = serializers.SerializerMethodField(read_only=True)
    email_generated = serializers.SerializerMethodField(read_only=True)
    new_status = serializers.SerializerMethodField(read_only=True)
    new_assignee = serializers.SerializerMethodField(read_only=True)
    new_department = serializers.SerializerMethodField(read_only=True)
    new_priority = serializers.SerializerMethodField(read_only=True)
    new_internal_status = serializers.SerializerMethodField(read_only=True)
    new_client = serializers.SerializerMethodField(read_only=True)
    new_cc = serializers.SerializerMethodField(read_only=True)
    title_changed = serializers.SerializerMethodField(read_only=True)
    description_changed = serializers.SerializerMethodField(read_only=True)
    is_staff_generated = serializers.SerializerMethodField(read_only=True)
    last_edited = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_is_staff_generated(model):
        if model.created_by:
            return model.created_by.is_staff
        if type(model).__name__.lower() == 'ticketupdate':
            if model.email_message:
                user = AppUser.objects.filter(email=model.email_message.sender_address).first()
                if user:
                    return user.is_staff
                return False
        return False

    @staticmethod
    def get_message_owner_email(model):
        if model.created_by:
            return model.created_by.email
        if type(model).__name__.lower() == 'ticketupdate':
            if model.email_message:
                return model.email_message.sender_address
        return None

    @staticmethod
    def get_last_edited(model):
        return model.last_edited

    @staticmethod
    def get_email_generated(model):
        if type(model).__name__.lower() == 'ticketnote':
            return False
        return True if model.email_message is not None else False

    @staticmethod
    def get_ticket_activity(model):
        if type(model).__name__.lower() == 'ticketnote':
            return False
        if model.reply_text and (not model.new_status or not model.new_internal_status):
            return False
        return True

    @staticmethod
    def get_title_changed(model):
        if type(model).__name__.lower() == 'ticketnote':
            return False
        if model.title_changed:
            return model.title_changed
        return None

    @staticmethod
    def get_description_changed(model):
        if type(model).__name__.lower() == 'ticketnote':
            return False
        if model.description_changed:
            return model.description_changed
        return None

    @staticmethod
    def get_new_cc(model):
        if type(model).__name__.lower() == 'ticketnote':
            return False
        if model.new_cc:
            return str(model.new_cc)
        return None

    @staticmethod
    def get_new_client(model):
        if type(model).__name__.lower() == 'ticketnote':
            return False
        if model.new_client:
            return str(model.new_client)
        return None

    @staticmethod
    def get_new_internal_status(model):
        if type(model).__name__.lower() == 'ticketnote':
            return False
        if model.new_internal_status:
            return TicketStatus.internal_status_map.get(model.new_internal_status, _('N/A'))
        return None

    @staticmethod
    def get_new_priority(model):
        if type(model).__name__.lower() == 'ticketnote' or model.reply_text:
            return None
        if model.new_priority:
            return TicketPriority.priority_map.get(model.new_priority, _('N/A'))
        return None

    @staticmethod
    def get_new_status(model):
        if type(model).__name__.lower() == 'ticketnote' or model.reply_text:
            return None
        if model.new_status:
            return TicketStatus.status_map.get(model.new_status, _('N/A'))
        return None

    @staticmethod
    def get_new_department(model):
        if type(model).__name__.lower() == 'ticketnote' or model.reply_text:
            return None
        if model.new_department:
            return str(model.new_department)
        return None

    @staticmethod
    def get_new_assignee(model):
        if type(model).__name__.lower() == 'ticketnote' or model.reply_text:
            return None
        if model.new_assignee:
            return {
                'id': model.new_assignee.id,
                'display': model.new_assignee.get_full_name()
            }
        return None

    @staticmethod
    def get_message_type(model):
        return type(model).__name__.lower()

    @staticmethod
    def get_message(model):
        if type(model).__name__.lower() == 'ticketnote':
            return model.note_text
        else:
            return model.reply_text

    @staticmethod
    def get_created_by_display(model):
        if model.created_by:
            user = model.created_by
            return user.get_full_name() if user.get_full_name() else user.username
        elif type(model).__name__.lower() == 'ticketupdate':
            if model.email_message:
                return model.email_message.sender_address
        else:
            return _('n/a')


class TicketSerializer(serializers.ModelSerializer):
    department_display = serializers.SerializerMethodField(required=False, read_only=True)
    status_display = serializers.SerializerMethodField(required=False, read_only=True)
    internal_status_display = serializers.SerializerMethodField(required=False, read_only=True)
    assigned_to_display = serializers.SerializerMethodField(required=False, read_only=True)
    client_display = serializers.SerializerMethodField(required=False, read_only=True)
    description = serializers.CharField(max_length=10240, allow_null=True, allow_blank=True, required=False)
    created_at = serializers.ReadOnlyField()
    last_reply_at = serializers.ReadOnlyField()
    created_by = UserMinSerializer(read_only=True, default=serializers.CurrentUserDefault())
    priority_display = serializers.SerializerMethodField(required=False, read_only=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), required=True, allow_null=False)
    created_by_email = serializers.SerializerMethodField(required=False, read_only=True)
    ticket_owner_email = serializers.SerializerMethodField(required=False, read_only=True)
    associated_attachment_ids = serializers.CharField(write_only=True, required=False, allow_null=True)
    service = serializers.PrimaryKeyRelatedField(read_only=True)
    main_attachments = serializers.SerializerMethodField(read_only=True, required=False)
    replies_and_notes = serializers.SerializerMethodField(required=False, read_only=True)
    is_staff_generated = serializers.SerializerMethodField(required=False, read_only=True)
    created_by_display = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'created_at',
            'last_reply_at',
            'created_by',
            'created_by_display',
            'is_staff_generated',
            'ticket_owner_email',
            'assigned_to',
            'assigned_to_display',
            'client',
            'client_display',
            'title',
            'description',
            'department',
            'department_display',
            'status',
            'status_display',
            'internal_status',
            'internal_status_display',
            'priority',
            'priority_display',
            'cc_recipients',
            'linked_tickets',
            'created_by_email',
            'associated_attachment_ids',
            'service',
            'main_attachments',
            'replies_and_notes',
        )

    @staticmethod
    def validate_priority(priority):
        if not priority:
            return priority
        if not TicketPriority.priority_map.get(priority, None):
            raise ValidationError(_('Invalid priority.'))
        return priority

    @staticmethod
    def validate_status(status):
        if not status:
            return status
        if not TicketStatus.status_map.get(status, None):
            raise ValidationError(_('Invalid status.'))
        return status

    @staticmethod
    def validate_internal_status(internal_status):
        if not internal_status:
            return internal_status
        if not TicketStatus.internal_status_map.get(internal_status, None):
            raise ValidationError(_('Invalid status.'))
        return internal_status

    @staticmethod
    def validate_cc_recipients(recipients):
        if not recipients:
            return recipients
        if recipients[-1] == ',':
            raise ValidationError(detail=_('No email after the last comma'))
        email_regex = re.compile(r".+\@.+\..+")
        emails_list = recipients.split(',')
        for email in emails_list:
            if not email_regex.match(email):
                raise ValidationError(detail=_('Invalid list of emails'))
        return recipients

    @staticmethod
    def get_created_by_display(model: Ticket):
        if model.created_by:
            user = model.created_by  # type: AppUser
            return user.get_full_name() if user.get_full_name() else user.username
        elif model.email_message:
            return model.email_message.sender_address
        else:
            return _('N/A')

    @staticmethod
    def get_is_staff_generated(model: Ticket):
        if model.created_by:
            return model.created_by.is_staff
        if model.email_message:
            user = AppUser.objects.filter(email=model.email_message.sender_address).first()
            if user:
                return user.is_staff
            return False
        return False

    @staticmethod
    def get_ticket_owner_email(model: Ticket):
        if model.created_by:
            return model.created_by.email
        if model.email_message and not model.created_by:
            return model.email_message.sender_address
        return None

    @staticmethod
    def get_replies_and_notes(model: Ticket):
        notes = TicketNote.objects.filter(ticket=model)
        updates = TicketUpdate.objects.filter(ticket=model)
        return RepliesAndNotesSerializer(
            instance=sorted(chain(notes, updates), key=attrgetter('created_at')),
            many=True
        ).data

    @staticmethod
    def get_main_attachments(model: Ticket):
        att = Attachment.objects.filter(ticket=model, ticket_update=None, ticket_note=None)
        if not att:
            return None
        return AttachmentBriefSerializer(instance=att, many=True, read_only=True).data

    @staticmethod
    def get_created_by_email(model: Ticket):
        # returns None if the ticket was not generated from a received email
        return model.email_message.sender_address if model.email_message is not None else None

    @staticmethod
    def get_client_display(model: Ticket):
        return str(model.client) if model.client else _('n/a')

    @staticmethod
    def get_department_display(model: Ticket):
        return str(model.department) if model.department else _('n/a')

    @staticmethod
    def get_priority_display(model: Ticket):
        return TicketPriority.priority_map.get(model.priority, _('n/a'))

    @staticmethod
    def get_status_display(model: Ticket):
        return TicketStatus.status_map.get(model.status, _('n/a'))

    @staticmethod
    def get_internal_status_display(model: Ticket):
        return TicketStatus.internal_status_map.get(model.internal_status, _('n/a'))

    @staticmethod
    def get_assigned_to_display(model: Ticket):
        if model.assigned_to:
            user = model.assigned_to
            return user.get_full_name() if user.get_full_name() else user.username
        else:
            return _('n/a')


class TicketListSerializer(serializers.ModelSerializer):
    assigned_to_display = serializers.SerializerMethodField()
    client_display = serializers.SerializerMethodField()
    department_display = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    internal_status_display = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        exclude = ('description',)

    @staticmethod
    def get_assigned_to_display(model: Ticket):
        if model.assigned_to:
            user = model.assigned_to
            return user.get_full_name() if user.get_full_name() else user.username
        else:
            return _('n/a')

    @staticmethod
    def get_client_display(model: Ticket):
        return str(model.client) if model.client else _('n/a')

    @staticmethod
    def get_department_display(model: Ticket):
        return str(model.department) if model.department else _('n/a')

    @staticmethod
    def get_priority_display(model: Ticket):
        return TicketPriority.priority_map.get(model.priority, _('n/a'))

    @staticmethod
    def get_status_display(model: Ticket):
        return TicketStatus.status_map.get(model.status, _('n/a'))

    @staticmethod
    def get_internal_status_display(model: Ticket):
        return TicketStatus.internal_status_map.get(model.internal_status, _('n/a'))


class TicketBriefSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    id = serializers.ReadOnlyField()
    title = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
