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

def render_healthcare_directory():
    st.markdown("### 🏥 Healthcare Directory & Logistics")
    st.info("Simulated API connections to local hospital networks and pharmacy inventories.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👨‍⚕️ Nearby Specialist Finder")
        specialty = st.selectbox("Select Specialty", ["Cardiologist", "Neurologist", "Pediatrician", "Dermatologist", "Oncologist"])
        insurance = st.selectbox("Insurance Provider Filter", ["All (Out of Pocket)", "BlueCross BlueShield", "Aetna", "Cigna", "UnitedHealthcare", "Medicare"])
        zipcode = st.text_input("Enter Zip Code / Pincode", value="10001")
        
        if st.button("🔍 Search Specialists"):
            with st.spinner("Querying local provider networks..."):
                time.sleep(0.01)
            st.success(f"Found 3 {specialty}s near {zipcode} accepting {insurance}:")
            
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <strong style="font-size: 1.1rem; color: #0f172a;">Dr. Sarah Jenkins, MD ({specialty})</strong><br>
                <span style="color: #64748b; font-size: 0.9rem;">📍 0.8 miles away | ⭐ 4.9/5 (124 reviews)</span><br>
                <span style="color: #10b981; font-weight: bold; font-size: 0.85rem;">✓ Accepts {insurance}</span><br>
                <button style="margin-top: 8px; background: #3b82f6; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">📅 Book Earliest: Tomorrow, 10:30 AM</button>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <strong style="font-size: 1.1rem; color: #0f172a;">Dr. Michael Chen, DO ({specialty})</strong><br>
                <span style="color: #64748b; font-size: 0.9rem;">📍 2.1 miles away | ⭐ 4.7/5 (89 reviews)</span><br>
                <span style="color: #10b981; font-weight: bold; font-size: 0.85rem;">✓ Accepts {insurance}</span><br>
                <button style="margin-top: 8px; background: #3b82f6; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">📅 Book Earliest: Thu, 2:15 PM</button>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 💊 Pharmacy Stock Locator")
        medication = st.text_input("Search Medication (e.g. Amoxicillin, Ozempic)", value="Ozempic 1mg Pen")
        radius = st.slider("Search Radius (miles)", 1, 25, 5)
        
        if st.button("📍 Check Live Inventory"):
            with st.spinner("Pinging live pharmacy inventory APIs..."):
                time.sleep(0.01)
            
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #ef4444; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <strong style="font-size: 1.1rem; color: #0f172a;">CVS Pharmacy (Main St)</strong><br>
                <span style="color: #64748b; font-size: 0.9rem;">📍 1.2 miles away</span><br>
                <span style="color: #ef4444; font-weight: bold; font-size: 0.9rem;">❌ Out of Stock - {medication}</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #10b981; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <strong style="font-size: 1.1rem; color: #0f172a;">Walgreens (Oak Ave)</strong><br>
                <span style="color: #64748b; font-size: 0.9rem;">📍 3.5 miles away</span><br>
                <span style="color: #10b981; font-weight: bold; font-size: 0.9rem;">✅ In Stock: 4 units - {medication}</span><br>
                <button style="margin-top: 8px; background: #10b981; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">🧾 Send Digital Prescription Here</button>
            </div>
            """, unsafe_allow_html=True)

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
    
    tab1, tab2, tab3 = st.tabs(["⚡ Command Center OS", "📊 Department Flow Analytics", "🏥 Healthcare Directory & Logistics"])
    with tab1: render_hospital_command_center()
    with tab2: st.info("Department Flow historical analytics goes here.")
    with tab3: render_healthcare_directory()
