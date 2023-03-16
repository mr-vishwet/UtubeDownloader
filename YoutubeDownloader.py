# YoutubeDownlaoder.py
import streamlit as st
from pytube import YouTube


def download_video(video_url, resolution, file_path):
    yt = YouTube(video_url)
    stream = yt.streams.filter(res=resolution).first()
    stream.download(output_path=".", filename=file_path)


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
                          '1080p : '+'( mb)', '720p : '+'( mb)', '480p : '+'(mb)', '360p :'+'(mb)', '240 : '+'(mb)', '144p :'+'(mb)'])

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
