from django.utils.translation import ugettext_lazy as _

from plugins.tickets.models.signature import StaffSignature
from plugins.tickets.staff.tickets.signatures_serializer import StaffSignatureSerializer

from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.filters import CustomFilter


class StaffSignaturesViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSignatureSerializer
    permission_classes = (StaffOnly,)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, CustomFilter, filters.SearchFilter)
    search_fields = (
        'content',
    )
    ordering_fields = ('department', 'user',)
    filter_fields = ('department', 'user',)
    ordering = ['user']
    queryset = StaffSignature.objects.all()

    def create(self, request, *args, **kwargs):
        if not request.data.get('user', None):
            request.data['user'] = request.user.id
        return super().create(request=request, *args, **kwargs)

    def perform_destroy(self, instance):
        if not instance.department:
            # don't allow deletion of the default signature if there are custom signatures for departments left
            count = StaffSignature.objects.filter(user=instance.user).exclude(department=None).count()
            if count > 0:
                raise APIBadRequest(
                    _('Cannot delete the default signature. Remove all signatures first.')
                )
        instance.delete()

    @action(detail=False, methods=['GET'])
    def get_signatures_for_current_user(self, request):
        qs = StaffSignature.objects.filter(user=request.user)
        return Response(data={
            'objects': StaffSignatureSerializer(instance=qs, many=True).data
        })

    @action(detail=False, methods=['POST'])
    def save_signatures(self, request):
        signatures = request.data.get('objects', None)
        if not signatures:
            raise APIBadRequest(_('No signatures to update were given'))
        for signature in signatures:
            try:
                update_signature = StaffSignature.objects.get(
                    id=signature['id'],
                    user=request.user,
                )  # type: StaffSignature
                update_signature.content = signature['content']
                update_signature.save()
            except StaffSignature.DoesNotExist:
                raise APIBadRequest(
                    _('Cannot update signature with id {} because you do not own it.').format(signature['id'])
                )
        return Response({'detail': _('Signatures updated')})

    @action(detail=False, methods=['GET', 'POST'])
    def add_global_signature(self, request):
        has_global_signature = StaffSignature.objects.filter(
            user=request.user,
            department=None
        ).count() > 0  # type: bool
        if has_global_signature:
            raise APIBadRequest(_('You already have a global signature'))
        StaffSignature.objects.create(
            user=request.user,
            department=None,
            content='',
        )
        return Response({'detail': 'Successfully created'})
