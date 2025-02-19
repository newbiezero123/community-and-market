from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLogoutView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('manage_address/', views.manage_address, name='manage_address'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]