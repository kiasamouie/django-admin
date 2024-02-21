from api.authentication.viewsets import (
    RegisterViewSet,
    LoginViewSet,
    ActiveSessionViewSet,
    LogoutViewSet,
)
from rest_framework import routers
from api.user.viewsets import UserViewSet, UserListViewSet
from api.playlists.viewsets import PlaylistViewSet
from api.mixes.viewsets import MixesViewSet

# Router
router = routers.SimpleRouter(trailing_slash=False)

# Users
# router.register("users/email/<str:email>", UserViewSet, basename="user")
router.register("users/edit", UserViewSet, basename="user-edit")
router.register("users/register", RegisterViewSet, basename="register")
router.register("users/login", LoginViewSet, basename="login")
router.register("users/checkSession", ActiveSessionViewSet, basename="check-session")
router.register("users/logout", LogoutViewSet, basename="logout")
router.register("users", UserListViewSet, basename="user-list")

# Playlists
router.register("playlists", PlaylistViewSet, basename="playlist")
# router.register("playlists/fetch_urls", PlaylistViewSet, basename="fetch_urls")

# Mixes
router.register("mixes", MixesViewSet, basename="mix")

urlpatterns = [
    *router.urls,
]
