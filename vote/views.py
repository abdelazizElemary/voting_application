from rest_framework import permissions, viewsets

from .models import Poll
from .serializers import PollSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]
