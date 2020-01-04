import logging

from django.utils.translation import ugettext_lazy as _
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from fleio.core.terms_of_service.exceptions import AgreedTOSDestroyException
from fleio.core.terms_of_service.tos_settings import TermsOfServiceSettingsConfig
from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.features import staff_active_features
from fleio.core.models import TermsOfService, TermsOfServiceAgreement
from fleiostaff.core.terms_of_service.serializers import StaffTOSSerializer, TermsOfServiceSettingsSerializer

LOG = logging.getLogger(__name__)


class TermsOfServiceViewSet(viewsets.ModelViewSet):
    serializer_class = StaffTOSSerializer
    permission_classes = (StaffOnly,)
    queryset = TermsOfService.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'title', 'version')
    ordering = ['-version']

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        conf = TermsOfServiceSettingsConfig(raise_if_required_not_set=False)
        response.data['settings'] = _get_tos_settings(configuration=conf)
        return response

    def perform_update(self, serializer):
        tos = self.get_object()
        if TermsOfServiceAgreement.objects.filter(terms_of_service=tos, agreed=True).count():
            raise APIBadRequest(_('You cannot change a terms of service that a user agreed with.'))
        return super().perform_update(serializer=serializer)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request=request, *args, **kwargs)
        except AgreedTOSDestroyException as e:
            raise APIBadRequest(str(e))


def _get_tos_settings(configuration: TermsOfServiceSettingsConfig):
    settings_serializer = TermsOfServiceSettingsSerializer(instance=configuration)
    return settings_serializer.data


@api_view(['GET', 'POST'])
@permission_classes((StaffOnly,))
def tos_settings_view(request):
    conf = TermsOfServiceSettingsConfig(raise_if_required_not_set=False)
    if request.method == 'GET':
        return Response(dict(tos_settings=_get_tos_settings(configuration=conf)))
    elif request.method == 'POST':
        if staff_active_features.is_enabled('demo'):
            raise APIBadRequest(_('Cannot change terms of service settings in demo mode'))
        require_end_users_to_agree_with_latest_tos = request.data.get(
            'require_end_users_to_agree_with_latest_tos', False
        )
        if TermsOfService.objects.filter(draft=False).count() == 0:
            if require_end_users_to_agree_with_latest_tos is True:
                raise APIBadRequest(
                    _('Cannot impose terms of service agreements as you have no active terms of service.')
                )
        serializer = TermsOfServiceSettingsSerializer(instance=conf, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(dict(tos_settings=_get_tos_settings(configuration=conf)))
    else:
        return Response({})
