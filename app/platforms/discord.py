
import os
import httpx
from datetime import datetime, timezone


def publish_to_discord(message: str, cta_link: str) -> dict:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        return {
            "platform": "Discord",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": "Discord webhook URL is missing."
        }

    try:
        post_text = f"{message.strip()} {cta_link}"

        response = httpx.post(
            webhook_url,
            params={"wait": "true"},
            json={"content": post_text},
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(
                f"Discord API error: {response.status_code} - "
                f"{response.text}"
            )

        message_data = response.json()

        # Retrieve webhook details to obtain the server ID.
        webhook_response = httpx.get(
            webhook_url,
            timeout=30
        )
        webhook_response.raise_for_status()
        webhook_data = webhook_response.json()

        message_id = message_data["id"]
        channel_id = message_data.get("channel_id") or webhook_data.get("channel_id")
        guild_id = webhook_data.get("guild_id")

        post_url = None

        if guild_id and channel_id:
            post_url = (
                f"https://discord.com/channels/"
                f"{guild_id}/{channel_id}/{message_id}"
            )

        return {
            "platform": "Discord",
            "status": "success",
            "post_url": post_url,
            "public_accessible": False,
            "posted_at": message_data.get(
                "timestamp",
                datetime.now(timezone.utc).isoformat()
            ),
            "error": None
        }

    except Exception as error:
        return {
            "platform": "Discord",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": str(error)
        }
