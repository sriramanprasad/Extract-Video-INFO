import streamlit as st
from googleapiclient.discovery import build
import re

# Set your API key here
API_KEY = st.secrets["api"]



def extract_video_id(video_url):
    # Regular expression to extract the video ID from the URL
    regex = r"(?:https:\/\/(?:www\.|m\.)?youtube\.com\/watch\?v=|https:\/\/youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, video_url)
    if match:
        return match.group(1)
    else:
        return None

def get_video_info(video_url):
    try:
        video_id = extract_video_id(video_url)
        if video_id:
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
                video_embed_url = f"https://www.youtube.com/embed/{video_id}"
                return hashtags, tags, video_embed_url, None
            else:
                return None, None, None, "Failed to fetch video details. Please check the video URL."
        else:
            return None, None, None, "Invalid YouTube video URL."
    except Exception as e:
        return None, None, None, f"Failed to fetch video details: {e}"

# Streamlit app
st.title('YouTube Video Info Extractor')

video_url = st.text_input('Enter YouTube Video URL:')

if st.button('Get Video Info'):
    if video_url:
        hashtags, tags, video_embed_url, error = get_video_info(video_url)
        if error:
            st.write(error)
        else:
            st.write('Embedded Video:')
            st.write(f'<iframe width="560" height="315" src="{video_embed_url}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
            
            with st.expander("Show Hashtags"):
                st.write(", ".join(hashtags))
                
            with st.expander("Show Tags"):
                st.write(", ".join(tags))
