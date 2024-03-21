# FableForgeAI-StoryEngine

Welcome to FableForgeAI-StoryEngine, an innovative platform designed to harness the power of AI for creating engaging narratives, chat experiences, and comic videos. Built with the fusion of several advanced AI models, including Gemini-Pro from Google's generative AI suite, this project offers users a unique opportunity to interact with, and generate creative content in new and exciting ways.

## Features

FableForgeAI-StoryEngine provides a range of features across different domains of content creation:

### ChatBot
- Engage in interactive conversations with an AI-powered chatbot.
- Utilize Gemini-Pro model for generating responses.

### Story Generator
- Generate short stories based on user inputs and uploaded images.
- Support for text-to-speech conversion for narrating the generated stories.
- Utilize Gemini-Pro and Gemini-Pro-Vision models for text and image-to-text generation.

### Comic Video Generator
- Create comic videos from user-provided story prompts.
- Leverage embeddings model response and Gradio Client for video generation.

## Installation

To set up FableForgeAI-StoryEngine on your local machine, follow these steps:

1. **Clone the Repository**
```
git clone https://github.com/YourUsername/FableForgeAI-StoryEngine.git
cd FableForgeAI-StoryEngine
```

2. **Install Requirements**
- Ensure you have Python 3.7+ installed on your machine.
- Install all required libraries using pip:
  ```
  pip install -r requirements.txt
  ```

## Usage

To use FableForgeAI-StoryEngine, execute the `main.py` script:
```
python main.py
```

Upon running, you can access the web interface through your browser at the address indicated by Streamlit, typically `http://localhost:8501`.

### Interacting with the Features
- **ChatBot:** Select 'ChatBot' from the sidebar menu and start conversing with the AI by typing in your messages.
- **Story Generator:** Navigate to 'Story Generator', upload an image (optional), provide some details or a theme for your story, and click on "Generate Story".
- **Comic Video Generator:** Choose 'Comic Video Generator', enter the story prompt in the provided text area, and click on "Generate Comic" to create your comic video.

## Configuration

Before running the application, ensure you configure the necessary API keys in `config.json`:
```json
{
  "GOOGLE_API_KEY": "YOUR_GOOGLE_API_KEY_HERE"
}
```
Replace YOUR_GOOGLE_API_KEY_HERE with your actual Google API key.