from django.shortcuts import render, redirect
from feedparser import parse
from .models import *


def news_feed(request):

    sources = NewsSource.objects.all()
    feeds = []
    for link in sources:
        feed = parse(link.url)
        feed_title = ''
        if 'feed' in feed and 'title' in feed['feed']:
            feed_title = feed['feed']['title']
        else:
            feed_title = link.url
            
        if 'entries' in feed and feed['entries'] != []:
            feeds.append({'feed_title': feed_title, 'feed_entries': feed['entries']})
        else: 
            feeds.append({'feed_title': "Source : " + feed_title, 'feed_entries': "Doesn't have any news"})
            
    context = {'feeds': feeds}
    return render(request, 'news_feed/news_feed.html', context)


def news_sources(request):
    sources = NewsSource.objects.all()
    context = {'links': sources}
    return render(request, 'news_feed/news_sources.html', context)


def add_source(request):
    if request.method == 'POST':
        source_link = request.POST.get('source_link')
        
        try:
            existing_source = NewsSource.objects.get(url=source_link)
        except NewsSource.DoesNotExist:
            NewsSource.objects.create(url=source_link)
            return redirect('news_sources')
        
    return redirect('news_sources')


def delete_source(request, source_id):
    if request.method == 'POST':
        try:
            NewsSource.objects.get(id=source_id).delete()
        except:
            return redirect('news_sources')
            
    return redirect('news_sources')

