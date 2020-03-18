
from django.urls import path
from macro_mate import views

from macro_mate.views import MyMeals, AddMeal, AllMeals

app_name = 'macro_mate'

urlpatterns = [
    path('', views.index, name='index'),
    # For meal views, only the default is named so the slugs can be appended in template
    path('meals/', AllMeals.as_view(), name='meals'),
    path('meals/<slug>/', AllMeals.as_view()),
    path('my_meals/', MyMeals.as_view(), name="my_meals"),
    path('my_meals/<slug>/', MyMeals.as_view()),
    path('add_meal/', AddMeal.as_view(), name='add_meal'),
    path('meal/<slug:meal_id_slug>/', views.meal, name='meal'),
]
