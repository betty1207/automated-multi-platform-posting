import os
from datetime import datetime, timezone

import httpx


def publish_to_slack(message: str) -> dict:
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    channel_id = os.getenv("SLACK_CHANNEL_ID")

    if not bot_token or not channel_id:
        return {
            "platform": "Slack",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": "Slack credentials are missing.",
        }

    headers = {
        "Authorization": f"Bearer {bot_token}",
        "Content-Type": "application/json",
    }

    try:
        # Publish the message.
        response = httpx.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            json={
                "channel": channel_id,
                "text": message,
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()

        if not data.get("ok"):
            raise Exception(data.get("error", "Slack posting failed."))

        message_timestamp = data["ts"]

        posted_at = datetime.fromtimestamp(
            float(message_timestamp),
            tz=timezone.utc,
        )

        posted_url = None
        permalink_error = None

        # Retrieve the published message's permalink.
        try:
            permalink_response = httpx.get(
                "https://slack.com/api/chat.getPermalink",
                headers={"Authorization": f"Bearer {bot_token}"},
                params={
                    "channel": channel_id,
                    "message_ts": message_timestamp,
                },
                timeout=30,
            )

            permalink_response.raise_for_status()
            permalink_data = permalink_response.json()

            if permalink_data.get("ok"):
                posted_url = permalink_data.get("permalink")
            else:
                permalink_error = permalink_data.get(
                    "error",
                    "Could not retrieve the message permalink.",
                )

        except Exception as error:
            permalink_error = str(error)

        return {
            "platform": "Slack",
            "status": "success",
            "posted_url": posted_url,
            "public_access": False,
            "date": posted_at.date().isoformat(),
            "time": posted_at.time().isoformat(timespec="seconds"),
            "error": (
                f"Message published, but permalink retrieval failed: {permalink_error}"
                if permalink_error
                else None
            ),
        }

    except Exception as error:
        return {
            "platform": "Slack",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": str(error),
        }