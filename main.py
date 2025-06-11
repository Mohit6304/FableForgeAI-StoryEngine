import os
import time
from dotenv import load_dotenv
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import requests
from gemini_utility import (
    load_gemini_pro_model,
    gemini_pro_response,
    gemini_pro_vision_response,
    embeddings_model_response,
    gemini_stream_response,
    get_available_models,
    check_api_key
)
from gradio_client import Client

# Load environment variables from .env file
load_dotenv()

# Accessing the API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

working_dir = os.path.dirname(os.path.abspath(__file__))

# Enhanced page configuration
st.set_page_config(
    page_title="FableForge AI - Story Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': 'https://github.com/your-repo/issues',
        'About': "# FableForge AI Story Engine\nPowered by Gemini 2.0 & Latest AI Models"
    }
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Check API key on startup
if not GEMINI_API_KEY:
    st.error("🔑 Google API Key not found! Please set your GEMINI_API_KEY in the .env file.")
    st.stop()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "api_status" not in st.session_state:
    st.session_state.api_status = check_api_key()

# Main header
st.markdown('<h1 class="main-header">🧠 FableForge AI - Story Engine</h1>', unsafe_allow_html=True)

# Sidebar with enhanced navigation
with st.sidebar:
    
    # API Status indicator
    if st.session_state.api_status:
        st.success("🟢 API Connected")
    else:
        st.error("🔴 API Disconnected")
        
    st.markdown("---")
    
    # Enhanced navigation menu
    selected = option_menu(
        'Navigation',
        ['🤖 ChatBot', '📚 Story Generator', '🎬 Comic Video Generator', '🎯 AI Assistant'],
        icons=['chat-dots-fill', 'book-fill', 'play-fill', 'robot'],
        menu_icon='cpu-fill',
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#667eea", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee"
            },
            "nav-link-selected": {"background-color": "#667eea"},
        }
    )
    
    st.markdown("---")
    
    # Model selection
    available_models = get_available_models()
    selected_model = st.selectbox(
        "🎯 Select AI Model",
        available_models[:5],  # Show first 5 models
        help="Choose the AI model for content generation"
    )
    
    # Settings section
    with st.expander("⚙️ Settings"):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, help="Controls randomness in responses")
        max_tokens = st.slider("Max Tokens", 100, 2048, 1000, help="Maximum response length")

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Enhanced text-to-speech function
def text2speech(text):
    """Convert text to speech using Hugging Face API"""
    if not HUGGINGFACE_API_KEY:
        st.warning("⚠️ Hugging Face token not found. Audio generation disabled.")
        return None
        
    API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": text}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"❌ Audio generation failed. Status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ Audio generation error: {str(e)}")
        return None

# Enhanced ChatBot page
if selected == '🤖 ChatBot':
    model = load_gemini_pro_model()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:  
        st.session_state.chat_session = model.start_chat(history=[])

    # Display the chatbot's title on the page
    st.title("🤖 Enhanced AI ChatBot")
    
    # Add features row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔄 Clear Chat"):
            st.session_state.chat_session = model.start_chat(history=[])
            st.rerun()
    with col2:
        if st.button("💾 Save Chat"):
            st.download_button(
                "Download Chat",
                data=str(st.session_state.chat_session.history),
                file_name="chat_history.txt",
                mime="text/plain"
            )
    with col3:
        stream_mode = st.toggle("🌊 Stream Mode", help="Enable streaming responses")
    with col4:
        if st.button("📊 Chat Stats"):
            st.info(f"Messages: {len(st.session_state.chat_session.history)}")

    # Chat container with enhanced styling
    chat_container = st.container(height=400)
    
    with chat_container:
        # Display the chat history
        for message in st.session_state.chat_session.history:
            with st.chat_message(translate_role_for_streamlit(message.role)):
                st.markdown(message.parts[0].text)

    # Input field for user's message with enhanced features
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_prompt = st.chat_input("💬 Ask me anything...")
        
    with col2:
        if st.button("🎤 Voice Input"):
            st.info("Voice input feature - Coming soon!")
    
    if user_prompt:
        # Add user's message to chat and display it
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_prompt)

        # Generate and display response
        with chat_container:
            with st.chat_message("assistant"):
                if stream_mode:
                    # Streaming response
                    response_placeholder = st.empty()
                    response_text = ""
                    
                    try:
                        response = gemini_stream_response(user_prompt)
                        for chunk in response:
                            if hasattr(chunk, 'text'):
                                response_text += chunk.text
                                response_placeholder.markdown(response_text + "▌")
                        response_placeholder.markdown(response_text)
                        
                        # Update session manually for streaming
                        st.session_state.chat_session.history.append(
                            type('Message', (), {'role': 'user', 'parts': [type('Part', (), {'text': user_prompt})]})()
                        )
                        st.session_state.chat_session.history.append(
                            type('Message', (), {'role': 'model', 'parts': [type('Part', (), {'text': response_text})]})()
                        )
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                else:
                    # Regular response
                    try:
                        gemini_response = st.session_state.chat_session.send_message(user_prompt)
                        st.markdown(gemini_response.text)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# Enhanced Story Generator page
