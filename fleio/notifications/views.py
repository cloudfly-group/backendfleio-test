from rest_framework import filters, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend

from fleio.core.drf import EndUserOnly
from fleio.notifications.formatting import NOTIFICATION_DISPLAY_NAMES
from fleio.notifications.models import UserNotificationsSettings
from .serializers import DispatcherLogDetailSerializer, DispatcherLogSerializer
from .models import DispatcherLog, NotificationTemplate


class NotificationViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = DispatcherLogSerializer
    permission_classes = (EndUserOnly,)
    serializer_map = {'list': DispatcherLogSerializer,
                      'retrieve': DispatcherLogDetailSerializer}
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ('name', )
    ordering = ('name',)
    ordering_fields = ('generated',)

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        return (DispatcherLog.objects
                .filter(notification__client__in=self.request.user.clients.all()).order_by('generated'))

    @action(detail=True, methods=['POST'])
    def view(self, request, pk):
        obj = self.get_object()
        obj.status = DispatcherLog.SEEN
        obj.save(update_fields=['status'])
        return Response({'detail': 'Seen'})

    @action(detail=True, methods=['POST'])
    def unseen(self, request, pk):
        obj = self.get_object()
        obj.status = DispatcherLog.PENDING
        obj.save(update_fields=['status'])
        return Response({'detail': 'Unseen'})

    def list(self, request, *args, **kwargs):
        response = super().list(request=request, *args, **kwargs)
        response.data['extra'] = {
            'unseen_count': self.get_queryset().exclude(status=DispatcherLog.SEEN).count()
        }
        return response

    @action(detail=False, methods=['POST'])
    def mark_all_as_read(self, request):
        del request  # unused
        DispatcherLog.objects.filter(
            notification__client__in=self.request.user.clients.all()
        ).update(status=DispatcherLog.SEEN)
        return Response({'detail': _('All notifications were marked as read.')})

    @action(detail=False, methods=['GET'])
    def get_user_notifications_settings(self, request):
        notifications_settings = getattr(
            request.user, 'notifications_settings', None
        )  # type: UserNotificationsSettings
        response_data = {}
        templates = NotificationTemplate.objects.exclude(name__contains='staff').order_by('name').all()
        for template in templates:
            response_data[template.name] = {
                'name': template.name,
                'display_name': NOTIFICATION_DISPLAY_NAMES.get(template.name, template.name),
                'enabled': notifications_settings.is_notification_enabled(
                    template.name
                ) if notifications_settings else True,
            }
        return Response({
            'detail': response_data,
        })

    @action(detail=False, methods=['POST'])
    def set_user_notifications_settings(self, request):
        notifications_settings = getattr(
            request.user, 'notifications_settings', None
        )  # type: UserNotificationsSettings
        if not notifications_settings:
            notifications_settings = UserNotificationsSettings.objects.create(user=request.user)

        for template_name, settings in request.data['notifications_settings'].items():
            notifications_settings.set_notification_enabled_flag(template_name, settings['enabled'])
        return Response()
