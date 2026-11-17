import os
import httpx

from datetime import datetime, timezone


def publish_to_telegram(message: str, cta_link: str) -> dict:

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        return {
            "platform": "Telegram",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": "Telegram credentials are missing."
        }

    try:
        post_text = f"{message.strip()} {cta_link}"

        api_url = (
            f"https://api.telegram.org/bot{bot_token}/sendMessage"
        )

        response = httpx.post(
            api_url,
            json={
                "chat_id": chat_id,
                "text": post_text
            },
            timeout=30
        )

        result = response.json()

        # Check whether Telegram accepted the message.
        if response.status_code != 200 or not result.get("ok"):
            raise Exception(
                result.get(
                    "description",
                    "Telegram publishing failed."
                )
            )

        message_data = result["result"]

        message_id = message_data["message_id"]
        chat_username = message_data["chat"].get("username")

        post_url = None

        if chat_username:
            post_url = (
                f"https://t.me/{chat_username}/{message_id}"
            )

        return {
            "platform": "Telegram",
            "status": "success",
            "post_url": post_url,
            "public_accessible": bool(post_url),
            "posted_at": datetime.fromtimestamp(
                message_data["date"],
                timezone.utc
            ).isoformat(),
            "error": None
        }

    except Exception as error:

        return {
            "platform": "Telegram",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": str(error)
        }