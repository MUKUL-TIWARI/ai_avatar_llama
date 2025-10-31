from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get your Hugging Face token
hf_token = os.getenv("HF_TOKEN")


model_name = "meta-llama/Llama-2-7b-chat-hf"

print("⏳ Loading LLaMA-2-7B on GPU...")

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_threshold=6.0,
    llm_int8_enable_fp32_cpu_offload=True  # ✅ enables CPU offload
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

# ✅ FIX: Let the model automatically choose correct devices
print("🧩 Checking GPU availability...")
print("CUDA available:", torch.cuda.is_available())
print("GPU device name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU detected")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    use_auth_token=hf_token,
    quantization_config=bnb_config,
    device_map="auto",           # ✅ replaces {"": "cuda"}
    torch_dtype=torch.float16,   # ✅ still uses half precision
)

model.eval()

def get_ai_response(prompt):
    # ✅ Automatically sends input tensors to the right device
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            top_p=0.9
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
