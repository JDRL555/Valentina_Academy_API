   
from django.urls import path, re_path, include
from django.contrib import admin

from users.urls import urlpatterns as user_views
from courses.urls import urlpatterns as courses_views
from recipes.urls.recipes import urlpatterns as recipe_views
from recipes.urls.ingredients import urlpatterns as ingredients_views 
from recipes.urls.export import urlpatterns as export_recipes_views
from survey.urls.question import urlpatterns as question_views
from survey.urls.answers import urlpatterns as answer_views
from survey.urls.surveys import urlpatterns as survey_views



urlpatterns = [
    path('', include(courses_views)),
    path('admin/', admin.site.urls),
    path('users/', include(user_views)),
    path('recipes/', include(recipe_views)),
    path('ingredients/', include(ingredients_views)),
    path('export_recipe/<str:recipe_id>/', include(export_recipes_views)),
    path("questions/", include(question_views)),
    path("answers/", include(answer_views)),
    path("surveys/", include(survey_views))
]
