# app.py

import os
import streamlit as st
from gtts import gTTS

def text_to_speech(text):
    # Convert the input text to speech using gTTS
    tts = gTTS(text=text, lang='en')
    audio_file_path = "output.mp3"
    tts.save(audio_file_path)

    return audio_file_path

# Streamlit UI
st.title("Text to Speech Converter")
st.write("Type a sentence, and the AI will pronounce it for you. Simply enter the text and listen to the audio output.")

# Text input
text_input = st.text_area("Enter your text here")

# Button to trigger the conversion
if st.button("Convert to Speech"):
    if text_input:
        # Convert text to speech and get the audio file path
        audio_file = text_to_speech(text_input)
        
        # Display the audio player
        st.audio(audio_file)
    else:
        st.warning("Please enter some text to convert.")
