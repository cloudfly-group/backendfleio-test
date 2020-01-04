import re

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fleio.billing.models.service import Service
from fleio.core.models import AppUser
from plugins.tickets.models import Ticket
from plugins.tickets.models.ticket_update import TicketUpdate
from plugins.tickets.models.ticket import TicketStatus
from plugins.tickets.models.attachment import Attachment
from plugins.tickets.models.department import Department

from fleio.core.serializers import UserMinSerializer
from plugins.tickets.staff.tickets.attachments_serializers import AttachmentBriefSerializer, AttachmentSerializerDetail


class TicketUpdateUpdateSerializer(serializers.ModelSerializer):
    created_by = UserMinSerializer(read_only=True, default=serializers.CurrentUserDefault())
    created_at = serializers.ReadOnlyField()
    last_edited_by = UserMinSerializer(read_only=True)
    attachments = AttachmentSerializerDetail(many=True, required=False, read_only=True)

    class Meta:
        model = TicketUpdate
        fields = '__all__'


class TicketUpdateSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializerDetail(many=True, required=False, read_only=True)
    created_by = UserMinSerializer(read_only=True, default=serializers.CurrentUserDefault())
    created_by_display = serializers.SerializerMethodField(required=False, read_only=True)
    new_status_display = serializers.SerializerMethodField(required=False, read_only=True)
    new_status = serializers.CharField(required=False, read_only=True, allow_null=True, allow_blank=True)
    new_department_display = serializers.SerializerMethodField(required=False, read_only=True)
    new_department = serializers.CharField(required=False, read_only=True, allow_null=True, allow_blank=True)
    created_at = serializers.ReadOnlyField()
    new_client = serializers.CharField(required=False, read_only=True, allow_null=True, allow_blank=True)
    new_client_display = serializers.SerializerMethodField(required=False, read_only=True)
    last_edited_by = UserMinSerializer(read_only=True)
    new_cc = serializers.CharField(required=False, read_only=True, allow_null=True, allow_blank=True)
    email_generated = serializers.SerializerMethodField(required=False, read_only=True)
    ticket_activity = serializers.SerializerMethodField(required=False, read_only=True)
    update_owner_email = serializers.SerializerMethodField(required=False, read_only=True)
    is_staff_generated = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = TicketUpdate
        fields = (
            'id',
            'created_at',
            'created_by',
            'is_staff_generated',
            'created_by_display',
            'reply_text',
            'ticket_activity',
            'new_status',
            'new_status_display',
            'new_internal_status',
            'description_changed',
            'new_department',
            'new_department_display',
            'title_changed',
            'new_client',
            'new_client_display',
            'last_edited',
            'last_edited_by',
            'new_cc',
            'attachments',
            'email_generated',
            'update_owner_email',
        )

    @staticmethod
    def get_is_staff_generated(model: TicketUpdate):
        if model.created_by:
            return model.created_by.is_staff
        if model.email_message:
            user = AppUser.objects.filter(email=model.email_message.sender_address).first()
            if user:
                return user.is_staff
            return False
        return False

    @staticmethod
    def get_update_owner_email(model: TicketUpdate):
        if model.created_by:
            return model.created_by.email
        if model.email_message and not model.created_by:
            return model.email_message.sender_address
        return None

    @staticmethod
    def get_ticket_activity(model: TicketUpdate):
        if model.reply_text and (not model.new_status or not model.new_internal_status):
            return False
        return True

    @staticmethod
    def get_email_generated(model: TicketUpdate):
        return True if model.email_message is not None else False

    @staticmethod
    def get_created_by_display(model: TicketUpdate):
        if model.created_by:
            user = model.created_by
            return user.get_full_name() if user.get_full_name() else user.username
        elif model.email_message:
            return model.email_message.sender_address
        else:
            return _('N/A')

    @staticmethod
    def get_new_status_display(model: TicketUpdate):
        return TicketStatus.status_map.get(model.new_status, _('n/a'))

    @staticmethod
    def get_new_department_display(model: TicketUpdate):
        return str(model.new_department) if model.new_department else _('n/a')

    @staticmethod
    def get_new_client_display(model: TicketUpdate):
        return str(model.new_client) if model.new_client else _('n/a')


class ClientFilteredServicesPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(ClientFilteredServicesPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        clients = request.user.clients.all()
        if not clients:
            return None
        return queryset.filter(client__in=clients)


class TicketSerializer(serializers.ModelSerializer):
    updates = TicketUpdateSerializer(many=True, required=False, read_only=True)
    department_display = serializers.SerializerMethodField(required=False, read_only=True)
    status_display = serializers.SerializerMethodField(required=False, read_only=True)
    client_display = serializers.SerializerMethodField(required=False, read_only=True)
    description = serializers.CharField(max_length=10240, allow_null=True, allow_blank=True, required=False)
    created_at = serializers.ReadOnlyField()
    created_by = UserMinSerializer(read_only=True, default=serializers.CurrentUserDefault())
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), required=True, allow_null=False)
    assigned_to_display = serializers.SerializerMethodField(required=False, read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(read_only=True)
    associated_attachment_ids = serializers.CharField(write_only=True, required=False, allow_null=True)
    service = ClientFilteredServicesPrimaryKeyRelatedField(queryset=Service.objects, allow_null=True, required=False)
    main_attachments = serializers.SerializerMethodField(read_only=True, required=False)
    created_by_email = serializers.SerializerMethodField(required=False, read_only=True)
    ticket_owner_email = serializers.SerializerMethodField(required=False, read_only=True)
    is_staff_generated = serializers.SerializerMethodField(required=False, read_only=True)
    created_by_display = serializers.SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'created_at',
            'is_staff_generated',
            'created_by',
            'created_by_display',
            'client',
            'client_display',
            'title',
            'description',
            'department',
            'department_display',
            'status',
            'status_display',
            'updates',
            'cc_recipients',
            'assigned_to',
            'created_by_email',
            'ticket_owner_email',
            'assigned_to_display',
            'associated_attachment_ids',
            'main_attachments',
            'service',
        )

    @staticmethod
    def get_created_by_display(model: Ticket):
        if model.created_by:
            user = model.created_by  # type: AppUser
            return user.get_full_name() if user.get_full_name() else user.username
        elif model.email_message:
            return model.email_message.sender_address
        else:
            return _('n/a')

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
    def get_main_attachments(model: Ticket):
        att = Attachment.objects.filter(ticket=model, ticket_update=None, ticket_note=None)
        if not att:
            return None
        return AttachmentBriefSerializer(instance=att, many=True, read_only=True).data

    @staticmethod
    def get_ticket_owner_email(model: Ticket):
        if model.created_by:
            return model.created_by.email
        if model.email_message and not model.created_by:
            return model.email_message.sender_address
        return None

    @staticmethod
    def get_created_by_email(model: Ticket):
        # returns None if the ticket was not generated from a received email
        return model.email_message.sender_address if model.email_message is not None else None

    @staticmethod
    def validate_status(status):
        if not status:
            return status
        if not TicketStatus.status_map.get(status, None):
            raise ValidationError(_('Invalid status.'))
        return status

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
    def get_assigned_to_display(model: Ticket):
        if model.assigned_to:
            user = model.assigned_to
            return user.get_full_name() if user.get_full_name() else user.username
        else:
            return _('N/A')

    @staticmethod
    def get_client_display(model: Ticket):
        return str(model.client) if model.client else _('n/a')

    @staticmethod
    def get_department_display(model: Ticket):
        return str(model.department) if model.department else _('n/a')

    @staticmethod
    def get_status_display(model: Ticket):
        return TicketStatus.status_map.get(model.status, _('n/a'))


class TicketListSerializer(serializers.ModelSerializer):
    client_display = serializers.SerializerMethodField()
    department_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    status = serializers.CharField()

    class Meta:
        model = Ticket
        exclude = ('priority', 'internal_status', 'assigned_to', 'linked_tickets', 'description',)

    @staticmethod
    def get_client_display(model: Ticket):
        return str(model.client) if model.client else _('n/a')

    @staticmethod
    def get_department_display(model: Ticket):
        return str(model.department) if model.department else _('n/a')

    @staticmethod
    def get_status_display(model: Ticket):
        return TicketStatus.status_map.get(model.status, _('n/a'))


class TicketCreateSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False)
    description = serializers.CharField(max_length=10240, allow_null=True, allow_blank=True, required=False)
    associated_attachment_ids = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Ticket
        exclude = ('priority', 'internal_status', 'assigned_to', 'linked_tickets',)

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
