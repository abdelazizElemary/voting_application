from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = [
        "email",
        "last_name",
        "first_name",
    ]

    fieldsets = (
        (None, {"fields": ("password", "otp")}),
        (_("Personal info"), {"fields": (("first_name", "last_name"), "email")}),
        (
            _("Permissions"),
            {
                "fields": ("is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created")}),
        (_("Polls"), {"fields": ("polls",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )

    readonly_fields = ["created", "polls"]
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("last_name", "first_name")
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def polls(self, obj):
        polls = []
        for poll in obj.polls.all():
            polls.append(poll.title)

        return polls
