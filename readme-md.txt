# YouTube Downloader - Streamlit GUI

A streamlined GUI application built with Streamlit for downloading YouTube videos in various formats using yt-dlp.

## Features

- Clean and intuitive user interface
- View detailed video information (title, channel, duration, etc.)
- Display video thumbnail
- Browse all available download formats with detailed information
- Select formats with different resolutions, filesize, and content types
- Choose audio-only, video-only, or combined formats
- Download progress tracking

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/youtube-downloader-streamlit.git
cd youtube-downloader-streamlit
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```
streamlit run app.py
```

2. The app will open in your web browser at `http://localhost:8501`

3. Enter a YouTube URL in the input field

4. Select your preferred format from the available options

5. Click "Download" to save the video to your specified directory

## Screenshots

![App Screenshot](screenshot.png)

## Dependencies

- Python 3.7+
- Streamlit
- yt-dlp
- pandas

## Disclaimer

This application is for educational purposes only. Please respect copyright laws and YouTube's Terms of Service. Only download videos that you have permission to download.

## License

MIT
