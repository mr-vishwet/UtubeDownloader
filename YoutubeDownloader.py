# YoutubeDownlaoder.py
import streamlit as st
from pytube import YouTube
import requests
from moviepy.editor import VideoFileClip, AudioFileClip

def download_video(url, resolution, file_path):
    yt = YouTube(url)
    #st.image(yt.thumbnail_url)
    st.write(" Title : "+yt.title)
    streams = yt.streams.filter(progressive=True, file_extension='mp4', res=resolution)
    st.write(streams)
    if streams:
        stream = streams.order_by('resolution').desc().first()
        st.write(stream)
        if stream is not None:
            video_size = streams[0].filesize / (1024 * 1024)
            st.write(f"Video size: {video_size:.2f} MB")
            stream.download(output_path=".", filename=file_path)
        else:
            st.write("Critical download")
            streams = yt.streams.filter(type="video")
            st.write(streams)
            diffs = [abs(int(s.resolution[:-1]) - int(resolution[:-1])) for s in streams]
            closest_stream = streams[diffs.index(min(diffs))]
            audio_file = AudioFileClip(url)
            closest_stream = closest_stream.set_audio(audio_file)
            video_size = closest_stream.filesize / (1024 * 1024)
            st.write(f"Video size: {video_size:.2f} MB")
            #closest_stream.write_videofile(".")
            closest_stream.download(output_path=".", filename=file_path)
        return yt.title
    

def convert_int(s):
    return int(''.join(filter(str.isdigit, s)))

def download_audio(url, quality, file_path):
    yt = YouTube(url)
    st.image(yt.thumbnail_url)
    st.write("Title: " + yt.title)
    streams = yt.streams.filter(only_audio=True, abr=quality)
    if streams:
        stream = streams.first()
        audio_size = stream.filesize / (1024 * 1024)
        st.write(f"Audio size: {audio_size:.2f} MB")
        stream.download(output_path=".", filename=file_path)
    else:
        streams = yt.streams.filter(type="audio")
        diffs = [abs( convert_int(s.abr) - convert_int(quality) ) for s in streams]
        closest_stream = streams[diffs.index(min(diffs))]
        audio_size = closest_stream.filesize / (1024 * 1024)
        st.write(f"Audio size: {audio_size:.2f} MB")
        closest_stream.download(output_path=".", filename=file_name)
    return yt.title


# Set page title
st.set_page_config(page_title='YouTube Downloader')

# Set page header
st.header('YouTube Downloader')

st.write("##### Video Download ")
# Ask user for YouTube video URL
url = st.text_input("Enter YouTube video URL:")
resolution = st.selectbox('Select video quality:', [
                          '1080p', '720p', '480p', '360p', '240p', '144p'])

# Define download button
if st.button('Download Video'):
    try:
        file_name = "video.mp4"
        video_name = download_video(url, resolution, file_name)

        # Read the downloaded file as bytes
        with open(file_name, 'rb') as f:
            video_data = f.read()
        st.download_button(
            label="Click Here to Download",
            data=video_data,
            file_name=video_name+".mp4",
            mime='video/mp4'
        )
    except Exception as e:
        st.write("Error:", e)

# Create form for audio download

# Ask user for YouTube video URL
st.write("##### Only Audio Download ")

# Ask user for audio quality
quality_options = ['128kbps', '192kbps', '256kbps']
quality = st.selectbox('Select audio quality:', quality_options)

# Define download button
if st.button('Download Audio'):
    # Set download path to Downloads folder by default
    try:
        # download the audio to the default download directory on the remote server
        file_name ="audio.mp3"
        audio_name = download_audio(url, quality, file_name)

    # offer the downloaded audio as a download button
        with open(file_name, "rb") as f:
            audio_data = f.read()
        st.download_button(
            label="Click Here to Download",
            data=audio_data,
            mime="audio/mp3",
            file_name=audio_name+".mp3"
        )
    except Exception as e:
        st.write("Error:", e)
        

