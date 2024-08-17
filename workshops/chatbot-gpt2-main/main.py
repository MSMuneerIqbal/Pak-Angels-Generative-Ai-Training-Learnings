import streamlit as st
from langchain.llms import HuggingFaceHub
import os

# Replace 'your_hugging_face_token' with your actual Hugging Face token
hf_token = os.getenv('HUGGINGFACEHUB_API_TOKEN', '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')

# Initialize the HuggingFace model
repo_id = "openai-community/gpt2"  # Ensure this is the correct repository ID
llm = HuggingFaceHub(repo_id=repo_id, huggingfacehub_api_token=hf_token, model_kwargs={"max_length": 128, "temperature": 0.7})

# Streamlit interface
st.title("Chat with GPT-2")
st.write("This chatbot is powered by a GPT-2 model hosted on Hugging Face.")

user_input = st.text_input("You:", "Type your message here...")

if st.button("Send"):
    if user_input:
        try:
            # Generate response
            response = llm(user_input)
            
            # Check if the response is a string or a dictionary
            if isinstance(response, dict):
                st.write(f"Bot: {response.get('text', 'No response text found.')}")
            else:
                st.write(f"Bot: {response}")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.write("Please enter a message.")
