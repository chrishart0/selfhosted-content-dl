from fastapi import FastAPI, Query, Path, Body, HTTPException
from pydantic import BaseModel
from pytube import YouTube
import vimeo_dl as vimeo

app = FastAPI()

# Set the root directory for downloads (This will be your default download path)
ROOT_DIRECTORY = "./test-downloads"

# Model for initiating a download
class DownloadRequest(BaseModel):
    url: str
    service: str
    filePath: str = None  # This will now be relative to ROOT_DIRECTORY

# Model for managing downloads
class ManageDownload(BaseModel):
    guid: str

# Model for configuration
class Config(BaseModel):
    default_path: str
    preferred_format: str


def determine_service(url: str) -> str:
    """
    Determines the video service based on the given URL.
    """
    if "youtube.com" in url or "youtu.be" in url:
        return 'youtube'
    elif "vimeo.com" in url:
        return 'vimeo'
    else:
        raise HTTPException(status_code=400, detail="Unsupported service or invalid URL")

@app.get("/video/info")
async def get_video_info(url: str = Query(..., description="The video URL")):
    """
    Retrieves essential information about a video from a specified service.
    - Determine the service based on the URL.
    - Fetch video information using appropriate service API/library.
    """

    video_info = {}

    try:
        service = determine_service(url)
        
        if service == 'youtube':
            # It's a YouTube URL
            yt_video = YouTube(url)
            video_info = {
                "title": yt_video.title,
                "description": yt_video.description,
                "views": yt_video.views,
                "author": yt_video.author,
                "published_date": yt_video.publish_date,
                "length": yt_video.length,
                "thumbnail_url": yt_video.thumbnail_url
            }
        elif service == 'vimeo':
            # It's a Vimeo URL
            vi_video = vimeo.new(url)
            video_info = {
                "title": vi_video.title,
                "description": getattr(vi_video, 'description', None),
                "views": getattr(vi_video, 'view_count', None), 
                "author": getattr(vi_video, 'author_name', None), 
                "published_date": getattr(vi_video, 'upload_date', None), 
                "length": vi_video.duration,
                "thumbnail_url": getattr(vi_video, 'thumbnail', None),
            }

        return video_info 

    except HTTPException as he:
        raise he  # re-raise the HTTPException directly
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/download")
async def initiate_download(download_request: DownloadRequest):
    """
    Initiates a video download from a specified service.
    - Validate the URL and service.
    - Generate a unique GUID for this download task.
    - If filePath is provided in download_request, it should be relative to ROOT_DIRECTORY.
    - Queue the download task and initiate a background job for downloading the video.
    - Return the GUID for checking download status.
    """

    # Construct the absolute file path by combining ROOT_DIRECTORY and download_request.filePath
    absolute_file_path = f"{ROOT_DIRECTORY}/{download_request.filePath}" if download_request.filePath else None
    pass


@app.get("/download/status/{guid}")
async def get_download_status(guid: str = Path(..., description="The unique GUID of the download task")):
    """
    Retrieves the status of a video download using a GUID.
    - Look up the status of the download task associated with the specified GUID.
    - Return the download status, progress, and file path if completed.
    """
    pass


@app.get("/downloads")
async def list_downloads():
    """
    Lists all past and current download tasks.
    - Fetch all download tasks from the queue/database.
    - Return a list of download tasks with their status and other relevant information.
    """
    pass


@app.post("/download/cancel")
async def cancel_download(manage_download: ManageDownload):
    """
    Cancels an ongoing download.
    - Look up the download task associated with the specified GUID.
    - Cancel the download task and update the status.
    """
    pass


@app.post("/download/delete")
async def delete_download(manage_download: ManageDownload):
    """
    Deletes a downloaded video file.
    - Look up the download task associated with the specified GUID.
    - Delete the video file from the file system and update the status.
    """
    pass


@app.get("/downloads/search")
async def search_downloads(query: str = Query(..., description="The search query")):
    """
    Searches through download history based on a query.
    - Search through the download tasks based on the provided query.
    - Return a list of matching download tasks.
    """
    pass


@app.post("/download/pause")
async def pause_download(manage_download: ManageDownload):
    """
    Pauses an ongoing download.
    - Look up the download task associated with the specified GUID.
    - Pause the download task and update the status.
    """
    pass


@app.post("/download/resume")
async def resume_download(manage_download: ManageDownload):
    """
    Resumes a paused download.
    - Look up the download task associated with the specified GUID.
    - Resume the download task and update the status.
    """
    pass


@app.get("/download/metadata")
async def get_metadata(manage_download: ManageDownload):
    """
    Fetches metadata of a downloaded video.
    - Look up the download task associated with the specified GUID.
    - Fetch and return the metadata of the downloaded video.
    """
    pass


@app.post("/download/metadata")
async def update_metadata(manage_download: ManageDownload):
    """
    Updates metadata of a downloaded video.
    - Look up the download task associated with the specified GUID.
    - Update the metadata of the downloaded video based on provided data.
    """
    pass


@app.post("/config")
async def update_config(config: Config):
    """
    Updates default configuration settings.
    - Update configuration settings like default download path, preferred video format, and resolution.
    """
    pass

