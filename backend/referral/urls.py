from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('auth/phone/', views.PhoneAuthView.as_view(), name='phone_auth'),
    path('auth/code/', views.CodeAuthView.as_view(), name='code_auth'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile_page/', views.ProfilePageView.as_view(), name='profile_page'),
] 