import streamlit as st
import pandas as pd
from database import get_connection

def get_care_routines(patient_id=None):
    conn = get_connection()
    if patient_id:
        df = pd.read_sql_query("SELECT id, task_type, description, due_date, status FROM care_routines WHERE patient_id = ?", conn, params=(patient_id,))
    else:
        df = pd.read_sql_query("SELECT id, patient_id, task_type, description, due_date, status FROM care_routines", conn)
    conn.close()
    return df

def add_care_routine(patient_id, task_type, description, due_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO care_routines (patient_id, task_type, description, due_date)
        VALUES (?, ?, ?, ?)
    """, (patient_id, task_type, description, due_date))
    conn.commit()
    conn.close()

def update_routine_status(routine_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE care_routines SET status = ? WHERE id = ?", (new_status, routine_id))
    conn.commit()
    conn.close()

def render_routines():
    st.markdown(
        """
        <div style="
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        border-radius: 20px;
        padding: 35px 30px;
        color: white;
        box-shadow: 0 20px 40px -10px rgba(245, 158, 11, 0.4);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.2);
        ">
        <div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: rgba(255,255,255,0.1); border-radius: 50%; filter: blur(30px); pointer-events: none;"></div>
        <div style="position: absolute; bottom: -80px; left: 10%; width: 200px; height: 200px; background: rgba(255,255,255,0.15); border-radius: 50%; filter: blur(25px); pointer-events: none;"></div>

        <div style="display: flex; align-items: center; gap: 25px; position: relative; z-index: 1;">
        <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); width: 80px; height: 80px; border-radius: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.4);">
        <span style="font-size: 40px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">💊</span>
        </div>
        <div>
        <h2 style="margin: 0; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.15);">Smart Care Routines</h2>
        <p style="margin: 8px 0 0 0; font-size: 1.1rem; opacity: 0.95; font-weight: 500; letter-spacing: 0.2px;">Medication Reminders & Post-Op Follow-ups</p>
        </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    active_patient_id = st.session_state.get("active_patient_id")
    
    if not active_patient_id:
        st.warning("Please select a patient from the sidebar to view their care routines.")
        return
        
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px; margin-top: 10px;">
            <div style="background: linear-gradient(135deg, #fcd34d, #f59e0b); color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(245,158,11,0.3);">
                📋
            </div>
            <div>
                <h3 style="margin: 0; font-weight: 800; color: #0f172a; font-size: 1.5rem; letter-spacing: -0.5px;">Active Care Plan</h3>
                <p style="margin: 2px 0 0 0; color: #64748b; font-size: 1rem;">Track upcoming patient actions and routines.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    routines_df = get_care_routines(active_patient_id)
    
    if routines_df.empty:
        st.info("No active care routines. The AI can create reminders automatically during chat!")
    else:
        for idx, row in routines_df.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                with col1:
                    icon = "💊" if "medication" in str(row['task_type']).lower() else "🩺"
                    st.markdown(f"**{icon} {row['task_type']}** - {row['description']}")
                    st.caption(f"📅 Due: {row['due_date']} | 🟢 Status: {row['status']}")
                with col2:
                    if row['status'] != 'Done':
                        if st.button("Mark Done", key=f"btn_{row['id']}"):
                            update_routine_status(row['id'], 'Done')
                            st.rerun()
                st.divider()

    with st.expander("➕ Add Manual Routine"):
        task_type = st.selectbox("Task Type", ["Medication Reminder", "Post-Op Follow-up", "General Check-in"])
        desc = st.text_input("Description", placeholder="e.g. Take 500mg Amoxicillin")
        due_date = st.date_input("Due Date")
        
        if st.button("Add Routine"):
            add_care_routine(active_patient_id, task_type, desc, str(due_date))
            st.success("Routine added!")
            st.rerun()
