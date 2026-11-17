
from pydantic import BaseModel, Field, HttpUrl, field_validator
import re


class PostingRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Message to publish (maximum 200 characters)"
    )

    cta_link: HttpUrl = Field(
        ...,
        description="The single call-to-action URL"
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty.")

        # Count URLs in the message.
        urls = re.findall(r"https?://\S+", value)

        if urls:
            raise ValueError(
                "Put the call-to-action URL in cta_link, not in the message."
            )

        return value
