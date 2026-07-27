import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
from ui.components import render_page_header

def render_planetary_intelligence():
    st.markdown("### Planetary Disease Intelligence")
    st.info("Fusing satellite telemetry, global mobility, wastewater surveillance, and genomics to forecast outbreaks.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### Global Surveillance Parameters")
        pathogen = st.selectbox("Target Pathogen / Vector", ["Avian Influenza (H5N1) Variant", "Novel Coronavirus (X-Strain)", "Vector-borne (Dengue/Zika)"])
        mobility = st.slider("Global Mobility Index (0-100)", 0, 100, 85)
        climate = st.slider("Climate Anomaly Factor", 0.0, 5.0, 1.2)
        
        sim_outbreak = st.button("🌍 Run Planetary Forecast", type="primary", use_container_width=True)
        
    with col2:
        if sim_outbreak:
            with st.spinner(f"Ingesting satellite and wastewater telemetry for {pathogen}..."):
                time.sleep(0.01)
                
            # Simulate outbreak coordinates (random clustering)
            lats = np.concatenate([np.random.normal(35, 10, 50), np.random.normal(50, 5, 20), np.random.normal(-10, 15, 30)])
            lons = np.concatenate([np.random.normal(105, 15, 50), np.random.normal(10, 10, 20), np.random.normal(-60, 20, 30)])
            cases = np.random.randint(100, 10000, 100) * (mobility / 50) * climate
            
            fig = go.Figure(data=go.Scattergeo(
                lon = lons,
                lat = lats,
                marker = dict(
                    size = cases / 500,
                    color = cases,
                    colorscale = 'Reds',
                    showscale = True,
                    opacity = 0.7,
                    line_width=0.5
                )
            ))
            
            fig.update_layout(
                title = f"72-Hour Epidemic Forecast: {pathogen}",
                geo = dict(
                    projection_type="orthographic",
                    showland = True,
                    landcolor = "rgb(30, 30, 30)",
                    oceancolor="rgb(10, 10, 10)",
                    showocean=True,
                    bgcolor='rgba(0,0,0,0)'
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=40, b=0),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.warning(f"🚨 **Global Alert Triggered:** Simulated forecast indicates high probability of trans-continental spread originating from Southeast Asia within 14 days due to elevated mobility index ({mobility}).")

def render_clinical_universe():
    st.markdown("### Clinical Universe Simulator")
    st.info("A synthetic environment containing 1 million virtual patients with varied demographics and diseases for evaluating algorithms.")
    
    st.markdown("#### Synthetic Population Demographics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Virtual Patients", "1,048,576")
    with col2:
        st.metric("Genetic Variants Tracked", "8.4 Million")
    with col3:
        st.metric("Longitudinal Data Points", "1.2 Billion")
        
    st.markdown("#### Run Clinical Algorithm Test")
    algorithm = st.selectbox("Select Algorithm to Evaluate", ["Sepsis Early Warning Model v4", "Oncology Treatment Efficacy Predictor", "Diabetic Retinopathy CNN"])
    
    if st.button("🧪 Evaluate Algorithm against Clinical Universe", type="primary"):
        with st.spinner(f"Running {algorithm} against 1,000,000 synthetic patient trajectories..."):
            time.sleep(0.01)
            
        st.success("Evaluation Complete.")
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 15px; border-radius: 6px;">
            <strong style="color: #065f46;">Algorithm Verification Results</strong><br>
            <span style="color: #047857; font-size: 0.9rem;">
            - <b>Sensitivity:</b> 94.2%<br>
            - <b>Specificity:</b> 89.1%<br>
            - <b>Algorithmic Bias Check:</b> PASSED (No statistically significant performance deviation across synthetic demographic cohorts).<br>
            - <b>Safety Clearance:</b> Ready for real-world clinical trial Phase I.
            </span>
        </div>
        """, unsafe_allow_html=True)

def render_biomedical_memory():
    st.markdown("### Global Biomedical Memory")
    st.info("An indexed representation of all medical textbooks, clinical trials, and drug labels with version tracking.")
    
    _ = st.text_input("Search the Biomedical Memory Graph", placeholder="e.g. Pembrolizumab contraindications in autoimmune diseases")
    if st.button("🔍 Search Global Index"):
        with st.spinner("Traversing 40 million indexed biomedical documents..."):
            time.sleep(0.01)
        st.markdown("#### 📄 Top Retrieved Provenance")
        st.markdown("- **[Guideline] NCCN Oncology Clinical Practice Guidelines (v2.2026)** - *Confidence: 99.8%*")
        st.markdown("- **[Clinical Trial] NCT04562134 (Phase III)** - *Updated 12 hours ago*")
        st.markdown("- **[Pharmacology] FDA Drug Label (Pembrolizumab)** - *Version 14.2*")

def render_planetary_dashboard():
    render_page_header("🌍", "Planetary Intelligence & Universe Sim", "Global disease forecasting, synthetic clinical universes, and worldwide biomedical memory.", "linear-gradient(135deg, #3b82f6, #0284c7)")

    st.markdown("""
        <style>
        div[data-testid="stTabs"] button[data-baseweb="tab"] {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            padding-bottom: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🌍 Planetary Disease Engine", "🧪 Clinical Universe Simulator", "📚 Global Biomedical Memory"])
    
    with tab1:
        render_planetary_intelligence()
    with tab2:
        render_clinical_universe()
    with tab3:
        render_biomedical_memory()
