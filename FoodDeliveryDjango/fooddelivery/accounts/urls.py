from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('address/add/', views.address_create, name='address_create'),
    path('address/<int:address_id>/edit/', views.address_edit, name='address_edit'),
    path('address/<int:address_id>/delete/', views.address_delete, name='address_delete'),
    path('address/<int:address_id>/set-default/', views.set_default_address, name='set_default_address'),
]
