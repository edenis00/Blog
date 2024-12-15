from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.home_view, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('create/', views.create_posts_view, name='create'),
    path('post_detail/<int:post_id>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/edit_post/', views.edit_post_view, name='edit_post'),
    path('post/<int:id>/edit_comment/', views.edit_comment_view, name="edit_comment"),
]
