from django.urls import path, include
from .views import registration_view, logout_view, login_view, profile_view, update_profile

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('profile/<int:pk>', profile_view, name='author_profile'),
    path('profile/<int:pk>/update', update_profile, name='update_profile'),
    ]
