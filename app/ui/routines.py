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
        <div class="card">
        <h3>💊 Smart Care Routines</h3>
        <p>Medication Reminders & Post-Op Follow-ups</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    active_patient_id = st.session_state.get("active_patient_id")
    
    if not active_patient_id:
        st.warning("Please select a patient from the sidebar to view their care routines.")
        return
        
    st.markdown("### 📋 Active Care Plan")
    
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
