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
    description="An API for publishing messages across multiple platforms.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Automated Multi-Platform Posting System is running!"
    }


@app.post("/posting")
def create_posting(request: PostingRequest):

    # Publish to Bluesky
    bluesky_result = publish_to_bluesky(
        message=request.message,
        cta_link=str(request.cta_link)
    )

    # Publish to Telegram
    telegram_result = publish_to_telegram(
        message=request.message,
        cta_link=str(request.cta_link)
    )

    # Publish to Discord
    discord_result = publish_to_discord(
        message=request.message,
        cta_link=str(request.cta_link)
    )

    # Publish to Slack
    slack_result = publish_to_slack(
    message=request.message,
    cta_link=str(request.cta_link)
)

    # Publish to Mastodon
    mastodon_result = publish_to_mastodon(
    message=request.message,
    cta_link=str(request.cta_link)
)
    return {
        "message": "Posting process completed.",
        "results": [
            bluesky_result,
            telegram_result,
            discord_result,
            slack_result,
            mastodon_result
        ]
    }