from django.urls import path
from Frontend import views
urlpatterns=[path('index/', views.index, name='index'),]