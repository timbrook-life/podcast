import requests, os, boto3, uuid
from flask import Response, request
from bs4 import BeautifulSoup
from datetime import datetime
from flask_api import FlaskAPI
from src.utils import require_valid_token, AsyncProccessor
from src.podcast import populate_episode, populate_podcast
from twirp.AsyncTypes_pb2 import DurationPayload

key = os.environ.get("ACCESS_KEY_ID")
secret = os.environ.get("SECRET_ACCESS_KEY")
s3 = boto3.client(
    "s3",
    aws_access_key_id=key,
    aws_secret_access_key=secret,
    region_name="sfo2",
    endpoint_url="https://sfo2.digitaloceanspaces.com",
)
app = FlaskAPI(__name__)


def get_podcasts(id):
    res = requests.get(
        "http://postgrest-api/podcasts",
        headers={"Accept": "application/vnd.pgrst.object+json"},
        params={
            "select": "*,episodes(*)",
            "id": f"eq.{id}",
            "episodes.published": "eq.true",
        },
    )

    return res.json()


@app.route("/pod.xml")
def podcasts():
    doc = BeautifulSoup(features="xml")

    rss_feed = doc.new_tag(
        "rss",
        **{
            "xmlns:atom": "http://www.w3.org/2005/Atom",
            "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
            "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
            "version": "2.0",
        },
    )

    channel = doc.new_tag("channel")
    channel = populate_podcast(doc, channel, get_podcasts(1))

    rss_feed.append(channel)
    doc.append(rss_feed)

    return Response(str(doc), mimetype="text/xml")


# TODO: modulize


@app.route("/api/upload", methods=["POST"])
@require_valid_token()
def upload():
    upload_id = str(uuid.uuid4())
    file = f"{upload_id}.mp3"
    signed_upload_url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": "timbrook-podcast", "Key": file},
        ExpiresIn="720",
    )

    token = request.cookies.get("token")

    # Pre creation episode and set file handle reference
    episode = requests.post(
        "http://postgrest-api.production.svc.cluster.local/episodes?select=id",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.pgrst.object+json",
            "Prefer": "return=representation",
        },
        data={"storage_key": file},
    ).json()

    return {"endpoint": signed_upload_url, "upload_id": upload_id, "id": episode["id"]}


@app.route("/api/configure", methods=["POST"])
@require_valid_token()
def configure():
    ep_id = request.data["id"]
    pod_id = request.data["pod"]
    token = request.cookies.get("token")

    res = requests.patch(
        f"http://postgrest-api.production.svc.cluster.local/episodes?id=eq.{ep_id}",
        headers={"Authorization": f"Bearer {token}", "Prefer": "return=representation"},
        data={"podcast": pod_id},
    ).json()
    handle = res[0]["storage_key"]

    # Trigger Postprocessor for figuring our metadata
    AsyncProccessor("calulate_duration").dispatch(
        data=DurationPayload(handle=handle, episode=ep_id), token=token
    )

    return {"status": "ok", "updates": res}
