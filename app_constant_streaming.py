import streamlit as st
from google.cloud import speech
import os

import streamlit as st
from google.cloud import speech
from google.oauth2 import service_account

# This pulls the data from the 'Secrets' section you filled out in Streamlit
try:
    creds_info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(creds_info)
    client = speech.SpeechClient(credentials=credentials)
except Exception as e:
    st.error(f"Credentials not found or invalid: {e}")
    st.stop()
    
st.set_page_config(page_title="VoiceNotes", layout="centered")
# Replace with your key path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gen-lang-client-0785559721-35a88d77a6dd.json"

def transcribe_audio_file(audio_bytes):
    client = speech.SpeechClient()

    # Wrap the bytes in the RecognitionAudio object
    audio = speech.RecognitionAudio(content=audio_bytes)
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # This is important: it helps Google understand the audio quality
        sample_rate_hertz=16000, 
        language_code="nl-NL",
        # Adding these helps with the 'pausing' issue
        enable_automatic_punctuation=True,
        # Use the latest 'long' model for better pause handling
        model="latest_long", 
        use_enhanced=True,
    )

    # Use recognize instead of streaming_recognize for st.audio_input files
    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    
    return transcript if transcript else "No speech detected."

st.title("🎤 Reliable Speech-to-Text")

audio_value = st.audio_input("Record your message")

if audio_value:
    with st.spinner("Processing full audio..."):
        # We pass the bytes directly
        result_text = transcribe_audio_file(audio_value.getvalue())
        st.subheader("Final Transcription:")

        st.write(result_text)
