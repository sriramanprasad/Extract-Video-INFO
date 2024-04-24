import streamlit as st
from googleapiclient.discovery import build

# Set your API key here
API_KEY = "API KEY HERE"

def get_video_info(video_url):
    try:
        video_id = video_url.split("v=")[1]
        youtube = build("youtube", "v3", developerKey=API_KEY)
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        if response['items']:
            snippet = response['items'][0]['snippet']
            hashtags = [word[1:] for word in snippet['description'].split() if word.startswith('#')]
            tags = snippet.get('tags', [])
            return hashtags, tags, None
        else:
            return None, None, "Failed to fetch video details. Please check the video URL."
    except Exception as e:
        return None, None, f"Failed to fetch video details: {e}"

# Streamlit app
st.title('YouTube Video Info Extractor')

video_url = st.text_input('Enter YouTube Video URL:')

if st.button('Get Video Info'):
    if video_url:
        hashtags, tags, error = get_video_info(video_url)
        if error:
            st.write(error)
        else:
            st.write(f'Hashtags: {", ".join(hashtags)}')
            st.write(f'Tags: {", ".join(tags)}')
