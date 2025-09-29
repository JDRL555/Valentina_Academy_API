from django.urls import path

from ..views import RecipePDFViewSet
from rest_framework_mongoengine.routers import SimpleRouter

router = SimpleRouter()

router.register(r"", RecipePDFViewSet, basename="export")

urlpatterns = [] + router.urls