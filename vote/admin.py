from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from vote.models import Choice, Poll


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "expired"]
    readonly_fields = ("choices",)

    def choices(self, obj):
        choices = []
        for choice in obj.choices.all():
            choices.append(choice.name)
        return choices


admin.site.register(Choice)
