# type: ignore
import streamlit as st
import sounddevice as sd
import wave
import numpy as np
from vosk import Model, KaldiRecognizer
import json
from groq import Groq
import tempfile

# Set up Groq API client
client = Groq(
    api_key="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",
)

# Load Vosk model
model = Model("./vosk-model-small-en-in-0.4")  # Ensure this path is correct

def record_audio(duration=5, fs=16000):
    """Record audio from the microphone."""
    st.write("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    st.write("Recording finished.")
    
    # Save the recording as a .wav file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
        wf = wave.open(temp_wav_file, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())
        temp_wav_file_path = temp_wav_file.name
        wf.close()

    return temp_wav_file_path

def transcribe_audio(audio_path):
    """Transcribe audio using Vosk."""
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    result = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result += res['text'] + " "

    return result.strip()

def chatbot(audio_path):
    """Process transcription and generate feedback."""
    user_input = transcribe_audio(audio_path)

    if not user_input:
        return "Error: Could not transcribe the audio."

    messages = [
        {"role": "system", "content": "You are an English tutor. Your job is to provide detailed feedback on grammar and vocabulary."},
        {"role": "user", "content": f"Please review the following text and provide feedback on grammar and vocabulary: {user_input}"}
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-groq-70b-8192-tool-use-preview",
    )
    response_text = chat_completion.choices[0].message.content

    return response_text

def main():
    st.title("Real-Time Voice-to-Text Chatbot")
    st.header("Powered by Vosk and Llama3 70B")
    st.write("Speak to the chatbot and get feedback on your grammar and vocabulary in real-time.")

    if st.button("Start Recording"):
        audio_path = record_audio(duration=5)  # Record for 5 seconds
        response_text = chatbot(audio_path)
        st.text_area("Feedback", response_text, height=200)

if __name__ == "__main__":
    main()
