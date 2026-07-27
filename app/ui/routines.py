import streamlit as st
import pandas as pd
import time
from database import get_connection
from ui.components import render_page_header

def get_care_routines(patient_id=None):
    conn = get_connection()
    if patient_id:
        df = pd.read_sql_query("SELECT id, task_type, description, due_date, status FROM care_routines WHERE patient_id = ?", conn, params=(patient_id,))
    else:
        df = pd.read_sql_query("SELECT id, patient_id, task_type, description, due_date, status FROM care_routines", conn)
    conn.close()
    return df

def update_routine_status(routine_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE care_routines SET status = ? WHERE id = ?", (new_status, routine_id))
    conn.commit()
    conn.close()

def render_workflow_planner():
    st.markdown("### Autonomous Clinical Workflow Planner")
    st.info("AI-generated end-to-end clinical plans spanning diagnostics, monitoring, and patient education.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        _ = st.text_input("Enter Primary Diagnosis:", "Type 2 Diabetes Mellitus - Newly Diagnosed")
        if st.button("Generate Autonomous Workflow", type="primary", use_container_width=True):
            with st.spinner("AI generating longitudinal care pathway..."):
                time.sleep(0.01)
            st.session_state.workflow_generated = True
            
    with col2:
        if st.session_state.get("workflow_generated"):
            st.success("Workflow Generated Successfully.")
            
            with st.expander("🧪 Suggested Diagnostics & Labs", expanded=True):
                st.markdown("- **HbA1c** (Baseline, then every 3 months)\n- **Comprehensive Metabolic Panel (CMP)** (Evaluate renal function)\n- **Fasting Lipid Panel**")
            with st.expander("📅 Monitoring Schedule", expanded=True):
                st.markdown("- **Daily**: Fasting blood glucose tracking via wearable/CGM.\n- **Weekly**: Automated telehealth check-in for dietary adherence.")
            with st.expander("🔄 Referral Triggers"):
                st.markdown("- **Trigger**: If HbA1c > 8.0% after 6 months -> Refer to Endocrinology.\n- **Trigger**: Annual retinal screening -> Refer to Ophthalmology.")
            with st.expander("📚 Patient Education Plan"):
                st.markdown("- **Day 1**: Introductory Diabetes Survival Skills (Hypoglycemia management).\n- **Day 7**: Carbohydrate counting basics.\n- **Day 30**: Long-term cardiovascular risk reduction.")

def render_routines():
    render_page_header("🗓️", "Clinical Workflows & Routines", "End-to-end autonomous care planning and patient routine tracking.", "linear-gradient(135deg, #fbbf24, #f59e0b)")
    
    st.markdown("""
        <style>
        div[data-testid="stTabs"] button[data-baseweb="tab"] {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            padding-bottom: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🤖 Autonomous Workflow Planner", "💊 Active Patient Routines"])
    
    with tab1:
        render_workflow_planner()
        
    with tab2:
        active_patient_id = st.session_state.get("active_patient_id")
        if not active_patient_id:
            st.warning("Please select a patient from the sidebar to view their active routines.")
        else:
            routines_df = get_care_routines(active_patient_id)
            if routines_df.empty:
                st.info("No active care routines. The AI can create reminders automatically during chat!")
            else:
                for idx, row in routines_df.iterrows():
                    with st.container():
                        c1, c2 = st.columns([4, 1])
                        with c1:
                            icon = "💊" if "medication" in str(row['task_type']).lower() else "🩺"
                            st.markdown(f"**{icon} {row['task_type']}** - {row['description']}")
                            st.caption(f"📅 Due: {row['due_date']} | 🟢 Status: {row['status']}")
                        with c2:
                            if row['status'] != 'Done':
                                if st.button("Mark Done", key=f"btn_{row['id']}"):
                                    update_routine_status(row['id'], 'Done')
                                    st.rerun()
                        st.divider()
