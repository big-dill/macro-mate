
from django.urls import path
from macro_mate import views

app_name = 'macro_mate'

urlpatterns = [
    path('', views.index, name='index'),
    path('meals/<slug:meal_id_slug>/', views.meal, name='meal'),
    path('meals/', views.meals, name='meals'),
    path('your_meals/', views.your_meals, name="your_meals")

]
