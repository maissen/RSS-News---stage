# news_feed/utils.py

import feedparser
from django.utils import timezone
import html

def fetch_news_from_url(url):
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description = html.unescape(entry.summary) if hasattr(entry, 'summary') else ""

        # Check for published date in different fields
        pub_date_parsed = getattr(entry, 'published_parsed', None)
        if not pub_date_parsed:
            pub_date_parsed = getattr(entry, 'updated_parsed', None)

        if pub_date_parsed:
            pub_date = timezone.datetime.fromtimestamp(time.mktime(pub_date_parsed))
            pub_date = timezone.make_aware(pub_date)

            articles.append({
                'title': title,
                'link': link,
                'description': description,
                'pub_date': pub_date,
            })

    return articles
