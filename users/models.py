from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from model_utils.models import TimeStampedModel

from .managers import UserManager


class User(AbstractBaseUser, TimeStampedModel, PermissionsMixin):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(_("email address"), max_length=255, unique=True)
    first_name = models.CharField(
        _("first name"), max_length=256, blank=True, db_index=True
    )
    last_name = models.CharField(
        _("last name"), max_length=256, blank=True, db_index=True
    )
    is_staff = models.BooleanField(_("is staff"), default=False)
    is_active = models.BooleanField(_("is active"), default=True)

    objects = UserManager()

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
