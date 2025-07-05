import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load token from .env
load_dotenv()
#HF_TOKEN = os.getenv("HF_TOKEN") # this is used if I want it to run on my pc 
HF_TOKEN = st.secrets["HF_TOKEN"] # this is used if I want it to run on Streamlit cloud

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

st.set_page_config(page_title="🖌️ AI Art Generator (HuggingFace)", layout="centered")
st.title("🎨 AI Art Generator using Stable Diffusion")

prompt = st.text_input("Enter a creative prompt:", placeholder="e.g. A futuristic cyberpunk dragon")

if st.button("Generate Image") and prompt:
    with st.spinner("Creating image..."):
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
#            st.image(image, caption="✨ AI Art Created", use_column_width=True)
            st.image(image, caption="✨ AI Art Created", use_container_width=True)


            # Download option
            st.download_button("📥 Download Image", data=response.content, file_name="ai_art.png", mime="image/png")
        else:
            st.error(f"Generation failed! Code {response.status_code}")
else:
    st.info("Type something creative and click 'Generate Image'")

