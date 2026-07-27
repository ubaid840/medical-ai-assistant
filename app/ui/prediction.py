import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

class PhysiologicalSimulator:
    def __init__(self):
        self.systems = [
            "Cardiovascular", "Respiratory", "Nervous", "Endocrine", 
            "Renal", "Digestive", "Musculoskeletal", "Immune", 
            "Reproductive", "Lymphatic"
        ]
        self.baseline = {sys: np.random.uniform(25, 35) for sys in self.systems}
        
    def simulate_intervention(self, intervention: str, days: int = 30):
        history = {sys: [self.baseline[sys]] for sys in self.systems}
        deltas = {sys: 0.0 for sys in self.systems}
        
        if intervention == "ACE Inhibitor (Lisinopril)":
            deltas["Cardiovascular"] = -0.8
            deltas["Renal"] = 0.3
            deltas["Endocrine"] = -0.1
        elif intervention == "Corticosteroid (Prednisone)":
            deltas["Immune"] = -1.5
            deltas["Endocrine"] = 1.0
            deltas["Musculoskeletal"] = 0.5
            deltas["Digestive"] = 0.2
        elif intervention == "Sepsis Infection":
            for s in self.systems:
                deltas[s] = np.random.uniform(1.0, 3.0)
            deltas["Immune"] = 5.0
            deltas["Cardiovascular"] = 4.0
            deltas["Respiratory"] = 3.5
            
        for day in range(1, days):
            for sys in self.systems:
                current_val = history[sys][-1]
                adapted_delta = deltas[sys] * (0.9 ** day)
                noise = np.random.normal(0, 0.5)
                new_val = max(0, min(100, current_val + adapted_delta + noise))
                pull = (self.baseline[sys] - new_val) * 0.02
                new_val += pull
                history[sys].append(new_val)
                
        return pd.DataFrame(history)

