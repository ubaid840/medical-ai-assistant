import streamlit as st
import time
import numpy as np
import plotly.graph_objects as go

def render_surgical_sim():
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #ef4444, #b91c1c); border-radius: 20px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(239, 68, 68, 0.3);">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">🔪 Robotic Surgery Digital Twin</h1>
            <p style="margin-top: 10px; font-size: 1.1rem; opacity: 0.9;">Real-time intraoperative telemetry and AI predictive modeling.</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🤖 Da Vinci Telemetry Stream", "🩺 Multi-Agent Case Review"])
    
    with tab1:
        st.markdown("### 🔴 Live Operative Feed (Patient: ID-7839)")
        st.info("Streaming intraoperative vital fluctuations and robotic arm kinematics.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("▶️ Start Live Telemetry Stream", type="primary"):
                placeholder = st.empty()
                alert_placeholder = st.empty()
                
                # Simulate a live feed for a few iterations
                for i in range(15):
                    # Generate some random mock vitals
                    hr_data = np.random.normal(75 + i*2, 5, 20)
                    bp_data = np.random.normal(120 - i*1.5, 8, 20)
                    time_x = np.arange(20) + i
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=time_x, y=hr_data, mode='lines', name='Heart Rate (bpm)', line=dict(color='#ef4444', width=3)))
                    fig.add_trace(go.Scatter(x=time_x, y=bp_data, mode='lines', name='Systolic BP (mmHg)', line=dict(color='#3b82f6', width=3)))
                    
                    fig.update_layout(
                        title="Continuous Intraoperative Vitals",
                        height=350,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        yaxis=dict(range=[40, 160]),
                        margin=dict(l=0, r=0, t=40, b=0)
                    )
                    placeholder.plotly_chart(fig, use_container_width=True)
                    
                    if i == 10:
                        alert_placeholder.markdown("""
                            <div style="background-color: #fef2f2; border-left: 5px solid #ef4444; padding: 15px; border-radius: 8px; margin-top: 10px; animation: pulse 1s infinite;">
                                <strong style="color: #b91c1c; font-size: 1.2rem;">⚠️ AI Predictive Warning: Critical Event Imminent</strong><br>
                                <span style="color: #991b1b;">92% probability of acute hypotensive episode in 14 seconds due to prolonged vena cava compression by robotic arm 3. Recommend immediate 5-degree counter-traction.</span>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    time.sleep(0.01)
                
                alert_placeholder.markdown("""
                    <div style="background-color: #ecfdf5; border-left: 5px solid #10b981; padding: 15px; border-radius: 8px; margin-top: 10px;">
                        <strong style="color: #065f46; font-size: 1.2rem;">✅ Event Averted</strong><br>
                        <span style="color: #047857;">Traction adjusted. Vitals stabilizing.</span>
                    </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### Robotic Kinematics")
            st.metric("Arm 1 Latency", "12 ms", "-1 ms")
            st.metric("Arm 2 Latency", "14 ms", "0 ms")
            st.metric("Arm 3 Latency", "18 ms", "+4 ms", delta_color="inverse")
            st.metric("Haptic Feedback Confidence", "99.8%", "Optimal")
            
            st.markdown("#### Real-Time Tissue Classification")
            st.progress(85, text="Malignancy Boundary Confidence (85%)")
            st.progress(98, text="Nerve Preservation Safety (98%)")

    with tab2:
        patient_case = st.text_area("Enter Patient Surgical Case Details:", "68yo M with severe aortic stenosis and history of COPD. Planning for TAVR vs SAVR. Ejection fraction 40%.")
        
        if st.button("Initiate AI Medical Board Review"):
            st.divider()
            st.markdown("### 🏥 Active Simulation")
            
            chat_container = st.container()
            
            with chat_container:
                time.sleep(0.01)
                with st.chat_message("Lead Surgeon AI", avatar="👨‍⚕️"):
                    st.write("**Lead Surgeon AI:** Reviewing case. Given the EF of 40% and COPD history, surgical aortic valve replacement (SAVR) carries high morbidity. I propose Transcatheter Aortic Valve Replacement (TAVR) via transfemoral approach.")
                
                time.sleep(0.01)
                with st.chat_message("Anesthesiologist AI", avatar="💉"):
                    st.write("**Anesthesiologist AI:** I agree with TAVR to avoid general anesthesia and prolonged intubation, which is critical given his severe COPD. We should proceed with conscious sedation and local anesthesia.")
                    
                time.sleep(0.01)
                with st.chat_message("Cardiologist AI", avatar="❤️"):
                    st.write("**Cardiologist AI:** Wait, we need to ensure the femoral arteries are of adequate caliber for the TAVR delivery system. Have we reviewed the CT angiogram of the lower extremities?")
                    
                time.sleep(0.01)
                with st.chat_message("Lead Surgeon AI", avatar="👨‍⚕️"):
                    st.write("**Lead Surgeon AI:** Good catch. Assuming CT angio is clear, TAVR is the definitive path. If iliofemoral access is poor, we will need to consider an alternative access route like transaxillary.")
                    
                time.sleep(0.01)
                with st.chat_message("Ethical AI", avatar="⚖️"):
                    st.write("**Ethical AI:** The board has reached a consensus favoring TAVR, conditional on CT angio results. Ensure the patient is informed about the risks of vascular complications and stroke.")

            st.success("Simulation Complete. Consensus reached.")
            
            st.markdown("""
            **Final Board Recommendation:**
            1. Primary Plan: Transfemoral TAVR under conscious sedation.
            2. Prerequisite: Urgent CT Angiogram of lower extremities to confirm vascular access.
            3. Backup Plan: Transaxillary TAVR if femoral access is inadequate.
            """)
