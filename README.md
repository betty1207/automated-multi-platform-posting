# Automated Multi-Platform Posting System

A Python-based REST API that automatically publishes a single message to five social media platforms: Bluesky, Telegram, Discord, Slack, and Mastodon.

The system uses FastAPI to receive and validate messages, then publishes them independently across the supported platforms.

## Features

- Publish messages to five social media platforms through one API endpoint.
- Validate messages before publishing.
- Enforce a maximum message length of 200 characters.
- Require exactly one valid HTTP or HTTPS URL inside the message.
- Handle platform failures independently.
- Return individual publishing results for each platform.
- Include posting URLs, public accessibility, dates, times, and error details.
- Keep API credentials in environment variables.

## Supported Platforms

1. Bluesky
2. Telegram
3. Discord
4. Slack
5. Mastodon

## Technology Stack

- Python 3
- FastAPI
- Uvicorn
- Pydantic
- HTTPX
- AT Protocol Python SDK
- Pytest
- Python Dotenv

## Project Structure

```text
automated-multi-platform-posting/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   │
│   └── platforms/
│       ├── __init__.py
│       ├── bluesky.py
│       ├── telegram.py
│       ├── discord.py
│       ├── slack.py
│       └── mastodon.py
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/betty1207/automated-multi-platform-posting.git
```

### 2. Navigate to the project directory

```bash
cd automated-multi-platform-posting
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root directory using `.env.example` as a reference.

Configure the following environment variables:

```env
BLUESKY_HANDLE=
BLUESKY_APP_PASSWORD=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

DISCORD_WEBHOOK_URL=

SLACK_BOT_TOKEN=
SLACK_CHANNEL_ID=

MASTODON_ACCESS_TOKEN=
MASTODON_API_BASE_URL=https://mastodon.social
```

Add the appropriate credentials for each platform.

**Security:** Never commit your `.env` file or expose API tokens and passwords publicly.

## Running the Application

Start the FastAPI server using:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

The application will be available at:

```text
http://localhost:4000
```

Interactive API documentation:

```text
http://localhost:4000/docs
```

## API Endpoint

### POST `/posting`

Publishes a message to all five supported platforms.

**Request URL:**

```text
http://localhost:4000/posting
```

**Request Body:**

```json
{
  "message": "Check out our latest business platform and grow your online visibility. https://example.com"
}
```

### Validation Rules

- The request must contain a `message` field.
- The message cannot be empty.
- The complete message cannot exceed 200 characters.
- Exactly one valid HTTP or HTTPS URL must be included inside the message.
- Additional request fields are not accepted.

### Example Response

```json
{
  "success": true,
  "results": [
    {
      "platform": "Bluesky",
      "status": "success",
      "posted_url": "https://bsky.app/profile/example/post/123",
      "public_access": true,
      "date": "2026-11-17",
      "time": "19:00:00",
      "error": null
    },
    {
      "platform": "Telegram",
      "status": "success",
      "posted_url": "https://t.me/example/123",
      "public_access": true,
      "date": "2026-11-17",
      "time": "19:00:00",
      "error": null
    },
    {
      "platform": "Discord",
      "status": "success",
      "posted_url": "https://discord.com/channels/example",
      "public_access": false,
      "date": "2026-11-17",
      "time": "19:00:00",
      "error": null
    },
    {
      "platform": "Slack",
      "status": "success",
      "posted_url": "https://example.slack.com/archives/example",
      "public_access": false,
      "date": "2026-11-17",
      "time": "19:00:00",
      "error": null
    },
    {
      "platform": "Mastodon",
      "status": "success",
      "posted_url": "https://mastodon.social/@example/123",
      "public_access": true,
      "date": "2026-11-17",
      "time": "19:00:00",
      "error": null
    }
  ]
}
```

*The response above is an illustrative example, not a record of an actual API execution.*

### Response Fields

| Field | Description |
|---|---|
| `success` | Indicates whether at least one platform published successfully. |
| `platform` | Name of the social media platform. |
| `status` | Publishing status: `success` or `failed`. |
| `posted_url` | URL of the published message, when available. |
| `public_access` | Indicates whether the post is publicly accessible. |
| `date` | Date of publication in UTC. |
| `time` | Time of publication in UTC. |
| `error` | Error description, or `null` when there is no error. |

Each platform is processed independently. A failure on one platform does not prevent publishing attempts on the remaining platforms.

## Running Tests

Run the automated tests using:

```bash
python -m pytest -v
```

The tests cover:

- Successful requests and platform results.
- Message length validation.
- Missing URLs.
- Multiple URLs.
- Invalid URLs.
- Empty messages.
- Rejection of additional request fields.
- Independent platform failure handling.
- Overall publishing success status.

## Security

- Platform credentials are loaded through environment variables.
- The `.env` file is excluded from version control.
- Never publish private API credentials in the repository.

## Author

Betelhem Tsega

GitHub: https://github.com/betty1207