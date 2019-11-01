from src.feed.db.session import Session
from src.feed.db.podcast import Podcast
from src.feed.db.episode import Episode
from bs4 import BeautifulSoup


class PodcastFeedGenerator:
    def __init__(self, pod_id: int) -> None:
        self.pod_id = pod_id
        self.doc = BeautifulSoup(features="xml")

    def new_rss_feed_header(self):
        rss_feed = self.doc.new_tag(
            "rss",
            **{
                "xmlns:atom": "http://www.w3.org/2005/Atom",
                "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
                "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
                "version": "2.0",
            },
        )
        self.doc.append(rss_feed)
        return rss_feed

    def query_podcast(self):
        sess = Session()
        return sess.query(Podcast).get(self.pod_id)

    def render(self) -> str:
        rss_feed = self.new_rss_feed_header()
        pod = self.query_podcast()

        channel = pod.generate_rss_channel()
        for ep in pod.episodes:
            channel.append(ep.generate_rss_item())

        rss_feed.append(channel)

        return str(self.doc)
