import httpx
import pytest
import os

# Define the base URL of your FastAPI application
BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_get_video_info():
    async with httpx.AsyncClient() as client:
        # Test with a valid YouTube URL
        youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        response = await client.get(f"{BASE_URL}/video/info?url={youtube_url}")
        assert response.status_code == 200
        assert response.json()['title'] == "Never Gonna Give You Up"

        # Test with a valid Vimeo URL
        vimeo_url = "https://vimeo.com/518118016"
        response = await client.get(f"{BASE_URL}/video/info?url={vimeo_url}")
        assert response.status_code == 200
        assert response.json()['title'] == "MINECRAFT RICK ROLL!"

        # Test with an invalid URL
        invalid_url = "https://invalid.url"
        response = await client.get(f"{BASE_URL}/video/info?url={invalid_url}")
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_initiate_download():
    async with httpx.AsyncClient() as client:
        # Define the URL of a video to download
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        # Send a request to initiate the download
        response = await client.post(f"{BASE_URL}/download", json={"url": video_url})
        
        # Check that the response status code is 200 (OK)
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        
        # Parse the response JSON
        response_json = response.json()
        
        # Construct the expected file path
        expected_file_path = f"./test-downloads/youtube/Rick Astley/Never Gonna Give You Up.mp4"
        print("response_json:", response_json)

        # Check that the response JSON contains the correct file path
        assert response_json['file_path'] == expected_file_path, f"Expected '{expected_file_path}' but got '{response_json['file_path']}'"
