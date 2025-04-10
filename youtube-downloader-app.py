# app.py
import streamlit as st
import yt_dlp
import os
import time
import pandas as pd

st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="🎬",
    layout="wide"
)

def get_video_info(url):
    """Extract video information including title, thumbnail, and formats"""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        st.error(f"Error extracting video info: {str(e)}")
        return None

def format_filesize(filesize):
    """Format filesize in human-readable format"""
    if not filesize:
        return "N/A"
    
    try:
        if filesize < 1024:
            return f"{filesize} B"
        elif filesize < 1024 * 1024:
            return f"{filesize/1024:.1f} KB"
        elif filesize < 1024 * 1024 * 1024:
            return f"{filesize/1024/1024:.1f} MB"
        else:
            return f"{filesize/1024/1024/1024:.2f} GB"
    except:
        return "N/A"

def download_video(url, format_id, output_path):
    """Download the video in the specified format"""
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': format_id if format_id else 'best',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return True
    except Exception as e:
        st.error(f"Download error: {str(e)}")
        return False

def show_formats_as_table(formats):
    """Display formats as a sortable table"""
    # Prepare data for the table
    data = []
    
    for f in formats:
        filesize = format_filesize(f.get('filesize'))
        
        # Extract video and audio codecs
        vcodec = f.get('vcodec', 'none')
        acodec = f.get('acodec', 'none')
        
        # Determine content type
        if vcodec != 'none' and acodec != 'none':
            content_type = "Video + Audio"
        elif vcodec != 'none':
            content_type = "Video only"
        elif acodec != 'none':
            content_type = "Audio only"
        else:
            content_type = "Unknown"
            
        # Determine quality
        resolution = f.get('resolution', 'N/A')
        fps = f.get('fps', 'N/A')
        
        # Format bitrate
        tbr = f.get('tbr')
        bitrate = f"{tbr:.0f}kbps" if tbr else "N/A"
        
        data.append({
            "Format ID": f.get('format_id', 'N/A'),
            "Extension": f.get('ext', 'N/A'),
            "Resolution": resolution,
            "FPS": fps,
            "Bitrate": bitrate,
            "Type": content_type,
            "Filesize": filesize,
        })
    
    # Create and return DataFrame
    df = pd.DataFrame(data)
    return df

def main():
    st.title("🎬 YouTube Downloader")
    st.write("Enter a YouTube URL to download videos in your preferred format")
    
    # Create tabs for different functions
    tab1, tab2 = st.tabs(["Download", "About"])
    
    with tab1:
        # Input field for YouTube URL
        url = st.text_input("Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
        
        col1, col2 = st.columns([3, 2])
        
        # Set default download directory to user's Downloads folder
        default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        output_path = col2.text_input("Download Directory", value=default_download_dir)
        
        if url:
            # Show loading spinner while fetching video info
            with st.spinner("Fetching video information..."):
                info = get_video_info(url)
            
            if info:
                # Display video information
                with col1:
                    st.subheader("Video Information")
                    
                    # Organize video details in a cleaner layout
                    video_details_col1, video_details_col2 = st.columns([1, 1])
                    
                    with video_details_col1:
                        st.markdown(f"**Title:** {info.get('title', 'N/A')}")
                        st.markdown(f"**Channel:** {info.get('uploader', 'N/A')}")
                        st.markdown(f"**Duration:** {time.strftime('%H:%M:%S', time.gmtime(info.get('duration', 0)))}")
                    
                    with video_details_col2:
                        st.markdown(f"**View Count:** {info.get('view_count', 'N/A'):,}")
                        st.markdown(f"**Upload Date:** {info.get('upload_date', 'N/A')}")
                        st.markdown(f"**Video ID:** {info.get('id', 'N/A')}")
                
                # Display thumbnail
                if 'thumbnail' in info:
                    st.image(info['thumbnail'], use_column_width=True)
                
                # Format selection
                st.subheader("Available Formats")
                formats = info.get('formats', [])
                
                if formats:
                    # Show formats in a table
                    df = show_formats_as_table(formats)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Extract format IDs for selection
                    format_options = [f"{row['Format ID']} - {row['Type']} - {row['Resolution']} - {row['Extension']} - {row['Filesize']}" 
                                     for _, row in df.iterrows()]
                    
                    # Add a "Best quality" option at the top
                    format_options.insert(0, "best - Best quality (recommended)")
                    
                    # Format selection dropdown
                    selected_format = st.selectbox("Select Format", format_options)
                    
                    # Extract the format ID from the selection
                    format_id = "best" if selected_format.startswith("best") else selected_format.split(" - ")[0]
                    
                    # Download button
                    if st.button("Download Video"):
                        with st.spinner("Downloading... This may take a while depending on file size"):
                            success = download_video(url, format_id, output_path)
                            if success:
                                st.success("✅ Download completed!")
                                st.balloons()
                else:
                    st.warning("No formats available for this video")

    with tab2:
        st.subheader("About This App")
        st.markdown("""
        This YouTube Downloader is built with Streamlit and yt-dlp, allowing you to:
        
        - Download videos from YouTube in various formats and qualities
        - See detailed information about available formats
        - Choose between video-only, audio-only, or combined formats
        
        ### How to Use
        1. Paste a YouTube URL in the input field
        2. Wait for the video information to load
        3. Select your preferred download format
        4. Click the Download button
        
        ### Disclaimer
        This tool is for educational purposes only. Please respect copyright laws and YouTube's Terms of Service. Only download videos that you have the right to download.
        """)

if __name__ == "__main__":
    main()