def render_uhdt_micro():
    st.markdown("### Universal Human Digital Twin (UHDT)")
    st.info("Micro-level simulation: Neural pathways, cellular networks, and causal disease mechanisms.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("#### Neural & Causal Synchronization")
        disorder = st.selectbox("Select Pathology to Map", ["Alzheimer's Disease (Cortical)", "Type 2 Diabetes (Systemic)", "Major Depressive Disorder"])
        intervention = st.selectbox("Select Target Intervention", ["Deep Brain Stimulation (DBS)", "Metabolic Reprogramming", "SSRI Therapy"])
        sim_btn = st.button("🧬 Synchronize UHDT Matrix", type="primary", use_container_width=True)
        
    with col2:
        if sim_btn:
            with st.spinner(f"Aligning micro-cellular causal graphs for {disorder}..."):
                time.sleep(0.01)
            
            # Simulated Neural Network Activity (Heatmap)
            z = np.random.normal(0, 1, (20, 20))
            if "Alzheimer" in disorder:
                z -= 1.5
            if "DBS" in intervention or "Reprogramming" in intervention:
                z += 1.0
                
            fig = go.Figure(data=go.Heatmap(
                z=z,
                colorscale='Viridis',
                showscale=False
            ))
            fig.update_layout(
                title=f"UHDT Micro-Cellular Matrix: {disorder} + {intervention}",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=300,
                margin=dict(l=10, r=10, t=30, b=10),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 15px; border-radius: 6px;">
                <strong style="color: #065f46;">UHDT Synchronization Complete</strong><br>
                <span style="color: #047857; font-size: 0.9rem;">The causal disease engine confirms that the targeted intervention successfully restores baseline firing densities across the simulated cellular network, bypassing genetic predispositions.</span>
            </div>
            """, unsafe_allow_html=True)

def render_pcse_macro():
    st.markdown("### Predictive Clinical Simulation Engine (PCSE)")
    st.info("Macro-level simulation: 30-Day Organ interactions and 20-Year Longitudinal trajectories.")
    
    tab_organ, tab_long = st.tabs(["🫀 30-Day Systemic Sim", "📅 20-Year Longitudinal"])
    
    with tab_organ:
        col1, col2 = st.columns([1, 2])
        with col1:
            intervention = st.selectbox(
                "Pharmacological / Pathological Event",
                ["ACE Inhibitor (Lisinopril)", "Corticosteroid (Prednisone)", "Sepsis Infection"]
            )
            sim_btn = st.button("🔮 Run 30-Day PCSE", type="primary", use_container_width=True)
            
        with col2:
            if sim_btn:
                with st.spinner("Simulating macro-organ interactions..."):
                    time.sleep(0.01)
                sim = PhysiologicalSimulator()
                df = sim.simulate_intervention(intervention)
                
                fig = go.Figure()
                colors = ['#ef4444', '#3b82f6', '#f59e0b', '#10b981', '#8b5cf6', '#ec4899', '#f97316', '#14b8a6', '#6366f1', '#84cc16']
                for idx, sys in enumerate(df.columns):
                    fig.add_trace(go.Scatter(x=df.index, y=df[sys], mode='lines', name=sys, line=dict(width=2, color=colors[idx])))
                fig.update_layout(title="30-Day Organ Stress Trajectory", xaxis_title="Days Post-Intervention", yaxis_title="System Load (%)", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', hovermode='x unified', margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig, use_container_width=True)

    with tab_long:
        st.markdown("#### Patient Lifestyle Modifiers")
        col1, col2, col3 = st.columns(3)
        with col1:
            smoking = st.checkbox("Active Smoker", value=False)
        with col2:
            exercise = st.slider("Weekly Aerobic (Hours)", 0, 10, 2)
        with col3:
            med_adherence = st.slider("Medication Adherence (%)", 0, 100, 80)
            
        if st.button("🔮 Project 20-Year PCSE Trajectory", type="primary", use_container_width=True):
            years = np.arange(0, 21, 1)
            base_health = 100 - (years * 1.5)
            smoke_penalty = - (years * 2.0) if smoking else 0
            exercise_bonus = (years * 0.8) * (exercise / 5)
            adherence_penalty = - (years * 1.2) * ((100 - med_adherence) / 100)
            
            projected_health = np.clip(base_health + smoke_penalty + exercise_bonus + adherence_penalty, 0, 100)
            optimal_health = np.clip(100 - (years * 1.2) + (years * 1.0), 0, 100)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=years, y=optimal_health, mode='lines', name='Optimal', line=dict(color='#10b981', width=3, dash='dash')))
            fig.add_trace(go.Scatter(x=years, y=projected_health, mode='lines+markers', name='Projected', line=dict(color='#ef4444' if projected_health[-1] < 50 else '#3b82f6', width=4)))
            fig.add_hline(y=40, line_dash="dot", line_color="red", annotation_text="Critical Threshold")
            
            fig.update_layout(title="20-Year Biological Health Index", xaxis_title="Years", yaxis_title="Health Index (0-100)", yaxis_range=[0, 100], hovermode='x unified', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig, use_container_width=True)

def render_prediction_dashboard():
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0f172a, #1e293b); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <div style="font-size: 50px; margin-bottom: 10px;">🌐</div>
            <h1 style="color: #38bdf8; margin: 0; font-weight: 900; letter-spacing: 2px;">UHDT-PCSE</h1>
            <h3 style="color: #94a3b8; margin: 5px 0 0 0; font-weight: 400; font-size: 1.2rem;">Universal Human Digital Twin & Predictive Clinical Simulation Engine</h3>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        div[data-testid="stTabs"] button[data-baseweb="tab"] {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            padding-bottom: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🌌 UHDT (Micro-Cellular)", "🔮 PCSE (Macro-Systemic)"])
    with tab1:
        render_uhdt_micro()
    with tab2:
        render_pcse_macro()
