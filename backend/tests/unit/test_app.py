import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

vimeo_url = "https://vimeo.com/518118016"
vimeo_video_title = "MINECRAFT RICK ROLL!"

#ToDo: Manage this better somehow
ROOT_DIRECTORY = "./test-downloads"

# Define the URL of a video to download
youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

@pytest.mark.asyncio
async def test_get_video_info():
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
    
    # Send a request to initiate the download
    response = client.post("/download", json={"url": youtube_url})
    
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

def test_get_download_status():

    # Define the URL of a video to download
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Send a request to initiate the download
    download_response = client.post("/download", json={"url": youtube_url})
    
    # Check that the download response status code is 200 (OK)
    assert download_response.status_code == 200
    
    # Parse the download response JSON to get the file path
    download_response_json = download_response.json()
    file_path = download_response_json['file_path']
    
    # Replace the root directory and backslashes in the file path to match the URL-encoded path
    encoded_file_path = file_path.replace("\\", "/")
    print("encoded_file_path:", encoded_file_path)
    
    # Send a request to get the download status
    status_response = client.get(f"/download/status/{encoded_file_path}")  # Fixed line
    print("status_response:", status_response)
    
    # Parse the status response JSON
    status_response_json = status_response.json()
    print("status_response_json:", status_response_json)
    
    # Check that the status response status code is 200 (OK)
    assert status_response.status_code == 200

    # Check that the status response JSON contains a status for the download task
    assert 'status' in status_response_json
    
    # Optional: Check that the status is "Downloading" or "Completed"
    assert status_response_json['status'] in ["Downloading", "Completed"]
