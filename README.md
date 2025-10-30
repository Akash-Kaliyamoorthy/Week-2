# ⚡ EV Charging Assistant Chatbot

An AI-powered chatbot to help users find EV charging stations using Machine Learning recommendations and Generative AI conversations.

## 🎯 Features

- 💬 **Conversational AI** - Chat naturally about EV charging using Claude
- 📍 **Station Finder** - Find nearby charging stations using Open Charge Map API
- 🤖 **ML Recommendations** - Simple ML algorithm ranks stations by distance, charger type, and availability
- 🚀 **Easy Deployment** - Deploy for free on Streamlit Cloud

## 🛠️ Tech Stack

- **Streamlit** - Web interface
- **OpenAI API (GPT-3.5)** - Generative AI chatbot
- **Open Charge Map API** - Charging station data
- **Python** - Backend logic with simple ML

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ev-charging-chatbot.git
cd ev-charging-chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up API key
Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

**Get OpenAI API Key**: https://platform.openai.com/api-keys

### 4. Run the app
```bash
streamlit run app.py
```

## 🚀 Deploy to Streamlit Cloud

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy on Streamlit
1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Connect your GitHub repo
4. Set **Main file path**: `app.py`
5. Click "Advanced settings" → "Secrets"
6. Add your API key:
```
OPENAI_API_KEY = "sk-your-openai-key-here"
```
7. Click "Deploy"!

## 📖 How It Works

### Machine Learning Component
Simple recommendation algorithm that scores stations based on:
- Distance (closer = higher score)
- Charger type (Fast chargers = bonus points)
- Operational status (working stations prioritized)

### Gen AI Component
OpenAI GPT-3.5 provides:
- Natural language understanding
- Conversational responses
- Context-aware answers about charging stations

## 🎓 Project Report Points

**Problem Statement**: Range anxiety prevents EV adoption. Users need easy access to charging station information.

**Solution**: AI chatbot combining ML recommendations with conversational interface.

**ML Used**: Distance-based ranking algorithm with multi-factor scoring.

**Gen AI Used**: OpenAI GPT-3.5 for natural language processing and user interaction.

## 📝 License

MIT License - Feel free to use for your project!

## 🤝 Contributing

This is a beginner project. Feel free to fork and improve!

---
Made with ❤️ for EV enthusiasts