from django.shortcuts import render, redirect
from feedparser import parse
from .models import *

def news_feed(request):
    articles = []

    if request.method == 'POST':
        feed = parse(request.POST.get('source_url'))
        articles = feed.entries
            
    context = {'articles': articles}
    return render(request, 'news_feed/news_feed.html', context)


def news_sources(request):
    sources = NewsSource.objects.all()
    context = {'links': sources}
    return render(request, 'news_feed/news_sources.html', context)



def add_source(request):
    if request.method == 'POST':
        source_link = request.POST.get('source_link')
        if not source_link:
            return redirect('news_sources')
        
        try:
            NewsSource.objects.create(link=source_link)
        except:
            return redirect('news_sources')
            
    return redirect('news_sources')


def delete_source(request, source_id):
    if request.method == 'POST':
        try:
            NewsSource.objects.get(id=source_id).delete()
        except:
            return redirect('news_sources')
            
    return redirect('news_sources')

