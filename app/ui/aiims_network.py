import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

def generate_aiims_data():
    hospitals = [
        "AIIMS New Delhi",
        "AIIMS Jodhpur",
        "AIIMS Bhopal",
        "AIIMS Rishikesh",
        "AIIMS Bhubaneswar",
        "AIIMS Patna",
        "AIIMS Raipur"
    ]
    
    data = []
    for h in hospitals:
        icu_capacity = np.random.randint(50, 150)
        icu_occupancy = np.random.randint(40, icu_capacity + 10)
        er_wait = np.random.randint(10, 120)
        trauma_level = np.random.choice(["Level 1", "Level 2"])
        
        status = "Critical" if (icu_occupancy / icu_capacity) > 0.95 else ("Warning" if (icu_occupancy / icu_capacity) > 0.85 else "Stable")
        
        data.append({
            "Hospital": h,
            "ICU Capacity": f"{icu_occupancy}/{icu_capacity}",
            "Load %": round((icu_occupancy / icu_capacity) * 100, 1),
            "ER Wait (mins)": er_wait,
            "Trauma Status": trauma_level,
            "Status": status
        })
    return pd.DataFrame(data)

def render_aiims_network():
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a8a, #1e40af); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #3b82f6; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <div style="font-size: 50px; margin-bottom: 10px;">🏥</div>
            <h1 style="color: #ffffff; margin: 0; font-weight: 900; letter-spacing: 2px;">AIIMS National Network</h1>
            <h3 style="color: #bfdbfe; margin: 5px 0 0 0; font-weight: 400; font-size: 1.2rem;">All India Institute of Medical Sciences Interoperability Hub</h3>
        </div>
    """, unsafe_allow_html=True)

    df = generate_aiims_data()
    
    st.markdown("### Real-Time Network Triage")
    
    # Network metrics
    col1, col2, col3, col4 = st.columns(4)
    avg_load = df['Load %'].mean()
    col1.metric("National ICU Load", f"{avg_load:.1f}%", f"{avg_load - 80:.1f}% from baseline", delta_color="inverse")
    col2.metric("Active ER Wait Avg", f"{df['ER Wait (mins)'].mean():.0f} mins", "-5 mins")
    col3.metric("Critical Nodes", len(df[df['Status'] == 'Critical']), "+1 since last hour", delta_color="inverse")
    col4.metric("AI Interventions Today", "1,244", "+12%")
    
    st.divider()
    
    # Hospital Status Grid
    st.markdown("#### Campus Live Status")
    
    for _, row in df.iterrows():
        color = "#ef4444" if row['Status'] == "Critical" else ("#f59e0b" if row['Status'] == "Warning" else "#10b981")
        st.markdown(f"""
        <div style="border-left: 5px solid {color}; padding: 15px; margin-bottom: 10px; background: rgba(255,255,255,0.7); border-radius: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <div>
                <strong style="font-size: 1.2rem; color: #0f172a;">{row['Hospital']}</strong><br>
                <span style="color: #475569; font-size: 0.9rem;">Trauma Level: {row['Trauma Status']}</span>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 0.85rem; color: #64748b;">ICU Load</span><br>
                <strong style="color: {color}; font-size: 1.1rem;">{row['Load %']}% ({row['ICU Capacity']})</strong>
            </div>
            <div style="text-align: right; min-width: 120px;">
                <span style="font-size: 0.85rem; color: #64748b;">ER Wait</span><br>
                <strong style="font-size: 1.1rem;">{row['ER Wait (mins)']} min</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    
    # AI Transfer Orchestration
    st.markdown("### Autonomous Transfer Orchestration")
    st.info("The AI continuously monitors national loads to preemptively re-route incoming severe trauma to campuses with high ICU elasticity.")
    
    col_t1, col_t2 = st.columns([1, 2])
    with col_t1:
        st.markdown("##### Immediate Triage Required")
        st.error("🚨 Mass Casualty Incident (MCI) detected near Jodhpur. AIIMS Jodhpur projected to hit 110% capacity in 45 mins.")
        if st.button("🤖 Activate AI Load Balancing", type="primary", use_container_width=True):
            with st.spinner("AI computing optimal national re-routing trajectories..."):
                time.sleep(0.01)
            
            # Map logic
            fig = go.Figure(go.Sankey(
                node = dict(
                  pad = 15,
                  thickness = 20,
                  line = dict(color = "black", width = 0.5),
                  label = ["Incident (Jodhpur)", "AIIMS Jodhpur", "AIIMS Delhi", "AIIMS Bhopal", "AIIMS Rishikesh"],
                  color = ["#ef4444", "#f59e0b", "#10b981", "#10b981", "#3b82f6"]
                ),
                link = dict(
                  source = [0, 0, 0, 1], # indices correspond to labels
                  target = [1, 2, 3, 4],
                  value = [40, 25, 15, 10],
                  color = ["rgba(239, 68, 68, 0.4)", "rgba(16, 185, 129, 0.4)", "rgba(16, 185, 129, 0.4)", "rgba(59, 130, 246, 0.4)"]
              )))
            fig.update_layout(title_text="AI Recommended Patient Re-Routing (Sankey Flow)", font_size=10, height=350, margin=dict(t=30, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
            
            with col_t2:
                st.plotly_chart(fig, use_container_width=True)
                st.success("✅ Protocol Active: 40 patients remain at AIIMS Jodhpur. 40 patients auto-diverted to AIIMS Delhi & Bhopal via medevac.")
