from django.conf.urls import url
from django.urls import path
from macro_mate import views

app_name = 'macro_mate'

urlpatterns = [
    path('', views.index, name='index'),
    path('meals/', views.meals, name='meals'),
    path('my_meals/', views.my_meals, name="my_meals"),
    path('add_meal/', views.add_meal, name='add_meal'),

]
