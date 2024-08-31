import os
import gradio as gr
import whisper
from gtts import gTTS
from io import BytesIO
import numpy as np
import pydub
from pydub import AudioSegment
from groq import Groq

# Set your Groq API key
os.environ['GROQ_API_KEY'] = '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'

# Load Whisper model
model = whisper.load_model("base")  # Choose the appropriate model size

# Initialize Groq client
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to transcribe audio using Whisper
def transcribe_audio(audio_file):
    try:
        audio_file.seek(0)
        audio = whisper.load_audio(audio_file)
        result = model.transcribe(audio)
        return result['text']
    except Exception as e:
        return f"Error in transcription: {str(e)}"

# Function to generate a response using Groq's LLaMA model
def generate_response(prompt):
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",  # Ensure this model name is correct
        )
        response_text = chat_completion.choices[0].message.content
        return response_text
    except Exception as e:
        return f"Error in response generation: {str(e)}"

# Function to convert text to speech using GTTS
def text_to_speech(text):
    try:
        tts = gTTS(text, lang='en')
        audio_io = BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        
        # Convert BytesIO to AudioSegment
        audio_segment = AudioSegment.from_file(audio_io, format='mp3')
        
        # Save AudioSegment to file
        response_audio_path = '/tmp/response_audio.wav'
        audio_segment.export(response_audio_path, format='wav')
        
        return response_audio_path
    except Exception as e:
        return None, f"Error in text-to-speech conversion: {str(e)}"

# Chatbot function combining all steps
def chatbot(audio_file):
    try:
        # Transcribe audio
        text = transcribe_audio(audio_file)
        
        if "Error" in text:
            return None, None, text
        
        # Generate response
        response = generate_response(text)
        
        if "Error" in response:
            return None, None, response
        
        # Convert response to speech
        response_audio_path = text_to_speech(response)
        
        if not response_audio_path:
            return None, None, "Error in text-to-speech conversion."
        
        # Return response audio file path and text response
        return response_audio_path, response
    
    except Exception as e:
        return None, None, f"Error: {str(e)}"

# Create and launch Gradio interface
iface = gr.Interface(
    fn=chatbot,
    inputs=gr.Audio(type="numpy", label="Input Audio"),  # Use numpy for audio input
    outputs=[gr.Audio(type="filepath", label="Response Audio"), gr.Textbox(label="Response")],  # Use filepath for audio output
    live=True,
    title="Voice to Voice Chatbot",
    description="Interact with the chatbot to improve your English conversation skills."
)

iface.launch()
