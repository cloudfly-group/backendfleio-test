from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


RECORD_TYPES = (
    ('A', _('Address Mapping')),
    ('AAAA', _('IP Version 6')),
    ('MX', _('Mail Exchange')),
    ('NS', _('Name Server')),
    ('SOA', _('Start of Authority')),
    ('CNAME', _('Canonical Name')),
    ('PTR', _('Reverse-lookup Pointer')),
    ('TXT', _('Text')),
    ('SRV', _('Service locator')),
    ('SSHFP', _('SSH Public Key Fingerprint')),
)

ZONE_TYPES = (
    ('PRIMARY', _('Primary')),
    ('SECONDARY', _('Secondary'))
)


class RecordSetCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type_ = serializers.ChoiceField(choices=RECORD_TYPES)
    records = serializers.ListField(min_length=1)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=255, required=False)
    region_name = serializers.CharField(required=False)


class RecordSetListSerializer(serializers.Serializer):
    STATUS = (
        ('PENDING', _('Pending')),
        ('ACTIVE', _('Active')),
        ('ERROR', _('Error'))
    )

    name = serializers.CharField(max_length=255, required=False)
    type = serializers.ChoiceField(choices=RECORD_TYPES, required=False)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=255, required=False)
    status = serializers.ChoiceField(choices=STATUS, required=False)
    region_name = serializers.CharField(required=False)


class RecordSetAlterSerializer(serializers.Serializer):
    region_name = serializers.CharField(required=False)
    records = serializers.ListField(required=False)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=255, required=False)


class DnsUpdateSerializer(serializers.Serializer):
    """Base DNS serializer"""
    email = serializers.EmailField(required=False)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)
    region_name = serializers.CharField(required=False)


class DnsCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=True)
    ttl = serializers.IntegerField(required=False, min_value=0, default=3600)
    description = serializers.CharField(required=False)
    region_name = serializers.CharField(required=False)

    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        if not values['name'].endswith('.'):
            values['name'] += '.'
        return values


class DnsFilterSerializer(serializers.Serializer):
    STATUSES = (
        ('PENDING', _('Pending')),
        ('ACTIVE', _('Active')),
        ('ERROR', _('Error'))
    )

    email = serializers.EmailField(required=False)
    ttl = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)
    region_name = serializers.CharField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    zone_type = serializers.ChoiceField(choices=ZONE_TYPES, required=False)
    status = serializers.ChoiceField(choices=STATUSES, required=False)

    def validate(self, attrs):
        zone_type = attrs.pop('zone_type', None)

        if zone_type:
            attrs['type'] = zone_type

        return attrs


class GetPtrFromIpSerializer(serializers.Serializer):
    ip = serializers.IPAddressField(required=True, protocol='both')
    region_name = serializers.CharField(required=True)


class CreateOrUpdatePtrSerializer(serializers.Serializer):
    ip = serializers.IPAddressField(required=True)
    zone_id = serializers.CharField(required=False)
    record = serializers.CharField(required=True)
    region_name = serializers.CharField(required=True)


class ListRecordsSerializer(serializers.Serializer):
    def to_representation(self, recordsets):
        modifiable_recordsets = []
        read_only_recordsets = []
        for recordset in recordsets:
            recordset.pop('created_at', None)
            recordset.pop('updated_at', None)
            recordset.pop('links', None)
            recordset.pop('version', None)
            recordset.pop('description', None)
            recordset['deleted'] = False
            if recordset['type'] == 'SOA' or \
                    (recordset['type'] == 'NS' and recordset['zone_name'] == recordset['name']):
                read_only_recordsets.append(recordset)
            else:
                modifiable_recordsets.append(recordset)
        return {'recordsets': modifiable_recordsets, 'read_only_recordsets': read_only_recordsets}


class SyncRecordSetsSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36, required=False, default=-1)
    records = serializers.ListField(min_length=1)
    zone_id = serializers.CharField(max_length=36)
    name = serializers.CharField(max_length=255)
    type = serializers.ChoiceField(choices=RECORD_TYPES)
    ttl = serializers.IntegerField(allow_null=True)
    deleted = serializers.BooleanField(default=False, required=False)
    created = serializers.BooleanField(default=False, required=False)


class DnsSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=36)
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=True)
    ttl = serializers.IntegerField(required=False, min_value=0, default=3600)
    description = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=RECORD_TYPES)
    project_id = serializers.CharField(max_length=36)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def to_representation(self, instance):
        current_rep = super().to_representation(instance=instance)
        if current_rep['name'].endswith('.'):
            current_rep['name'] = current_rep['name'][:-1]
        return current_rep
