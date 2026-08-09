import streamlit as st
import time
import numpy as np
import plotly.graph_objects as go

def render_bci_dashboard():
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
        <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, transparent 70%); border-radius: 50%; pointer-events: none;"></div>
        
        <h3 style="margin-top: 0; font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #4c1d95, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🧠 Neural-Link Decoder</h3>
        <p style="color: #64748b; font-size: 1.05rem; margin-bottom: 0;">Brain-Computer Interface for Locked-In Syndrome Communication</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### ⚡ Raw Motor Cortex Spikes (Channel 64)")
        
        if st.button("📡 Initiate Neural Stream Sync", type="primary"):
            placeholder = st.empty()
            decoder_placeholder = st.empty()
            
            # Simulated EEG Spike Stream
            for i in range(15):
                # Generate mock neural spikes
                time_x = np.linspace(0, 2, 100)
                spikes = np.sin(time_x * np.pi * 5) * np.exp(-time_x) + np.random.normal(0, 0.2, 100)
                if i in [3, 8, 12]:
                    spikes[40:50] += 5.0 # Simulated intentional burst
                    
                fig = go.Figure(data=go.Scatter(y=spikes, mode='lines', line=dict(color='#8b5cf6', width=2)))
                fig.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=20, b=0),
                    plot_bgcolor='black',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                )
                placeholder.plotly_chart(fig, use_container_width=True)
                
                # Mock LLM decoding process
                if i == 4:
                    decoder_placeholder.info("Decoding Motor Intent: 'THIRSTY'")
                elif i == 9:
                    decoder_placeholder.info("Decoding Motor Intent: 'ADJUST BED UP'")
                elif i == 13:
                    decoder_placeholder.success("🎙️ **Synthesized Voice:** 'I am thirsty. Please adjust my bed up.'")
                
                time.sleep(0.01)
                
    with col2:
        st.markdown("#### BCI Telemetry")
        st.metric("Implant Signal Quality", "99.2%", "Optimal")
        st.metric("Decoding Latency", "42 ms", "-5 ms")
        st.metric("Electrode Impedance", "1.2 kΩ", "Stable")
        
        st.markdown("""
        <div style="background: rgba(139, 92, 246, 0.1); border-left: 4px solid #8b5cf6; padding: 15px; border-radius: 6px; margin-top: 20px;">
            <strong style="color: #5b21b6;">LLM Decoder Status</strong><br>
            <span style="color: #6d28d9; font-size: 0.9rem;">The multimodal LLM is successfully mapping raw neural embeddings to English semantic tokens at 24 words per minute.</span>
        </div>
        """, unsafe_allow_html=True)
