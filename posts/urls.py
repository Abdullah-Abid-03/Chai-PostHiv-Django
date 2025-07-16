from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [ # at app level
    path('index/', views.homepage, name='index'),
    path('createtweet/', views.create_tweet, name='create_tweet'),
    path('savetweet/', views.savetweet, name='savetweet'),
    path('edit_tweet/<int:tweet_id>/', views.edit_tweet, name='edit_tweet'),
    path('delete_tweet/<int:tweet_id>/', views.delete_tweet, name='delete_tweet'),
    path('index/pic_view/<int:pic_id>', views.picture, name='picture'),
    path('register/', views.register, name='register'),
    path('login_form/', views.login_user, name='login_form'),
    path('logout_view/', views.logout_view, name='logout'),

]