from django.urls import path
from django.contrib.auth import views as auth_views
# from django.views.generic import TemplateView

from .forms import (UserLoginForm)
# only for password reset form 

from .import views

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),    
    path('register/', views.account_register, name='register'),

    # for email validation only 
    # path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'), 

    # user portals 
    path('dashboard/', views.dashboard, name='dashboard'),
    # editing user profile not needed at the moment 
    # path('profile/edit/', views.edit_details, name='edit_details'),
    path('profile/delete_user', views.delete_user, name='delete_user'),

    # View, update, delete addresses
    path('addresses/', views.view_address, name='address'),
    path('add_addresses/', views.add_address, name='add_address'),
    path('addresses/edit/<slug:id>/', views.edit_address, name='edit_address'),
    path('addresses/delete/<slug:id>/', views.delete_address, name='delete_address'),
    path('addresses/set_default/<slug:id>/', views.set_default, name='set_default'),
    
    # orders
    path('user_orders', views.user_orders, name='user_orders'),
    # Wishlist
]