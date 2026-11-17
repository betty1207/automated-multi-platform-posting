# Automated Multi-Platform Posting System

A Python application that receives a message and a call-to-action (CTA) link through a FastAPI endpoint and publishes the content to five platforms.

## Supported Platforms

- Bluesky
- Telegram
- Discord
- Slack
- Mastodon

## Features

- FastAPI endpoint for submitting posts.
- Message validation with a maximum length of 200 characters.
- CTA URL validation.
- Automatic publishing to five platforms.
- Individual publishing results for each platform.
- Error handling so a failure on one platform does not prevent attempts on the others.
- Post URLs, publication timestamps, and accessibility information where available.

## Technology Stack

- Python 3
- FastAPI
- HTTPX
- AT Protocol Python SDK
- Pydantic
- Pytest

## Project Structure

```text
automated-multi-platform-posting/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── platforms/
│       ├── __init__.py
│       ├── bluesky.py
│       ├── telegram.py
│       ├── discord.py
│       ├── slack.py
│       └── mastodon.py
├── tests/
│   └── test_api.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd automated-multi-platform-posting
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and configure the credentials for the five platforms.

Use `.env.example` as a reference.

Never commit your actual `.env` file or share your access tokens, passwords, or webhook URLs.

## Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload --port 4000
```

The API will be available at:

```text
http://localhost:4000
```

Interactive API documentation:

```text
http://localhost:4000/docs
```

## API Endpoint

### POST /posting

Accepts a message and one CTA link.

Example request:

```json
{
  "message": "Check out our latest project!",
  "cta_link": "https://example.com"
}
```

The application attempts to publish the content to all five configured platforms and returns an individual result for each platform.

Each result includes:

- `platform`
- `status`
- `post_url`
- `public_accessible`
- `posted_at`
- `error`

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The API tests use mocked platform publishing functions, so they do not publish real messages.

## Notes

- Each platform requires its own account and API credentials.
- Public accessibility depends on the platform's visibility settings and access requirements.
- Slack and Discord message links may require membership or access to the relevant workspace or server.
- Actual publishing requires valid credentials and the appropriate platform permissions.

## Security

- API credentials are stored in environment variables.
- `.env` is excluded from Git using `.gitignore`.
- Never publish real access tokens, passwords, or webhook URLs in the repository.