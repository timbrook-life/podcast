from datetime import datetime

CDN_BASE_URL = "https://pod-cdn.timbrook.tech"


def populate_episode(doc, data):
    item = doc.new_tag("item")
    bare_tags = {
        "title": data["name"],
        "itunes:duration": data["duration"],
        "description": data["description"],
        "itunes:subtitle": data["description"],
        "itunes:summary": data["description"],
    }
    for t, v in bare_tags.items():
        tag = doc.new_tag(t)
        tag.string = v if v is not None else ""
        item.append(tag)

    guid = doc.new_tag("guid", isPermaLink="false")
    guid.string = data["storage_key"]
    item.append(guid)

    url = f"{CDN_BASE_URL}/{data['storage_key']}"

    item.append(doc.new_tag("enclosure", url=url, type="audio/mpeg"))

    return item


def populate_podcast(doc, channel, podcast):
    # basics
    bare_tags = {
        "title": podcast["name"],
        "description": podcast["description"],
        "language": "en-us",
        "docs": "http://www.rssboard.org/rss-specification",
        "generator": "myself",
        "lastBuildDate": datetime.now().ctime(),
    }
    for t, v in bare_tags.items():
        tag = doc.new_tag(t)
        tag.string = v
        channel.append(tag)

    # Links
    link = podcast["url"]
    lt = doc.new_tag("link")
    lt.string = link
    channel.append(lt)

    lta = doc.new_tag("atom:link", href=link, rel="self")
    channel.append(lta)

    # iTunes category and friends
    cat = doc.new_tag("itunes:category", text="Technology")
    cat.append(doc.new_tag("itunes:category", text="Podcasting"))
    channel.append(cat)

    channel.append(
        doc.new_tag(
            "itunes:image",
            href="https://timbrook-podcast.sfo2.digitaloceanspaces.com/podcover.png",
        )
    )
    expl = doc.new_tag("itunes:explicit")
    expl.string = "yes"
    channel.append(expl)

    # Episodes
    for ep in podcast["episodes"]:
        channel.append(populate_episode(doc, ep))

    return channel
