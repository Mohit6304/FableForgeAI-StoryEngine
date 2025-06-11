# 🧠 FableForge AI - Story Engine

> **Transform your imagination into captivating stories with the power of AI**

[![Streamlit](https://img.shields.io/badge/Streamlit-1.45.0-FF6B6B.svg)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-4285F4.svg)](https://ai.google.dev/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg)](https://python.org)

An AI-powered storytelling platform built with Streamlit and Google's Gemini models. Create stories, generate comics, chat with AI, and more!

## ✨ Features

- 🤖 **AI ChatBot** - Intelligent conversations with streaming responses
- 📚 **Story Generator** - Create stories from images or text prompts  
- 🎬 **Comic Video Generator** - Transform stories into visual comics
- 🎯 **AI Assistant** - Writing help, grammar check, translation
- 🎨 **Creative Writing** - Poems, lyrics, character descriptions

## 🚀 Quick Setup with install.py

The easiest way to get started is using our automated installation script:

### **Option 1: Automated Installation**

1. **Download and run the installer**
   ```bash
   python install.py
   ```

The installer will automatically:
- ✅ Check Python version compatibility (3.9+)
- 📦 Install all required packages
- ⚙️ Create `.env` file template
- 🔑 Guide you through API key setup
- 🧪 Test the installation
- 🚀 Launch the application

### **What install.py does:**

- **Python Version Check**: Ensures you have Python 3.9 or higher
- **Package Installation**: Installs all dependencies from requirements.txt
- **Environment Setup**: Creates `.env` file with proper template
- **API Key Configuration**: Guides you to set up required API keys
- **Installation Testing**: Verifies all packages work correctly
- **Application Launch**: Optionally starts the Streamlit app

## 🛠 Manual Installation

### **Prerequisites**
- Python 3.9 or higher
- Google API Key ([Get one here](https://aistudio.google.com/app/apikey))
- Hugging Face Token ([Get one here](https://huggingface.co/settings/tokens))

### **Steps**

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/FableForgeAI-StoryEngine.git
   cd FableForgeAI-StoryEngine
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file:
   ```env
   GEMINI_API_KEY=your_google_api_key_here
   HUGGINGFACE_API_KEY=your_hugging_face_token_here
   ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎯 How to Use

### **ChatBot**
- Start conversations with AI
- Toggle streaming mode for real-time responses
- Save chat history
- Adjust temperature and token settings

### **Story Generator**
- **Image Stories**: Upload an image and add text prompts
- **Text Stories**: Describe your story idea in detail
- **Creative Writing**: Generate poems, lyrics, character descriptions
- Choose genre, length, and tone
- Generate audio narration

### **Comic Video Generator**
- Write your story script
- Select comic style and duration
- Customize characters and audio settings
- Generate and download video

### **AI Assistant**
- **Writing Help**: Improve text, check grammar
- **Translation**: Multi-language support
- **Tone Change**: Adjust writing style
- **Research**: Get information and analysis

## ⚙️ Configuration

### **Model Settings**
- Choose from multiple Gemini models
- Adjust temperature (0.0-1.0) for creativity
- Set max tokens (100-2048) for response length

### **Audio Settings**
- Text-to-speech generation
- Multiple voice options
- High-quality audio output

## 📋 Requirements

```
streamlit>=1.45.0
google-generativeai>=0.8.5
streamlit-option-menu>=0.3.13
python-dotenv>=1.0.1
Pillow>=10.3.0
requests>=2.32.3
gradio-client>=1.3.0
numpy>=1.26.4
```

## 🔧 Environment Variables

Your `.env` file should contain:

```env
# Google Gemini API Key
GEMINI_API_KEY=your_api_key_here

# Hugging Face API Key (for audio generation)
HUGGINGFACE_API_KEY=your_token_here
```

## 🐛 Troubleshooting

**API Key Issues:**
- Verify your `.env` file exists and contains valid keys
- Check API key permissions and quotas

**Installation Problems:**
- Use `python install.py` for automated setup
- Ensure Python 3.9+ is installed
- Try creating a virtual environment

**Import Errors:**
- Run `pip install -r requirements.txt` again
- Check Python path and virtual environment

---

Built with ❤️ using Streamlit | Powered by Google Gemini AI

