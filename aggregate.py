import feedparser
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz

FEEDS = [
    "https://clementbobin.github.io/obsidian/index.xml"
]

def fetch_all_feeds(feed_urls):
    entries = []
    for url in feed_urls:
        parsed = feedparser.parse(url)
        for entry in parsed.entries:
            entries.append({
                "title": entry.title,
                "link": entry.link,
                "description": entry.get("summary", ""),
                "published": entry.get("published_parsed")
            })
    return entries

def generate_combined_feed(entries):
    fg = FeedGenerator()
    fg.title("Aggregated Feed")
    fg.link(href="https://yourusername.github.io/yourrepo/feed.xml")
    fg.description("Combined RSS feed from multiple sources")
    fg.language("en")

    entries.sort(key=lambda e: e["published"] or datetime.min.timetuple(), reverse=True)

    for e in entries:
        fe = fg.add_entry()
        fe.title(e["title"])
        fe.link(href=e["link"])
        fe.description(e["description"])
        if e["published"]:
            fe.pubDate(datetime(*e["published"][:6], tzinfo=pytz.UTC))

    fg.rss_file("docs/feed.xml")

if __name__ == "__main__":
    all_entries = fetch_all_feeds(FEEDS)
    generate_combined_feed(all_entries)
