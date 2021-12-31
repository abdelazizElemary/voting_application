from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers

from . import views

app_name = "users"

router = routers.DefaultRouter()
router.register(r"users", views.UserView, "users")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.LoginAPI.as_view(), name="knox_login"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("registration/", views.RegistrationAPI.as_view(), name="rest_register"),
]
