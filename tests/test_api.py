from fastapi.testclient import TestClient
import app.main as main

client = TestClient(main.app)

PLATFORMS = ["Bluesky", "Telegram", "Discord", "Slack", "Mastodon"]


def successful_result(platform):
    return {
        "platform": platform,
        "status": "success",
        "posted_url": f"https://example.com/{platform.lower()}",
        "public_access": True,
        "date": "2026-11-17",
        "time": "19:00:00",
        "error": None,
    }


def test_posting_endpoint_returns_five_platform_results(monkeypatch):
    for platform, function_name in [
        ("Bluesky", "publish_to_bluesky"),
        ("Telegram", "publish_to_telegram"),
        ("Discord", "publish_to_discord"),
        ("Slack", "publish_to_slack"),
        ("Mastodon", "publish_to_mastodon"),
    ]:
        monkeypatch.setattr(
            main,
            function_name,
            lambda message, p=platform: successful_result(p),
        )

    response = client.post(
        "/posting",
        json={
            "message": "Check out our platform https://example.com"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert len(data["results"]) == 5
    assert [r["platform"] for r in data["results"]] == PLATFORMS

    for result in data["results"]:
        assert set(result.keys()) == {
            "platform",
            "status",
            "posted_url",
            "public_access",
            "date",
            "time",
            "error",
        }
        assert result["status"] == "success"


def test_message_over_200_characters_is_rejected():
    response = client.post(
        "/posting",
        json={
            "message": "A" * 190 + " https://example.com"
        },
    )

    assert response.status_code == 422


def test_message_without_url_is_rejected():
    response = client.post(
        "/posting",
        json={"message": "Check out our platform"},
    )

    assert response.status_code == 422


def test_message_with_multiple_urls_is_rejected():
    response = client.post(
        "/posting",
        json={
            "message": "Visit https://example.com and https://google.com"
        },
    )

    assert response.status_code == 422


def test_invalid_url_is_rejected():
    response = client.post(
        "/posting",
        json={"message": "Visit https://"},
    )

    assert response.status_code == 422


def test_empty_message_is_rejected():
    response = client.post(
        "/posting",
        json={"message": "   "},
    )

    assert response.status_code == 422


def test_separate_cta_link_field_is_rejected():
    response = client.post(
        "/posting",
        json={
            "message": "Check out our platform https://example.com",
            "cta_link": "https://example.com",
        },
    )

    assert response.status_code == 422


def test_one_platform_failure_does_not_stop_others(monkeypatch):
    called_platforms = []

    def successful(platform):
        def publish(message):
            called_platforms.append(platform)
            return successful_result(platform)

        return publish

    def failing_bluesky(message):
        called_platforms.append("Bluesky")
        return {
            "platform": "Bluesky",
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": "Test failure",
        }

    monkeypatch.setattr(main, "publish_to_bluesky", failing_bluesky)
    monkeypatch.setattr(main, "publish_to_telegram", successful("Telegram"))
    monkeypatch.setattr(main, "publish_to_discord", successful("Discord"))
    monkeypatch.setattr(main, "publish_to_slack", successful("Slack"))
    monkeypatch.setattr(main, "publish_to_mastodon", successful("Mastodon"))

    response = client.post(
        "/posting",
        json={
            "message": "Testing failure handling https://example.com"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert len(data["results"]) == 5
    assert data["results"][0]["status"] == "failed"
    assert all(
        result["status"] == "success"
        for result in data["results"][1:]
    )
    assert called_platforms == PLATFORMS


def test_all_platforms_failing_returns_false(monkeypatch):
    def failing(platform):
        return lambda message: {
            "platform": platform,
            "status": "failed",
            "posted_url": None,
            "public_access": False,
            "date": None,
            "time": None,
            "error": "Test failure",
        }

    for platform, function_name in zip(
        PLATFORMS,
        [
            "publish_to_bluesky",
            "publish_to_telegram",
            "publish_to_discord",
            "publish_to_slack",
            "publish_to_mastodon",
        ],
    ):
        monkeypatch.setattr(
            main,
            function_name,
            failing(platform),
        )

    response = client.post(
        "/posting",
        json={
            "message": "Testing failures https://example.com"
        },
    )

    assert response.status_code == 200
    assert response.json()["success"] is False