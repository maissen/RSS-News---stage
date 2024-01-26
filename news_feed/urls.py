from django.urls import path
from .views import *


urlpatterns = [
    path('', welcome, name='welcome'),

    path('login/', user_login, name='user_login'),
    path('register/', user_register, name='user_register'),
    path('logout/', user_logout, name='user_logout'),

    path('feed/', news_feed, name='news_feed'),
    path('sources/', news_sources, name='news_sources'),
    path('sources/add/', add_source, name='add_source'),
    path('sources/delete/<int:source_id>/', delete_source, name='delete_source'),

    path('category/add/', add_category, name='add_category'),
    path('category/delete/', delete_category, name='delete_category'),
]