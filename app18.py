import streamlit as st
import google.generativeai as genai
import speech_recognition as sr  # Voice Input
import cv2  # Camera Integration
import pytesseract  # OCR for Handwritten Text Recognition
import sqlite3  # User authentication & storage
from uuid import uuid4  # Unique ID for versioning

# --- CONFIGURE TESSERACT OCR (Windows Users) ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- API CONFIGURATION ---
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# --- DATABASE FOR USER AUTHENTICATION ---
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

# --- INITIALIZE DATABASE ---
init_db()

# --- USER AUTHENTICATION PAGE ---
def login_page():
    st.sidebar.subheader("🔑 User Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login = st.sidebar.button("Login")
    register = st.sidebar.button("Register")
    
    if login:
        if login_user(username, password):
            st.session_state["authenticated"] = True
            st.success("✅ Logged in successfully!")
        else:
            st.error("❌ Invalid username or password")
    
    if register:
        if register_user(username, password):
            st.success("✅ Registered successfully! Please login.")
        else:
            st.error("❌ Username already exists!")

# --- MAIN APP ---
def main():
    if "authenticated" not in st.session_state:
        login_page()
        return
    
    st.markdown("<h1 style='text-align: center;'>🤖 UwU Code Generator X 🚀</h1>", unsafe_allow_html=True)
    st.sidebar.header("🔧 Advanced Features")
    
    language_choice = st.sidebar.selectbox("🌍 Choose Programming Language", ["UwU", "Python", "JavaScript", "Rust", "C++", "C++ to UwU"])
    user_prompt = st.text_area("📝 Describe your vision for UwU code 🚀", placeholder="e.g. Print 'Hello, World!' in UwU language", height=150)
    
    # --- Voice Input ---
    if st.button("🎙️ Voice Input"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎙️ Speak now...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                user_prompt += " " + text
                st.text_area("📝 Updated Prompt from Voice:", user_prompt, height=150)
            except:
                st.error("❌ Speech recognition failed")

    # --- Image Text Extraction (OCR) ---
    if st.button("📸 Capture Photo"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            st.image(frame, channels="BGR", caption="📸 Captured Image")
            try:
                text = pytesseract.image_to_string(frame)
                user_prompt += " " + text
                st.text_area("📝 Extracted Text from Image:", user_prompt, height=150)
            except Exception as e:
                st.error(f"❌ OCR Failed: {e}")
        else:
            st.error("❌ Failed to capture image")

    # --- C++ to UwU Code Conversion ---
    if language_choice == "C++ to UwU":
        cpp_code = st.text_area("🔄 Paste C++ Code to Convert:")
        if st.button("🚀 Convert to UwU Code!"):
            uwu_code = get_code_suggestion(f"Convert this C++ code to UwU: {cpp_code}")
            st.code(uwu_code, language="uwu", line_numbers=True)
    
    # --- Code Generation ---
    else:
        if st.button("✨ Generate Code!"):
            if user_prompt:
                uwu_code = generate_code_in_language(user_prompt, language_choice)
                st.code(uwu_code, language=language_choice.lower(), line_numbers=True)
            else:
                st.warning("⚠ Please enter a description!")

    # --- Footer ---
    st.markdown("""
        <div style="text-align:center; padding-top:20px;">
            <b>Made with ❤ for UwU lovers! By Nitish, Shivam, Shubham, Sourish ✨</b>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
