from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.home_veiw, name='home'),
    path('logout', views.login_view, name='logout')
]
