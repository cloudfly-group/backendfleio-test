from collections import OrderedDict

from django.db import models
from django.utils.translation import ugettext_lazy as _


class CodeInsertionPoints:
    beginning_of_head = 'beginning_of_head'
    end_of_head = 'end_of_head'
    beginning_of_body = 'beginning_of_body'
    end_of_body = 'end_of_body'
    base_tag = 'base_tag'

    insertion_point_to_marker_map = {
        beginning_of_head: '<!-- beginning of head -->',
        end_of_head: '<!-- end of head -->',
        beginning_of_body: '<!-- beginning of body -->',
        end_of_body: '<!-- end of body -->',
        base_tag: '<base href="/">',
    }

    code_insertion_points_name_map = OrderedDict([
        (beginning_of_head, _('the beginning of <head> tag')),
        (end_of_head, _('the end of the <head> tag')),
        (beginning_of_body, _('the beginning of <body> tag')),
        (end_of_body, _('the end of the <body> tag')),
        (base_tag, _('the <base> tag(replaces tag with new code)')),
    ])

    code_insertion_points_helptext_map = OrderedDict([
        (beginning_of_head, _('This code will be inserted right after the start of the <head> HTML tag.')),
        (end_of_head, _('This code will be inserted just before the end of the <head> HTML tag.')),
        (beginning_of_body, _('This code will be inserted right after the start of the <body> HTML tag.')),
        (end_of_body, _('This code will be inserted just before the end of the <body> HTML tag.')),
        (base_tag, _(
            'This code replace the <base> HTML tag. You need to make sure you include a correct base tag here'
            'or you can render the frontend unusable.'
        )),
    ])


class FrontendFileTypes:
    enduser_index = 'enduser_index'
    staff_index = 'staff_index'

    frontend_file_types_map = OrderedDict([
        (enduser_index, _('enduser index')),
        (staff_index, _('staff index')),
    ])


class CustomCode(models.Model):
    # NOTE: installers must be updated if this model is changed
    insertion_point = models.CharField(max_length=128, db_index=True)
    code = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True, db_index=True)
    frontend_file_type = models.CharField(max_length=128, db_index=True)

    class Meta:
        unique_together = ('insertion_point', 'frontend_file_type')
