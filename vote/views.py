from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import Choice, Poll
from .serializers import PollSerializer


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Poll.objects.all().order_by("-expiry_date")

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, pk=None):
        data = request.data.copy()
        poll = Poll.objects.get(id=pk)
        user = request.user
        print(poll.voters.all())
        if poll.expired:
            return Response(
                {"error": "poll expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user in poll.voters.all():
            return Response(
                {"error": "already voted on this poll"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # increase votes on selected choice
        choice = Choice.objects.get(name=data["choice"])
        choice.votes = choice.votes + 1

        # add user to the voters list of the poll to disable voting again
        poll.voters.add(user)
        choice.save()
        poll.save()
        serializer = PollSerializer(poll)

        return Response(serializer.data, status=status.HTTP_200_OK)
