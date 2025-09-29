from ..views import RecipeViewSet
from rest_framework_mongoengine.routers import SimpleRouter

router = SimpleRouter()

router.register(r"", RecipeViewSet)


urlpatterns = [] + router.urls
