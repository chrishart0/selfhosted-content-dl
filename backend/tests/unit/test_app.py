import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

vimeo_url = "https://vimeo.com/518118016"
vimeo_video_title = "MINECRAFT RICK ROLL!"

@pytest.mark.asyncio
async def test_get_video_info():
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    response = client.get(f"/video/info?url={youtube_url}")
    assert response.status_code == 200
    assert response.json()['title'] == "Never Gonna Give You Up"

    response = client.get(f"/video/info?url={vimeo_url}")
    assert response.status_code == 200
    assert response.json()['title'] == "MINECRAFT RICK ROLL!"

    # Test an invalid URL
    invalid_url = "https://invalid.url"
    response = client.get(f"/video/info?url={invalid_url}")
    assert response.status_code == 400  # assuming your app returns a 400 status code for unsupported services

def test_initiate_youtube_download():
    # Define the URL of a video to download
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Send a request to initiate the download
    response = client.post("/download", json={"url": video_url})
    
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Parse the response JSON
    response_json = response.json()
    print(response_json['file_path'])
    
    # Check that the response JSON contains a GUID for the download task
    assert 'file_path' in response_json

def test_initiate_vimeo_download():
    
    # Send a request to initiate the download
    response = client.post("/download", json={"url": vimeo_url})
    
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Parse the response JSON
    response_json = response.json()
    print(response_json['file_path'])
    
    # Check that the response JSON contains a GUID for the download task
    assert 'file_path' in response_json
