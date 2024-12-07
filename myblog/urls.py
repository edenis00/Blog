from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.home_view, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('create/', views.create_posts_view, name='create'),
    path('post_detail/<int:post_id>/', views.post_detial_view, name='post_detail'),
]
