from django.urls import path
from rest_framework.routers import SimpleRouter

from courses import views

router = SimpleRouter()
router.register(r"courses", views.CourseViewSet)
router.register(r"purchased", views.PurchasedCourseViewSet)
router.register(r"courses_media", views.CourseMediaViewSet)
router.register(r"category", views.CategoryViewSet)

urlpatterns = [
  path(
    "courses/export_certificate/", 
    views.CourseCertificateViewSet.as_view({ "post": "create" }), name="pdf"
  ),
  path(
    "courses/complete/", 
    views.CompleteCourseViewsSet.as_view({ "post": "create" }), name="complete"
  )
] + router.urls
