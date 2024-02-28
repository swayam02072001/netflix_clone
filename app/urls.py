from django.urls import path
from .views import *
app_name='app'
urlpatterns=[
    path('index/',index,name='index'),
    path('',login,name='login'),
    path('logout/',logout,name='logout'),
    path('signup/',signup,name='signup'),
    path('search/',search,name='search'),
    path('my_list/',my_list,name='my_list'),
    path('movie/<str:pk>',movie,name='movie'),
    path('genre/<str:pk>',genre,name='genre'),
    path('add_to_list/',add_to_list,name='add_to_list')
]