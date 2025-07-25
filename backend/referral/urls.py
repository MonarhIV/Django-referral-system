from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile_page/', views.ProfilePageView.as_view(), name='profile_page')
] 