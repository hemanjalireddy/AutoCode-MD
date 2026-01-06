import streamlit as st
import requests
import os

# Docker networking: 'backend' is the container name
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="CuraLogic - Day 2", layout="wide")
st.title("🩺 Medical Note Digitizer")

uploaded_file = st.file_uploader("Upload Doctor's Note", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption="Scanned Note", use_container_width=True)
    
    with col2:
        if st.button("Analyze with Llama Vision"):
            with st.spinner("Reading handwriting..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{BACKEND_URL}/api/v1/digitize", files=files)
                    
                    if response.status_code == 200:
                        st.success("Analysis Complete!")
                        st.json(response.json()['data'])
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")