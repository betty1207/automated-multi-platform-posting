import os
from datetime import datetime, timezone

from atproto import Client


def publish_to_bluesky(message: str) -> dict:
    handle = os.getenv("BLUESKY_HANDLE")
    app_password = os.getenv("BLUESKY_APP_PASSWORD")

    if not handle or not app_password:
        return {
            "platform": "Bluesky",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": "Bluesky credentials are missing.",
        }

    try:
        client = Client()
        client.login(handle, app_password)

        # Publish the exact message supplied to the API.
        response = client.send_post(message)

        record_key = response.uri.split("/")[-1]
        posted_url = (
            f"https://bsky.app/profile/{handle}/post/{record_key}"
        )

        posted_at = datetime.now(timezone.utc)

        return {
            "platform": "Bluesky",
            "status": "success",
            "posted_url": posted_url,
            "public_access": True,
            "date": posted_at.date().isoformat(),
            "time": posted_at.time().isoformat(timespec="seconds"),
            "error": None,
        }

    except Exception as error:
        return {
            "platform": "Bluesky",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": str(error),
        }