from ..views import IngredientViewSet
from rest_framework_mongoengine.routers import SimpleRouter

router = SimpleRouter()

router.register(r"", IngredientViewSet)


urlpatterns = [] + router.urls