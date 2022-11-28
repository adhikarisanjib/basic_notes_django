from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid

from django.contrib.auth import get_user_model
User = get_user_model()


class Note(models.Model):
    id = models.UUIDField(
        verbose_name = _('ID'),
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=256,
        null=True,
        blank=True,
    )
    body = models.TextField(
        verbose_name=_('Body'),
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(
        verbose_name=_('Date Joined'),
        auto_now_add=True,
        editable=False,
    )
    date_updated = models.DateTimeField(
        verbose_name=_('Last Update'),
        auto_now=True,
        editable=False,
    )

    class Meta:
        ordering = ('-date_updated',)

    def __str__(self):
        return f'{self.user}-{self.title}'

