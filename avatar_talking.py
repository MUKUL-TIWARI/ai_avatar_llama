import pyttsx3
import cv2
import numpy as np
import time
import random
import threading
from phonemizer import phonemize
from transformers import pipeline
from moviepy.editor import VideoFileClip 
import torch

# =============================
# 🎭 Emotion Analyzer
# =============================
sentiment_model = pipeline("sentiment-analysis")

def detect_emotion(text):
    """Return basic emotion (positive, negative, neutral)."""
    try:
        result = sentiment_model(text)[0]
        label = result['label'].lower()
        if 'positive' in label:
            return "happy"
        elif 'negative' in label:
            return "sad"
        else:
            return "neutral"
    except Exception as e:
        print("⚠️ Emotion analysis failed:", e)
        return "neutral"


# =============================
# 🧠 MAIN FUNCTION
# =============================
def speak_and_sync(text, video_path="assets/cartoon_avatar.mp4"):
    """Speak with live cartoon avatar synced with phonemes + emotion animation."""
    
    emotion = detect_emotion(text)
    print(f"🧠 Detected Emotion: {emotion}")

    engine = pyttsx3.init()
    engine.setProperty('rate', 175)

    # Load base avatar animation (cartoon loop)
    try:
        clip = VideoFileClip(video_path).resize((400, 400)).loop(duration=10)
    except Exception as e:
        print("⚠️ Could not load video, using static fallback:", e)
        clip = None

    # Convert text → phonemes
    try:
        phonemes = phonemize(text, language='en-us', backend='espeak', strip=True).split()
    except Exception as e:
        print("⚠️ Phonemizer failed:", e)
        phonemes = []

    speaking_flag = [True]

    # =============================
    # 🧩 Animation Thread
    # =============================
    def animate_avatar():
        cap = None
        if clip:
            cap = cv2.VideoCapture(video_path)
        else:
            frame = np.zeros((400, 400, 3), dtype=np.uint8)
            cv2.putText(frame, "Avatar Missing", (100, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        phoneme_idx = 0

        while speaking_flag[0]:
            # Read next frame
            if cap and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
            else:
                frame = np.zeros((400, 400, 3), dtype=np.uint8)

            # Add emotion-based facial overlay
            if emotion == "happy":
                cv2.ellipse(frame, (200, 300), (60, 30), 0, 0, 180, (0, 255, 0), 3)  # smile
                cv2.line(frame, (150, 100), (180, 80), (0, 255, 0), 3)
                cv2.line(frame, (250, 100), (220, 80), (0, 255, 0), 3)
            elif emotion == "sad":
                cv2.ellipse(frame, (200, 330), (60, 30), 0, 180, 360, (255, 0, 0), 3)  # frown
                cv2.line(frame, (150, 100), (180, 120), (255, 0, 0), 3)
                cv2.line(frame, (250, 100), (220, 120), (255, 0, 0), 3)
            else:
                cv2.line(frame, (150, 100), (250, 100), (255, 255, 255), 2)  # neutral eyebrows

            # Simulate mouth opening based on phoneme
            if phonemes:
                phoneme = phonemes[phoneme_idx % len(phonemes)]
                if phoneme in ['AA', 'AE', 'AH', 'AO', 'EH', 'ER', 'IH', 'IY', 'UH', 'UW']:
                    mouth_open = 20
                else:
                    mouth_open = 10
                phoneme_idx += 1
            else:
                mouth_open = random.randint(8, 20)

            # Draw mouth region
            cv2.rectangle(frame, (160, 260), (240, 260 + mouth_open), (0, 0, 0), -1)

            # Random blinking eyes
            if random.random() < 0.03:
                cv2.rectangle(frame, (150, 150), (180, 170), (0, 0, 0), -1)
                cv2.rectangle(frame, (220, 150), (250, 170), (0, 0, 0), -1)
            else:
                cv2.circle(frame, (165, 160), 10, (255, 255, 255), -1)
                cv2.circle(frame, (235, 160), 10, (255, 255, 255), -1)

            cv2.imshow("AI Cartoon Avatar", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if cap:
            cap.release()
        cv2.destroyAllWindows()

    # Start animation + voice
    anim_thread = threading.Thread(target=animate_avatar)
    anim_thread.start()

    engine.say(text)
    engine.runAndWait()

    speaking_flag[0] = False
    time.sleep(0.3)
    cv2.destroyAllWindows()
    print("✅ Avatar emotion animation complete.")
