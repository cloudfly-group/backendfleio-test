from rest_framework import serializers

from plugins.tickets.models.attachment import Attachment


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = '__all__'


class AttachmentSerializerDetail(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = ('id', 'file_name', 'disk_file', 'content_type', 'ticket_note', 'ticket_update',
                  'email_message',)


class AttachmentBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'file_name',)
        read_only_fields = ('id', 'file_name',)
