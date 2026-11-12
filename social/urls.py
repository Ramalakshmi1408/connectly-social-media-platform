from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('create-post/', views.create_post_view, name='create_post'),
    path('like/<int:post_id>/', views.like_post_view, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment_view, name='add_comment'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
path('follow/<str:username>/', views.follow_view, name='follow'),
path('edit-post/<int:post_id>/', views.edit_post_view, name='edit_post'),
path('delete-post/<int:post_id>/', views.delete_post_view, name='delete_post'),
path('search/', views.search_view, name='search'),
]