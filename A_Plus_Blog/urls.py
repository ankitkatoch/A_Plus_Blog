''"""A_Plus_Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from django_email_verification import urls as email_urls
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('email/', include(email_urls)),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('admin/', admin.site.urls),
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('account/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('account/password_change/',
                       auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
                       name='password_change'),
    path('account/password_reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='accounts/password_reset_done.html'),
                       name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
    path('account/password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset'),
    path('account/reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='accounts/password_reset_complete.html'),
                       name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
