from rest_framework import serializers
from .models import Courses, Category, Purchased_course, Courses_media

from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ["id", "name"]
    
class CourseMediaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Courses_media
    fields = [
      "id", "url_video", "url_cover"
    ]

class CourseSerializer(serializers.ModelSerializer):
  category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)
  user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
  media = serializers.PrimaryKeyRelatedField(queryset=Courses_media.objects.all(), required=True)
  
  class Meta:
    model = Courses
    fields = [
      "id", 
      "title", 
      "description", 
      "duration", 
      "price", 
      "user", 
      "category", 
      "media", 
      "recipe", 
      "created_at"
    ]
    
class PurchasedCourseSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
  course = serializers.PrimaryKeyRelatedField(queryset=Courses.objects.all(), required=True)
  
  class Meta:
    model = Purchased_course
    fields = [
      "course", "user", "is_purchased", "completed", "purchased_at"
    ]
