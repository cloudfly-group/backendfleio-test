from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from fleio.billing.models import Product

from fleio.core.models import AppUser

from fleio.utils.model import dict_to_choices


class TODOStatus(object):
    open = 'open'
    in_progress = 'in progress'
    done = 'done'

    status_map = {
        open: _('Open'),
        in_progress: _('In Progress'),
        done: _('Done')
    }

    @classmethod
    def get_choices(cls):
        return dict_to_choices(cls.status_map)


class TODOManager(models.Manager):
    def add_todo(
            self,
            title: str,
            description: str,
            status: str = TODOStatus.open,
            assigned_to: AppUser = None,
            created_by: AppUser = None
    ):
        return self.create(
            title=title,
            description=description,
            status=status,
            assigned_to=assigned_to,
            created_by=created_by
        )


class TODO(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    assigned_to = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=10240)
    status = models.CharField(max_length=100)

    objects = TODOManager()

    class Meta:
        verbose_name_plural = 'TODOs'

    def __str__(self):
        return '{} - {}'.format(self.title, self.status)


class TODOCommentManager(models.Manager):
    pass


class TODOComment(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    todo = models.ForeignKey(TODO, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    comment_text = models.CharField(max_length=10240, null=True, blank=True)
    new_status = models.CharField(max_length=100, null=True, blank=True)
    new_assignee = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    description_changed = models.BooleanField(default=False, blank=True)
    title_changed = models.BooleanField(default=False, blank=True)

    objects = TODOCommentManager()


class TODOProductSettings(models.Model):
    todo_user = models.ForeignKey(AppUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='todo_product_settings'
    )
    add_todo_on_create = models.BooleanField(default=False)
    add_todo_on_destroy = models.BooleanField(default=False)
    add_todo_on_suspend = models.BooleanField(default=False)
    add_todo_on_resume = models.BooleanField(default=False)
    add_todo_on_renew = models.BooleanField(default=False)
    add_todo_on_change_cycle = models.BooleanField(default=False)
