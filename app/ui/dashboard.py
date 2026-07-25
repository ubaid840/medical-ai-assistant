import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_dashboard():
    st.markdown("""
        <div style='background: white; padding: 25px 30px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border: 1px solid #f1f5f9; margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 8px;'>
                <div style='background: linear-gradient(135deg, #fce7f3, #fbcfe8); color: #be185d; padding: 10px; border-radius: 12px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);'>
                    <span style='font-size: 24px;'>📊</span>
                </div>
                <h3 style='color: #0f172a; font-weight: 800; font-size: 1.7rem; margin: 0;'>Longitudinal Vitals Dashboard</h3>
            </div>
            <p style='color: #64748b; font-size: 1.1rem; margin-top: 5px; margin-bottom: 0;'>Interactive analysis of patient telemetry and historical vitals.</p>
        </div>
    """, unsafe_allow_html=True)

    # Generate mock data deterministically based on patient ID or just random for now
    np.random.seed(42) # Consistent for demo
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    
    systolic = np.random.normal(128, 12, 30)
    diastolic = np.random.normal(82, 8, 30)
    hr = np.random.normal(74, 6, 30)
    glucose = np.random.normal(105, 18, 30)
    
    df = pd.DataFrame({
        'Date': dates,
        'Systolic': systolic,
        'Diastolic': diastolic,
        'HeartRate': hr,
        'Glucose': glucose
    })

    metric_choice = st.selectbox("Select Telemetry to Analyze", ["Blood Pressure", "Heart Rate", "Blood Glucose"])

    if metric_choice == "Blood Pressure":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Systolic'], mode='lines+markers', name='Systolic (mmHg)', line=dict(color='#ef4444', width=3)))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Diastolic'], mode='lines+markers', name='Diastolic (mmHg)', line=dict(color='#3b82f6', width=3)))
        fig.update_layout(title="30-Day Blood Pressure Trends", xaxis_title="Date", yaxis_title="mmHg", hovermode='x unified', margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    elif metric_choice == "Heart Rate":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['HeartRate'], mode='lines+markers', name='Heart Rate (bpm)', line=dict(color='#f59e0b', width=3)))
        fig.update_layout(title="30-Day Heart Rate Trends", xaxis_title="Date", yaxis_title="BPM", hovermode='x unified', margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Glucose'], mode='lines+markers', name='Glucose (mg/dL)', line=dict(color='#10b981', width=3)))
        fig.update_layout(title="30-Day Fasting Glucose Trends", xaxis_title="Date", yaxis_title="mg/dL", hovermode='x unified', margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("🤖 Ask AI to Analyze Trends"):
        if st.button("Generate Trend Report", use_container_width=True):
            with st.spinner("Analyzing telemetry data..."):
                from chatbot import ask_medical_ai
                prompt = f"Analyze the following patient 30-day vitals trends. Note any anomalies. Data summary: Avg Systolic {np.mean(systolic):.0f}, Avg Diastolic {np.mean(diastolic):.0f}, Avg HR {np.mean(hr):.0f}, Avg Glucose {np.mean(glucose):.0f}."
                response = ask_medical_ai(prompt, "dashboard_analysis")
                st.write_stream(response.get("answer_generator", ["Unable to analyze."]))
