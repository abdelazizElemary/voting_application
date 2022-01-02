from django.db.models import fields
from rest_framework import serializers

from .models import Choice, Poll


class PollSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        read_only_fields = ["created", "modified", "choices"]
        fields = [
            "id",
            "voters",
            "title",
            "description",
            "expiry_date",
            "expired",
        ] + read_only_fields

    def get_choices(self, obj):
        choices = []
        for choice in obj.choices.all():
            choices.append([{"id": choice.id, "name": choice.name, "votes": choice.votes}])
        return choices


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        read_only_fields = ["id"]
        fields = read_only_fields + [
            "id",
            "name",
            "poll",
            "votes",
        ]
