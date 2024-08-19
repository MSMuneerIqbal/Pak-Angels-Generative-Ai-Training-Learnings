# -*- coding: utf-8 -*-


import os
import gradio as gr
import whisper
from gtts import gTTS
from groq import Groq

# Set up Groq API client
client = Groq(
    api_key="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",
)
# Load Whisper model
model = whisper.load_model("base")

def chatbot(audio):
    # Transcribe the audio input using Whisper
    transcription = model.transcribe(audio)
    user_input = transcription["text"]

    # Generate a response using Llama 8B via Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="llama3-8b-8192",
    )
    response_text = chat_completion.choices[0].message.content

    # Convert the response text to speech using gTTS
    tts = gTTS(text=response_text, lang='en')
    tts.save("response.mp3")

    return response_text, "response.mp3"

# Create a custom interface
def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown(
            """
            <h1 style="text-align: center; color: #4CAF50;">Voice-to-Voice Chatbot</h1>
            <h3 style="text-align: center;">Powered by OpenAI Whisper, Llama 8B, and gTTS</h3>
            <p style="text-align: center;">Talk to the AI-powered chatbot and get responses in real-time. Start by recording your voice.</p>
            """
        )
        with gr.Row():
            with gr.Column(scale=1):
                audio_input = gr.Audio(type="filepath", label="Record Your Voice")
            with gr.Column(scale=2):
                chatbot_output_text = gr.Textbox(label="Chatbot Response")
                chatbot_output_audio = gr.Audio(label="Audio Response")

        submit_button = gr.Button("Submit")

        submit_button.click(chatbot, inputs=audio_input, outputs=[chatbot_output_text, chatbot_output_audio])

    return demo

# Launch the interface
if __name__ == "__main__":
    interface = build_interface()
    interface.launch()
