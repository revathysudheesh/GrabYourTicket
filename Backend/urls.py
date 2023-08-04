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
             path('add_admin/', views.add_admin, name='add_admin'),
             path('list_admin/', views.list_admin, name='list_admin'),
             path('edit_admin/<int:dataid>/', views.edit_admin, name='edit_admin'),
             path('delete_admin/<int:dataid>/', views.delete_admin, name='delete_admin'),
             path('change_password_admin/<int:dataid>/', views.change_password_admin, name='change_password_admin'),
             path('update_password_admin/<int:dataid>/', views.update_password_admin, name='update_password_admin'),
             path('theatre_details/', views.theatre_details, name='theatre_details'),
             path('edit_theatre/<int:dataid>/', views.edit_theatre, name='edit_theatre'),
             path('update_theatre/<int:dataid>/', views.update_theatre, name='update_theatre'),

             ]