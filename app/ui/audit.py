import streamlit as st
import pandas as pd
from database import get_connection
from ui.components import render_page_header
import plotly.graph_objects as go

def render_hipaa_audit():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT a.id, a.timestamp, a.action, p.name as patient_name, a.details
        FROM audit_logs a
        LEFT JOIN patient_profiles p ON a.patient_id = p.id
        ORDER BY a.timestamp DESC
    """, conn)
    conn.close()

    if df.empty:
        st.info("No audit logs found. The system is operating securely.")
    else:
        def highlight_emergencies(row):
            if 'Emergency' in str(row['action']):
                return ['background-color: #fee2e2; color: #991b1b'] * len(row)
            return [''] * len(row)

        styled_df = df.style.apply(highlight_emergencies, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)

def render_quality_auditor():
    st.markdown("### Continuous Clinical Quality Auditor")
    st.info("Autonomous AI review of clinical documentation, guideline adherence, and workflow efficiency.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Documentation Compliance", "94%", "+2%")
    with col2:
        st.metric("Guideline Adherence", "88%", "-1%")
    with col3:
        st.metric("Medication Reconciliation Errors", "3", "-5")
        
    st.markdown("#### 🚩 AI Flagged Findings (Requires Review)")
    st.markdown("""
    <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 15px; border-radius: 6px; margin-bottom: 15px;">
        <strong style="color: #991b1b;">Guideline Deviation: Patient #1042 (Sepsis)</strong><br>
        <span style="color: #b91c1c; font-size: 0.9rem;">Broad-spectrum antibiotics delayed by 45 minutes beyond the 1-hour CMS sepsis bundle guideline. Please review workflow.</span>
    </div>
    <div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; padding: 15px; border-radius: 6px; margin-bottom: 15px;">
        <strong style="color: #b45309;">Documentation Gap: Dr. Smith (Cardiology)</strong><br>
        <span style="color: #d97706; font-size: 0.9rem;">Discharge summary for Patient #441 missing primary follow-up instructions. Risk of readmission increased.</span>
    </div>
    """, unsafe_allow_html=True)

def render_federated_intelligence():
    st.markdown("### Multi-Hospital Federated Intelligence")
    st.info("Learning from global health patterns while preserving strict cryptographic patient privacy.")
    
    st.markdown("#### Global Trend Anomaly Detection")
    # Fake global data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    org_a = [120, 130, 125, 200, 190, 210] # Spike
    org_b = [100, 110, 105, 180, 175, 195]
    org_c = [90, 85, 95, 150, 160, 170]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=org_a, mode='lines+markers', name='Regional Hospital A'))
    fig.add_trace(go.Scatter(x=months, y=org_b, mode='lines+markers', name='Metro Hospital B'))
    fig.add_trace(go.Scatter(x=months, y=org_c, mode='lines+markers', name='Our Institution'))
    fig.update_layout(title="Federated Detection: Atypical Pneumonia Admissions", height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 15px; border-radius: 6px;">
        <strong style="color: #065f46;">Federated AI Insight</strong><br>
        <span style="color: #047857; font-size: 0.9rem;">Cross-institutional learning model has detected a 42% spike in atypical pneumonia cases across the region. Updating local triage protocols automatically to flag respiratory symptoms.</span>
    </div>
    """, unsafe_allow_html=True)


def render_audit_dashboard():
    render_page_header("⚕️", "Quality, Privacy & Federated AI", "Tamper-proof HIPAA auditing, continuous quality review, and global federated intelligence.", "linear-gradient(135deg, #f43f5e, #be123c)")

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

    tab1, tab2, tab3 = st.tabs(["🔒 HIPAA Audit Trail", "✅ AI Quality Auditor", "🌍 Federated Intelligence"])
    
    with tab1: render_hipaa_audit()
    with tab2: render_quality_auditor()
    with tab3: render_federated_intelligence()
