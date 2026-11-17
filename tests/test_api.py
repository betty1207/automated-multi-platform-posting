
from fastapi.testclient import TestClient

import app.main as main


client = TestClient(main.app)


def successful_result(platform):
    return {
        "platform": platform,
        "status": "success",
        "post_url": f"https://example.com/{platform.lower()}",
        "public_accessible": True,
        "posted_at": "2026-11-17T19:00:00+00:00",
        "error": None
    }


def test_posting_endpoint_returns_five_platform_results(monkeypatch):
    platforms = [
        "Bluesky",
        "Telegram",
        "Discord",
        "Slack",
        "Mastodon"
    ]

    monkeypatch.setattr(
        main,
        "publish_to_bluesky",
        lambda **kwargs: successful_result("Bluesky")
    )
    monkeypatch.setattr(
        main,
        "publish_to_telegram",
        lambda **kwargs: successful_result("Telegram")
    )
    monkeypatch.setattr(
        main,
        "publish_to_discord",
        lambda **kwargs: successful_result("Discord")
    )
    monkeypatch.setattr(
        main,
        "publish_to_slack",
        lambda **kwargs: successful_result("Slack")
    )
    monkeypatch.setattr(
        main,
        "publish_to_mastodon",
        lambda **kwargs: successful_result("Mastodon")
    )

    response = client.post(
        "/posting",
        json={
            "message": "Testing my posting system",
            "cta_link": "https://example.com"
        }
    )

    assert response.status_code == 200

    results = response.json()["results"]

    assert len(results) == 5
    assert [result["platform"] for result in results] == platforms
    assert all(result["status"] == "success" for result in results)


def test_message_over_200_characters_is_rejected():
    response = client.post(
        "/posting",
        json={
            "message": "A" * 201,
            "cta_link": "https://example.com"
        }
    )

    assert response.status_code == 422


def test_invalid_cta_link_is_rejected():
    response = client.post(
        "/posting",
        json={
            "message": "Testing invalid link",
            "cta_link": "not-a-valid-url"
        }
    )

    assert response.status_code == 422


def test_empty_message_is_rejected():
    response = client.post(
        "/posting",
        json={
            "message": "   ",
            "cta_link": "https://example.com"
        }
    )

    assert response.status_code == 422


def test_one_platform_failure_does_not_stop_others(monkeypatch):
    called_platforms = []

    def successful(platform):
        def publish(**kwargs):
            called_platforms.append(platform)
            return successful_result(platform)

        return publish

    def failing_bluesky(**kwargs):
        called_platforms.append("Bluesky")

        return {
            "platform": "Bluesky",
            "status": "failed",
            "post_url": None,
            "public_accessible": False,
            "posted_at": None,
            "error": "Test failure"
        }

    monkeypatch.setattr(
        main,
        "publish_to_bluesky",
        failing_bluesky
    )
    monkeypatch.setattr(
        main,
        "publish_to_telegram",
        successful("Telegram")
    )
    monkeypatch.setattr(
        main,
        "publish_to_discord",
        successful("Discord")
    )
    monkeypatch.setattr(
        main,
        "publish_to_slack",
        successful("Slack")
    )
    monkeypatch.setattr(
        main,
        "publish_to_mastodon",
        successful("Mastodon")
    )

    response = client.post(
        "/posting",
        json={
            "message": "Testing platform failure handling",
            "cta_link": "https://example.com"
        }
    )

    assert response.status_code == 200

    results = response.json()["results"]

    assert len(results) == 5
    assert results[0]["status"] == "failed"

    assert called_platforms == [
        "Bluesky",
        "Telegram",
        "Discord",
        "Slack",
        "Mastodon"
    ]
