from django.shortcuts import render
from feedparser import parse

def news_feed(request):
    articles = []

    if request.method == 'POST':
        feed = parse(request.POST.get('source_url'))
        articles = feed.entries
            
    context = {'articles': articles}
    return render(request, 'news_feed/news_feed.html', context)
