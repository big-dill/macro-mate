from django.urls import path
from macro_mate import views
app_name = 'macro_mate'

urlpatterns = [
    path('', views.index, name='index'),
    #path('login/', views.user_login, name='login'),
    #path('register/', views.register, name='register'),
]
