from django.urls import path
from .views import (
    HomeView,
    profile_view,
    register_view,
    logout_view,
    login_view,
    profile_update_view,
    single_post,
    post_create_view,
    post_update_view,
    comment_view,
)

urlpatterns = [
    path('', HomeView, name='home'),
    # post 
    path("single/<slug>/", single_post, name="single_post_view"),
    path("post-create/", post_create_view, name="post_create_view"),
    path("post-update/<slug>/", post_update_view, name="post_update_view"),
    # profile
    path('profile/<str:pk>/', profile_view, name='profile_view'),
    path('register/', register_view, name='register_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('profile-update/<str:pk>/', profile_update_view, name='profile_update_view'),
    path('contact/', comment_view, name='contact_view'),
]
