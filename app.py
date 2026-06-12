import streamlit as st
import replicate
import os
from PIL import Image
from io import BytesIO

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AI Image Generator", 
    page_icon="🎨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mobile-friendly CSS
st.markdown("""
    <style>
    /* Mobile Dark Theme */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Hide default streamlit header on mobile */
    header {visibility: hidden;}
    
    /* Mobile-friendly inputs */
    .stTextInput > div > div > input {
        font-size: 18px;
        padding: 15px;
    }
    
    /* Bigger buttons for touch */
    .stButton > button {
        padding: 15px 30px;
        font-size: 18px;
        border-radius: 12px;
    }
    
    /* Full width on mobile */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIC ---
def generate_image(prompt, aspect_ratio="1:1", guidance=7.5):
    try:
        output = replicate.run(
            "stability-ai/stable-diffusion:39ed52f2a78e9348f5d894c2c321e1e49b6ae5a3f73631f7b8c6d683c98e0d65",
            input={
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "guidance_scale": guidance,
                "num_inference_steps": 30
            }
        )
        return output[0]
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- UI ---
st.title("🎨 AI Image Generator")
st.caption("Create stunning images with AI")

# Sidebar for API Token (collapsible on mobile)
with st.sidebar:
    st.header("⚙️ Settings")
    api_token = st.text_input("API Token", type="password", help="Get from replicate.com")
    
    st.divider()
    
    guidance = st.slider("Creativity", 1.0, 20.0, 7.5)
    
    st.info("💡 Tip: Be descriptive! 'A realistic cyberpunk cat with neon eyes, rainy city background, cinematic lighting, 8k quality'")

# Main Input
prompt = st.text_area("Describe your image...", height=100, placeholder="Enter your prompt here...")

# Options
col1, col2 = st.columns(2)
with col1:
    ratio = st.selectbox("Aspect Ratio", ["1:1", "16:9", "9:16", "21:9"])
with col2:
    style = st.selectbox("Style", ["Realistic", "Anime", "3D Render", "Oil Painting", "Cyberpunk"])

# Generate Button
if st.button("🎨 Generate Image", type="primary", use_container_width=True):
    if not prompt:
        st.warning("Please enter a prompt!")
    elif not api_token:
        st.warning("Please enter your API Token!")
    else:
        os.environ["REPLICATE_API_TOKEN"] = api_token
        
        full_prompt = f"{prompt}, {style} style"
        
        with st.spinner("Creating your image... 🎨"):
            image_url = generate_image(full_prompt, ratio, guidance)
            
            if image_url:
                st.success("✨ Done!")
                st.image(image_url, caption=prompt, use_container_width=True)
                
                # Download button
                st.download_button("📥 Download", data=image_url, file_name="ai-art.png")

# History section
st.divider()
st.subheader("📸 Recent Generations")