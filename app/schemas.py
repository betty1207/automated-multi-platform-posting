
import re

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, TypeAdapter, field_validator


URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)
HTTP_URL_ADAPTER = TypeAdapter(HttpUrl)


class PostingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="The complete message to publish, including exactly one CTA URL (maximum 200 characters).",
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty.")

        urls = URL_PATTERN.findall(value)

        if len(urls) == 0:
            raise ValueError("Message must include exactly one CTA URL.")

        if len(urls) > 1:
            raise ValueError("Message must include exactly one CTA URL, not multiple URLs.")

        # Remove common sentence-ending punctuation before validating the URL.
        url = urls[0].rstrip(".,!?;:")

        try:
            HTTP_URL_ADAPTER.validate_python(url)
        except Exception:
            raise ValueError("The CTA link must be a valid HTTP or HTTPS URL.")

        return value
