import os
from datetime import datetime

import httpx


def publish_to_mastodon(message: str) -> dict:
    access_token = os.getenv("MASTODON_ACCESS_TOKEN")
    base_url = os.getenv(
        "MASTODON_API_BASE_URL",
        "https://mastodon.social",
    ).rstrip("/")

    if not access_token:
        return {
            "platform": "Mastodon",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": "Mastodon access token is missing.",
        }

    try:
        response = httpx.post(
            f"{base_url}/api/v1/statuses",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            data={
                "status": message,
                "visibility": "public",
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

        posted_url = data.get("url")
        visibility = data.get("visibility")

        posted_at = datetime.fromisoformat(
            data["created_at"].replace("Z", "+00:00")
        )

        return {
            "platform": "Mastodon",
            "status": "success",
            "posted_url": posted_url,
            "public_access": (
                visibility == "public" and bool(posted_url)
            ),
            "date": posted_at.date().isoformat(),
            "time": posted_at.time().isoformat(timespec="seconds"),
            "error": None,
        }

    except Exception as error:
        return {
            "platform": "Mastodon",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": str(error),
        }