elif selected == '📚 Story Generator':
    st.title("📚 AI Story Generator")
    
    # Enhanced layout with tabs
    tab1, tab2, tab3 = st.tabs(["🖼️ Image + Text Story", "📝 Text-Only Story", "🎨 Creative Writing"])
    
    with tab1:
        st.header("📷 Image-Based Story Generation")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📤 Upload Your Image")
            uploaded_image = st.file_uploader(
                "Choose an image...", 
                type=["jpg", "jpeg", "png", "webp"],
                help="Upload an image to generate a story based on it"
            )
            
            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            st.subheader("✍️ Story Details")
            user_text = st.text_area(
                "Provide story theme or details...",
                placeholder="E.g., A magical adventure, mystery thriller, romantic comedy...",
                height=100
            )
            
            # Story configuration
            story_length = st.selectbox(
                "📏 Story Length",
                ["Short (5-10 lines)", "Medium (10-20 lines)", "Long (20-30 lines)"]
            )
            
            story_genre = st.selectbox(
                "🎭 Genre",
                ["Adventure", "Mystery", "Romance", "Horror", "Comedy", "Sci-Fi", "Fantasy"]
            )
            
            include_moral = st.checkbox("✨ Include Moral Lesson", value=True)
            
            generate_audio = st.checkbox("🔊 Generate Audio", value=True)
        
        if st.button("🎯 Generate Image Story", type="primary"):
            if uploaded_image is not None and user_text.strip():
                with st.spinner("🤖 AI is crafting your story..."):
                    # Enhanced prompt
                    length_map = {
                        "Short (5-10 lines)": "5-10 lines",
                        "Medium (10-20 lines)": "10-20 lines", 
                        "Long (20-30 lines)": "20-30 lines"
                    }
                    
                    prompt = f"""
                    Generate a {story_genre.lower()} story based on this image with the following requirements:
                    - Theme/Details: {user_text}
                    - Length: {length_map[story_length]}
                    - Genre: {story_genre}
                    - Include moral lesson: {include_moral}
                    
                    Make the story engaging, creative, and well-structured.
                    """
                    
                    story = gemini_pro_vision_response(prompt, image)
                    
                    # Display results
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.image(image, caption="Story Inspiration", use_container_width=True)
                    
                    with col2:
                        st.subheader("📖 Generated Story")
                        st.write(story)
                        
                        # Audio generation
                        if generate_audio and story:
                            with st.spinner("🎵 Generating audio..."):
                                audio_bytes = text2speech(story)
                                if audio_bytes:
                                    st.audio(audio_bytes, format="audio/wav")
                        
                        # Download options
                        st.download_button(
                            "📥 Download Story",
                            story,
                            file_name=f"story_{int(time.time())}.txt",
                            mime="text/plain"
                        )
    
    with tab2:
        st.header("📝 Text-Only Story Generation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            user_text = st.text_area(
                "📝 Describe your story idea:",
                placeholder="Describe characters, setting, plot, or any story elements...",
                height=150
            )
        
        with col2:
            st.subheader("⚙️ Story Settings")
            story_length = st.radio("Length", ["Short", "Medium", "Long"])
            story_tone = st.selectbox("Tone", ["Cheerful", "Dark", "Mysterious", "Humorous", "Dramatic"])
            target_audience = st.selectbox("Audience", ["Children", "Teenagers", "Adults", "All Ages"])
            
        if st.button("✨ Generate Text Story", type="primary"):
            if user_text.strip():
                with st.spinner("🎭 Creating your story..."):
                    prompt = f"""
                    Create a {story_length.lower()} {story_tone.lower()} story suitable for {target_audience.lower()} 
                    based on: {user_text}
                    
                    Make it engaging and include a meaningful conclusion.
                    """
                    
                    story = gemini_pro_response(prompt)
                    
                    st.subheader("📚 Your Generated Story")
                    st.write(story)
                    
                    # Audio option
                    if st.checkbox("🎵 Generate Audio Version"):
                        with st.spinner("🎤 Creating audio..."):
                            audio_bytes = text2speech(story)
                            if audio_bytes:
                                st.audio(audio_bytes, format="audio/wav")
    
    with tab3:
        st.header("🎨 Creative Writing Assistant")
        
        writing_type = st.selectbox(
            "✍️ What would you like to write?",
            ["Poem", "Song Lyrics", "Short Story", "Character Description", "World Building", "Dialogue"]
        )
        
        if writing_type == "Poem":
            col1, col2 = st.columns(2)
            with col1:
                poem_style = st.selectbox("Style", ["Free Verse", "Haiku", "Sonnet", "Limerick"])
                theme = st.text_input("Theme", placeholder="Love, Nature, Adventure...")
            with col2:
                mood = st.selectbox("Mood", ["Happy", "Sad", "Peaceful", "Energetic"])
                length = st.selectbox("Length", ["Short", "Medium", "Long"])
            
            if st.button(f"🎭 Generate {poem_style} Poem"):
                prompt = f"Write a {poem_style.lower()} poem about {theme} with a {mood.lower()} mood. Length: {length.lower()}"
                result = gemini_pro_response(prompt)
                st.write(result)
        
        # Add similar sections for other writing types...

