import streamlit as st
import google.generativeai as genai
from groq import Groq
from PIL import Image
import os

# --- 1. CONFIGURATION (SECURE) ---
# Professional Practice: Accessing keys from the secure Streamlit Secrets vault
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("API Keys not found in Streamlit Secrets. Please configure them in the 'Advanced Settings' of your dashboard.")
    st.stop()

# Initialize clients using secrets
genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

# Track usage for the Enterprise Dashboard
if 'credits_used' not in st.session_state:
    st.session_state.credits_used = 0

st.set_page_config(page_title="Vibe-Check Pro", page_icon="✨", layout="wide")

# --- 2. THE UI ---
st.title("✨ Vibe-Check: Enterprise Multi-Agent")
st.markdown("Automated Brand DNA with **Gemini 3-flash-preview** & **Llama 3.3 (via Groq)**")

uploaded_file = st.file_uploader("Upload Brand Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Client Sample", use_container_width=True)
    
    if st.button("Generate Professional Audit"):
        with st.spinner("🧬 Agent 1: Extracting Visual DNA..."):
            try:
                # Step 1: Gemini Vision Analysis
                gemini_model = genai.GenerativeModel('gemini-3-flash-preview')
                vision_prompt = "Analyze this image and provide technical facts: HEX colors, font style, and aesthetic vibe."
                dna_report = gemini_model.generate_content([vision_prompt, image]).text
                
                st.subheader("🧪 Phase 1: Visual DNA (Gemini)")
                st.write(dna_report)

                # Step 2: Groq Creative Refinement
                with st.spinner("👂 Agent 2: Crafting Creative Strategy..."):
                    chat_completion = groq_client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "You are a Senior Creative Director specialized in 2026 digital trends."},
                            {"role": "user", "content": f"Based on this DNA: {dna_report}, write 3 high-converting viral ad hooks."}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    
                    st.subheader("💡 Phase 2: Creative Ad Hooks (Groq)")
                    st.success(chat_completion.choices[0].message.content)

                st.session_state.credits_used += 1

            except Exception as e:
                st.error(f"System Error: {e}")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("🏢 Enterprise Dashboard")
    st.metric("Total Audits Done", f"{st.session_state.credits_used}")
    st.write("---")
    st.info("**Architecture:** Multi-Modal Agentic Workflow (Python-Native)")

    st.write("Logged in as: **Professional Brand Strategist**")
