import streamlit as st
import time
import random
import json
import cv2  # Camera Integration
import numpy as np
import pytesseract  # OCR for Handwritten Text Recognition
import speech_recognition as sr  # Voice Input
from transformers import pipeline  # AI-powered auto-complete

# ✅ Ensure set_page_config is the FIRST Streamlit command
st.set_page_config(page_title="UwU Code Generator X 🚀", page_icon="🤖", layout="wide")

# --- DARK MODE TOGGLE ---
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
            body { background: #1e1e1e; color: #ffffff; }
            .stButton button { background-color: #ff33cc !important; }
        </style>
    """, unsafe_allow_html=True)

# --- AI AUTO-COMPLETE ---
try:
    auto_complete = pipeline("text-generation", model="EleutherAI/gpt-neo-125M", device_map="auto")
except Exception as e:
    st.error(f"❌ Error loading AI model: {str(e)}")

def get_code_suggestion(prompt):
    try:
        response = auto_complete(prompt, max_length=100, num_return_sequences=1)
        return response[0]['generated_text']
    except Exception as e:
        st.error(f"❌ AI Generation Error: {str(e)}")
        return ""

# --- UI CONFIGURATION ---
def set_ui_config():
    st.markdown("""
        <style>
            .title { font-size: 3em; font-weight: bold; text-align: center; color: #33FFC2; }
            .subtitle { font-size: 1.2em; text-align: center; color: #bbb; margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

def render_app_header():
    st.markdown("<div class='title'>🤖 UwU Code Generator X 🚀</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Turn your ideas into UwU code effortlessly! 💫</div>", unsafe_allow_html=True)

# --- HANDWRITTEN TEXT RECOGNITION ---
def recognize_handwritten_text(image):
    try:
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # ✅ Fix Windows Path Issue
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        st.error(f"❌ OCR Error: {str(e)}")
        return ""

def capture_camera_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        st.image(frame, channels="BGR", caption="📸 Captured Image")
        if st.button("📝 Extract Handwritten Text"):
            extracted_text = recognize_handwritten_text(frame)
            st.text_area("Extracted Text:", extracted_text, height=100)
    else:
        st.error("❌ Failed to capture image")

# --- SPEECH RECOGNITION ---
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak now...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("❌ Couldn't understand the audio.")
            return ""
        except sr.RequestError as e:
            st.error(f"❌ Speech Recognition Error: {str(e)}")
            return ""

# --- AI CODE GENERATION ---
def generate_uwu_code(prompt):
    # Placeholder for Local Model Call
    uwu_code = f"(✿◕‿◕) ~ Processing: {prompt} ~ (◕‿◕✿)"
    return uwu_code

# --- LIVE CHAT ASSISTANT ---
def chat_with_ai():
    st.sidebar.header("💬 AI Chat Assistant")
    user_query = st.sidebar.text_input("Ask me anything about UwU coding!")
    if user_query:
        response = get_code_suggestion(user_query)
        st.sidebar.write("🤖 AI says:", response)

# --- MAIN APP ---
def main():
    set_ui_config()
    render_app_header()
    chat_with_ai()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        user_prompt = st.text_area("📝 Describe your vision for UwU code 🚀",
                                   placeholder="e.g. Print 'Hello, World!' in UwU language", height=150)
        if st.button("✨ Auto-Complete Code!"):
            suggestion = get_code_suggestion(user_prompt)
            st.text_area("💡 Suggested Code:", suggestion, height=150)
    with col2:
        if st.button("📸 Capture from Camera!"):
            capture_camera_image()
        if st.button("🎙️ Speak to UwU!"):
            speech_text = recognize_speech()
            if speech_text:
                user_prompt += " " + speech_text
    
    if user_prompt:
        st.markdown("**🔎 UwU Code Preview:**")
        st.code(f"(✿◕‿◕) ~ Processing: {user_prompt} ~ (◕‿◕✿)", language="plaintext")
    
    col1, col2, col3 = st.columns(3)
    with col2:
       if st.button("✨ Generate UwU Code!"):
          if user_prompt:
              with st.spinner("Generating UwU Code... 💫"):
                   start_time = time.time()
                   uwu_code = generate_uwu_code(user_prompt)
                   if uwu_code:
                      end_time = time.time()
                      st.success(f"✅ UwU Code Generated in {end_time - start_time:.2f} seconds!")
                      st.code(uwu_code, language="uwu", line_numbers=True)
                   else:
                       st.error("❌ Failed to generate UwU code. Try again!")
          else:
             st.warning("⚠ Please enter a description!")
    
    st.markdown("""
        <div class="footer">
            Made with ❤ for UwU lovers! By <b>Nitish, Shivam, Shubham, Sourish</b> ✨
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
