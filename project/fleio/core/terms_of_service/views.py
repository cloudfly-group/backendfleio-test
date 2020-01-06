import datetime
import logging

import pytz
from ipware.ip import get_ip

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as utcnow
from rest_framework import filters, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from fleio.core.drf import EndUserOnly
from fleio.core.exceptions import APIBadRequest

from fleio.core.models import TermsOfService, TermsOfServiceAgreement
from fleio.core.terms_of_service.serializers import TermsOfServiceAgreementSerializer
from fleio.core.terms_of_service.tos_settings import tos_settings

LOG = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def tos_preview(request):
    requested_id = request.query_params.get('id', None)
    filter_params = {'draft': False}
    if requested_id:
        filter_params['id'] = requested_id
    latest_version_tos = TermsOfService.objects.filter(**filter_params).order_by('-version').first()
    if not latest_version_tos:
        return Response({'tos_data': None})
    return Response({
        'tos_data': {
            'title': latest_version_tos.title,
            'version': latest_version_tos.version,
            'content': latest_version_tos.content,
        }
    })


class TermsOfServiceAgreementsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TermsOfServiceAgreementSerializer
    permission_classes = (EndUserOnly,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id',)

    def get_queryset(self):
        return TermsOfServiceAgreement.objects.filter(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def get_active_tos(self, request, *args, **kwargs):
        del request, args, kwargs  # unused
        latest_version_tos = TermsOfService.objects.filter(draft=False).order_by('-version').first()
        if not latest_version_tos:
            return Response({'tos_data': None})
        try:
            tos_agreement = TermsOfServiceAgreement.objects.get_or_create(
                terms_of_service=latest_version_tos, user=self.request.user,
            )[0]  # type: TermsOfServiceAgreement
        except Exception as e:
            raise APIBadRequest(str(e))

        remind_later_button_available = True
        if tos_settings.forbid_access_after:
            forbid_after_datetime = datetime.datetime.strptime(
                tos_settings.forbid_access_after,
                '%Y-%m-%d %H:%M:%S'
            )
            forbid_after_datetime = forbid_after_datetime.replace(tzinfo=pytz.utc)
            if utcnow() > forbid_after_datetime:
                remind_later_button_available = False
        return Response({
            'tos_data': {
                'agreement_id': tos_agreement.id,
                'title': tos_agreement.terms_of_service.title,
                'version': tos_agreement.terms_of_service.version,
                'content': tos_agreement.terms_of_service.content,
                'agreed': tos_agreement.agreed,
                'remind_later_button_available': remind_later_button_available,
            }
        })

    @action(detail=True, methods=['POST'])
    def agree(self, request, pk, *args, **kwargs):
        del pk, args, kwargs  # unused
        tos_agreement = self.get_object()  # type: TermsOfServiceAgreement
        if tos_agreement.agreed is True:
            raise APIBadRequest(_('You already agreed with this.'))
        tos_agreement.agreed = True
        tos_agreement.agreed_at = utcnow()
        tos_agreement.ip = get_ip(request)
        tos_agreement.save()
        return Response({'detail': _('You agreed with terms of service.')})
