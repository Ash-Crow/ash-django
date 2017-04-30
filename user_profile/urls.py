from django.conf.urls import url, include
from user_profile import views

urlpatterns = [
    url(r'profile', views.profile, name='profile'),
    url(r'accounts/login', views.login_oauth, name='login'),
    url(r'oauth/', include('social_django.urls', namespace='social')),
    url(r'', views.index),
]