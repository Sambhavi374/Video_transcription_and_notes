import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import RequestBlocked

load_dotenv() # loads all env variables from .env file

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # sets the API key for Google Generative AI

prompt = """You are a Youtube video summarizer. You will take the transcript text and make proper detailed notes out of it.
Notes are structured in the form of bullet point, with main headings, subheadings and their respective content points.
It should also contain diagrams and images related to the topic they are where necessary.
The notes should be in a markdown format, so that they can be easily copied and pasted into a note-taking app.
The notes should also contain the time stamps of the video.
You can also give the articles related to the topics the user asks from the internet along with their source links.
Word limit for video less than 10 minutes is 750 words, for video between 10-30 mins is 1500-2000 words, for 30mis to 1 hour is 2000-2500 words, 
and for those over 1 hour is 3000-5000 words.
The transcript text is as follows:"""

##Extracting the transcript from the youtube video.
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        proxies = {
            "http": "http://40.76.69.94:8080",
            "https": "http://40.76.69.94:8080"
        }
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i['text']

        return transcript

    except RequestBlocked:
        raise Exception("Request blocked. Try using a different proxy or IP.")
    except Exception as e:
        raise e
    

##Summarizing the video transcript.
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel(model="gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text


st.title("YouTube Video Notes Generator")
st.write("This app generates detailed notes from a YouTube video")
youtube_link = st.text_input("YouTube Video URL")

if st.button("Generate Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("#### Detailed Notes")
        st.markdown(summary)
        st.download_button(
            label="Download Notes",
            data=summary,
            file_name="youtube_notes.md",
            mime="text/markdown"
        )    



