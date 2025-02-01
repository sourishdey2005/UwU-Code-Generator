import streamlit as st
import google.generativeai as genai
import time
import random
import json
import os
from streamlit_lottie import st_lottie

# --- API CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyCOvjCXNr-24ZVABhxMqbbD9mV7Wlr1k5U"  # Replace with your key
genai.configure(api_key=GEMINI_API_KEY)

# --- UI CONFIGURATION ---
def set_ui_config():
    st.set_page_config(page_title="UwU Code Generator X 🚀", page_icon="🤖", layout="wide")
    st.markdown("""
        <style>
            @keyframes glow {
                0% { text-shadow: 0 0 5px #33FFC2, 0 0 10px #33FFC2, 0 0 15px #33FFC2; }
                100% { text-shadow: 0 0 10px #ff33cc, 0 0 20px #ff33cc, 0 0 30px #ff33cc; }
            }
            body { background: linear-gradient(120deg, #011C37, #0B3D91, #080B0D);
                   background-size: 400% 400%; animation: gradient 20s ease infinite; color: #ddd; }
            .title { font-size: 3em; font-weight: bold; text-align: center; animation: glow 1.5s infinite alternate; }
            .subtitle { font-size: 1.2em; text-align: center; color: #bbb; margin-bottom: 20px; }
            .footer { position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; 
                      font-size: 1em; font-weight: bold; background: rgba(0, 0, 0, 0.5); }
            .stButton button { background-color: #FF33CC !important; color: white !important; font-weight: bold; }
            .stTextArea textarea { background-color: #222 !important; color: #ddd !important; border: 1px solid #555;}
            .stCode pre { background-color: #1a1a1a !important; border: 1px solid #333; padding: 15px; }
        </style>
    """, unsafe_allow_html=True)

def render_app_header():
    st.markdown("<div class='title'>🤖 UwU Code Generator X 🚀</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Turn your ideas into UwU code effortlessly! 💫</div>", unsafe_allow_html=True)

# --- LOAD ANIMATIONS ---
def load_lottie_animation(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None

def display_random_animation():
    animations = [
        "lottie_animations/cute_robot.json",
        "lottie_animations/cat_coding.json",
        "lottie_animations/brain.json",
        "lottie_animations/flying_heart.json",
        "lottie_animations/loading.json"
    ]
    animation = random.choice(animations)
    animation_data = load_lottie_animation(animation)
    if animation_data:
        st_lottie(animation_data, height=150, speed=1, loop=True, quality='medium')

# --- API CALL FUNCTION ---
def generate_uwu_code(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Convert this into UwU esolang with comments and optimizations:\n\n{prompt}")
        return response.text
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        return None

# --- MAIN APP ---
def main():
    set_ui_config()
    render_app_header()
    
    col1, col2 = st.columns([3,1])
    with col1:
        user_prompt = st.text_area("📝 Describe your vision for UwU code 🚀",
                                   placeholder="e.g. Print 'Hello, World!' in UwU language", height=150)
        char_count = len(user_prompt)
        st.markdown(f"<p style='color:#bbb;'>Character Count: {char_count}</p>", unsafe_allow_html=True)
    with col2:
        display_random_animation()
    
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
