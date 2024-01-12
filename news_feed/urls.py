from django.urls import path
from .views import *


urlpatterns = [
    path('', news_feed, name='news_feed'),
    path('sources/', news_sources, name='news_sources'),
    path('sources/add/', add_source, name='add_source'),
    path('sources/delete/<int:source_id>/', delete_source, name='delete_source'),

    path('category/add/', add_category, name='add_category'),
]