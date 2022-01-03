from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "users"

router = routers.DefaultRouter()
router.register(r"users", views.UserView, "users")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.LoginAPI.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("register/", views.RegistrationAPI.as_view(), name="register"),
    path("verify/", views.verify, name="verify"),
]
