# Video Downloader API
[![Backend Build and Test](https://github.com/chrishart0/selfhosted-content-dl/actions/workflows/python-api.yml/badge.svg)](https://github.com/chrishart0/selfhosted-content-dl/actions/workflows/python-api.yml)

A FastAPI based application to download videos from YouTube and potentially other platforms in the future.

## Setup

### Install Dependencies
1. Clone the repository to your local machine.

```bash
git clone https://github.com/your-username/video-downloader-api.git
cd video-downloader-api
```

2. Create a virtual environment.
```
python3 -m venv .venv
```

3. Activate the virtual environment.
On macOS and Linux:
```
source .venv/bin/activate
```

On Windows
```
.venv\Scripts\activate
```

4. Install the required dependencies.
```
pip install -r requirements.txt
```

### Configuration

Update the ROOT_DIRECTORY variable in main.py to your desired download directory.

```
# Set the root directory for downloads
ROOT_DIRECTORY = "/path/to/download/directory"
```


## Usage

Start the App
```
# Ensure you are in the backend dir
uvicorn app.main:app --reload
```

Once the FastAPI application is running, you can access the API documentation at http://localhost:8000/docs. This interactive documentation allows you to try out the API endpoints, view their descriptions, and see the expected input and output formats.

The primary endpoint for initiating a download is POST /download, where you provide the video URL and the service (e.g., youtube). You can optionally specify a relative file path under ROOT_DIRECTORY for saving the downloaded video.

After initiating a download, you can use the returned GUID to check the download status, pause, resume, cancel, or delete the download, among other operations.

## Contributing
I would love some help. 


### Running the Tests
The project contains unit tests to ensure everything is working as expected.

Ensure you are in the `backend` directory and your virtual environment is activated.

#### Run the unit tests:
```
# Ensure you are in the backend dir first
pytest --cov=app --cov-fail-under=80

```

#### Run the Integration tests:
First, ensure the API is up
```
# Ensure you are in the backend dir first
pytest backend/tests/integration/

```

## License
This project is licensed under the MIT License. See the LICENSE file for details. Fell free to copy code, take as you see fit. 