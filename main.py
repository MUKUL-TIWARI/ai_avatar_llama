import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from app_ui import run_ui
from face_scan import scan_face
from avatar_talking import speak_and_sync

# --------------------------------------------
# 1️⃣ Load LLaMA model
# --------------------------------------------
print("⏳ Loading LLaMA-2-7B on GPU...")

model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("✅ Model loaded successfully!\n")

# --------------------------------------------
# 2️⃣ Scan face live
# --------------------------------------------
face_file = scan_face()
if not face_file:
    print("❌ Face scan cancelled. Exiting.")
    exit()

print(f"✅ Face captured and saved as {face_file}\n")

# --------------------------------------------
# 3️⃣ Simple AI response generator
# --------------------------------------------
def generate_reply(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=120)
    reply = tokenizer.decode(output[0], skip_special_tokens=True)
    return reply.strip()

# --------------------------------------------
# 4️⃣ Avatar + Voice Integration
# --------------------------------------------
def chat_with_voice(prompt):
    print("🧠 Generating reply...")
    ai_reply = generate_reply(prompt)
    print("AI:", ai_reply)
    speak_and_sync(ai_reply, face_file)

# --------------------------------------------
# 5️⃣ Launch UI
# --------------------------------------------
print("🤖 Starting AI Cartoon ChatBuddy (UI Mode)")
run_ui(face_file)
