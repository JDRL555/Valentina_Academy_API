from ..views import QuestionsViewSet
from rest_framework_mongoengine.routers import SimpleRouter

router = SimpleRouter()

router.register(r"", QuestionsViewSet)


urlpatterns = [] + router.urls