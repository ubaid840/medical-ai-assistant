import streamlit as st
import time
import numpy as np
import plotly.graph_objects as go

def render_nanobot_controller():
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
        <div style="position: absolute; top: -50px; right: -50px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, transparent 70%); border-radius: 50%; pointer-events: none;"></div>
        
        <h3 style="margin-top: 0; font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #065f46, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🦠 Autonomous Nanobot Swarm Controller</h3>
        <p style="color: #64748b; font-size: 1.05rem; margin-bottom: 0;">Command Center for intravascular medical nanobot swarms targeting Circulating Tumor Cells (CTCs).</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🧭 Intravascular Swarm Trajectory (3D)")
        
        if st.button("💉 Inject Swarm & Begin Hunt", type="primary"):
            placeholder = st.empty()
            metrics_placeholder = st.empty()
            
            # Simulate a 3D Nanobot Swarm searching for a tumor cell
            for i in range(15):
                # Swarm of 500 nanobots moving through a vessel
                # They start diffuse and slowly converge on a target at (5, 5, 5)
                convergence = i / 14.0 # 0 to 1
                
                # Random spread
                x = np.random.normal(0, 5 - (convergence * 4), 500) + (convergence * 5)
                y = np.random.normal(0, 5 - (convergence * 4), 500) + (convergence * 5)
                z = np.random.normal(0, 5 - (convergence * 4), 500) + (convergence * 5)
                
                fig = go.Figure()
                # Nanobots
                fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(size=3, color='#10b981', opacity=0.6), name='Nanobots'))
                # Target Tumor
                fig.add_trace(go.Scatter3d(x=[5], y=[5], z=[5], mode='markers', marker=dict(size=15, color='#ef4444', symbol='diamond'), name='Metastatic Cell'))
                
                fig.update_layout(
                    height=450,
                    margin=dict(l=0, r=0, t=0, b=0),
                    scene=dict(
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        zaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                placeholder.plotly_chart(fig, use_container_width=True)
                
                if i < 7:
                    metrics_placeholder.info(f"Phase: **Search & Navigate** | Swarm Cohesion: {int(50 + convergence*20)}% | Speed: 12 mm/s")
                elif i < 14:
                    metrics_placeholder.warning(f"Phase: **Target Acquired** | Swarm Cohesion: {int(50 + convergence*40)}% | Converging...")
                else:
                    metrics_placeholder.success("Phase: **Ablation Complete** | Target Destroyed | Swarm dissipating for renal clearance.")
                    
                time.sleep(0.01)
                
    with col2:
        st.markdown("#### Swarm Telemetry")
        st.metric("Active Units", "99,412 / 100,000", "-588 (Clearance)")
        st.metric("Current Location", "Hepatic Portal Vein", "Moving 12 mm/s")
        st.metric("Target", "Circulating Tumor Cell", "CD44+ Signature")
        
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 15px; border-radius: 6px; margin-top: 20px;">
            <strong style="color: #065f46;">On-Board Payload</strong><br>
            <span style="color: #047857; font-size: 0.9rem;">Each nanobot is armed with localized thermal ablation lasers and 0.01µg of targeted Doxorubicin. Activation requires 95% swarm consensus.</span>
        </div>
        """, unsafe_allow_html=True)
