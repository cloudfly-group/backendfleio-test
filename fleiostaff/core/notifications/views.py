from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _

from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from fleio.activitylog.utils.decorators import log_staff_activity
from fleio.notifications.formatting import NotificationTemplatesHelpText
from fleiostaff.core.notifications.serializers import (NotificationsCategoriesSerializer,
                                                       NotificationTemplateSerializer,
                                                       NotificationTemplateSerializerCreate)

from fleio.notifications.models import Category, NotificationTemplate
from fleio.core.features import staff_active_features
from fleio.core.drf import StaffOnly
from fleio.core.exceptions import APIBadRequest
from fleio.core.filters import CustomFilter


@log_staff_activity(category_name='core', object_name='notification template')
class NotificationTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationTemplateSerializer
    serializer_map = {
        'create': NotificationTemplateSerializerCreate
    }
    permission_classes = (StaffOnly,)
    queryset = NotificationTemplate.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter, CustomFilter)
    ordering_fields = ('name', 'id', 'category',)
    ordering = ('name',)
    filter_fields = ('name', 'category',)
    search_fields = ('name',)

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        if self.action == 'list':
            qs = NotificationTemplate.objects.filter(
                language=getattr(settings, 'DEFAULT_NOTIFICATION_TEMPLATE_LANGUAGE_CODE'))
        else:
            qs = NotificationTemplate.objects.all()
        if not staff_active_features.is_enabled('openstack'):
            qs = qs.exclude(category__name='openstack')
        return qs

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        template_name = serializer.validated_data.get('name', None)
        language = serializer.validated_data.get('language', None)
        related_template = NotificationTemplate.objects.filter(name=template_name).first()
        template_category = related_template.category
        try:
            serializer.save(category=template_category, language=language)
        except IntegrityError as e:
            raise APIBadRequest(_('Duplicate entry. A template in this language already exists.'))

    @action(detail=False, methods=['post'])
    def update_templates_set(self, request):
        updated_templates = request.data
        for template in updated_templates:
            serializer = NotificationTemplateSerializer(data=template)
            serializer.is_valid(raise_exception=True)
            template = NotificationTemplate.objects.get(
                name=serializer.validated_data.get('name'),
                language=serializer.validated_data.get('language')
            )
            serializer.update(instance=template, validated_data=serializer.validated_data)
        return Response({'detail': 'Successfully updated.'})

    @action(detail=False, methods=['get'])
    def get_available_languages_for_template(self, request):
        """
        Gets all templates related to the default one
        """
        template_name = request.query_params.get('template_name', None)
        used_languages = NotificationTemplate.objects.filter(name=template_name).values_list('language', flat=True)
        used_languages_map = dict()
        for language in used_languages:
            used_languages_map[language] = True
        all_languages = getattr(settings, 'LANGUAGES')
        available_languages = list()
        for language in all_languages:
            if language[0] in used_languages_map:
                pass
            else:
                available_languages.append(dict(language_code=language[0], language_display=language[1]))
        return Response({
            'objects': available_languages
        })

    def perform_destroy(self, template):
        # don't allow deletion of the template using the default language
        if template.language == getattr(settings, 'DEFAULT_NOTIFICATION_TEMPLATE_LANGUAGE_CODE', 'en'):
            raise PermissionDenied(_('Cannot delete the default notification template.'))
        # don't allow deletion of the last template of some kind
        templates_count = NotificationTemplate.objects.filter(name=template.name).count()
        if templates_count == 1:
            raise PermissionDenied(_('Cannot delete the last notification template of this kind.'))
        template.delete()

    @action(detail=False, methods=['get'])
    def create_options(self, request):
        languages = getattr(settings, 'LANGUAGES')
        languages_options = list()
        for language_code, language_display in languages:
            languages_options.append(dict(language_code=language_code, language_display=language_display))
        languages_options.sort(key=lambda x: x['language_code'])
        return Response({
            'languages': languages_options,
            'help_text_map': NotificationTemplatesHelpText.help_text_map,
        })

    @action(detail=False, methods=['get'])
    def get_editable_notification_templates(self, request):
        """
        Gets all templates related to the default one
        """
        template_id = request.query_params.get('template_id', None)
        try:
            template = NotificationTemplate.objects.get(id=template_id)
        except NotificationTemplate.DoesNotExist:
            raise NotFound(_('Template does not exist.'))
        notification_templates = NotificationTemplate.objects.filter(name=template.name)
        return Response({
            'objects': NotificationTemplateSerializer(instance=notification_templates, many=True).data,
        })


class NotificationsCategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationsCategoriesSerializer
    permission_classes = (StaffOnly,)
    queryset = Category.objects.all()
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter, CustomFilter)
    ordering = ('name',)
    ordering_fields = ('name', 'id',)
    filter_fields = ('name',)
    search_fields = ('name',)
