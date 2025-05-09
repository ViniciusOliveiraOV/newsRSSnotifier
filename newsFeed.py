import feedparser
import subprocess
import time
import os

RSS_FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCYO_jab_esuFRV4b17AJtAw",
    "https://anixea.blogspot.com/feeds/posts/default?alt=rss"
]

def fetch_all_entries(feeds):
    all_entries = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            all_entries.append((entry.title, entry.link))
    seen = set()
    unique_entries = []
    for title, link in all_entries:
        if link not in seen:
            unique_entries.append((title, link))
            seen.add(link)
    return unique_entries

def show_notification(title, message):
    subprocess.run(['notify-send', title, message])

def save_links(links, filename="shown_links.txt", max_links=500):
    links = list(links)[-max_links:]
    with open(filename, "w") as f:
        for link in links:
            f.write(link + "\n")

def load_links(filename="shown_links.txt"):
    if not os.path.exists(filename):
        return set()
    with open(filename, "r") as f:
        return set(line.strip() for line in f if line.strip())

def main():
    shown_links = load_links()
    while True:
        entries = fetch_all_entries(RSS_FEEDS)
        new_entries = [entry for entry in entries if entry[1] not in shown_links]
        if new_entries:
            for title, link in new_entries:
                show_notification(title, link)
                shown_links.add(link)
                save_links(shown_links)
                time.sleep(10)
        else:
            time.sleep(10)

if __name__ == "__main__":
    main()