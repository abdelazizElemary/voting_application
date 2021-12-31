from django.contrib import admin
from django.urls import include, path

api_patterns = [
    path("auth/", include("users.urls")),
    path("vote/", include("vote.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_patterns)),
]
