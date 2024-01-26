from django.contrib import admin
from .models import *

admin.site.register(NewsSource)
admin.site.register(SourceCategory)

'''
https://feeds.bbci.co.uk/news/technology/rss.xml
https://feeds.bbci.co.uk/news/rss.xml
'''

