import streamlit as st
from google.oauth2 import service_account
from google.cloud import speech
import json

st.set_page_config(page_title="Gemini Speech-to-Text", page_icon="🎙️")

st.title("🎙️ Gemini Speech-to-Text")

def info_box():
    with st.expander("🛠️ Connection Status & Debug Info"):
        if "gcp_service_account" in st.secrets:
            st.success("Secrets found in Streamlit Cloud!")
            # Show keys (but hide the sensitive private_key)
            safe_secrets = dict(st.secrets["gcp_service_account"])
            if "private_key" in safe_secrets:
                safe_secrets["private_key"] = "•••••••••• (Hidden for Security)"
            st.json(safe_secrets)
        else:
            st.error("Secrets not detected. Check your Streamlit Cloud 'Secrets' settings.")

def get_speech_client():
    """Initializes the Google Speech Client using Streamlit Secrets."""
    try:
        # 1. Load the secrets dictionary
        creds_info = dict(st.secrets["gcp_service_account"])
        
        # 2. Fix potential newline issues in the private key
        # This handles both the triple-quote format and the \n format
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
            
        # 3. Create credentials
        credentials = service_account.Credentials.from_service_account_info(creds_info)
        
        # 4. Return the client
        return speech.SpeechClient(credentials=credentials)
    except Exception as e:
        st.error(f"Failed to create Google Cloud client: {e}")
        return None

# Sidebar / Debug info
info_box()

# Main App Logic
client = get_speech_client()

if client:
    st.write("### Upload an Audio File")
    uploaded_file = st.file_uploader("Choose a file (wav, mp3, flac)", type=["wav", "mp3", "flac"])

    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        
        if st.button("Transcribe Audio"):
            with st.spinner("Processing with Google Speech-to-Text..."):
                try:
                    content = uploaded_file.read()
                    audio = speech.RecognitionAudio(content=content)
                    
                    # Basic configuration - you can adjust based on your language/needs
                    config = speech.RecognitionConfig(
                        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                        sample_rate_hertz=16000,
                        language_code="en-US",
                    )

                    response = client.recognize(config=config, audio=audio)

                    if not response.results:
                        st.warning("No speech detected in the audio file.")
                    
                    for result in response.results:
                        st.info(f"**Transcription:** {result.alternatives[0].transcript}")
                        st.write(f"*Confidence: {result.alternatives[0].confidence:.2%}*")
                
                except Exception as e:
                    st.error(f"Transcription Error: {e}")
else:
    st.warning("Waiting for valid credentials to connect...")
    

# import streamlit as st
# from google.cloud import speech
# import os

# import streamlit as st
# from google.cloud import speech
# from google.oauth2 import service_account

# # This pulls the data from the 'Secrets' section you filled out in Streamlit
# try:
#     creds_info = st.secrets["gcp_service_account"]
#     credentials = service_account.Credentials.from_service_account_info(creds_info)
#     client = speech.SpeechClient(credentials=credentials)
# except Exception as e:
#     st.error(f"Credentials not found or invalid: {e}")
#     st.stop()
    
# st.set_page_config(page_title="VoiceNotes", layout="centered")
# # Replace with your key path
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gen-lang-client-0785559721-35a88d77a6dd.json"

# def transcribe_audio_file(audio_bytes):
#     client = speech.SpeechClient()

#     # Wrap the bytes in the RecognitionAudio object
#     audio = speech.RecognitionAudio(content=audio_bytes)
    
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         # This is important: it helps Google understand the audio quality
#         sample_rate_hertz=16000, 
#         language_code="nl-NL",
#         # Adding these helps with the 'pausing' issue
#         enable_automatic_punctuation=True,
#         # Use the latest 'long' model for better pause handling
#         model="latest_long", 
#         use_enhanced=True,
#     )

#     # Use recognize instead of streaming_recognize for st.audio_input files
#     response = client.recognize(config=config, audio=audio)

#     transcript = ""
#     for result in response.results:
#         transcript += result.alternatives[0].transcript + " "
    
#     return transcript if transcript else "No speech detected."

# st.title("🎤 Reliable Speech-to-Text")

# audio_value = st.audio_input("Record your message")

# if audio_value:
#     with st.spinner("Processing full audio..."):
#         # We pass the bytes directly
#         result_text = transcribe_audio_file(audio_value.getvalue())
#         st.subheader("Final Transcription:")

#         st.write(result_text)


