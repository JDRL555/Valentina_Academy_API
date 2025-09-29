from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UsersViewSet,LogoutViewSet,RegisterViewSet,Auth_userViewSet,LoginViewSet, RolViewSet


router = SimpleRouter()
router.register(r"", UsersViewSet)


urlpatterns = [
  path("login/", LoginViewSet.as_view({ "post": "create" }), name="login"),
  path(
    "role/", 
    RolViewSet.as_view({ 
      "post": "create", 
      "put": "update", 
      "delete": "destroy" 
    }), 
    name="manage_rol"
  ),
  path("role/<int:user_id>/", RolViewSet.as_view({ "get": "list" }), name="get_rol"),
  path("register/", RegisterViewSet.as_view({ "post": "create" }), name="register"),
  path("auth/<str:token>/", Auth_userViewSet.as_view({ "get": "list" }), name="auth"),
  path("logout/<str:token>/", LogoutViewSet.as_view({ "post": "create" }), name="logout"),
] + router.urls