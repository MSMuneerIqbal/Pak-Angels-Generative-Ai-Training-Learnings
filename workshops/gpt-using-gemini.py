# type: ignore
import streamlit as st
import google.generativeai as genai

# Streamlit app UI
st.markdown("<h1 style='color: red;'>Generative AI Prompt Interface</h1>", unsafe_allow_html=True)

# Sidebar for API key input
st.sidebar.info("The model only gets Google API key.")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")

# Text input for the user's prompt in the main page
user_input = st.text_input("Enter your prompt:")

# Button to submit the API key and prompt
if st.button("Generate Response"):
    if api_key and user_input:
        # Configure the API key
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Function to get a response from the model
        def get_response_from_model(user_input):
            response = model.generate_content(user_input)
            return response.text
        
        # Get the response and display it
        output = get_response_from_model(user_input)
        st.write("**Generated Response:**")
        st.write(output)
    else:
        st.write("Please enter both the API key and a prompt to generate a response.")
