import os
from datetime import datetime, timezone

import httpx


def publish_to_telegram(message: str) -> dict:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        return {
            "platform": "Telegram",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": "Telegram credentials are missing.",
        }

    try:
        api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

        # Bypass problematic environment proxy settings.
        with httpx.Client(
            timeout=45,
            trust_env=False,
        ) as client:

            response = client.post(
                api_url,
                json={
                    "chat_id": chat_id,
                    "text": message,
                },
            )

            response.raise_for_status()
            data = response.json()

        if not data.get("ok"):
            raise Exception(
                data.get("description", "Telegram posting failed.")
            )

        message_data = data["result"]
        message_id = message_data["message_id"]

        chat_username = message_data.get("chat", {}).get("username")

        posted_url = None

        if chat_username:
            posted_url = f"https://t.me/{chat_username}/{message_id}"

        posted_at = datetime.fromtimestamp(
            message_data["date"],
            tz=timezone.utc,
        )

        return {
            "platform": "Telegram",
            "status": "success",
            "posted_url": posted_url,
            "public_access": bool(posted_url),
            "date": posted_at.date().isoformat(),
            "time": posted_at.time().isoformat(timespec="seconds"),
            "error": None,
        }

    except Exception as error:
        return {
            "platform": "Telegram",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": str(error),
        }