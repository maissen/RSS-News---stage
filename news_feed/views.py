from django.shortcuts import render, redirect
from feedparser import parse
from .models import *


def news_feed(request):

    sources = NewsSource.objects.all()
    entries = [] 
    for link in sources:
        feed = parse(link.url)
        if 'entries' in feed:
            entries.extend(feed.entries)
        else: 
            continue
            
    context = {'entries': entries}
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

