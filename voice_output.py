import os
from gtts import gTTS
from playsound import playsound

def speak_response(text):
    """
    Converts AI text response to voice using gTTS (Google Text-to-Speech)
    and saves as response.wav
    """
    print("🗣️ Converting text to speech...")

    try:
        # Generate speech
        tts = gTTS(text=text, lang="en")
        tts.save("response.mp3")

        # Convert to .wav (for Wav2Lip compatibility)
        os.system("ffmpeg -y -i response.mp3 response.wav >nul 2>&1")

        # Optional: play voice in real time
        playsound("response.mp3")

        print("✅ Voice generated successfully!")

    except Exception as e:
        print("❌ Error generating voice:", e)
