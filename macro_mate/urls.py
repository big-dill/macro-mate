
from django.urls import path
from macro_mate import views

from macro_mate.views import MyMeals, AddMeal, AllMeals

app_name = 'macro_mate'

urlpatterns = [
    path('', views.index, name='index'),
    path('meals/', AllMeals.as_view(), name='meals'),
    path('meals/<slug:tag_slug>/', AllMeals.as_view()),
    path('my_meals/', MyMeals.as_view(), name="my_meals"),
    path('my_meals/<slug:tag_slug>/', MyMeals.as_view()),
    path('add_meal/', AddMeal.as_view(), name='add_meal'),
    path('add_meal/<slug:meal_id_slug>', AddMeal.as_view()),
    path('meal/', views.meal, name='meal'),
    path('meal/<slug:meal_id_slug>/', views.meal),
]
