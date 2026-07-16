import streamlit as st
import pandas as pd
from database import get_connection
from datetime import datetime, timedelta

def get_appointments(patient_id=None):
    conn = get_connection()
    if patient_id:
        df = pd.read_sql_query("SELECT id, appointment_date, reason, status, insurance_details FROM appointments WHERE patient_id = ?", conn, params=(patient_id,))
    else:
        df = pd.read_sql_query("SELECT id, patient_id, appointment_date, reason, status FROM appointments", conn)
    conn.close()
    return df

def add_appointment(patient_id, date_str, reason, insurance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (patient_id, appointment_date, reason, insurance_details)
        VALUES (?, ?, ?, ?)
    """, (patient_id, date_str, reason, insurance))
    conn.commit()
    conn.close()

def render_operations():
    st.markdown(
        """
        <div class="card">
        <h3>📅 Patient Management & Operations</h3>
        <p>Automated Intake & Scheduling Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    active_patient_id = st.session_state.get("active_patient_id")
    
    if not active_patient_id:
        st.warning("Please select a patient from the sidebar to view their appointments and intake forms.")
        return
        
    st.markdown("### 📋 Automated Intake Data")
    # In a real app this would be filled out by AI during chat
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name, age, allergies, medications, chronic_conditions FROM patient_profiles WHERE id = ?", (active_patient_id,))
    patient = c.fetchone()
    conn.close()
    
    if patient:
        st.info(f"**Patient:** {patient['name']} (Age: {patient['age']})  \n"
                f"**Known Allergies:** {patient['allergies']}  \n"
                f"**Current Meds:** {patient['medications']}")
    
    st.markdown("### 🗓️ Upcoming Appointments")
    
    appointments = get_appointments(active_patient_id)
    if not appointments.empty:
        st.dataframe(appointments, use_container_width=True)
    else:
        st.info("No upcoming appointments found. The AI can schedule them automatically via Chat!")
        
    with st.expander("➕ Manually Schedule Appointment"):
        col1, col2 = st.columns(2)
        with col1:
            apt_date = st.date_input("Date")
            apt_time = st.time_input("Time")
        with col2:
            reason = st.text_input("Reason for Visit", placeholder="e.g. Follow-up for hypertension")
            insurance = st.text_input("Insurance Details", placeholder="e.g. BlueCross PPO")
            
        if st.button("Book Appointment"):
            datetime_str = f"{apt_date} {apt_time}"
            add_appointment(active_patient_id, datetime_str, reason, insurance)
            st.success(f"Appointment booked for {datetime_str}!")
            st.rerun()
