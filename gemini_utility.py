import os
import time
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Google.generativeai with API key
genai.configure(api_key=GOOGLE_API_KEY)

def load_gemini_pro_model():
    """Load the latest Gemini 2.0 Flash model for better performance"""
    try:
        gemini_pro_model = genai.GenerativeModel("gemini-2.0-flash")
        return gemini_pro_model
    except Exception as e:
        # Fallback to 1.5 flash if 2.0 is not available
        print(f"Warning: Could not load gemini-2.0-flash, falling back to gemini-1.5-flash. Error: {e}")
        return genai.GenerativeModel("gemini-1.5-flash")

def load_gemini_pro_vision_model():
    """Load the latest Gemini vision model"""
    try:
        return genai.GenerativeModel("gemini-2.0-flash")
    except Exception as e:
        print(f"Warning: Could not load gemini-2.0-flash for vision, falling back to gemini-1.5-flash. Error: {e}")
        return genai.GenerativeModel("gemini-1.5-flash")

def gemini_pro_vision_response(prompt, image):
    """Get response from Gemini Vision model - image/text to text"""
    try:
        gemini_pro_vision_model = load_gemini_pro_vision_model()
        response = gemini_pro_vision_model.generate_content([prompt, image])
        result = response.text
        return result
    except Exception as e:
        return f"Error generating vision response: {str(e)}"

def embeddings_model_response(input_text):
    """Get response from embeddings model - text to embeddings"""
    try:
        # Use the latest embedding model
        embedding_model = "models/text-embedding-004"
        embedding = genai.embed_content(
            model=embedding_model,
            content=input_text,
            task_type="retrieval_document"
        )
        embedding_list = embedding["embedding"]
        return embedding_list
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        # Fallback to older model
        try:
            embedding_model = "models/embedding-001"
            embedding = genai.embed_content(
                model=embedding_model,
                content=input_text,
                task_type="retrieval_document"
            )
            embedding_list = embedding["embedding"]
            return embedding_list
        except Exception as fallback_e:
            return f"Error generating embeddings: {str(fallback_e)}"

def gemini_pro_response(user_prompt):
    """Get response from Gemini model - text to text"""
    try:
        gemini_pro_model = load_gemini_pro_model()
        response = gemini_pro_model.generate_content(user_prompt)
        result = response.text
        return result
    except Exception as e:
        return f"Error generating response: {str(e)}"

def gemini_stream_response(user_prompt):
    """Get streaming response from Gemini model"""
    try:
        gemini_pro_model = load_gemini_pro_model()
        response = gemini_pro_model.generate_content(user_prompt, stream=True)
        return response
    except Exception as e:
        return f"Error generating streaming response: {str(e)}"

def get_available_models():
    """Get list of available Gemini models"""
    try:
        models = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                models.append(model.name)
        return models
    except Exception as e:
        print(f"Error fetching models: {e}")
        return ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]

def check_api_key():
    """Check if API key is valid"""
    try:
        models = list(genai.list_models())
        return True
    except Exception as e:
        print(f"API key validation failed: {e}")
        return False
