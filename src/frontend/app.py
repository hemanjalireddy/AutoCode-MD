import streamlit as st
import requests
import os
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AutoCode MD",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Docker networking
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_URL = f"{BACKEND_URL}/api/v1"


# --- MAIN APP LAYOUT ---

# (Removed st.title to get rid of the header text)

# Container for the main dashboard content
dashboard = st.container()

with dashboard:
    # --- SECTION 1: UPLOAD & ACTIONS ---
    col_upload, col_action = st.columns([2, 1])
    
    with col_upload:
        # label_visibility="collapsed" hides the "Upload Scanned Note" label
        uploaded_file = st.file_uploader("Upload Scanned Note", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

    with col_action:
        # Added a small spacer to align button with the uploader box
        st.write("") 
        analyze_btn = st.button("🚀 Analyze Document", use_container_width=True)

    # --- LOGIC TRIGGER ---
    if uploaded_file and analyze_btn:
        with st.spinner("Analyzing..."):
            try:
                # --- API CALL ---
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{API_URL}/digitize", files=files)
                
                if response.status_code == 200:
                    data = response.json().get('data', {})
                    extracted = data.get('extracted_data', {})
                    coding = data.get('coding_result', {})

                    # --- UI SECTION: SUCCESS BANNER ---
                    st.markdown("""
                        <div class="success-box">
                            <span style='font-size: 1.2rem;'>✅</span> Analysis Complete!
                        </div>
                    """, unsafe_allow_html=True)

                    # --- UI SECTION: HANDWRITTEN TEXT ---
                    with st.expander("👁️ Handwritten Text Extraction", expanded=True):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.text_area("Diagnosis / Impression", value=extracted.get('diagnosis_text', ''), height=100)
                        with col2:
                            st.text_area("Procedures / Meds", value=extracted.get('procedure_text', ''), height=100)

                    # --- UI SECTION: BILLING CODES ---
                    st.markdown("### 🏷️ Assigned Billing Codes")
                    
                    metric_col1, metric_col2, metric_col3 = st.columns([1.5, 1.5, 1.5])
                    
                    with metric_col1:
                        st.metric("ICD-10 Diagnosis", coding.get('icd10_code', 'N/A'), delta="Primary")
                    
                    with metric_col2:
                        conf = coding.get('confidence_score', 0.0)
                        st.metric("Confidence", f"{conf:.1%}")
                        st.progress(conf)
                    
                    with metric_col3:
                        st.metric("CPT Procedure", coding.get('cpt_code', 'None'))

                    # --- UI SECTION: REASONING ---
                    reasoning_text = coding.get('reasoning', 'No reasoning provided.')
                    st.markdown(f"""
                        <div class="reasoning-box">
                            <span class="reasoning-label">Reasoning:</span>
                            {reasoning_text}
                        </div>
                    """, unsafe_allow_html=True)

                else:
                    st.error(f"Analysis Failed: {response.text}")

            except Exception as e:
                st.error(f"Connection Error: {e}")

    elif not uploaded_file:
        # Just a clean hint since the big drag/drop text is gone
        st.info("👆 Upload a patient record to begin.")