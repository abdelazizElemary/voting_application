from rest_framework import routers

from . import views

app_name = "vote"

router = routers.SimpleRouter()
router.register("polls", views.PollViewSet, basename="polls")

urlpatterns = router.urls
