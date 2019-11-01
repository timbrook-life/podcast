from src.feed.db.session import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from bs4 import BeautifulSoup


class Podcast(Base):
    __tablename__ = "podcasts"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    url = Column(String)

    episodes = relationship(
        "Episode", primaryjoin="and_(Podcast.id == Episode.podcast, Episode.published)"
    )

    def generate_rss_channel(self):
        channel = BeautifulSoup(features="xml").new_tag("channel")
        bare_tags = {
            "title": self.name,
            "description": self.description,
            "language": "en-us",
            "docs": "http://www.rssboard.org/rss-specification",
            "generator": "myself",
            "lastBuildDate": datetime.now().ctime(),
        }
        for t, v in bare_tags.items():
            tag = BeautifulSoup(features="xml").new_tag(t)
            tag.string = v
            channel.append(tag)

        # Links
        lt = BeautifulSoup(features="xml").new_tag("link")
        lt.string = self.url
        channel.append(lt)

        lta = BeautifulSoup(features="xml").new_tag(
            "atom:link", href=self.url, rel="self"
        )
        channel.append(lta)

        # iTunes category and friends
        cat = BeautifulSoup(features="xml").new_tag(
            "itunes:category", text="Technology"
        )
        cat.append(
            BeautifulSoup(features="xml").new_tag("itunes:category", text="Podcasting")
        )
        channel.append(cat)

        channel.append(
            BeautifulSoup(features="xml").new_tag(
                "itunes:image",
                href="https://timbrook-podcast.sfo2.digitaloceanspaces.com/podcover.png",
            )
        )
        expl = BeautifulSoup(features="xml").new_tag("itunes:explicit")
        expl.string = "yes"
        channel.append(expl)

        return channel
