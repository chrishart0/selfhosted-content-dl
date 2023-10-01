import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_video_info():
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    response = client.get(f"/video/info?url={youtube_url}")
    assert response.status_code == 200
    assert response.json()['title'] == "Never Gonna Give You Up"

    vimeo_url = "https://vimeo.com/518118016"
    response = client.get(f"/video/info?url={vimeo_url}")
    assert response.status_code == 200
    assert response.json()['title'] == "MINECRAFT RICK ROLL!"

    # Test an invalid URL
    invalid_url = "https://invalid.url"
    response = client.get(f"/video/info?url={invalid_url}")
    assert response.status_code == 400  # assuming your app returns a 400 status code for unsupported services
