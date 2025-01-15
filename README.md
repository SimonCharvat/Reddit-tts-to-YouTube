# Reddit to YouTube Bot

This Python script automates the process of downloading posts from a subreddit, converting them to speech and video, and uploading them to YouTube. It features a simple graphical user interface (GUI) built using Tkinter.

## Features

- Connects to Reddit via API to fetch posts from a specified subreddit.
- Converts the posts into speech using text-to-speech (TTS) functionality.
- Combines the speech and text into a video.
- Uploads the generated video to YouTube via API.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

   **Note:** The library `apiclient` might require the following dependency to be installed manually:
   ```bash
   pip install --upgrade google-api-python-client
   ```

## Setup

Before running the script, you need to set up the following credential files.
You can use `reddit_credentials-template.json` and `youtube_credentials-template.json` as templates, but don't forget to rename the files.

1. **YouTube API credentials**:
   - Create a file named `youtube_credentials.json`.
   - Fill it with your YouTube API credentials. Example:
     ```json
     {
         "web": {
           "client_id": "111111111-222aaa222aaa222aaa.apps.googleusercontent.com",
           "client_secret": "2222aaaa2222aaaa2222aaaa",
           "redirect_uris": [],
           "auth_uri": "https://accounts.google.com/o/oauth2/auth",
           "token_uri": "https://accounts.google.com/o/oauth2/token"
         }
     }
     ```

2. **Reddit API credentials**:
   - Create a file named `reddit_credentials.json`.
   - Fill it with your Reddit API credentials. Example:
     ```python
     creds = {
         "public": "111AAA111AAA",
         "secret": "111AAA-111AAA"
     }

     data = {
         "grant_type": "password",
         "username": "your_reddit_username",
         "password": "your_reddit_password"
     }
     ```

These files are ignored by Git to prevent accidental exposure of credentials.

## Run

To start the app, run `UI.py` which simple launches Tkinter UI.


## Setup avaliable subreddits
To add more subreddits or configure the number of posts per video, go to the following file `texts\0_subreddit_list.csv`.

## Notes

- Ensure your Reddit and YouTube API credentials are valid and have the necessary permissions.
- Do not commit your `youtube_credentials.json` or `reddit_credentials.py` files to Git for security reasons.
