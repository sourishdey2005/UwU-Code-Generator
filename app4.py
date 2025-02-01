import streamlit as st
import google.generativeai as genai
import time

# Expose API Key
GEMINI_API_KEY = "************************"

# Configure API once
genai.configure(api_key=GEMINI_API_KEY)

# --- UI CONFIGURATION ---
def set_ui_config():
    st.set_page_config(page_title="UwU Code Generator X 🚀", page_icon="🤖", layout="wide")
    st.markdown("""
        <style>
            body { background: linear-gradient(-45deg, #011C37,#003466, #080B0D);
                   background-size: 400% 400%; animation: gradient 20s ease infinite; color: #ddd; }
            .title { font-size: 2.2em; font-weight: bold; text-align: center; margin-bottom: 10px; }
            .footer { position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px 0px 15px; 
                      font-size: 1em; font-weight: bold; background: rgba(0, 0, 0, 0.5); }
            .stButton button { background-color: #33FFC2 !important; color: black !important; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

def render_app_header():
    st.markdown("<div class='title'>🤖 UwU Code Generator X 🚀</div>", unsafe_allow_html=True)
    st.markdown("Transforming thoughts to UwU code like never before 💫", unsafe_allow_html=True)

# --- API CALL FUNCTION ---
def generate_uwu_code(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"Convert the following task into UwU esolang code:\n\n{prompt}")
        return response.text
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        return None

# --- MAIN APP ---
def main():
    set_ui_config()
    render_app_header()

    user_prompt = st.text_area("📝 Describe your vision for UwU code 🚀",
                               placeholder="e.g. Print 'Hello, World!' in UwU language", height=120)

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
