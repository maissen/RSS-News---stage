from django.urls import path
from .views import *


urlpatterns = [
    path('', news_feed, name='news_feed'),
]