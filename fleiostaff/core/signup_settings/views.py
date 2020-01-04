from django.utils.translation import ugettext_lazy as _

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.features import staff_active_features
from fleio.notifications.models import NotificationTemplate
from fleio.notifications.serializers import NotificationTemplateOptionsSerializer

from fleiostaff.core.signup_settings.serializers import SignUpSettingsSerializer
from fleio.core.signup.settings import SignUpSettingsConfig


def get_sign_up_settings(configuration: SignUpSettingsConfig, with_email_templates: bool = False):
    settings_serializer = SignUpSettingsSerializer(instance=configuration)
    response_obj = dict(
        signup_settings=settings_serializer.data
    )
    if with_email_templates:
        templates = NotificationTemplate.objects.all().values('name').distinct()
        nt_serializer = NotificationTemplateOptionsSerializer(instance=templates, many=True)
        response_obj['notification_templates'] = nt_serializer.data
    return Response(response_obj)


@api_view(['GET', 'POST'])
@permission_classes((StaffOnly,))
def sign_up_settings_view(request):
    conf = SignUpSettingsConfig(raise_if_required_not_set=False)
    if request.method == 'GET':
        return get_sign_up_settings(configuration=conf, with_email_templates=True)
    elif request.method == 'POST':
        if staff_active_features.is_enabled('demo'):
            raise APIBadRequest(_('Cannot change sign up settings in demo mode'))
        serializer = SignUpSettingsSerializer(instance=conf, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return get_sign_up_settings(configuration=conf)
    else:
        return Response({})
