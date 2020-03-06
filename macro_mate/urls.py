from django.urls import path
from macro_mate import views
app_name = 'macro_mate'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login')
]
