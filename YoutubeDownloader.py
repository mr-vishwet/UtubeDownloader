# YoutubeDownlaoder.py
import streamlit as st
from pytube import YouTube
import requests

def get_file_size(url: str) -> int:
    headers = requests.head(url).headers
    content_length = headers.get("Content-Length")
    if content_length is None:
        return 0
    return int(content_length)


def download_video(video_url, resolution, file_path):
    yt = YouTube(video_url)
    #stream = yt.streams.filter(res=resolution, progressive=True, file_extension='mp4').first()
    streams = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution)
    stream = streams.order_by('resolution').desc().first()
    if stream is not None:
        video_size = streams[0].filesize / (1024 * 1024)
        st.write("Video size: {video_size:.2f} MB")
        stream.download(output_path=".", filename=file_path)
    else:
        st.error("No stream available for the selected resolution.")
        


def download_audio(video_url, quality, file_name):
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True, abr=quality).first()
    stream.download(output_path=".", filename=file_name)


# Set page title
st.set_page_config(page_title='YouTube Downloader')

# Set page header
st.header('YouTube Downloader')

st.write("##### Video Download ")
# Ask user for YouTube video URL
video_url = st.text_input('Enter YouTube video URL:', key = 'video_download')
resolution = st.selectbox('Select video quality:', [
                          '1080p', '720p', '480p', '360p', '240p', '144p'])

# Define download button
if st.button('Download Video'):
    try:
        file_name = "video.mp4"
        download_video(video_url, resolution, file_name)

        # Read the downloaded file as bytes
        with open(file_name, 'rb') as f:
            video_data = f.read()
        st.download_button(
            label="Click Here to Download",
            data=video_data,
            file_name=file_name,
            mime='video/mp4'
        )
    except Exception as e:
        st.write("Error:", e)

# Create form for audio download

# Ask user for YouTube video URL
st.write("##### Only Audio Download ")
url = st.text_input('Enter YouTube video URL:', key = 'audio_download')

# Ask user for audio quality
quality_options = ['128kbps', '192kbps', '256kbps']
quality = st.selectbox('Select audio quality:', quality_options)

# Define download button
if st.button('Download Audio'):
    # Set download path to Downloads folder by default
    try:
        # download the audio to the default download directory on the remote server
        download_audio(video_url, quality, file_name)

    # offer the downloaded audio as a download button
        with open(file_name, "rb") as f:
            audio_data = f.read()
        st.download_button(
            label="Click Here to Download",
            data=audio_data,
            mime="audio/mp3",
            file_name=file_name
        )
    except Exception as e:
        st.write("Error:", e)
