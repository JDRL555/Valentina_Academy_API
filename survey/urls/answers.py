from ..views import AnswersViewSet
from rest_framework_mongoengine.routers import SimpleRouter

router = SimpleRouter()

router.register(r"", AnswersViewSet)


urlpatterns = [] + router.urls