import streamlit as st
import subprocess
import os

def download_audio(url):
    # Use yt-dlp to download the audio; it will handle naming automatically
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "URL",
        url
    ]
    try:
        # Run the command
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        # Return the error message from yt-dlp
        return str(e)
    return "Download complete!"

def main():
    st.title("Audio Downloader")
    st.write("Enter the URL of the video you want to download audio from:")

    url = st.text_input("Video URL")

    if st.button("Download"):
        if url:
            with st.spinner("Downloading..."):
                result = download_audio(url)
                if result == "Download complete!":
                    # List the downloaded files in the current directory
                    files = [f for f in os.listdir() if f.endswith('.mp3')]
                    if files:
                        st.success(result)
                        st.markdown("### Downloaded Files:")
                        for file in files:
                            st.markdown(f"[{file}](./{file})")
                    else:
                        st.error("No audio files found.")
                else:
                    st.error(result)
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main()
