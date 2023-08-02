from django.urls import path
from Backend import views

urlpatterns=[path('admin_home/', views.admin_home, name='admin_home'),
             path('login_reg/', views.login_reg, name='login_reg'),
             path('signup/', views.signup, name='signup'),
             path('admin_login/', views.admin_login, name='admin_login'),
             path('admin_logout/', views.admin_logout, name='admin_logout'),
             path('my_profile/', views.my_profile, name='my_profile'),
             path('update_user/<int:dataid>/', views.update_user, name="update_user"),
             path('change_password/', views.change_password, name='change_password'),
             path('update_password/', views.update_password, name='update_password'),
             ]