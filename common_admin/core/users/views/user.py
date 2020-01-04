from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from fleio.core.drf import SuperUserOnly
from fleio.core.exceptions import APIConflict
from fleio.reseller.utils import user_reseller_resources
from fleiostaff.core.signals import user_impersonated


class AdminUserViewSet(ModelViewSet):
    permission_classes = (SuperUserOnly,)
    serializer_map = {}

    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    @action(detail=True, methods=['POST'])
    def impersonate(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk, is_active=True, is_staff=False)
        request.session['impersonate'] = user.pk
        user_impersonated.send(sender=__name__, user=request.user, username=request.user.username,
                               user_id=request.user.pk, impersonated_user_name=user.username,
                               impersonated_user_id=user.pk, request=request)
        reseller_resources = user_reseller_resources(request.user)
        enduser_panel_url = reseller_resources.enduser_panel_url if reseller_resources else None

        return Response(
            {
                'detail': _('User {} impersonated').format(user.username),
                'enduser_panel_url': enduser_panel_url
            }
        )

    @action(methods=['post'], detail=False)
    def stop_impersonation(self, request):
        try:
            request.session.pop('impersonate')
            return Response({'detail': _('User is no longer impersonated')})
        except Exception as e:
            del e  # unused
            raise APIConflict(detail=_('No user is impersonated'))
