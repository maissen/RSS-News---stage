from django.shortcuts import render, redirect
from feedparser import parse
from .models import *


def news_feed(request):
    categories = SourceCategory.objects.all()
    feeds_by_category = []

    for category in categories:
        sources = NewsSource.objects.filter(category=category)
        feeds = []

        for source in sources:
            feed = parse(source.url)
            feed_title = feed.feed.title if 'feed' in feed and 'title' in feed.feed else source.url

            if 'entries' in feed and feed.entries:
                feed_entries = feed.entries
            else:
                feed_entries = [{'title': "No News", 'published': '', 'description': '', 'link': ''}]

            feeds.append({'source_title': source.title, 'feed_title': feed_title, 'feed_entries': feed_entries})

        feeds_by_category.append({'category': category, 'feeds': feeds})

    context = {'categories': categories,'feeds_by_category': feeds_by_category}
    return render(request, 'news_feed/news_feed.html', context)


def news_sources(request):
    categories = SourceCategory.objects.all()
    sources = NewsSource.objects.all()
    context = {'categories': categories, 'links': sources}
    return render(request, 'news_feed/news_sources.html', context)


def add_source(request):
    if request.method == 'POST':
        source_title = request.POST.get('source_title')
        source_link = request.POST.get('source_link')
        source_category_id = request.POST.get('source_category')
        
        try:
            existing_source = NewsSource.objects.get(url=source_link)
        except NewsSource.DoesNotExist:
            try:
                source_category = SourceCategory.objects.get(id=source_category_id)
            except SourceCategory.DoesNotExist:
                return redirect('news_sources')

            # Create the NewsSource instance with the retrieved category instance
            NewsSource.objects.create(
                title=source_title,
                url=source_link,
                category=source_category
            )
            return redirect('news_sources')

    return redirect('news_sources')


def delete_source(request, source_id):
    if request.method == 'POST':
        try:
            NewsSource.objects.get(id=source_id).delete()
        except:
            return redirect('news_sources')
            
    return redirect('news_sources')


def add_category(request):

    if request.method == 'POST':
        category_title = request.POST.get('category_title').capitalize()
        SourceCategory.objects.create(
            title=category_title
        )

    return redirect('news_sources')


def delete_category(request):
    if request.method == 'POST':
        try:
            category_id = request.POST.get('category_for_deletion')
            print("category id ::::: ", category_id)
            SourceCategory.objects.get(id=category_id).delete()
        except:
            return redirect('news_sources')

    return redirect('news_sources')



