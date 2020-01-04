from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from fleio.core.exceptions import APIBadRequest
from fleio.notifications.models import Category, NotificationTemplate


class NotificationTemplateSerializer(serializers.ModelSerializer):
    category_display = serializers.SerializerMethodField(required=False, read_only=True)
    template_languages = serializers.SerializerMethodField(required=False, read_only=True)
    has_all_available_languages = serializers.SerializerMethodField(required=False, read_only=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    language_display = serializers.SerializerMethodField(required=False, read_only=True)
    content = serializers.CharField(allow_blank=True)

    class Meta:
        model = NotificationTemplate
        fields = ('id', 'name', 'content', 'title', 'category', 'category_display', 'language', 'template_languages',
                  'language_display', 'has_all_available_languages', 'disable_notification')

    def validate_title(self, title):
        category = self.initial_data.get('category_display', None)
        if not category:
            return title
        if category == 'ticket':
            error_field = 'title{}'.format(self.initial_data.get('id'))
            error_display = dict()
            error_display[error_field] = _('You need to use the "[#{{ variables.ticket_id }}] format in the title"')

            if '[#{{' not in title:
                raise APIBadRequest(error_display)
            start_index = title.index('[#{{') + 3
            try:
                end_index = title.index('}', start_index)
                if title[end_index:end_index + 3] != '}}]':
                    raise APIBadRequest(error_display)
            except ValueError:
                raise APIBadRequest(error_display)
            if 'variables.ticket_id' not in title[start_index:end_index]:
                raise APIBadRequest(error_display)
        return title

    @staticmethod
    def get_category_display(notification: NotificationTemplate):
        return notification.category.name

    @staticmethod
    def get_has_all_available_languages(template: NotificationTemplate):
        count_related_templates = NotificationTemplate.objects.filter(name=template.name).count()
        if count_related_templates == len(getattr(settings, 'LANGUAGES')):
            return True
        else:
            return False

    @staticmethod
    def get_language_display(template: NotificationTemplate):
        languages = getattr(settings, 'LANGUAGES')
        languages = dict(languages)
        if template.language in languages:
            return languages[template.language]
        return 'N/A'

    @staticmethod
    def get_template_languages(notification: NotificationTemplate):
        template_languages = NotificationTemplate.objects.filter(
            name=notification.name
        ).values_list('language', flat=True)
        return template_languages


class NotificationTemplateSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = NotificationTemplate
        fields = ('id', 'name', 'content', 'title', 'language')


class NotificationsCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
