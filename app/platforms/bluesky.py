import os
from datetime import datetime, timezone

from atproto import Client


def publish_to_bluesky(message: str, cta_link: str) -> dict:
    handle = os.getenv("BLUESKY_HANDLE")
    app_password = os.getenv("BLUESKY_APP_PASSWORD")

    if not handle or not app_password:
        return {
            "platform": "Bluesky",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": "Bluesky credentials are missing."
        }

    try:
        client = Client()

        # Step 1: Authenticate with Bluesky.
        client.login(handle, app_password)

        # Step 2: Prepare the message and CTA link.
        post_text = f"{message.strip()} {cta_link}"

        # Step 3: Publish the post.
        response = client.send_post(post_text)

        # Step 4: Extract the post identifier.
        record_key = response.uri.split("/")[-1]

        # Step 5: Construct the public post URL.
        post_url = (
            f"https://bsky.app/profile/{handle}/post/{record_key}"
        )

        return {
            "platform": "Bluesky",
            "status": "success",
            "post_url": post_url,
            "public_accessible": True,
            "posted_at": datetime.now(timezone.utc).isoformat(),
            "error": None
        }

    except Exception as error:
        return {
            "platform": "Bluesky",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": str(error)
        }