import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
from ui.components import render_page_header

def render_dashboard():
    render_page_header("🫀", "Live ICU Telemetry", "Real-time, continuous monitoring of patient vitals with AI anomaly detection.", "linear-gradient(135deg, #ef4444, #991b1b)")

    # ---------------------------------------------------------
    # State Management for Live Streaming
    # ---------------------------------------------------------
    if "icu_active" not in st.session_state:
        st.session_state.icu_active = False
        
    if "icu_data" not in st.session_state:
        # Initialize 60 seconds of baseline data
        st.session_state.icu_data = {
            "time": list(range(60)),
            "hr": [75] * 60,
            "spo2": [99] * 60,
            "sys": [120] * 60,
            "dia": [80] * 60
        }
        st.session_state.anomaly_triggered = False
        st.session_state.anomaly_timer = 0

    # ---------------------------------------------------------
    # Control Panel
    # ---------------------------------------------------------
    st.markdown("### 🔴 Central Monitoring Station")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.info("Simulating high-frequency data stream from bedside monitors.")
    with col2:
        if st.session_state.icu_active:
            if st.button("⏹ Stop Monitor", use_container_width=True):
                st.session_state.icu_active = False
                st.rerun()
        else:
            if st.button("▶️ Start Live Telemetry", use_container_width=True, type="primary"):
                st.session_state.icu_active = True
                st.session_state.anomaly_triggered = False
                st.session_state.anomaly_timer = 0
                st.rerun()

    placeholder = st.empty()

    # ---------------------------------------------------------
    # Live Streaming Logic
    # ---------------------------------------------------------
    if st.session_state.icu_active:
        data = st.session_state.icu_data
        
        # Advance time array
        data["time"].pop(0)
        data["time"].append(data["time"][-1] + 1)
        
        # Simulate Anomaly Trigger (2% chance per tick)
        if not st.session_state.anomaly_triggered and random.random() < 0.02:
            st.session_state.anomaly_triggered = True
            st.session_state.anomaly_timer = 30 # Anomaly lasts for 30 ticks
            
        if st.session_state.anomaly_triggered:
            st.session_state.anomaly_timer -= 1
            if st.session_state.anomaly_timer <= 0:
                st.session_state.anomaly_triggered = False # Recover
                
        # Generate new data points based on state
        if st.session_state.anomaly_triggered:
            # Tachycardia and Desaturation
            new_hr = min(180, data["hr"][-1] + random.randint(2, 10))
            new_spo2 = max(82, data["spo2"][-1] - random.randint(1, 4))
            new_sys = max(70, data["sys"][-1] - random.randint(1, 5))
            new_dia = max(40, data["dia"][-1] - random.randint(1, 3))
        else:
            # Normal Baseline Fluctuations
            new_hr = max(60, min(100, data["hr"][-1] + random.randint(-2, 2)))
            new_spo2 = max(95, min(100, data["spo2"][-1] + random.randint(-1, 1)))
            new_sys = max(110, min(130, data["sys"][-1] + random.randint(-2, 2)))
            new_dia = max(70, min(85, data["dia"][-1] + random.randint(-2, 2)))
            
        data["hr"].pop(0)
        data["hr"].append(new_hr)
        
        data["spo2"].pop(0)
        data["spo2"].append(new_spo2)
        
        data["sys"].pop(0)
        data["sys"].append(new_sys)
        
        data["dia"].pop(0)
        data["dia"].append(new_dia)

        # ---------------------------------------------------------
        # Render the Live Dashboard
        # ---------------------------------------------------------
        with placeholder.container():
            if st.session_state.anomaly_triggered:
                st.markdown(
                    """
                    <div style="background-color: #7f1d1d; border: 2px solid #ef4444; border-radius: 8px; padding: 15px; margin-bottom: 20px; animation: pulse 1s infinite;">
                        <h3 style="color: white; margin: 0; text-align: center;">🚨 CRITICAL ALERT: TACHYCARDIA & DESATURATION DETECTED 🚨</h3>
                    </div>
                    <style>
                    @keyframes pulse {
                        0% { opacity: 1; }
                        50% { opacity: 0.5; }
                        100% { opacity: 1; }
                    }
                    </style>
                    """, unsafe_allow_html=True
                )
            
            col_a, col_b, col_c = st.columns(3)
            
            # Vitals UI Cards
            def metric_card(title, value, unit, color):
                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 20px; text-align: center;">
                    <h4 style="color: #94a3b8; margin: 0;">{title}</h4>
                    <h1 style="color: {color}; margin: 5px 0; font-size: 3rem;">{value} <span style="font-size: 1rem; color: #64748b;">{unit}</span></h1>
                </div>
                """, unsafe_allow_html=True)
                
            with col_a:
                metric_card("Heart Rate", new_hr, "bpm", "#f43f5e" if new_hr < 110 else "#ef4444")
            with col_b:
                metric_card("SpO2", new_spo2, "%", "#0ea5e9" if new_spo2 > 92 else "#ef4444")
            with col_c:
                metric_card("Blood Pressure", f"{new_sys}/{new_dia}", "mmHg", "#10b981" if new_sys > 90 else "#ef4444")
            
            st.write("")
            
            # Streaming Charts
            fig = go.Figure()
            
            # HR Trace
            fig.add_trace(go.Scatter(x=data["time"], y=data["hr"], mode='lines', line=dict(color='#f43f5e', width=3), name='Heart Rate'))
            # SpO2 Trace
            fig.add_trace(go.Scatter(x=data["time"], y=data["spo2"], mode='lines', line=dict(color='#0ea5e9', width=3), name='SpO2'))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=30, b=10),
                xaxis=dict(showgrid=False, showticklabels=False, range=[data["time"][0], data["time"][-1]]),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', range=[40, 200]),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=400
            )
            
            # Ensure the chart updates immediately without waiting for user interaction by providing a changing key
            st.plotly_chart(fig, use_container_width=True, key="icu_chart")

        # Sleep and Rerun Loop
        time.sleep(0.01)
        st.rerun()
        
    else:
        # Show Historical Data when not streaming
        st.markdown("---")
        st.markdown("### 📅 Historical 30-Day Trends")
        
        np.random.seed(42)
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        df = pd.DataFrame({
            'Date': dates,
            'Systolic': np.random.normal(128, 12, 30),
            'Diastolic': np.random.normal(82, 8, 30),
            'HeartRate': np.random.normal(74, 6, 30),
            'Glucose': np.random.normal(105, 18, 30)
        })

        metric_choice = st.selectbox("Select Historical Telemetry", ["Blood Pressure", "Heart Rate", "Blood Glucose"])

        fig = go.Figure()
        if metric_choice == "Blood Pressure":
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Systolic'], mode='lines+markers', name='Systolic (mmHg)', line=dict(color='#ef4444', width=3)))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Diastolic'], mode='lines+markers', name='Diastolic (mmHg)', line=dict(color='#3b82f6', width=3)))
            fig.update_layout(title="30-Day Blood Pressure Trends", yaxis_title="mmHg")
        elif metric_choice == "Heart Rate":
            fig.add_trace(go.Scatter(x=df['Date'], y=df['HeartRate'], mode='lines+markers', name='Heart Rate (bpm)', line=dict(color='#f59e0b', width=3)))
            fig.update_layout(title="30-Day Heart Rate Trends", yaxis_title="BPM")
        else:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Glucose'], mode='lines+markers', name='Glucose (mg/dL)', line=dict(color='#10b981', width=3)))
            fig.update_layout(title="30-Day Fasting Glucose Trends", yaxis_title="mg/dL")
            
        fig.update_layout(xaxis_title="Date", hovermode='x unified', margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
