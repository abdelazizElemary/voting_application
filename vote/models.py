from datetime import datetime, timezone

from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from users.models import User


class Poll(TimeStampedModel):
    voters = ManyToManyField(User, related_name="polls", blank=True)
    title = models.CharField(_("title"), max_length=256, blank=True, db_index=True, unique=True)
    description = models.CharField(_("description"), max_length=256, blank=True, db_index=True)
    expiry_date = models.DateTimeField(_("expiry date"), null=True, blank=True)

    class Meta:
        verbose_name = _("poll")
        verbose_name_plural = _("polls")

    def __str__(self):
        return f"{self.title}"

    @property
    def expired(self):
        now = make_aware(datetime.now(), timezone=timezone.utc)
        return now >= self.expiry_date


class Choice(models.Model):
    name = models.CharField(_("choice name"), max_length=256, unique=True)
    poll = models.ForeignKey(Poll, related_name="choices", null=True, blank=True, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("choice")
        verbose_name_plural = _("choices")

    def __str__(self):
        return f"{self.name}"
