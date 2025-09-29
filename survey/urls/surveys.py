from ..views import SurveysViewSet
from rest_framework_mongoengine.routers import SimpleRouter

router = SimpleRouter()

router.register(r"", SurveysViewSet)


urlpatterns = [] + router.urls