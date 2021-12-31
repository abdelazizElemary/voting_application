from rest_framework import serializers

from .models import Poll


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        read_only_fields = ["created", "modified"]
        fields = read_only_fields + [
            "id",
            "voter",
            "title",
            "description",
            "expiry_date",
        ]
