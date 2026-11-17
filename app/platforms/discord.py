import os
from datetime import datetime, timezone

import httpx


def publish_to_discord(message: str) -> dict:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        return {
            "platform": "Discord",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": "Discord webhook URL is missing.",
        }

    try:
        response = httpx.post(
            webhook_url,
            params={"wait": "true"},
            json={"content": message},
            timeout=30,
        )

        response.raise_for_status()
        message_data = response.json()

        message_id = message_data["id"]
        posted_at = datetime.fromisoformat(
            message_data["timestamp"].replace("Z", "+00:00")
        )

        # Retrieve webhook details to identify the server and channel.
        webhook_response = httpx.get(
            webhook_url,
            timeout=30,
        )

        webhook_response.raise_for_status()
        webhook_data = webhook_response.json()

        guild_id = webhook_data.get("guild_id")
        channel_id = webhook_data.get("channel_id")

        posted_url = None

        if guild_id and channel_id:
            posted_url = (
                f"https://discord.com/channels/"
                f"{guild_id}/{channel_id}/{message_id}"
            )

        return {
            "platform": "Discord",
            "status": "success",
            "posted_url": posted_url,
            "public_access": False,
            "date": posted_at.date().isoformat(),
            "time": posted_at.time().isoformat(timespec="seconds"),
            "error": None,
        }

    except Exception as error:
        return {
            "platform": "Discord",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": str(error),
        }