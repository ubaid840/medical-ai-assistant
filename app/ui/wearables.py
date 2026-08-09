import streamlit as st
import numpy as np
import time
import plotly.graph_objects as go

def render_wearables():
    st.markdown("""
        <div style="
        background: linear-gradient(135deg, #10b981 0%, #047857 100%);
        border-radius: 20px;
        padding: 35px 30px;
        color: white;
        box-shadow: 0 20px 40px -10px rgba(16, 185, 129, 0.4);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.2);
        ">
        <div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: rgba(255,255,255,0.1); border-radius: 50%; filter: blur(30px); pointer-events: none;"></div>
        <div style="position: absolute; bottom: -80px; left: 10%; width: 200px; height: 200px; background: rgba(255,255,255,0.15); border-radius: 50%; filter: blur(25px); pointer-events: none;"></div>

        <div style="display: flex; align-items: center; gap: 25px; position: relative; z-index: 1;">
        <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); width: 80px; height: 80px; border-radius: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.4);">
        <span style="font-size: 40px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">⌚</span>
        </div>
        <div>
        <h2 style="margin: 0; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.15);">Live Wearable Data Stream</h2>
        <p style="margin: 8px 0 0 0; font-size: 1.1rem; opacity: 0.95; font-weight: 500; letter-spacing: 0.2px;">Mock Apple Watch / Fitbit telemetry data with real-time AI anomaly detection.</p>
        </div>
        </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Heart Rate", value="72 bpm", delta="-1 bpm")
    with col2:
        st.metric(label="SpO2", value="99%", delta="0%")
    with col3:
        st.metric(label="Blood Glucose (CGM)", value="105 mg/dL", delta="+5 mg/dL", delta_color="inverse")
    with col4:
        st.metric(label="Sleep Score", value="84/100", delta="+2 pts")
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px; margin-top: 25px;">
            <div style="background: linear-gradient(135deg, #ef4444, #b91c1c); color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(239,68,68,0.3);">
                🫀
            </div>
            <div>
                <h3 style="margin: 0; font-weight: 800; color: #0f172a; font-size: 1.5rem; letter-spacing: -0.5px;">Live ECG Feed</h3>
                <p style="margin: 2px 0 0 0; color: #64748b; font-size: 1rem;">Real-time continuous cardiac monitoring.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if st.button("Start Live Stream", type="primary"):
        chart_placeholder = st.empty()
        
        x_data = []
        y_data = []
        for i in range(50):
            x_data.append(i)
            # Generate a mock ECG waveform (P, QRS, T wave approximation)
            noise = np.random.normal(0, 0.05)
            pos = i % 10
            if pos == 5: val = 2.0 + noise # R peak
            elif pos == 4 or pos == 6: val = -0.5 + noise # Q/S
            elif pos == 2: val = 0.3 + noise # P wave
            elif pos == 8: val = 0.4 + noise # T wave
            else: val = noise # Baseline
                
            y_data.append(val)
            
            # Show a moving window
            window_x = x_data[-30:]
            window_y = y_data[-30:]
            
            fig = go.Figure(go.Scatter(x=window_x, y=window_y, mode='lines', line=dict(color='#10b981', width=3)))
            fig.update_layout(xaxis=dict(showgrid=False, zeroline=False, visible=False), 
                              yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-1, 3]),
                              plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                              margin=dict(l=0, r=0, t=0, b=0), height=250)
            
            chart_placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(0.01)
            
        st.success("✅ Stream complete. AI detected no severe arrhythmias during this segment.")