# Enhanced Comic Video Generator page
elif selected == '🎬 Comic Video Generator':
    st.title("🎬 AI Comic Video Generator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Story Script")
        user_prompt = st.text_area(
            "Write your comic story:",
            placeholder="Enter a detailed story or script for your comic video...",
            height=200
        )
        
        # Additional options
        comic_style = st.selectbox(
            "🎨 Comic Style",
            ["Classic Comic", "Manga", "Cartoon", "Realistic", "Abstract"]
        )
        
        video_duration = st.selectbox(
            "⏱️ Video Duration",
            ["Short (30s)", "Medium (1min)", "Long (2min)"]
        )
    
    with col2:
        st.subheader("⚙️ Generation Settings")
        
        # Preview options
        if st.button("👁️ Preview Story"):
            if user_prompt:
                enhanced_prompt = f"Enhance this story for comic video: {user_prompt}"
                enhanced_story = gemini_pro_response(enhanced_prompt)
                st.write("**Enhanced Story:**")
                st.write(enhanced_story)
        
        # Character settings
        with st.expander("👥 Character Settings"):
            character_count = st.number_input("Number of Characters", 1, 10, 2)
            art_style = st.selectbox("Art Style", ["2D", "3D", "Mixed"])
        
        # Audio settings
        with st.expander("🎵 Audio Settings"):
            include_music = st.checkbox("Background Music", True)
            include_effects = st.checkbox("Sound Effects", True)
            voice_style = st.selectbox("Narration Voice", ["Male", "Female", "Child", "Robot"])

    if st.button("🎬 Generate Comic Video", type="primary"):
        if user_prompt.strip():
            with st.spinner("🎭 Creating your comic video... This may take a few minutes."):
                try:
                    client = Client("ADOPLE/Video-Generator-AI")
                    result = client.predict(
                        user_prompt,
                        api_name="/generate_video"
                    )
                    
                    if result and 'video' in result:
                        video_data = result['video']
                        st.success("🎉 Comic video generated successfully!")
                        st.video(video_data)
                        
                        # Download option
                        st.download_button(
                            "📥 Download Video",
                            data=video_data,
                            file_name=f"comic_video_{int(time.time())}.mp4",
                            mime="video/mp4"
                        )
                    else:
                        st.error("❌ Video generation failed. Please try again.")
                        
                except Exception as e:
                    st.error(f"❌ Error generating video: {str(e)}")
                    st.info("💡 Tip: Try simplifying your story or check your internet connection.")

# New AI Assistant page
elif selected == '🎯 AI Assistant':
    st.title("🎯 AI Assistant Hub")
    
    # Assistant categories
    assistant_type = st.selectbox(
        "Choose Assistant Type:",
        ["📝 Writing Assistant", "🔍 Research Helper", "💡 Idea Generator", "🎨 Creative Assistant", "📚 Learning Tutor"]
    )
    
    if assistant_type == "📝 Writing Assistant":
        st.subheader("📝 Professional Writing Assistant")
        
        task = st.selectbox(
            "What do you need help with?",
            ["Improve Text", "Grammar Check", "Summarize", "Translate", "Change Tone", "Expand Ideas"]
        )
        
        user_text = st.text_area("Enter your text:", height=200)
        
        if task == "Change Tone":
            tone = st.selectbox("Select tone:", ["Professional", "Casual", "Friendly", "Formal", "Persuasive"])
        elif task == "Translate":
            language = st.selectbox("Translate to:", ["Spanish", "French", "German", "Italian", "Japanese", "Chinese"])
        
        if st.button(f"✨ {task}"):
            if user_text:
                if task == "Change Tone":
                    prompt = f"Rewrite this text in a {tone.lower()} tone: {user_text}"
                elif task == "Translate":
                    prompt = f"Translate this text to {language}: {user_text}"
                else:
                    prompt = f"{task} this text: {user_text}"
                
                result = gemini_pro_response(prompt)
                st.write("**Result:**")
                st.write(result)
    
    # Add other assistant types...

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🧠 <strong>FableForge AI Story Engine</strong> | Powered by Gemini 2.0 & Latest AI Models</p>
        <p>Built with ❤️ using Streamlit | Version 2.0.0</p>
    </div>
    """, 
    unsafe_allow_html=True
)