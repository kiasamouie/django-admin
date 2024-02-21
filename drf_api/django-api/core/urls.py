from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(("api.routers", "api"), namespace="api")),
    # path("api/users/", include(("api.routers", "users"), namespace="api")),
    # path("api/playlists/", include(("api.routers", "playlists"), namespace="playlists")),
]
