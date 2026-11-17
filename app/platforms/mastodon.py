import os
import httpx
from datetime import datetime, timezone


def publish_to_mastodon(message: str, cta_link: str) -> dict:
    access_token = os.getenv("MASTODON_ACCESS_TOKEN")
    base_url = os.getenv(
        "MASTODON_API_BASE_URL",
        "https://mastodon.social"
    ).rstrip("/")

    if not access_token:
        return {
            "platform": "Mastodon",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": "Mastodon access token is missing."
        }

    try:
        post_text = f"{message.strip()} {cta_link}"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = httpx.post(
            f"{base_url}/api/v1/statuses",
            headers=headers,
            data={
                "status": post_text,
                "visibility": "public"
            },
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        return {
            "platform": "Mastodon",
            "status": "success",
            "post_url": result.get("url"),
            "public_accessible": (
                result.get("visibility") == "public"
                and bool(result.get("url"))
            ),
            "posted_at": result.get(
                "created_at",
                datetime.now(timezone.utc).isoformat()
            ),
            "error": None
        }

    except Exception as error:
        return {
            "platform": "Mastodon",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": str(error)
        }