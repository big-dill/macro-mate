from django.urls import path
from api import views

# The app name for macro_mate AJAX API
app_name = 'api'

# API Ajax Patterns
urlpatterns = [
    path('tags/', views.TagsAPI.as_view(), name='tags'),
    path('meals/', views.MealsAPI.as_view(), name='meals'),
    path('nutrition/', views.NutritionAPI.as_view(), name='nutrition')

]
