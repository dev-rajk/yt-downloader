import streamlit as st
import subprocess
import os
from curl_cffi import requests

def fetch_video_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        # Fetch the video page to avoid bot warnings
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.url
    except requests.exceptions.RequestException as e:
        return str(e)

def download_audio(url):
    # Use yt-dlp to download the audio; it will handle naming automatically
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        url
    ]
    try:
        # Run the command
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        # Return the error message from yt-dlp
        return None, str(e)

    # Find the downloaded MP3 file
    files = [f for f in os.listdir() if f.endswith('.mp3')]
    if files:
        return files[0], "Download complete!"
    else:
        return None, "No audio files found."

def main():
    st.title("Audio Downloader")
    st.write("Enter the URL of the video you want to download audio from:")

    url = st.text_input("Video URL")

    if st.button("Download"):
        if url:
            with st.spinner("Fetching video page..."):
                real_url = fetch_video_page(url)
                if not real_url.startswith("http"):
                    st.error(f"Failed to fetch video page: {real_url}")
                    return

            with st.spinner("Downloading..."):
                audio_file, result = download_audio(real_url)
                if audio_file:
                    st.success(result)

                    # Provide a download button for the MP3 file
                    with open(audio_file, 'rb') as f:
                        audio_bytes = f.read()

                    st.download_button(
                        label="Download MP3",
                        data=audio_bytes,
                        file_name=audio_file,
                        mime='audio/mpeg'
                    )
                else:
                    st.error(result)
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
