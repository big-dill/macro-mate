from django.conf.urls import url
from django.urls import path
from macro_mate import views
app_name = 'macro_mate'

urlpatterns = [
    path('', views.index, name='index'),
    url('', views.meals, name='meals'),
]
