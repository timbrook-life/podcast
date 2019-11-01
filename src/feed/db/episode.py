from src.feed.db.session import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from bs4 import BeautifulSoup

CDN_BASE_URL = "https://pod-cdn.timbrook.tech"


class Episode(Base):
    __tablename__ = "episodes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    podcast = Column(Integer, ForeignKey("podcasts.id"))
    description = Column(String)
    url = Column(String)
    duration = Column(String)
    published = Column(Boolean)
    storage_key = Column(String)

    def generate_rss_item(self):
        item = BeautifulSoup(features="xml").new_tag("item")
        bare_tags = {
            "title": self.name,
            "itunes:duration": self.duration,
            "description": self.description,
            "itunes:subtitle": self.description,
            "itunes:summary": self.description,
        }

        for t, v in bare_tags.items():
            tag = BeautifulSoup(features="xml").new_tag(t)
            tag.string = v if v is not None else ""
            item.append(tag)

        guid = BeautifulSoup(features="xml").new_tag("guid", isPermaLink="false")
        guid.string = self.storage_key
        item.append(guid)

        url = f"{CDN_BASE_URL}/{self.storage_key}"

        item.append(
            BeautifulSoup(features="xml").new_tag(
                "enclosure", url=url, type="audio/mpeg"
            )
        )

        return item

