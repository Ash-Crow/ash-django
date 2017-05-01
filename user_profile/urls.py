from django.conf.urls import url, include
from user_profile import views as up_views

urlpatterns = [
    url(r'profile', up_views.profile, name='profile'),
    url(r'accounts/login', up_views.login_oauth, name='login'),
    url(r'oauth/', include('social_django.urls', namespace='social')),
    url(r'', up_views.index),
]