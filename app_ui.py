import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading
import os
from ai_brain import get_ai_response
from avatar_talking import speak_and_sync
from voice_input import get_voice_input
from capture_face import capture_user_face




class AvatarChatUI:
    def __init__(self, root, face_file):
        self.root = root
        self.root.title("AI Avatar ChatBuddy")
        self.root.geometry("800x600")
        self.root.config(bg="#1c1c1c")

        # Avatar Canvas (for animation)
        self.chat_canvas = tk.Canvas(root, width=400, height=300, bg="#1c1c1c", highlightthickness=0)
        self.chat_canvas.pack(pady=10)

        # ✅ Load user's scanned face if available
        if os.path.exists(face_file):
            avatar_path = face_file
        else:
            avatar_path = "assets/avatar.png"  # fallback image

        self.avatar_img = Image.open(avatar_path).resize((180, 180))
        self.avatar_photo = ImageTk.PhotoImage(self.avatar_img)
        self.avatar_label = self.chat_canvas.create_image(200, 150, image=self.avatar_photo)

        # Chat Display
        self.chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15,
                                                  bg="#2c2c2c", fg="white", font=("Arial", 11))
        self.chat_box.pack(padx=10, pady=10)
        self.chat_box.config(state=tk.DISABLED)

        # Mic Button
        self.mic_button = tk.Button(root, text="🎤 Speak", command=self.on_mic_click,
                                    bg="#0078D7", fg="white", font=("Arial", 12, "bold"),
                                    width=12, height=2)
        self.mic_button.pack(pady=10)

        # Entry Box for Manual Text Input
        self.input_frame = tk.Frame(root, bg="#1c1c1c")
        self.input_frame.pack(pady=10)

        self.entry = tk.Entry(self.input_frame, font=("Arial", 12), width=50)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.on_send_click,
                                     bg="#0078D7", fg="white", font=("Arial", 11))
        self.send_button.pack(side=tk.LEFT)

    # --- Functions ---
    def display_message(self, sender, text):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"{sender}: {text}\n\n")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.yview(tk.END)

    def on_send_click(self):
        user_input = self.entry.get().strip()
        if user_input:
            self.display_message("You", user_input)
            self.entry.delete(0, tk.END)
            threading.Thread(target=self.real_ai_response, args=(user_input,)).start()

    # def fake_ai_response(self, user_input):
    #     import time
    #     time.sleep(1.5)
    #     ai_reply = f"Hey! You said: {user_input}"
    #     self.display_message("AI", ai_reply)
    #     self.animate_avatar_talking(ai_reply)
    def real_ai_response(self, user_input):
        import subprocess
        from avatar_talking import speak_and_sync  # ✅ Add this import here

        result = subprocess.run(
        ["ollama", "run", "llama3:latest", user_input],
        capture_output=True, text=True, encoding="utf-8", errors="ignore")

        ai_reply = result.stdout.strip() or "Sorry, I didn’t catch that."
        self.display_message("AI", ai_reply)

        # 👇 Make the avatar speak and animate using your advanced function
        threading.Thread(target=speak_and_sync, args=(ai_reply,), daemon=True).start()



    def animate_avatar_talking(self, text):
        import time
        from threading import Thread

        def animate():
            self.avatar_talking = True

            bubble_bg = self.chat_canvas.create_rectangle(
                70, 10, 330, 90, fill="#2c2c2c", outline="#0078D7", width=2
            )
            bubble_text = self.chat_canvas.create_text(
                200, 50, text=text[:120] + ("..." if len(text) > 120 else ""),
                fill="white", font=("Arial", 12, "italic"), width=250
            )

            for _ in range(8):  # 8 cycles
                if not self.avatar_talking:
                    break
                self.chat_canvas.scale(self.avatar_label, 200, 150, 1.05, 0.95)
                self.root.update_idletasks()
                time.sleep(0.15)
                self.chat_canvas.scale(self.avatar_label, 200, 150, 0.95, 1.05)
                self.root.update_idletasks()
                time.sleep(0.15)

            self.chat_canvas.delete(bubble_bg)
            self.chat_canvas.delete(bubble_text)
            self.avatar_talking = False

        Thread(target=animate, daemon=True).start()

    def on_mic_click(self):
        """🎤 Capture voice, get AI reply, speak and sync"""
        self.display_message("System", "🎤 Listening...")

        def process_voice():
            try:
                user_text = get_voice_input()

                if not user_text:
                    self.display_message("System", "❌ Didn't catch any speech.")
                    return

                self.display_message("You (voice)", user_text)

                # Get AI response
                ai_reply = get_ai_response(user_text)
                self.display_message("AI", ai_reply)

                # Speak & lip sync
                speak_and_sync(ai_reply, "face_scan.jpg")

                # Animate avatar talking visually
                self.animate_avatar_talking(ai_reply)

            except Exception as e:
                self.display_message("System", f"❌ Error in mic input: {e}")

        # Run in background so UI doesn’t freeze
        threading.Thread(target=process_voice, daemon=True).start() 


def run_ui(face_file):
    root = tk.Tk()
    app = AvatarChatUI(root, face_file)
    root.mainloop()


if __name__ == "__main__":
    # 📸 Capture live photo of user before UI starts
    capture_user_face()

    # 🚀 Then open the Tkinter chat window (not PyQt)
    face_file = "face_scan.jpg"  # or whatever your capture function saves
    run_ui(face_file)


