import os

from dotenv import load_dotenv
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from IPython.display import Audio
import requests
from gemini_utility import (load_gemini_pro_model,
                            gemini_pro_response,
                            gemini_pro_vision_response,
                            embeddings_model_response)
from gradio_client import Client

# New Code: Load environment variables from .env file
load_dotenv()

# Accessing the API keys from environment variables
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
HUGGING_FACE_AUTH_TOKEN = os.getenv("HUGGING_FACE_AUTH_TOKEN")

working_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Syntax AI",
    page_icon="🧠",
    layout="centered",
)

with st.sidebar:
    selected = option_menu('Syntax AI',
                           ['ChatBot',
                            'Story Generator',
                            'Comic Video Generator',],
                           menu_icon='robot', icons=['chat-dots-fill', 'book-fill', 'image-fill', 'play-fill'],
                           default_index=0
                           )


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# chatbot page
if selected == 'ChatBot':
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:  
        st.session_state.chat_session = model.start_chat(history=[])

    # Display the chatbot's title on the page
    st.title("🤖 ChatBot")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask bot...")  
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)  

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

def text2speech(text):
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_AUTH_TOKEN}"}
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        audio_bytes = response.content
        return audio_bytes
    else:
        st.error("Failed to generate audio. Please try again.")
        return None

# Story Generator page
if selected == "Story Generator":

    st.title("📷 Snap Narrate")

    # Allow users to upload an image
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    
    # Input field for user's text
    user_text = st.text_area("Provide some details or a theme for the story...")
    
    if st.button("Generate Story") and uploaded_image is not None and user_text != "":
        image = Image.open(uploaded_image)

        col1, col2 = st.columns(2)

        with col1:
            resized_img = image.resize((800, 500))
            st.image(resized_img)
        
        # Concatenating user's text with the default prompt
        default_prompt = f"Given the image and the following details: '{user_text}', write a short story below 20 lines with a moral."

        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)
            audio_bytes = text2speech(caption)
            if audio_bytes is not None:
                st.audio(audio_bytes, format="audio/ogg")
                
    elif st.button("Generate Story only with text") and uploaded_image is None and user_text != "":
        default_prompt = f"using the following details: '{user_text}', write a short story below 20 lines with a moral."
        caption = gemini_pro_response(default_prompt)
        st.info(caption)
        audio_bytes = text2speech(caption)
        if audio_bytes is not None:
            st.audio(audio_bytes, format="audio/ogg")


# comic video generator page
if selected == "Comic Video Generator":

    st.title("Generate a Comic")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Enter the story to generate comic...")

    if st.button("Generate Comic"):
        response = embeddings_model_response(user_prompt)
        client = Client("ADOPLE/Video-Generator-AI")
        result = client.predict(
            user_prompt,	# str  in 'Comics Text' Textbox component
            api_name="/generate_video"
        )
        video_data = result['video']
        st.video(video_data)