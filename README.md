
![status](https://img.shields.io/badge/Status-Ongoing%20Development-blue?style=flat-square)

# 🤖 AI Avatar LLaMA

A fully interactive AI-powered avatar that listens, speaks, and interacts in real-time.  
Built using LLaMA, Whisper, OpenCV, Lip-Sync animation, and Text-to-Speech technologies.

---

## 🚧 Project Status: In Progress
This project is currently under development.  
I am working on multiple AIML and cybersecurity projects, so new features and updates will be added gradually.

---
 <b>Features</b>

. Voice Input — Speak to your AI avatar directly using a microphone

. LLaMA Model — Generates intelligent, human-like responses

. Voice Output — The avatar replies using realistic text-to-speech

. Lip-Sync Animation — Mouth movement synced with generated audio

. Custom Avatar — Add your own image or animated character face

. Modular Design — Easy to extend and improve

 <b>Tech Stack</b>
```

Component & Technology Used...

AI Model             Meta LLaMA

Voice Recognition    speech_recognition

Text-to-Speech       pyttsx3 or gTTS

Avatar Animation     MoviePy, OpenCV

Backend Logic        Python

Environment          Local (can be deployed on Flask later)
```
 <b>Project Structure</b>
```
ai-avatar-llama/
│
├── main.py                 # Main script to run the AI Avatar
├── avatar.jpg              # Avatar face image
├── voice_to_text.py        # Captures and converts user voice
├── text_to_speech.py       # Converts response text to speech
├── lip_sync.py             # Animates mouth movement
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

 <b>Installation</b>

1️⃣ Clone the Repository
```
git clone https://github.com/mukultiwari/ai-avatar-llama.git
cd ai-avatar-llama
```

2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

3️⃣ Run the Avatar
```
python main.py
```
 <b>How It Works</b>

1. The program listens to your voice input

2. It sends your speech to the LLaMA model for generating a response

3. The AI’s text response is converted into speech

4. The avatar’s mouth moves in sync with the generated audio

 <b>Demo Screenshot</b>

( project image will be added later)
```
![AI Avatar Demo](./assets/demo.png)
```

 <b>Future Improvements</b>

. Add a web interface (Flask or React frontend)

. Add facial expressions and head movement

. Support for multiple languages (English, Hindi, Japanese, etc.)

. Integrate with cloud-hosted AI models

 <b>Author</b>

Mukul Tiwari<br>
 B.Tech in AI & ML (Pursuing) 

 mukultiwari2003@gmail.com 
 
 https://github.com/MUKUL-TIWARI/MUKUL-TIWARI


📜 <b>License</b>

This project is licensed under the MIT License — feel free to use and modify with credit.
