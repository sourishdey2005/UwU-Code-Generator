import streamlit as st
import google.generativeai as genai
import time
import random
import json
import os
import speech_recognition as sr  # Voice Input
import cv2  # Camera Integration
import numpy as np
import pytesseract  # OCR for Handwritten Text Recognition
import base64  # File Download
import tempfile  # Temporary file handling
import threading  # For real-time collaboration
import difflib  # Code version comparison
import hashlib  # Unique hash generation for code versioning
import sqlite3  # User authentication & storage
import subprocess  # Code execution
import websockets  # Real-time collaboration
import asyncio
from streamlit_lottie import st_lottie
from transformers import pipeline  # AI-powered auto-complete
from uuid import uuid4  # Unique ID for versioning

# --- API CONFIGURATION ---
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your key
genai.configure(api_key=GEMINI_API_KEY)

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
auto_complete = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

def get_code_suggestion(prompt):
    response = auto_complete(f"Convert the following task into UwU esolang code with detailed comments and optimization:\n{prompt}", max_length=200, num_return_sequences=1)
    return response[0]['generated_text']

# --- MULTI-LANGUAGE CODE GENERATION ---
def generate_code_in_language(prompt, language):
    if language.lower() == "uwu":
        return get_code_suggestion(prompt)
    formatted_prompt = f"Generate {language} code for: {prompt} with detailed comments and optimization."
    return get_code_suggestion(formatted_prompt)

# --- VOICE INPUT FEATURE ---
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

# --- PHOTO CAPTURE FEATURE ---
def capture_photo():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        st.image(frame, channels="BGR", caption="📸 Captured Image")
        return frame
    else:
        st.error("❌ Failed to capture image")
        return None

# --- IMAGE TO TEXT USING OCR ---
def recognize_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# --- ENHANCED UI ---
st.markdown("""
    <style>
        .title { font-size: 3em; font-weight: bold; text-align: center; color: #33FFC2; }
        .subtitle { font-size: 1.5em; text-align: center; color: #bbb; margin-bottom: 20px; }
        .stTextArea textarea { background-color: #222 !important; color: #ddd !important; border: 1px solid #555; }
        .stCode pre { background-color: #1a1a1a !important; border: 1px solid #333; padding: 15px; }
    </style>
""", unsafe_allow_html=True)

def render_app_header():
    st.markdown("<div class='title'>🤖 UwU Code Generator X 🚀</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Turn your ideas into UwU code effortlessly! 💫</div>", unsafe_allow_html=True)

# --- MAIN APP ---
def main():
    render_app_header()
    st.sidebar.header("🔧 Advanced Features")
    
    language_choice = st.sidebar.selectbox("🌍 Choose Programming Language", ["UwU", "Python", "JavaScript", "Rust", "C++", "C++ to UwU"])
    user_prompt = st.text_area("📝 Describe your vision for UwU code 🚀", placeholder="e.g. Print 'Hello, World!' in UwU language", height=150)
    
    if st.button("🎙️ Voice Input"):
        voice_text = recognize_speech()
        if voice_text:
            user_prompt += " " + voice_text
            st.text_area("📝 Updated Prompt from Voice:", user_prompt, height=150)
    
    if st.button("📸 Capture Photo"):
        image = capture_photo()
        if image is not None:
            extracted_text = recognize_text_from_image(image)
            st.text_area("📝 Extracted Text from Image:", extracted_text, height=150)
            user_prompt += " " + extracted_text
    
    if language_choice == "C++ to UwU":
        cpp_code = st.text_area("🔄 Paste C++ Code to Convert:")
        if st.button("🚀 Convert to UwU Code!"):
            uwu_code = get_code_suggestion(f"Convert this C++ code to UwU: {cpp_code}")
            st.code(uwu_code, language="uwu", line_numbers=True)
    else:
        if st.button("✨ Generate Code!"):
            if user_prompt:
                uwu_code = generate_code_in_language(user_prompt, language_choice)
                st.code(uwu_code, language=language_choice.lower(), line_numbers=True)
            else:
                st.warning("⚠ Please enter a description!")
    
    st.markdown("""
        <div class="footer">
            Made with ❤ for UwU lovers! By <b>Nitish, Shivam, Shubham, Sourish</b> ✨
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
