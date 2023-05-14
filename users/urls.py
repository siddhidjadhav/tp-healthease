from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.profile, name="profile"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register"),
    path('server_info', views.server_info, name="server_info")
]



