from fastapi import FastAPI
from dotenv import load_dotenv

from app.schemas import PostingRequest

from app.platforms.bluesky import publish_to_bluesky
from app.platforms.telegram import publish_to_telegram
from app.platforms.discord import publish_to_discord
from app.platforms.slack import publish_to_slack
from app.platforms.mastodon import publish_to_mastodon


load_dotenv()

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    description="An API for automatically publishing messages across multiple social media platforms.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Automated Multi-Platform Posting System is running!"
    }


def create_failed_result(platform: str, error: str) -> dict:
    """Create a consistent failure response when a platform raises an exception."""
    return {
        "platform": platform,
        "status": "failed",
        "posted_url": None,
        "public_access": False,
        "date": None,
        "time": None,
        "error": error,
    }


@app.post("/posting")
def create_posting(request: PostingRequest):
    platforms = [
        ("Bluesky", publish_to_bluesky),
        ("Telegram", publish_to_telegram),
        ("Discord", publish_to_discord),
        ("Slack", publish_to_slack),
        ("Mastodon", publish_to_mastodon),
    ]

    results = []

    for platform_name, publish_function in platforms:
        try:
            result = publish_function(message=request.message)
            results.append(result)

        except Exception as error:
            results.append(
                create_failed_result(
                    platform=platform_name,
                    error=str(error),
                )
            )

    # The overall request is successful if at least one platform publishes.
    success = any(
        result["status"] == "success"
        for result in results
    )

    return {
        "success": success,
        "results": results,
    }