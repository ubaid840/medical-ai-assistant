import streamlit as st
import numpy as np
import time
import plotly.graph_objects as go

def render_wearables():
    st.markdown("""
        <div style='background: white; padding: 25px 30px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border: 1px solid #f1f5f9; margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 8px;'>
                <div style='background: linear-gradient(135deg, #dcfce7, #bbf7d0); color: #16a34a; padding: 10px; border-radius: 12px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);'>
                    <span style='font-size: 24px;'>⌚</span>
                </div>
                <h3 style='color: #0f172a; font-weight: 800; font-size: 1.7rem; margin: 0;'>Live Wearable Data Stream</h3>
            </div>
            <p style='color: #64748b; font-size: 1.1rem; margin-top: 5px; margin-bottom: 0;'>Mock Apple Watch / Fitbit telemetry data with real-time AI anomaly detection.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Heart Rate", value="72 bpm", delta="-1 bpm")
    with col2:
        st.metric(label="SpO2", value="99%", delta="0%")
    with col3:
        st.metric(label="Status", value="Normal Sinus Rhythm", delta="Stable")
        
    st.markdown("### 🫀 Live ECG Feed")
    
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
            time.sleep(0.1)
            
        st.success("✅ Stream complete. AI detected no severe arrhythmias during this segment.")
