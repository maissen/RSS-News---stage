# news_feed/management/commands/fetch_news.py

import feedparser
import time
from django.core.management.base import BaseCommand
from news_feed.models import NewsArticle
from django.utils import timezone

class Command(BaseCommand):
    help = 'Fetch and store news articles from an RSS feed'

    def add_arguments(self, parser):
        parser.add_argument('source_url', type=str, help='The source URL of the RSS feed')

    def handle(self, *args, **options):
        rss_feed_url = options['source_url']

        feed = feedparser.parse(rss_feed_url)

        for entry in feed.entries:
            title = entry.title
            link = entry.link
            description = entry.summary
            pub_date_parsed = entry.published_parsed
            source = feed.feed.title

            pub_date = timezone.datetime.fromtimestamp(time.mktime(pub_date_parsed))
            pub_date = timezone.make_aware(pub_date)

            if not NewsArticle.objects.filter(link=link).exists():
                NewsArticle.objects.create(
                    title=title,
                    link=link,
                    description=description,
                    pub_date=pub_date,
                    source=source
                )

        self.stdout.write(self.style.SUCCESS('News fetched and stored successfully.'))
