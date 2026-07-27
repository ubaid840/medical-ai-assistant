import streamlit as st
import plotly.graph_objects as go
import time
from ui.components import render_page_header

def render_hospital_command_center():
    st.markdown("""
        <div style="
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 30px;
        color: #0f172a;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255,255,255,0.8);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.8);
        ">
        <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(16,185,129,0.15) 0%, transparent 70%); border-radius: 50%; pointer-events: none;"></div>
        
        <h3 style="margin-top: 0; font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #1e293b, #334155); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Autonomous Hospital Command Center</h3>
        <p style="color: #64748b; font-size: 1.05rem; margin-bottom: 0;">Predictive resource load balancing and autonomous staff routing across all clinical departments.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Simulate data
    departments = ["Emergency Room", "Intensive Care Unit", "Surgical OR", "Pharmacy", "Laboratory", "Radiology"]
    current_load = [92, 85, 100, 60, 75, 80]
    predicted_load_12h = [115, 90, 70, 85, 95, 60]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Real-Time Departmental Load & 12-Hour Forecast")
        fig = go.Figure(data=[
            go.Bar(name='Current Utilization %', x=departments, y=current_load, marker_color='#3b82f6'),
            go.Bar(name='Predicted Utilization % (+12h)', x=departments, y=predicted_load_12h, marker_color='#ef4444')
        ])
        fig.update_layout(barmode='group', height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        fig.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Critical Capacity (100%)")
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("#### 🚨 AI Predictive Bottlenecks")
        
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 15px; border-radius: 6px; margin-bottom: 15px;">
            <strong style="color: #991b1b;">Emergency Room Overflow</strong><br>
            <span style="color: #b91c1c; font-size: 0.9rem;">Forecasted 115% capacity in 4 hours due to incoming multi-vehicle trauma.</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; padding: 15px; border-radius: 6px; margin-bottom: 15px;">
            <strong style="color: #b45309;">Laboratory Processing Delay</strong><br>
            <span style="color: #d97706; font-size: 0.9rem;">Predicted 95% utilization. Chemistry panels delayed by 45 mins.</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ Autonomously Re-Route Staff", type="primary", use_container_width=True):
            with st.spinner("AI calculating optimal staff reallocation..."):
                time.sleep(0.01)
            st.success("Staff Reallocated: 2 Surgical Nurses moved to ER Triage. 1 Pharmacist shifted to Lab Chemistry verification.")

def render_hospital():
    render_page_header("🏥", "Enterprise Hospital OS", "Autonomous orchestration of hospital resources, predictive capacity, and workflow.", "linear-gradient(135deg, #10b981, #059669)")
    
    # Custom CSS for tabs in this section
    st.markdown("""
        <style>
        div[data-testid="stTabs"] button[data-baseweb="tab"] {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            padding-bottom: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["⚡ Command Center OS", "📊 Department Flow Analytics"])
    with tab1: render_hospital_command_center()
    with tab2: st.info("Department Flow historical analytics goes here.")
