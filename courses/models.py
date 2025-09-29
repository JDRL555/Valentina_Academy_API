from django.db import models
from django.contrib.auth.models import User

import datetime

# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
      return self.name
    
class Courses_media(models.Model):
  url_video = models.TextField(max_length=800)
  url_cover = models.TextField(max_length=800)
  
  def __str__(self):
    return self.url_video

class Courses(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=250)
  duration = models.TimeField(auto_created=False, auto_now_add=False)
  price = models.DecimalField(max_digits=20, decimal_places=2)
  user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
  category = models.ForeignKey("courses.Category", on_delete=models.CASCADE, db_column="category")
  media = models.ForeignKey(Courses_media, on_delete=models.CASCADE, db_column="courses_media")
  recipe = models.CharField(max_length=500, null=True)
  created_at = models.DateField(default=datetime.date.today)
  
  def __str__(self):
    return self.title
  
class Purchased_course(models.Model):
  course = models.ForeignKey("courses.Courses", on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  is_purchased = models.BooleanField(default=False)
  completed = models.BooleanField(default=False)
  purchased_at = models.DateField(default=datetime.date.today)
  
  def __str__(self):
    return f"Course {self.course} {'purchased' if self.is_purchased else 'not purchased'}"