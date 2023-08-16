from django.urls import path
from Frontend import views
urlpatterns=[path('index/', views.index, name='index'),
             path('seating_plan/', views.seating_plan, name='seating_plan'),
             path('nowshowing/', views.nowshowing, name='nowshowing'),
             path('comingsoon/', views.comingsoon, name='comingsoon'),
             path('contactus/', views.contactus, name='contactus'),
             path('movie_details/<int:movie_id>/', views.movie_details, name='movie_details'),
             path('login_signup/', views.login_signup, name='login_signup'),
             path('user_login/', views.user_login, name='user_login'),
             path('user_logout/', views.user_logout, name='user_logout'),
             path('saveuser/', views.saveuser, name='saveuser'),
             path('save_message/', views.save_message, name='save_message'),
             path('post_review/<int:movie_id>/', views.post_review, name='post_review'),
             path('my_profile/', views.my_profile, name='my_profile'),

             ]