from django.conf.urls import url
from django.urls import path
from api import views

# The app name for our AJAX API
app_name = 'api'

# API Ajax Patterns
urlpatterns = [
    path('tags/', views.TagsAPI.as_view(), name='tags'),
    path('nutrition/', views.NutritionAPI.as_view(), name='nutrition')

]
