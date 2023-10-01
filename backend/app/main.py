from fastapi import FastAPI, Query, Path, Body, HTTPException
from pydantic import BaseModel
from pytube import YouTube
import vimeo_dl as vimeo
import os
from fastapi import BackgroundTasks

app = FastAPI()

# Set the root directory for downloads (This will be your default download path)
ROOT_DIRECTORY = "./test-downloads"

# Global dictionary to track download status. This is a simplification and not suitable for production.
DOWNLOAD_STATUS = {}

# Model for initiating a download
class DownloadRequest(BaseModel):
    url: str  # The video URL

# Model for managing downloads
class ManageDownload(BaseModel):
    guid: str

# Model for configuration
class Config(BaseModel):
    default_path: str
    preferred_format: str


###############
### Routes ####
###############

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
async def initiate_download(download_request: DownloadRequest, background_tasks: BackgroundTasks):
    """
    Initiates a video download from a specified service.
    - Validate the URL and service.
    - Generate a unique GUID for this download task.
    - Automatically determine the file path based on service name, channel, and file name.
    - Queue the download task and initiate a background job for downloading the video.
    - Return the GUID for checking download status.
    """

    try:
        # Determine the service
        service = determine_service(download_request.url)
        
        # Determine the file path based on service name, channel, and file name
        file_path = None
        full_path = None
        if service == 'youtube':
            yt_video = YouTube(download_request.url)
            channel = yt_video.author  # This assumes the author is the channel name
            title = yt_video.title
            file_path = f"{service}/{channel}/{title}.mp4"
            full_path = f"{ROOT_DIRECTORY}/{file_path}"
        elif service == 'vimeo':
            vi_video = vimeo.new(download_request.url)
            channel = getattr(vi_video, 'author_name', 'Unknown Channel')
            title = vi_video.title
            file_path = f"{service}/{channel}/{title}.mp4"
            full_path = f"{ROOT_DIRECTORY}/{file_path}"
        
        # Create download directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Define a background task for downloading the video
        def download_video():
            try:
                if service == 'youtube':
                    yt_video = YouTube(download_request.url)
                    ys = yt_video.streams.get_highest_resolution()
                    ys.download(output_path=os.path.dirname(full_path), filename=os.path.basename(file_path))
                elif service == 'vimeo':
                    vi_video = vimeo.new(download_request.url)
                    vi_best = vi_video.getbest()
                    vi_best.download(filepath=full_path, quiet=False)
                DOWNLOAD_STATUS[file_path] = {"status": "Completed", "file_path": file_path}
            except Exception as e:
                DOWNLOAD_STATUS[file_path] = {"status": f"Failed: {str(e)}"}
        
        # Add the download task to the background tasks queue
        background_tasks.add_task(download_video)
        
        # Add initial status to the DOWNLOAD_STATUS dictionary
        DOWNLOAD_STATUS[file_path] = {"status": "Downloading"}

        # For this example, we're returning the file path instead of a GUID.
        # In a real-world scenario, you might want to return a GUID and track download progress.
        return {"file_path": file_path}
    
    except HTTPException as he:
        raise he  # re-raise the HTTPException directly
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/download/status/{file_path:path}")
async def get_download_status(file_path: str = Path(..., description="The file path of the download task")):
    """
    Retrieves the status of a video download using the file path.
    - Look up the status of the download task associated with the specified file path.
    - Return the download status and file path if completed.
    """
    print("print DOWNLOAD_STATUS:", DOWNLOAD_STATUS)
    print("print file_path:", file_path)
    status_info = DOWNLOAD_STATUS.get(file_path, None)
    if status_info is None:
        raise HTTPException(status_code=404, detail=f" Download task not found")
    return status_info


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

