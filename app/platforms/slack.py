import os
import httpx
from datetime import datetime, timezone


def publish_to_slack(message: str, cta_link: str) -> dict:
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    channel_id = os.getenv("SLACK_CHANNEL_ID")

    if not bot_token or not channel_id:
        return {
            "platform": "Slack",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": "Slack credentials are missing."
        }

    headers = {
        "Authorization": f"Bearer {bot_token}",
        "Content-Type": "application/json"
    }

    try:
        post_text = f"{message.strip()} {cta_link}"

        # Publish the message
        response = httpx.post(
            "https://slack.com/api/chat.postMessage",
            headers=headers,
            json={
                "channel": channel_id,
                "text": post_text
            },
            timeout=30
        )

        result = response.json()

        if not result.get("ok"):
            raise Exception(
                result.get("error", "Slack publishing failed.")
            )

        message_ts = result["ts"]
        posted_channel = result["channel"]

        posted_at = datetime.fromtimestamp(
            float(message_ts),
            timezone.utc
        ).isoformat()

        # Retrieve the actual message permalink
        permalink_response = httpx.get(
            "https://slack.com/api/chat.getPermalink",
            headers=headers,
            params={
                "channel": posted_channel,
                "message_ts": message_ts
            },
            timeout=30
        )

        permalink_result = permalink_response.json()

        post_url = None
        error = None

        if permalink_result.get("ok"):
            post_url = permalink_result.get("permalink")
        else:
            error = (
                "Message posted successfully, but permalink retrieval "
                f"failed: {permalink_result.get('error', 'Unknown error')}"
            )

        return {
            "platform": "Slack",
            "status": "success",
            "post_url": post_url,
            "public_accessible": False,
            "posted_at": posted_at,
            "error": error
        }

    except Exception as error:
        return {
            "platform": "Slack",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": str(error)
        }